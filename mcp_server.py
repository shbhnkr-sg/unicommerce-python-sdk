"""Unicommerce MCP Server — exposes the full Unicommerce SDK as MCP tools."""

import hashlib
import json
import logging
import os
import sys
import threading
import time
from base64 import b64encode
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Annotated

from mcp.server.fastmcp import Context, FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from unicommerce import Unicommerce
from unicommerce.auth import AuthManager
from unicommerce.exceptions import UnicommerceError

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("unicommerce-mcp")


# ---------------------------------------------------------------------------
# Background token refresher
# ---------------------------------------------------------------------------

class TokenRefresher:
    """Daemon thread that proactively refreshes the OAuth token before expiry."""

    def __init__(self, auth: AuthManager, margin: float = 120.0) -> None:
        self._auth = auth
        self._margin = margin
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._last_refresh: float | None = None
        self._refresh_count = 0
        self._last_error: str | None = None

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        self._thread.join(timeout=5)

    def status(self) -> dict:
        remaining = max(0.0, self._auth._expires_at - time.monotonic())
        return {
            "is_valid": self._auth._is_token_valid(),
            "seconds_until_expiry": round(remaining, 1),
            "last_refresh_time_utc": (
                datetime.fromtimestamp(self._last_refresh, tz=timezone.utc).isoformat()
                if self._last_refresh else None
            ),
            "refresh_count": self._refresh_count,
            "last_error": self._last_error,
            "thread_alive": self._thread.is_alive(),
        }

    def _run(self) -> None:
        while not self._stop_event.is_set():
            try:
                buffer = self._auth._config.token_refresh_buffer
                sleep_for = (
                    self._auth._expires_at - buffer - self._margin - time.monotonic()
                )
                if sleep_for > 0:
                    if self._stop_event.wait(sleep_for):
                        return
                self._auth.force_refresh_sync()
                self._last_refresh = time.time()
                self._refresh_count += 1
                self._last_error = None
                logger.info("Token proactively refreshed (#%d)", self._refresh_count)
            except Exception as exc:
                self._last_error = str(exc)
                logger.warning("Token refresh failed: %s — retrying in 30s", exc)
                if self._stop_event.wait(30):
                    return


# ---------------------------------------------------------------------------
# Response cache
# ---------------------------------------------------------------------------

class ResponseCache:
    """Thread-safe in-memory TTL cache."""

    def __init__(self) -> None:
        self._store: dict[str, tuple[str, float]] = {}
        self._lock = threading.Lock()
        self._hits = 0
        self._misses = 0
        self._sets = 0

    def get(self, key: str) -> str | None:
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                self._misses += 1
                return None
            value, expires_at = entry
            if time.monotonic() >= expires_at:
                del self._store[key]
                self._misses += 1
                return None
            self._hits += 1
            return value

    def set(self, key: str, value: str, ttl: float) -> None:
        with self._lock:
            self._store[key] = (value, time.monotonic() + ttl)
            self._sets += 1
            if self._sets % 100 == 0:
                self._evict_expired()

    def clear(self) -> int:
        with self._lock:
            count = len(self._store)
            self._store.clear()
            return count

    def stats(self) -> dict:
        with self._lock:
            total = self._hits + self._misses
            return {
                "entries": len(self._store),
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate_percent": round(self._hits / total * 100, 1) if total else 0.0,
            }

    def _evict_expired(self) -> None:
        now = time.monotonic()
        expired = [k for k, (_, exp) in self._store.items() if now >= exp]
        for k in expired:
            del self._store[k]


def _cache_key(tool_name: str, args: tuple, kwargs: dict) -> str:
    parts = [tool_name]
    for a in args:
        parts.append(json.dumps(a, sort_keys=True, default=str) if isinstance(a, (dict, list)) else str(a))
    for k, v in sorted(kwargs.items()):
        serialized = json.dumps(v, sort_keys=True, default=str) if isinstance(v, (dict, list)) else str(v)
        parts.append(f"{k}={serialized}")
    return hashlib.sha256("|".join(parts).encode()).hexdigest()


_CACHE_TTL: dict[str, int] = {
    "get_product": 3600,
    "get_product_by_item_code": 3600,
    "search_products": 3600,
    "search_facilities": 3600,
    "get_facility_details": 3600,
    "get_gatepass": 3600,
    "search_gatepass": 3600,
    "get_vendor_backorder_items": 3600,
    "get_invoice_label": 86400,
    "get_invoice_pdf": 86400,
    "get_shipping_label_pdf": 86400,
    "check_serviceability": 600,
    "get_export_job_status": 86400,
}

_TERMINAL_EXPORT_STATUSES = frozenset({"COMPLETE", "SUCCESSFUL", "FAILED"})

_CACHE_IF: dict[str, object] = {
    "get_export_job_status": lambda data: data.get("status") in _TERMINAL_EXPORT_STATUSES,
}

_DTO_KEYS = frozenset({
    "saleOrderDTO", "itemTypeDTO", "facility",
    "shippingPackageDetailDTO", "inflowReceipt", "shippingManifest",
})


def _should_cache(tool_name: str, data: dict) -> bool:
    predicate = _CACHE_IF.get(tool_name)
    if predicate is not None and not predicate(data):
        return False
    if data.get("successful") is False:
        return False
    for key in _DTO_KEYS:
        if key in data and not data[key]:
            return False
    if data.get("elements") == [] or data.get("items") == []:
        return False
    return True


# ---------------------------------------------------------------------------
# Tool domain mapping (for tools://catalog resource)
# ---------------------------------------------------------------------------

_TOOL_DOMAINS: dict[str, str] = {}


def _register_domains(domain: str, names: list[str]) -> None:
    for n in names:
        _TOOL_DOMAINS[n] = domain


_register_domains("sale_orders", [
    "create_sale_order", "get_sale_order", "search_sale_orders",
    "cancel_sale_order", "edit_sale_order", "verify_sale_order",
    "set_sale_order_priority", "hold_sale_order", "unhold_sale_order",
    "hold_sale_order_items", "unhold_sale_order_items",
    "edit_sale_order_metadata", "edit_sale_order_item_metadata",
    "create_customer", "edit_customer", "switch_sale_order_facility",
    "add_sale_order_item_detail", "add_sale_order_item_detail_bulk",
])
_register_domains("inventory", [
    "adjust_inventory", "adjust_inventory_bulk", "get_inventory_snapshot",
    "mark_inventory_found", "get_nearby_store_inventory",
])
_register_domains("products", [
    "get_product", "get_product_by_item_code", "search_products",
    "create_or_edit_product", "create_or_edit_products_bulk",
    "create_or_edit_category", "create_channel_item_type",
])
_register_domains("fulfillment", [
    "create_shipping_package", "get_shipping_package", "search_shipping_packages",
    "edit_shipping_package", "split_shipping_package", "modify_shipping_package",
    "get_shipping_packages_by_status", "create_invoice", "get_invoice_details",
    "get_invoice_label", "create_invoice_and_label", "create_invoice_by_sale_order",
    "create_invoice_with_details", "create_invoice_and_allocate_provider",
    "get_invoice_pdf", "get_shipping_label_pdf", "check_serviceability",
    "allocate_shipping_provider", "update_tracking_status",
    "create_manifest", "get_manifest", "add_package_to_manifest",
    "create_and_close_manifest", "close_manifest",
    "dispatch_shipping_package", "force_dispatch_shipping_package",
    "create_and_dispatch", "mark_delivered", "create_picklist",
    "create_or_update_reason", "update_seal_id", "update_seal_id_bulk",
])
_register_domains("inbound", [
    "create_vendor", "create_or_edit_vendor_catalog", "get_vendor_backorder_items",
    "create_purchase_order", "get_purchase_order", "search_purchase_orders",
    "approve_purchase_order", "create_and_approve_purchase_order",
    "close_purchase_order", "create_grn", "get_grn", "add_item_to_grn",
    "add_item_to_grn_by_code", "search_grns",
])
_register_domains("returns", [
    "search_returns", "get_return", "create_reverse_pickup",
    "edit_reverse_pickup", "approve_reverse_pickup", "cancel_reverse_pickup",
    "allocate_courier_for_reverse_pickup", "mark_returned",
    "mark_returned_with_inventory_type", "create_alternate_item",
    "accept_alternate_item",
])
_register_domains("outbound", [
    "create_gatepass", "edit_gatepass", "scan_gatepass_item",
    "add_nontraceable_gatepass_item", "remove_gatepass_item",
    "complete_gatepass", "discard_gatepass", "search_gatepass", "get_gatepass",
])
_register_domains("facilities", [
    "search_facilities", "get_facility_details",
])
_register_domains("export_jobs", [
    "create_export_job", "get_export_job_status", "poll_export_job",
])
_register_domains("cache", ["clear_cache"])
_register_domains("session", ["set_facility", "get_facility"])


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def _serialize(response) -> dict:
    if response is None:
        return {"success": True}
    if hasattr(response, "raw") and response.raw:
        return response.raw
    if hasattr(response, "model_dump"):
        return response.model_dump(by_alias=True, exclude_none=True)
    return {"result": str(response)}


def _call(fn, *args, **kwargs) -> str:
    try:
        result = fn(*args, **kwargs)
        return json.dumps(_serialize(result), default=str, ensure_ascii=False)
    except UnicommerceError as exc:
        from mcp.server.fastmcp.exceptions import ToolError
        msg = str(exc)
        if hasattr(exc, "errors") and exc.errors:
            msg += " | " + json.dumps(exc.errors, default=str)
        raise ToolError(msg) from exc


def _pdf_call(fn, **kwargs) -> str:
    try:
        result = fn(**kwargs)
        return json.dumps({
            "content_base64": b64encode(result.content).decode(),
            "content_type": "application/pdf",
        })
    except UnicommerceError as exc:
        from mcp.server.fastmcp.exceptions import ToolError
        raise ToolError(str(exc)) from exc


def _cached_call(cache: ResponseCache, tool_name: str, fn, *args, **kwargs) -> str:
    ttl = _CACHE_TTL.get(tool_name, 0)
    if ttl == 0:
        return _call(fn, *args, **kwargs)
    key = _cache_key(tool_name, args, kwargs)
    hit = cache.get(key)
    if hit is not None:
        return hit
    result = _call(fn, *args, **kwargs)
    try:
        data = json.loads(result)
        if _should_cache(tool_name, data):
            cache.set(key, result, ttl)
    except (json.JSONDecodeError, TypeError):
        pass
    return result


def _cached_pdf_call(cache: ResponseCache, tool_name: str, fn, **kwargs) -> str:
    ttl = _CACHE_TTL.get(tool_name, 0)
    key = _cache_key(tool_name, (), kwargs)
    if ttl > 0:
        hit = cache.get(key)
        if hit is not None:
            return hit
    result = _pdf_call(fn, **kwargs)
    if ttl > 0:
        cache.set(key, result, ttl)
    return result


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------

@dataclass
class AppContext:
    client: Unicommerce
    refresher: TokenRefresher
    cache: ResponseCache
    facility_override: str | None = None


_app: AppContext | None = None


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    global _app
    tenant = os.environ.get("UC_TENANT", "")
    username = os.environ.get("UC_USERNAME", "")
    password = os.environ.get("UC_PASSWORD", "")
    facility = os.environ.get("UC_FACILITY") or None

    if not all([tenant, username, password]):
        logger.error("Set UC_TENANT, UC_USERNAME, UC_PASSWORD env vars")
        raise RuntimeError("Missing Unicommerce credentials in environment")

    client = Unicommerce(
        tenant=tenant,
        username=username,
        password=password,
        facility=facility,
    )
    refresher = TokenRefresher(client._auth)
    cache = ResponseCache()
    refresher.start()
    ctx = AppContext(client=client, refresher=refresher, cache=cache)
    _app = ctx
    try:
        yield ctx
    finally:
        _app = None
        refresher.stop()
        client.close()


mcp = FastMCP(
    "unicommerce",
    instructions=(
        "Unicommerce e-commerce platform tools. Manage sale orders, inventory, "
        "products, fulfillment, purchasing, returns, outbound, facilities, and exports. "
        "Read-only data is cached — use clear_cache if you suspect stale results. "
        "Use set_facility / get_facility to change the default facility for all calls. "
        "Use poll_export_job to wait for export jobs to complete instead of polling manually. "
        "Check token://status for auth health, cache://stats for cache metrics, "
        "tools://catalog for a full tool listing grouped by domain."
    ),
    lifespan=app_lifespan,
    host=os.environ.get("MCP_HOST", "0.0.0.0"),
    port=int(os.environ.get("MCP_PORT", "8000")),
    json_response=True,
)


def _client(ctx: Context) -> Unicommerce:
    return ctx.request_context.lifespan_context.client


def _cache(ctx: Context) -> ResponseCache:
    return ctx.request_context.lifespan_context.cache


def _app_ctx(ctx: Context) -> AppContext:
    return ctx.request_context.lifespan_context


def _resolve_facility(ctx: Context, explicit: str | None) -> str | None:
    if explicit:
        return explicit
    return _app_ctx(ctx).facility_override


# ---------------------------------------------------------------------------
# MCP Resources
# ---------------------------------------------------------------------------

@mcp.resource("token://status")
def token_status() -> str:
    """Current OAuth token health and refresh statistics."""
    return json.dumps(_app.refresher.status())


@mcp.resource("cache://stats")
def cache_stats() -> str:
    """Response cache hit/miss statistics."""
    return json.dumps(_app.cache.stats())


@mcp.resource("tools://catalog")
def tool_catalog() -> str:
    """Complete catalog of all available tools grouped by domain."""
    tools = mcp._tool_manager.list_tools()
    catalog = []
    for tool in tools:
        ann = tool.annotations
        entry = {
            "name": tool.name,
            "description": tool.description,
            "domain": _TOOL_DOMAINS.get(tool.name, "other"),
        }
        if ann is not None:
            entry["hints"] = {
                k: v for k, v in {
                    "read_only": ann.readOnlyHint,
                    "destructive": ann.destructiveHint,
                    "idempotent": ann.idempotentHint,
                }.items() if v is not None
            }
        catalog.append(entry)
    catalog.sort(key=lambda e: (e["domain"], e["name"]))
    return json.dumps(catalog, ensure_ascii=False)


# ===========================================================================
# SALE ORDERS
# ===========================================================================

@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False, idempotentHint=False),
)
def create_sale_order(
    ctx: Context,
    order: Annotated[dict, Field(description="Full sale order payload (see Unicommerce API docs)")],
    facility: Annotated[str | None, Field(description="Facility code override")] = None,
) -> str:
    """Create a new sale order in Unicommerce."""
    from unicommerce.models.sale_orders import CreateSaleOrderRequest
    req = CreateSaleOrderRequest(**order)
    return _call(_client(ctx).sale_orders.create, req, facility=_resolve_facility(ctx, facility))


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def get_sale_order(
    ctx: Context,
    code: Annotated[str, Field(description="Sale order code, e.g. SO-12345")],
    facility_codes: Annotated[list[str] | None, Field(description="Filter by facility codes")] = None,
) -> str:
    """Retrieve a sale order by its code."""
    return _call(_client(ctx).sale_orders.get, code, facility_codes=facility_codes)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def search_sale_orders(
    ctx: Context,
    filters: Annotated[dict, Field(description="Search filters — e.g. {\"statusCode\": \"CREATED\", \"channel\": \"SHOPIFY\"}")],
) -> str:
    """Search sale orders with flexible filters."""
    return _call(_client(ctx).sale_orders.search, **filters)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True),
)
def cancel_sale_order(
    ctx: Context,
    sale_order_code: Annotated[str, Field(description="Sale order code to cancel")],
    sale_order_item_codes: Annotated[list[str] | None, Field(description="Specific items to cancel (omit for full order)")] = None,
    cancellation_reason: Annotated[str | None, Field(description="Reason for cancellation")] = None,
    cancel_partially: Annotated[bool | None, Field(description="Allow partial cancellation")] = None,
) -> str:
    """Cancel a sale order or specific items within it."""
    return _call(
        _client(ctx).sale_orders.cancel,
        sale_order_code=sale_order_code,
        sale_order_item_codes=sale_order_item_codes,
        cancellation_reason=cancellation_reason,
        cancel_partially=cancel_partially,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False),
)
def edit_sale_order(
    ctx: Context,
    sale_order_code: Annotated[str, Field(description="Sale order code")],
    addresses: Annotated[list[dict], Field(description="Updated address list")],
) -> str:
    """Edit addresses on a sale order."""
    return _call(_client(ctx).sale_orders.edit, sale_order_code=sale_order_code, addresses=addresses)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False),
)
def verify_sale_order(
    ctx: Context,
    sale_order_code: Annotated[str, Field(description="Sale order code to verify")],
) -> str:
    """Verify a sale order."""
    return _call(_client(ctx).sale_orders.verify, sale_order_code=sale_order_code)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False),
)
def set_sale_order_priority(
    ctx: Context,
    sale_order_code: Annotated[str, Field(description="Sale order code")],
    priority: Annotated[int, Field(description="Priority value (higher = more urgent)")],
) -> str:
    """Set the priority of a sale order."""
    return _call(_client(ctx).sale_orders.set_priority, sale_order_code=sale_order_code, priority=priority)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def hold_sale_order(
    ctx: Context,
    sale_order_code: Annotated[str, Field(description="Sale order code")],
) -> str:
    """Put a sale order on hold."""
    return _call(_client(ctx).sale_orders.hold, sale_order_code=sale_order_code)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def unhold_sale_order(
    ctx: Context,
    sale_order_code: Annotated[str, Field(description="Sale order code")],
) -> str:
    """Release a sale order from hold."""
    return _call(_client(ctx).sale_orders.unhold, sale_order_code=sale_order_code)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def hold_sale_order_items(
    ctx: Context,
    sale_order_code: Annotated[str, Field(description="Sale order code")],
    sale_order_item_codes: Annotated[list[str], Field(description="Item codes to hold")],
) -> str:
    """Put specific items of a sale order on hold."""
    return _call(
        _client(ctx).sale_orders.hold_items,
        sale_order_code=sale_order_code,
        sale_order_item_codes=sale_order_item_codes,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def unhold_sale_order_items(
    ctx: Context,
    sale_order_code: Annotated[str, Field(description="Sale order code")],
    sale_order_item_codes: Annotated[list[str], Field(description="Item codes to unhold")],
) -> str:
    """Release specific items of a sale order from hold."""
    return _call(
        _client(ctx).sale_orders.unhold_items,
        sale_order_code=sale_order_code,
        sale_order_item_codes=sale_order_item_codes,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def edit_sale_order_metadata(
    ctx: Context,
    sale_order_code: Annotated[str, Field(description="Sale order code")],
    priority: Annotated[int | None, Field(description="New priority")] = None,
    custom_field_values: Annotated[list[dict] | None, Field(description="Custom fields [{\"name\": ..., \"value\": ...}]")] = None,
) -> str:
    """Edit metadata (priority, custom fields) on a sale order."""
    return _call(
        _client(ctx).sale_orders.edit_metadata,
        sale_order_code=sale_order_code,
        priority=priority,
        custom_field_values=custom_field_values,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def edit_sale_order_item_metadata(
    ctx: Context,
    sale_order_code: Annotated[str, Field(description="Sale order code")],
    sale_order_item_code: Annotated[str, Field(description="Item code")],
    custom_field_values: Annotated[list[dict], Field(description="Custom fields to set")],
) -> str:
    """Edit custom field values on a specific sale order item."""
    return _call(
        _client(ctx).sale_orders.edit_item_metadata,
        sale_order_code=sale_order_code,
        sale_order_item_code=sale_order_item_code,
        custom_field_values=custom_field_values,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def create_customer(
    ctx: Context,
    customer: Annotated[dict, Field(description="Customer data payload")],
) -> str:
    """Create a new customer."""
    return _call(_client(ctx).sale_orders.create_customer, customer=customer)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def edit_customer(
    ctx: Context,
    customer: Annotated[dict, Field(description="Customer data with updates")],
) -> str:
    """Edit an existing customer."""
    return _call(_client(ctx).sale_orders.edit_customer, customer=customer)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def switch_sale_order_facility(
    ctx: Context,
    facility_code: Annotated[str, Field(description="Target facility code")],
    sale_order_code: Annotated[str, Field(description="Sale order code")],
    sale_order_item_codes: Annotated[list[str], Field(description="Item codes to switch")],
) -> str:
    """Switch the fulfillment facility for specific sale order items."""
    return _call(
        _client(ctx).sale_orders.switch_facility,
        facility_code=facility_code,
        sale_order_code=sale_order_code,
        sale_order_item_codes=sale_order_item_codes,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def add_sale_order_item_detail(
    ctx: Context,
    sale_order_code: Annotated[str, Field(description="Sale order code")],
    sale_order_item_code: Annotated[str, Field(description="Item code")],
    item_details: Annotated[list[dict], Field(description="Item detail records to add")],
) -> str:
    """Add item details (serial numbers, IMEI, etc.) to a sale order item."""
    return _call(
        _client(ctx).sale_orders.add_item_detail,
        sale_order_code=sale_order_code,
        sale_order_item_code=sale_order_item_code,
        item_details=item_details,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def add_sale_order_item_detail_bulk(
    ctx: Context,
    sale_order_code: Annotated[str, Field(description="Sale order code")],
    sale_order_item_detail_dtos: Annotated[list[dict], Field(description="Bulk item detail DTOs")],
) -> str:
    """Bulk add item details across multiple items of a sale order."""
    return _call(
        _client(ctx).sale_orders.add_item_detail_bulk,
        sale_order_code=sale_order_code,
        sale_order_item_detail_dtos=sale_order_item_detail_dtos,
    )


# ===========================================================================
# INVENTORY
# ===========================================================================

@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def adjust_inventory(
    ctx: Context,
    item_sku: Annotated[str, Field(description="SKU code of the item")],
    quantity: Annotated[int, Field(description="Quantity to adjust")],
    shelf_code: Annotated[str, Field(description="Shelf code in the warehouse")],
    adjustment_type: Annotated[str, Field(description="INCREMENT or DECREMENT")],
    inventory_type: Annotated[str, Field(description="Inventory type")] = "GOOD_INVENTORY",
    transfer_to_shelf_code: Annotated[str | None, Field(description="Target shelf for transfers")] = None,
    remarks: Annotated[str | None, Field(description="Adjustment notes")] = None,
    facility: Annotated[str | None, Field(description="Facility code override")] = None,
) -> str:
    """Adjust inventory for a single item (increment, decrement, or transfer between shelves)."""
    return _call(
        _client(ctx).inventory.adjust,
        item_sku=item_sku,
        quantity=quantity,
        shelf_code=shelf_code,
        adjustment_type=adjustment_type,
        inventory_type=inventory_type,
        transfer_to_shelf_code=transfer_to_shelf_code,
        remarks=remarks,
        facility=_resolve_facility(ctx, facility),
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def adjust_inventory_bulk(
    ctx: Context,
    adjustments: Annotated[list[dict], Field(description="List of inventory adjustment objects")],
    facility: Annotated[str | None, Field(description="Facility code override")] = None,
) -> str:
    """Bulk adjust inventory for multiple items at once."""
    return _call(_client(ctx).inventory.adjust_bulk, adjustments=adjustments, facility=_resolve_facility(ctx, facility))


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def get_inventory_snapshot(
    ctx: Context,
    updated_since_in_minutes: Annotated[int, Field(description="Get items updated in last N minutes")] = 60,
    facility: Annotated[str | None, Field(description="Facility code override")] = None,
) -> str:
    """Get a snapshot of current inventory levels, optionally filtered by recent updates."""
    return _call(
        _client(ctx).inventory.get_snapshot,
        updated_since_in_minutes=updated_since_in_minutes,
        facility=_resolve_facility(ctx, facility),
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def mark_inventory_found(
    ctx: Context,
    item_sku: Annotated[str, Field(description="SKU code")],
    shelf_code: Annotated[str, Field(description="Shelf where item was found")],
    quantity_found: Annotated[int, Field(description="Quantity found")],
    ageing_start_date: Annotated[str | None, Field(description="Ageing start date (yyyy-MM-dd)")] = None,
    facility: Annotated[str | None, Field(description="Facility code override")] = None,
) -> str:
    """Mark lost inventory as found on a specific shelf."""
    return _call(
        _client(ctx).inventory.mark_found,
        item_sku=item_sku,
        shelf_code=shelf_code,
        quantity_found=quantity_found,
        ageing_start_date=ageing_start_date,
        facility=_resolve_facility(ctx, facility),
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True, openWorldHint=False),
)
def get_nearby_store_inventory(
    ctx: Context,
    customer_pincode: Annotated[str, Field(description="Customer's pincode")],
    facility_search_radius: Annotated[str, Field(description="Search radius")],
    facility_operational_type: Annotated[str, Field(description="Facility operational type")],
    facility_status: Annotated[str, Field(description="Facility status filter")],
    sku_code: Annotated[str, Field(description="SKU to check availability")],
    quantity: Annotated[int, Field(description="Required quantity")],
) -> str:
    """Check inventory availability at nearby stores for a given SKU and pincode."""
    return _call(
        _client(ctx).inventory.get_nearby_store_inventory,
        customer_pincode=customer_pincode,
        facility_search_radius=facility_search_radius,
        facility_operational_type=facility_operational_type,
        facility_status=facility_status,
        sku_code=sku_code,
        quantity=quantity,
    )


# ===========================================================================
# PRODUCTS
# ===========================================================================

@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def get_product(
    ctx: Context,
    sku_code: Annotated[str, Field(description="Product SKU code")],
) -> str:
    """Get product details by SKU code."""
    return _cached_call(_cache(ctx), "get_product", _client(ctx).products.get, sku_code=sku_code)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def get_product_by_item_code(
    ctx: Context,
    item_code: Annotated[str, Field(description="Unique item code")],
) -> str:
    """Get product details by item code (barcode/serial)."""
    return _cached_call(_cache(ctx), "get_product_by_item_code", _client(ctx).products.get_by_item_code, item_code=item_code)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def search_products(
    ctx: Context,
    filters: Annotated[dict, Field(description="Search filters — e.g. {\"skuCode\": \"SKU-*\", \"categoryCode\": \"ELECTRONICS\"}")],
) -> str:
    """Search products with flexible filters."""
    return _cached_call(_cache(ctx), "search_products", _client(ctx).products.search, **filters)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def create_or_edit_product(
    ctx: Context,
    item_type: Annotated[dict, Field(description="Product item type payload")],
) -> str:
    """Create a new product or edit an existing one."""
    return _call(_client(ctx).products.create_or_edit, item_type=item_type)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def create_or_edit_products_bulk(
    ctx: Context,
    item_types: Annotated[list[dict], Field(description="List of product item type payloads")],
) -> str:
    """Bulk create or edit multiple products."""
    return _call(_client(ctx).products.create_or_edit_bulk, item_types=item_types)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def create_or_edit_category(
    ctx: Context,
    category: Annotated[dict, Field(description="Category payload with name, code, etc.")],
) -> str:
    """Create or edit a product category."""
    return _call(_client(ctx).products.create_or_edit_category, category=category)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def create_channel_item_type(
    ctx: Context,
    params: Annotated[dict, Field(description="Channel item type parameters")],
) -> str:
    """Create a channel-specific item type mapping."""
    return _call(_client(ctx).products.create_channel_item_type, **params)


# ===========================================================================
# FULFILLMENT
# ===========================================================================

@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def create_shipping_package(
    ctx: Context,
    sale_order_code: Annotated[str, Field(description="Sale order code")],
    sale_order_item_codes: Annotated[list[str], Field(description="Item codes to pack")],
) -> str:
    """Create a shipping package for specified sale order items."""
    return _call(
        _client(ctx).fulfillment.create_shipping_package,
        sale_order_code=sale_order_code,
        sale_order_item_codes=sale_order_item_codes,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def get_shipping_package(
    ctx: Context,
    shipping_package_code: Annotated[str, Field(description="Shipping package code")],
) -> str:
    """Get details of a shipping package."""
    return _call(_client(ctx).fulfillment.get_shipping_package, shipping_package_code=shipping_package_code)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def search_shipping_packages(
    ctx: Context,
    filters: Annotated[dict, Field(description="Search filters for shipping packages")],
) -> str:
    """Search shipping packages with filters."""
    return _call(_client(ctx).fulfillment.search_shipping_packages, **filters)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def edit_shipping_package(
    ctx: Context,
    shipping_package_code: Annotated[str, Field(description="Shipping package code")],
    updates: Annotated[dict, Field(description="Fields to update")] = {},
) -> str:
    """Edit a shipping package."""
    return _call(
        _client(ctx).fulfillment.edit_shipping_package,
        shipping_package_code=shipping_package_code,
        **updates,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def split_shipping_package(
    ctx: Context,
    shipping_package_code: Annotated[str, Field(description="Shipping package to split")],
    split_packages: Annotated[list[dict], Field(description="Split configuration")],
) -> str:
    """Split a shipping package into multiple packages."""
    return _call(
        _client(ctx).fulfillment.split_shipping_package,
        shipping_package_code=shipping_package_code,
        split_packages=split_packages,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def modify_shipping_package(
    ctx: Context,
    sale_order_code: Annotated[str, Field(description="Sale order code")],
    sale_order_item_codes: Annotated[list[str], Field(description="Item codes to modify")],
) -> str:
    """Modify items in a shipping package."""
    return _call(
        _client(ctx).fulfillment.modify_shipping_package,
        sale_order_code=sale_order_code,
        sale_order_item_codes=sale_order_item_codes,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def get_shipping_packages_by_status(
    ctx: Context,
    status_code: Annotated[str | None, Field(description="Filter by status code")] = None,
) -> str:
    """Get shipping packages, optionally filtered by status."""
    return _call(_client(ctx).fulfillment.get_shipping_packages, status_code=status_code)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def create_invoice(
    ctx: Context,
    shipping_package_code: Annotated[str, Field(description="Shipping package code")],
) -> str:
    """Create an invoice for a shipping package."""
    return _call(_client(ctx).fulfillment.create_invoice, shipping_package_code=shipping_package_code)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def get_invoice_details(
    ctx: Context,
    shipping_package_code: Annotated[str, Field(description="Shipping package code")],
    is_return: Annotated[bool, Field(description="Whether this is a return invoice")] = False,
    payment_detail_required: Annotated[bool, Field(description="Include payment details")] = False,
) -> str:
    """Get invoice details for a shipping package."""
    return _call(
        _client(ctx).fulfillment.get_invoice_details,
        shipping_package_code=shipping_package_code,
        is_return=is_return,
        payment_detail_required=payment_detail_required,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def get_invoice_label(
    ctx: Context,
    shipping_package_code: Annotated[str, Field(description="Shipping package code")],
) -> str:
    """Get the invoice label for a shipping package."""
    return _cached_call(_cache(ctx), "get_invoice_label", _client(ctx).fulfillment.get_invoice_label, shipping_package_code=shipping_package_code)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def create_invoice_and_label(
    ctx: Context,
    shipping_package_code: Annotated[str, Field(description="Shipping package code")],
    generate_uniware_shipping_label: Annotated[bool, Field(description="Generate Uniware shipping label")] = True,
) -> str:
    """Create invoice and generate shipping label in one call."""
    return _call(
        _client(ctx).fulfillment.create_invoice_and_label,
        shipping_package_code=shipping_package_code,
        generate_uniware_shipping_label=generate_uniware_shipping_label,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def create_invoice_by_sale_order(
    ctx: Context,
    sale_order_code: Annotated[str, Field(description="Sale order code")],
    sale_order_item_codes: Annotated[list[str], Field(description="Item codes to invoice")],
) -> str:
    """Create an invoice directly from sale order item codes."""
    return _call(
        _client(ctx).fulfillment.create_invoice_by_sale_order,
        sale_order_code=sale_order_code,
        sale_order_item_codes=sale_order_item_codes,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def create_invoice_with_details(
    ctx: Context,
    sale_order_code: Annotated[str, Field(description="Sale order code")],
    invoice: Annotated[dict, Field(description="Invoice detail payload")],
) -> str:
    """Create an invoice with custom details."""
    return _call(
        _client(ctx).fulfillment.create_invoice_with_details,
        sale_order_code=sale_order_code,
        invoice=invoice,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def create_invoice_and_allocate_provider(
    ctx: Context,
    shipping_package_code: Annotated[str, Field(description="Shipping package code")],
) -> str:
    """Create invoice and allocate a shipping provider in one call."""
    return _call(
        _client(ctx).fulfillment.create_invoice_and_allocate_provider,
        shipping_package_code=shipping_package_code,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def get_invoice_pdf(
    ctx: Context,
    invoice_codes: Annotated[list[str], Field(description="Invoice codes to download")],
) -> str:
    """Download invoice PDF(s). Returns base64-encoded PDF content."""
    return _cached_pdf_call(
        _cache(ctx), "get_invoice_pdf",
        _client(ctx).fulfillment.get_invoice_pdf, invoice_codes=invoice_codes,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def get_shipping_label_pdf(
    ctx: Context,
    shipping_package_codes: Annotated[list[str], Field(description="Shipping package codes")],
) -> str:
    """Download shipping label PDF(s). Returns base64-encoded PDF content."""
    return _cached_pdf_call(
        _cache(ctx), "get_shipping_label_pdf",
        _client(ctx).fulfillment.get_shipping_label_pdf, shipping_package_codes=shipping_package_codes,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def check_serviceability(
    ctx: Context,
    pincode: Annotated[str, Field(description="Delivery pincode to check")],
    cash_on_delivery: Annotated[bool, Field(description="Check COD availability")],
) -> str:
    """Check if a pincode is serviceable and whether COD is available."""
    return _cached_call(
        _cache(ctx), "check_serviceability",
        _client(ctx).fulfillment.check_serviceability,
        pincode=pincode,
        cash_on_delivery=cash_on_delivery,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def allocate_shipping_provider(
    ctx: Context,
    shipping_package_code: Annotated[str, Field(description="Shipping package code")],
) -> str:
    """Allocate a shipping provider to a package."""
    return _call(
        _client(ctx).fulfillment.allocate_shipping_provider,
        shipping_package_code=shipping_package_code,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def update_tracking_status(
    ctx: Context,
    provider_code: Annotated[str, Field(description="Shipping provider code")],
    tracking_number: Annotated[str, Field(description="Tracking/AWB number")],
    tracking_status: Annotated[str, Field(description="New tracking status")],
    status_date: Annotated[str | None, Field(description="Status date (yyyy-MM-dd HH:mm:ss)")] = None,
    shipment_tracking_status_name: Annotated[str | None, Field(description="Human-readable status name")] = None,
    rto_tracking_number: Annotated[str | None, Field(description="RTO tracking number")] = None,
    rto_reason: Annotated[str | None, Field(description="RTO reason")] = None,
) -> str:
    """Update the tracking status of a shipment."""
    return _call(
        _client(ctx).fulfillment.update_tracking_status,
        provider_code=provider_code,
        tracking_number=tracking_number,
        tracking_status=tracking_status,
        status_date=status_date,
        shipment_tracking_status_name=shipment_tracking_status_name,
        rto_tracking_number=rto_tracking_number,
        rto_reason=rto_reason,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def create_manifest(
    ctx: Context,
    channel: Annotated[str, Field(description="Sales channel")],
    third_party_shipping: Annotated[bool, Field(description="Uses third-party shipping provider")],
    shipping_provider_code: Annotated[str | None, Field(description="Shipping provider code")] = None,
) -> str:
    """Create a new shipping manifest."""
    return _call(
        _client(ctx).fulfillment.create_manifest,
        channel=channel,
        third_party_shipping=third_party_shipping,
        shipping_provider_code=shipping_provider_code,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def get_manifest(
    ctx: Context,
    shipping_manifest_code: Annotated[str, Field(description="Manifest code")],
) -> str:
    """Get details of a shipping manifest."""
    return _call(_client(ctx).fulfillment.get_manifest, shipping_manifest_code=shipping_manifest_code)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def add_package_to_manifest(
    ctx: Context,
    shipping_manifest_code: Annotated[str, Field(description="Manifest code")],
    shipping_package_codes: Annotated[list[str], Field(description="Package codes to add")],
) -> str:
    """Add shipping packages to an existing manifest."""
    return _call(
        _client(ctx).fulfillment.add_package_to_manifest,
        shipping_manifest_code=shipping_manifest_code,
        shipping_package_codes=shipping_package_codes,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def create_and_close_manifest(
    ctx: Context,
    params: Annotated[dict, Field(description="Manifest creation parameters")],
) -> str:
    """Create a manifest and close it immediately."""
    return _call(_client(ctx).fulfillment.create_and_close_manifest, **params)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def close_manifest(
    ctx: Context,
    shipping_manifest_code: Annotated[str, Field(description="Manifest code to close")],
) -> str:
    """Close a shipping manifest (no more packages can be added)."""
    return _call(_client(ctx).fulfillment.close_manifest, shipping_manifest_code=shipping_manifest_code)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def dispatch_shipping_package(
    ctx: Context,
    shipping_package_code: Annotated[str, Field(description="Shipping package code")],
) -> str:
    """Dispatch a shipping package (mark as shipped)."""
    return _call(_client(ctx).fulfillment.dispatch, shipping_package_code=shipping_package_code)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def force_dispatch_shipping_package(
    ctx: Context,
    shipping_package_code: Annotated[str, Field(description="Shipping package code")],
) -> str:
    """Force dispatch a shipping package, bypassing normal validations."""
    return _call(_client(ctx).fulfillment.force_dispatch, shipping_package_code=shipping_package_code)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def create_and_dispatch(
    ctx: Context,
    sale_order_code: Annotated[str, Field(description="Sale order code")],
    sale_order_item_info: Annotated[list[dict], Field(description="Item info list")],
    shipping_package_info: Annotated[dict, Field(description="Shipping package configuration")],
    invoice_info: Annotated[dict | None, Field(description="Optional invoice details")] = None,
) -> str:
    """Create a shipping package and dispatch it in one call."""
    return _call(
        _client(ctx).fulfillment.create_and_dispatch,
        sale_order_code=sale_order_code,
        sale_order_item_info=sale_order_item_info,
        shipping_package_info=shipping_package_info,
        invoice_info=invoice_info,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def mark_delivered(
    ctx: Context,
    sale_order_code: Annotated[str, Field(description="Sale order code")],
    sale_order_item_codes: Annotated[list[str], Field(description="Item codes to mark delivered")],
    pod_code: Annotated[str | None, Field(description="Proof of delivery code")] = None,
) -> str:
    """Mark sale order items as delivered."""
    return _call(
        _client(ctx).fulfillment.mark_delivered,
        sale_order_code=sale_order_code,
        sale_order_item_codes=sale_order_item_codes,
        pod_code=pod_code,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def create_picklist(
    ctx: Context,
    shipping_package_codes: Annotated[list[str], Field(description="Package codes for the picklist")],
    destination: Annotated[str | None, Field(description="Picklist destination (omit for staging)")] = None,
) -> str:
    """Create a picklist for warehouse picking."""
    return _call(
        _client(ctx).fulfillment.create_picklist,
        shipping_package_codes=shipping_package_codes,
        destination=destination,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def create_or_update_reason(
    ctx: Context,
    name: Annotated[str, Field(description="Reason list name")],
    value: Annotated[str, Field(description="Reason value")],
) -> str:
    """Create or update a custom reason entry."""
    return _call(_client(ctx).fulfillment.create_or_update_reason, name=name, value=value)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def update_seal_id(
    ctx: Context,
    shipping_package_code: Annotated[str, Field(description="Shipping package code")],
    shipping_package_type_code: Annotated[str, Field(description="Package type code")],
    spt_item_seal_id: Annotated[str, Field(description="Seal ID")],
    shipment_actual_weight_calculation_required: Annotated[bool | None, Field(description="Recalculate weight")] = None,
) -> str:
    """Update the seal ID on a shipping package."""
    return _call(
        _client(ctx).fulfillment.update_seal_id,
        shipping_package_code=shipping_package_code,
        shipping_package_type_code=shipping_package_type_code,
        spt_item_seal_id=spt_item_seal_id,
        shipment_actual_weight_calculation_required=shipment_actual_weight_calculation_required,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def update_seal_id_bulk(
    ctx: Context,
    packages: Annotated[list[dict], Field(description="List of package seal update objects")],
) -> str:
    """Bulk update seal IDs on multiple shipping packages."""
    return _call(_client(ctx).fulfillment.update_seal_id_bulk, packages=packages)


# ===========================================================================
# INBOUND / PURCHASING
# ===========================================================================

@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def create_vendor(
    ctx: Context,
    vendor: Annotated[dict, Field(description="Vendor data payload")],
) -> str:
    """Create a new vendor."""
    return _call(_client(ctx).inbound.create_vendor, vendor=vendor)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def create_or_edit_vendor_catalog(
    ctx: Context,
    vendor_item_type: Annotated[dict, Field(description="Vendor item type mapping")],
) -> str:
    """Create or edit a vendor's product catalog mapping."""
    return _call(_client(ctx).inbound.create_or_edit_vendor_catalog, vendor_item_type=vendor_item_type)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def get_vendor_backorder_items(
    ctx: Context,
    filters: Annotated[dict, Field(description="Backorder search filters")],
) -> str:
    """Get vendor backorder items."""
    return _cached_call(_cache(ctx), "get_vendor_backorder_items", _client(ctx).inbound.get_vendor_backorder_items, **filters)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def create_purchase_order(
    ctx: Context,
    vendor_code: Annotated[str, Field(description="Vendor code")],
    purchase_order_items: Annotated[list[dict] | None, Field(description="PO line items")] = None,
) -> str:
    """Create a new purchase order."""
    return _call(
        _client(ctx).inbound.create_purchase_order,
        vendor_code=vendor_code,
        purchase_order_items=purchase_order_items,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def get_purchase_order(
    ctx: Context,
    purchase_order_code: Annotated[str, Field(description="Purchase order code")],
) -> str:
    """Get purchase order details."""
    return _call(_client(ctx).inbound.get_purchase_order, purchase_order_code=purchase_order_code)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def search_purchase_orders(
    ctx: Context,
    filters: Annotated[dict, Field(description="Search filters for purchase orders")],
) -> str:
    """Search purchase orders."""
    return _call(_client(ctx).inbound.search_purchase_orders, **filters)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def approve_purchase_order(
    ctx: Context,
    purchase_order_code: Annotated[str, Field(description="Purchase order code to approve")],
) -> str:
    """Approve a purchase order."""
    return _call(_client(ctx).inbound.approve_purchase_order, purchase_order_code=purchase_order_code)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def create_and_approve_purchase_order(
    ctx: Context,
    vendor_code: Annotated[str, Field(description="Vendor code")],
    user_id: Annotated[str, Field(description="Approving user ID")],
    purchase_order_items: Annotated[list[dict], Field(description="PO line items")],
) -> str:
    """Create and immediately approve a purchase order."""
    return _call(
        _client(ctx).inbound.create_and_approve_purchase_order,
        vendor_code=vendor_code,
        user_id=user_id,
        purchase_order_items=purchase_order_items,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def close_purchase_order(
    ctx: Context,
    purchase_order_code: Annotated[str, Field(description="Purchase order code to close")],
) -> str:
    """Close a purchase order."""
    return _call(_client(ctx).inbound.close_purchase_order, purchase_order_code=purchase_order_code)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def create_grn(
    ctx: Context,
    purchase_order_code: Annotated[str, Field(description="Purchase order code")],
) -> str:
    """Create a Goods Receipt Note (GRN) for a purchase order."""
    return _call(_client(ctx).inbound.create_grn, purchase_order_code=purchase_order_code)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def get_grn(
    ctx: Context,
    inflow_receipt_code: Annotated[str, Field(description="GRN / inflow receipt code")],
) -> str:
    """Get GRN (Goods Receipt Note) details."""
    return _call(_client(ctx).inbound.get_grn, inflow_receipt_code=inflow_receipt_code)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def add_item_to_grn(
    ctx: Context,
    inflow_receipt_code: Annotated[str, Field(description="GRN code")],
    inflow_receipt_item: Annotated[dict, Field(description="Item to add to the GRN")],
) -> str:
    """Add an item to a GRN by SKU."""
    return _call(
        _client(ctx).inbound.add_item_to_grn,
        inflow_receipt_code=inflow_receipt_code,
        inflow_receipt_item=inflow_receipt_item,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def add_item_to_grn_by_code(
    ctx: Context,
    inflow_receipt_code: Annotated[str, Field(description="GRN code")],
    item_code: Annotated[str, Field(description="Item code to add")],
    manufacturing_date: Annotated[str | None, Field(description="Manufacturing date")] = None,
) -> str:
    """Add an item to a GRN by item code."""
    return _call(
        _client(ctx).inbound.add_item_to_grn_by_code,
        inflow_receipt_code=inflow_receipt_code,
        item_code=item_code,
        manufacturing_date=manufacturing_date,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def search_grns(
    ctx: Context,
    filters: Annotated[dict, Field(description="GRN search filters")],
) -> str:
    """Search Goods Receipt Notes."""
    return _call(_client(ctx).inbound.search_grns, **filters)


# ===========================================================================
# RETURNS
# ===========================================================================

@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def search_returns(
    ctx: Context,
    return_type: Annotated[str, Field(description="Return type (e.g. CUSTOMER_RETURN)")],
    updated_from: Annotated[str | None, Field(description="Updated from date")] = None,
    updated_to: Annotated[str | None, Field(description="Updated to date")] = None,
    created_from: Annotated[str | None, Field(description="Created from date")] = None,
    created_to: Annotated[str | None, Field(description="Created to date")] = None,
    status_code: Annotated[str | None, Field(description="Status filter")] = None,
) -> str:
    """Search returns by type, date range, and status."""
    return _call(
        _client(ctx).returns.search,
        return_type=return_type,
        updated_from=updated_from,
        updated_to=updated_to,
        created_from=created_from,
        created_to=created_to,
        status_code=status_code,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def get_return(
    ctx: Context,
    shipment_code: Annotated[str | None, Field(description="Shipment code")] = None,
    reverse_pickup_code: Annotated[str | None, Field(description="Reverse pickup code")] = None,
) -> str:
    """Get return details by shipment code or reverse pickup code."""
    return _call(
        _client(ctx).returns.get,
        shipment_code=shipment_code,
        reverse_pickup_code=reverse_pickup_code,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def create_reverse_pickup(
    ctx: Context,
    sale_order_code: Annotated[str, Field(description="Sale order code")],
    reverse_pick_items: Annotated[list[dict], Field(description="Items for reverse pickup")],
    action_code: Annotated[str, Field(description="Action code (default WAC = Warehouse Accepted)")] = "WAC",
) -> str:
    """Create a reverse pickup request for returned items."""
    return _call(
        _client(ctx).returns.create_reverse_pickup,
        sale_order_code=sale_order_code,
        reverse_pick_items=reverse_pick_items,
        action_code=action_code,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def edit_reverse_pickup(
    ctx: Context,
    reverse_pickup_code: Annotated[str, Field(description="Reverse pickup code")],
    updates: Annotated[dict, Field(description="Fields to update")] = {},
) -> str:
    """Edit a reverse pickup request."""
    return _call(
        _client(ctx).returns.edit_reverse_pickup,
        reverse_pickup_code=reverse_pickup_code,
        **updates,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def approve_reverse_pickup(
    ctx: Context,
    reverse_pickup_codes: Annotated[list[str], Field(description="Reverse pickup codes to approve")],
) -> str:
    """Approve one or more reverse pickup requests."""
    return _call(_client(ctx).returns.approve_reverse_pickup, reverse_pickup_codes=reverse_pickup_codes)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True),
)
def cancel_reverse_pickup(
    ctx: Context,
    reverse_pickup_code: Annotated[str, Field(description="Reverse pickup code to cancel")],
) -> str:
    """Cancel a reverse pickup request."""
    return _call(_client(ctx).returns.cancel_reverse_pickup, reverse_pickup_code=reverse_pickup_code)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def allocate_courier_for_reverse_pickup(
    ctx: Context,
    reverse_pickup_codes: Annotated[list[str], Field(description="Reverse pickup codes")],
) -> str:
    """Allocate a courier for reverse pickup."""
    return _call(
        _client(ctx).returns.allocate_courier_for_reverse_pickup,
        reverse_pickup_codes=reverse_pickup_codes,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def mark_returned(
    ctx: Context,
    sale_order_code: Annotated[str, Field(description="Sale order code")],
    sale_order_items: Annotated[list[dict], Field(description="Items to mark as returned")],
    return_reason: Annotated[str, Field(description="Return reason")],
) -> str:
    """Mark sale order items as returned."""
    return _call(
        _client(ctx).returns.mark_returned,
        sale_order_code=sale_order_code,
        sale_order_items=sale_order_items,
        return_reason=return_reason,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def mark_returned_with_inventory_type(
    ctx: Context,
    sale_order_code: Annotated[str, Field(description="Sale order code")],
    sale_order_items: Annotated[list[dict], Field(description="Items with inventory type info")],
) -> str:
    """Mark items as returned with specific inventory type classification."""
    return _call(
        _client(ctx).returns.mark_returned_with_inventory_type,
        sale_order_code=sale_order_code,
        sale_order_items=sale_order_items,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def create_alternate_item(
    ctx: Context,
    sale_order_items: Annotated[list[dict], Field(description="Original sale order items")],
    sale_order_item_alternates: Annotated[list[dict], Field(description="Alternate item options")],
) -> str:
    """Create alternate item options for a return/exchange."""
    return _call(
        _client(ctx).returns.create_alternate_item,
        sale_order_items=sale_order_items,
        sale_order_item_alternates=sale_order_item_alternates,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def accept_alternate_item(
    ctx: Context,
    sale_order_code: Annotated[str, Field(description="Sale order code")],
    sale_order_item_codes: Annotated[list[str], Field(description="Item codes being replaced")],
    selected_alternate_item_sku: Annotated[str, Field(description="SKU of the selected alternate")],
) -> str:
    """Accept an alternate item for a return/exchange."""
    return _call(
        _client(ctx).returns.accept_alternate_item,
        sale_order_code=sale_order_code,
        sale_order_item_codes=sale_order_item_codes,
        selected_alternate_item_sku=selected_alternate_item_sku,
    )


# ===========================================================================
# OUTBOUND / GATEPASS
# ===========================================================================

@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def create_gatepass(
    ctx: Context,
    type: Annotated[str, Field(description="Gatepass type")],
    party_code: Annotated[str, Field(description="Party (vendor/customer) code")],
    ws_gate_pass: Annotated[dict | None, Field(description="Additional gatepass data")] = None,
) -> str:
    """Create a new outbound gatepass."""
    return _call(
        _client(ctx).outbound.create_gatepass,
        type=type,
        party_code=party_code,
        ws_gate_pass=ws_gate_pass,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def edit_gatepass(
    ctx: Context,
    gate_pass_code: Annotated[str, Field(description="Gatepass code")],
    ws_gate_pass: Annotated[dict | None, Field(description="Updated gatepass data")] = None,
) -> str:
    """Edit an existing gatepass."""
    return _call(
        _client(ctx).outbound.edit_gatepass,
        gate_pass_code=gate_pass_code,
        ws_gate_pass=ws_gate_pass,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def scan_gatepass_item(
    ctx: Context,
    gate_pass_code: Annotated[str, Field(description="Gatepass code")],
    item_code: Annotated[str, Field(description="Item code to scan")],
) -> str:
    """Scan an item into a gatepass."""
    return _call(
        _client(ctx).outbound.scan_item,
        gate_pass_code=gate_pass_code,
        item_code=item_code,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def add_nontraceable_gatepass_item(
    ctx: Context,
    gate_pass_code: Annotated[str, Field(description="Gatepass code")],
    item_sku: Annotated[str, Field(description="Item SKU")],
    inventory_type: Annotated[str, Field(description="Inventory type")],
    quantity: Annotated[int, Field(description="Quantity")],
    unit_price: Annotated[float, Field(description="Unit price")],
    shelf_code: Annotated[str, Field(description="Source shelf code")],
) -> str:
    """Add a non-traceable item to a gatepass."""
    return _call(
        _client(ctx).outbound.add_nontraceable_item,
        gate_pass_code=gate_pass_code,
        item_sku=item_sku,
        inventory_type=inventory_type,
        quantity=quantity,
        unit_price=unit_price,
        shelf_code=shelf_code,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def remove_gatepass_item(
    ctx: Context,
    gate_pass_code: Annotated[str, Field(description="Gatepass code")],
    item_code: Annotated[str, Field(description="Item code to remove")],
) -> str:
    """Remove an item from a gatepass."""
    return _call(
        _client(ctx).outbound.remove_gatepass_item,
        gate_pass_code=gate_pass_code,
        item_code=item_code,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def complete_gatepass(
    ctx: Context,
    gate_pass_code: Annotated[str, Field(description="Gatepass code to complete")],
) -> str:
    """Complete/finalize a gatepass."""
    return _call(_client(ctx).outbound.complete_gatepass, gate_pass_code=gate_pass_code)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True),
)
def discard_gatepass(
    ctx: Context,
    gate_pass_code: Annotated[str, Field(description="Gatepass code to discard")],
) -> str:
    """Discard/cancel a gatepass."""
    return _call(_client(ctx).outbound.discard_gatepass, gate_pass_code=gate_pass_code)


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def search_gatepass(
    ctx: Context,
    from_date: Annotated[str, Field(description="Start date (yyyy-MM-dd)")],
    to_date: Annotated[str, Field(description="End date (yyyy-MM-dd)")],
) -> str:
    """Search gatepasses within a date range."""
    return _cached_call(
        _cache(ctx), "search_gatepass",
        _client(ctx).outbound.search_gatepass,
        from_date=from_date,
        to_date=to_date,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def get_gatepass(
    ctx: Context,
    gate_pass_codes: Annotated[list[str], Field(description="Gatepass codes to retrieve")],
) -> str:
    """Get details of one or more gatepasses."""
    return _cached_call(_cache(ctx), "get_gatepass", _client(ctx).outbound.get_gatepass, gate_pass_codes=gate_pass_codes)


# ===========================================================================
# FACILITIES
# ===========================================================================

@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def search_facilities(
    ctx: Context,
    from_date: Annotated[str, Field(description="Start date (yyyy-MM-dd)")],
    to_date: Annotated[str, Field(description="End date (yyyy-MM-dd)")],
    date_type: Annotated[str, Field(description="Date field to filter on")] = "CREATED",
    facility_status: Annotated[str, Field(description="Status filter")] = "ALL",
) -> str:
    """Search facilities within a date range."""
    return _cached_call(
        _cache(ctx), "search_facilities",
        _client(ctx).facilities.search,
        from_date=from_date,
        to_date=to_date,
        date_type=date_type,
        facility_status=facility_status,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def get_facility_details(
    ctx: Context,
    facility_code: Annotated[str, Field(description="Facility code")],
) -> str:
    """Get details of a specific facility/warehouse."""
    return _cached_call(_cache(ctx), "get_facility_details", _client(ctx).facilities.get_details, facility_code=facility_code)


# ===========================================================================
# EXPORT JOBS
# ===========================================================================

@mcp.tool( annotations=ToolAnnotations(readOnlyHint=False))
def create_export_job(
    ctx: Context,
    export_job_type_name: Annotated[str, Field(description="Export job type (e.g. SALE_ORDER, INVENTORY)")],
    export_columns: Annotated[list[str], Field(description="Columns to include in the export")],
    export_filters: Annotated[list[dict] | None, Field(description="Optional filters for the export")] = None,
    frequency: Annotated[str, Field(description="ONETIME or RECURRING")] = "ONETIME",
    notification_email: Annotated[str | None, Field(description="Email to notify when export is ready")] = None,
    schedule_time: Annotated[str | None, Field(description="Schedule time for the export")] = None,
    cron_expression: Annotated[str | None, Field(description="Cron expression for recurring exports")] = None,
    report_name: Annotated[str | None, Field(description="Custom report name")] = None,
) -> str:
    """Create a data export job (CSV/Excel reports)."""
    return _call(
        _client(ctx).export_jobs.create,
        export_job_type_name=export_job_type_name,
        export_columns=export_columns,
        export_filters=export_filters,
        frequency=frequency,
        notification_email=notification_email,
        schedule_time=schedule_time,
        cron_expression=cron_expression,
        report_name=report_name,
    )


@mcp.tool( annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
)
def get_export_job_status(
    ctx: Context,
    job_code: Annotated[str, Field(description="Export job code")],
) -> str:
    """Check the status of an export job."""
    return _cached_call(_cache(ctx), "get_export_job_status", _client(ctx).export_jobs.get_status, job_code=job_code)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))
def poll_export_job(
    ctx: Context,
    job_code: Annotated[str, Field(description="Export job code returned by create_export_job")],
    poll_interval: Annotated[int, Field(description="Seconds between status checks")] = 10,
    timeout: Annotated[int, Field(description="Maximum seconds to wait before giving up")] = 300,
) -> str:
    """Poll an export job until it reaches a terminal status (COMPLETE, SUCCESSFUL, or FAILED).
    Blocks until the job finishes or the timeout is reached."""
    deadline = time.monotonic() + timeout
    client = _client(ctx)
    last_result = None

    while True:
        last_result = _call(client.export_jobs.get_status, job_code=job_code)
        data = json.loads(last_result)
        status = data.get("status")

        if status in _TERMINAL_EXPORT_STATUSES:
            cache = _cache(ctx)
            key = _cache_key("get_export_job_status", (), {"job_code": job_code})
            ttl = _CACHE_TTL.get("get_export_job_status", 86400)
            cache.set(key, last_result, ttl)
            return last_result

        if time.monotonic() >= deadline:
            data["_poll_timeout"] = True
            data["_message"] = f"Polling timed out after {timeout}s. Last status: {status}"
            return json.dumps(data, default=str, ensure_ascii=False)

        time.sleep(poll_interval)


# ===========================================================================
# SESSION
# ===========================================================================

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, idempotentHint=True))
def set_facility(
    ctx: Context,
    facility_code: Annotated[str | None, Field(description="Facility code to use for all subsequent calls. Pass null to clear and revert to the default.")] = None,
) -> str:
    """Set the default facility for all subsequent tool calls in this session. Overrides the UC_FACILITY environment variable. Pass null to clear."""
    _app_ctx(ctx).facility_override = facility_code
    config_default = _client(ctx)._config.facility
    effective = facility_code or config_default or None
    return json.dumps({"facility_override": facility_code, "config_default": config_default, "effective_facility": effective, "success": True})


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))
def get_facility(ctx: Context) -> str:
    """Get the current effective facility. Shows both the session override and the config default."""
    override = _app_ctx(ctx).facility_override
    config_default = _client(ctx)._config.facility
    effective = override or config_default or None
    return json.dumps({"session_override": override, "config_default": config_default, "effective_facility": effective})


# ===========================================================================
# CACHE MANAGEMENT
# ===========================================================================

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False))
def clear_cache(ctx: Context) -> str:
    """Clear all cached responses. Use when you suspect stale data."""
    count = _cache(ctx).clear()
    return json.dumps({"cleared_entries": count, "success": True})


# ===========================================================================
# Entry point
# ===========================================================================

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
