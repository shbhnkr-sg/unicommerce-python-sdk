# unicommerce

A modern, async-first Python SDK for the [Unicommerce](https://www.unicommerce.com/) REST API.

- Python 3.12+
- Sync and async clients (powered by [httpx](https://www.python-httpx.org/))
- Pydantic v2 models for all responses
- OAuth 2.0 with automatic token refresh
- Retry with exponential backoff
- Custom exception hierarchy
- **98 API methods** across 9 resource domains

## Installation

```bash
pip install unicommerce
```

## Quick Start

```python
from unicommerce import Unicommerce

client = Unicommerce(
    tenant="your-tenant",
    username="your-username",
    password="your-password",
)

# Search sale orders
results = client.sale_orders.search(status="CREATED")
for order in results.sale_orders:
    print(order.code, order.status_code)

# Get full order details
order = client.sale_orders.get(code="SO-12345")
print(order.sale_order_code)

# Adjust inventory
client.inventory.adjust(
    item_sku="SKU-100",
    quantity=10,
    shelf_code="DEFAULT",
    adjustment_type="ADD",
)

client.close()
```

## Async Usage

```python
import asyncio
from unicommerce import AsyncUnicommerce

async def main():
    async with AsyncUnicommerce(
        tenant="your-tenant",
        username="your-username",
        password="your-password",
    ) as client:
        order = await client.sale_orders.get(code="SO-12345")
        print(order.sale_order_code)

asyncio.run(main())
```

## API Reference

### Sale Orders (18 methods)

```python
# Search orders with filters
results = client.sale_orders.search(status="CREATED", channel="MYNTRA")

# Get full order with items and shipping packages
order = client.sale_orders.get(code="SO-12345")

# Create a sale order
from unicommerce.models import CreateSaleOrderRequest
order = client.sale_orders.create(CreateSaleOrderRequest(...))

# Cancel (full or partial)
client.sale_orders.cancel(
    sale_order_code="SO-12345",
    sale_order_item_codes=["SOI-001"],
    cancellation_reason="Customer request",
    cancel_partially=True,
)

# Edit addresses
client.sale_orders.edit(
    sale_order_code="SO-12345",
    addresses=[{"type": "SHIPPING", "city": "Mumbai"}],
)

# Verify / set priority
client.sale_orders.verify(sale_order_code="SO-12345")
client.sale_orders.set_priority(sale_order_code="SO-12345", priority=1)

# Customer management
client.sale_orders.create_customer(customer={"name": "John", "email": "john@example.com"})
client.sale_orders.edit_customer(customer={"code": "C-001", "name": "John Doe"})

# Edit order/item metadata
client.sale_orders.edit_metadata(
    sale_order_code="SO-12345",
    priority=1,
    custom_field_values=[{"name": "field1", "value": "val1"}],
)
client.sale_orders.edit_item_metadata(
    sale_order_code="SO-12345",
    sale_order_item_code="SOI-001",
    custom_field_values=[{"name": "field1", "value": "val1"}],
)

# Hold / unhold orders and items
client.sale_orders.hold(sale_order_code="SO-12345")
client.sale_orders.unhold(sale_order_code="SO-12345")
client.sale_orders.hold_items(sale_order_code="SO-12345", sale_order_item_codes=["SOI-001"])
client.sale_orders.unhold_items(sale_order_code="SO-12345", sale_order_item_codes=["SOI-001"])

# Switch facility
client.sale_orders.switch_facility(
    facility_code="WAREHOUSE-2",
    sale_order_code="SO-12345",
    sale_order_item_codes=["SOI-001"],
)

# Add item details (e.g. serial numbers, IMEI)
client.sale_orders.add_item_detail(
    sale_order_code="SO-12345",
    sale_order_item_code="SOI-001",
    item_details=[{"imeiNumber": "123456789"}],
)
client.sale_orders.add_item_detail_bulk(
    sale_order_code="SO-12345",
    sale_order_item_detail_dtos=[...],
)
```

### Inventory (5 methods)

```python
# Get inventory snapshot
snapshot = client.inventory.get_snapshot(updated_since_in_minutes=60)
for item in snapshot.inventory_snapshots:
    print(item.item_type_sku, item.inventory)

# Adjust inventory
client.inventory.adjust(
    item_sku="SKU-100",
    quantity=5,
    shelf_code="DEFAULT",
    adjustment_type="ADD",
    inventory_type="GOOD_INVENTORY",
)

# Bulk adjust
client.inventory.adjust_bulk(adjustments=[...])

# Mark quantity found (cycle count)
client.inventory.mark_found(
    item_sku="SKU-100",
    shelf_code="DEFAULT",
    quantity_found=10,
)

# Get nearby store inventory
client.inventory.get_nearby_store_inventory(
    channel_product_id="CP-001",
    pincode="110001",
)
```

### Products (7 methods)

```python
# Get product by SKU
product = client.products.get(sku_code="SKU-100")
print(product.name, product.category_name)

# Get product by item code
product = client.products.get_by_item_code(item_code="ITEM-001")

# Search products
results = client.products.search(skuCode="SKU-100")

# Create or edit a product
client.products.create_or_edit(item_type={"skuCode": "SKU-100", "name": "T-Shirt"})

# Bulk create or edit
client.products.create_or_edit_bulk(item_types=[...])

# Create or edit a category
client.products.create_or_edit_category(category={"name": "Apparel"})

# Create channel item type mapping
client.products.create_channel_item_type(
    channel_code="MYNTRA",
    channel_product_id="MYN-001",
    item_type_sku="SKU-100",
)
```

### Fulfillment (30 methods)

```python
# --- Shipping Packages ---

# Get shipping package details
sp = client.fulfillment.get_shipping_package(shipping_package_code="SP-001")

# Search shipping packages
results = client.fulfillment.search_shipping_packages(status="DISPATCHED")

# Create shipping package
client.fulfillment.create_shipping_package(
    sale_order_code="SO-12345",
    sale_order_item_codes=["SOI-001", "SOI-002"],
)

# Edit / split / modify shipping packages
client.fulfillment.edit_shipping_package(shipping_package_code="SP-001", actualWeight=1.5)
client.fulfillment.split_shipping_package(
    shipping_package_code="SP-001",
    split_packages=[{"saleOrderItemCodes": ["SOI-001"]}],
)
client.fulfillment.modify_shipping_package(
    sale_order_code="SO-12345",
    sale_order_item_codes=["SOI-001"],
)

# Get shipping packages by status
client.fulfillment.get_shipping_packages(status_code="DISPATCHED")

# --- Invoicing ---

# Create invoice
client.fulfillment.create_invoice(shipping_package_code="SP-001")

# Get invoice details
invoice = client.fulfillment.get_invoice_details(shipping_package_code="SP-001")

# Get invoice label (base64 PDF)
label = client.fulfillment.get_invoice_label(shipping_package_code="SP-001")

# Create invoice + shipping label
result = client.fulfillment.create_invoice_and_label(
    shipping_package_code="SP-001",
    generate_uniware_shipping_label=True,
)

# Create invoice by sale order code
client.fulfillment.create_invoice_by_sale_order(
    sale_order_code="SO-12345",
    sale_order_item_codes=["SOI-001"],
)

# Create invoice with full details
client.fulfillment.create_invoice_with_details(
    sale_order_code="SO-12345",
    invoice={"invoiceDate": "2026-06-21"},
)

# Create invoice and allocate shipping provider
client.fulfillment.create_invoice_and_allocate_provider(shipping_package_code="SP-001")

# --- Shipping Providers ---

# Allocate shipping provider
client.fulfillment.allocate_shipping_provider(shipping_package_code="SP-001")

# Check pincode serviceability
client.fulfillment.check_serviceability(pincode="110001", cash_on_delivery=False)

# --- Manifests ---

# Create manifest
manifest = client.fulfillment.create_manifest(
    channel="MYNTRA",
    third_party_shipping=True,
    shipping_provider_code="DELHIVERY",
)

# Get manifest
manifest = client.fulfillment.get_manifest(shipping_manifest_code="SM-001")

# Add packages to manifest
client.fulfillment.add_package_to_manifest(
    shipping_manifest_code="SM-001",
    shipping_package_codes=["SP-001", "SP-002"],
)

# Create and close manifest
client.fulfillment.create_and_close_manifest(channel="MYNTRA", thirdPartyShipping=True)

# Close manifest
client.fulfillment.close_manifest(shipping_manifest_code="SM-001")

# --- Dispatch ---

# Dispatch a shipping package
client.fulfillment.dispatch(shipping_package_code="SP-001")

# Force dispatch
client.fulfillment.force_dispatch(shipping_package_code="SP-001")

# Create and dispatch in one call
client.fulfillment.create_and_dispatch(
    sale_order_code="SO-12345",
    sale_order_item_info=[{"saleOrderItemCode": "SOI-001"}],
    shipping_package_info={"length": 10, "width": 10, "height": 10},
)

# Mark delivered
client.fulfillment.mark_delivered(
    sale_order_code="SO-12345",
    sale_order_item_codes=["SOI-001"],
)

# --- Other ---

# Update tracking status
client.fulfillment.update_tracking_status(
    provider_code="DELHIVERY",
    tracking_number="AWB123456",
    tracking_status="DELIVERED",
)

# Create picklist
client.fulfillment.create_picklist(shipping_package_codes=["SP-001", "SP-002"])

# Create or update reason list
client.fulfillment.create_or_update_reason(name="CANCEL_REASONS", value="Out of stock")

# Update seal ID
client.fulfillment.update_seal_id(
    shipping_package_code="SP-001",
    shipping_package_type_code="TYPE-1",
    spt_item_seal_id="SEAL-001",
)

# Bulk update seal IDs
client.fulfillment.update_seal_id_bulk(packages=[...])
```

### Inbound (14 methods)

```python
# --- Vendors ---

# Create vendor
client.inbound.create_vendor(vendor={"code": "V-001", "name": "Acme Corp"})

# Create or edit vendor catalog
client.inbound.create_or_edit_vendor_catalog(vendor_item_type={"vendorCode": "V-001", "skuCode": "SKU-100"})

# Get vendor backorder items
client.inbound.get_vendor_backorder_items(vendorCode="V-001")

# --- Purchase Orders ---

# Create purchase order
client.inbound.create_purchase_order(vendor_code="V-001")

# Get purchase order details
po = client.inbound.get_purchase_order(purchase_order_code="PO-001")

# Search purchase orders
results = client.inbound.search_purchase_orders(vendorCode="V-001")

# Approve purchase order
client.inbound.approve_purchase_order(purchase_order_code="PO-001")

# Create and approve in one call
client.inbound.create_and_approve_purchase_order(
    vendor_code="V-001",
    user_id="user@example.com",
    purchase_order_items=[{"itemSKU": "SKU-100", "quantity": 50}],
)

# Close purchase order
client.inbound.close_purchase_order(purchase_order_code="PO-001")

# --- GRN (Goods Receipt Notes) ---

# Create GRN
client.inbound.create_grn(purchase_order_code="PO-001")

# Get GRN details
grn = client.inbound.get_grn(inflow_receipt_code="IR-001")

# Search GRNs
results = client.inbound.search_grns(purchaseOrderCode="PO-001")

# Add item to GRN by SKU
client.inbound.add_item_to_grn(inflow_receipt_code="IR-001", item_sku="SKU-100", quantity=10)

# Add item to GRN by item code
client.inbound.add_item_to_grn_by_code(inflow_receipt_code="IR-001", item_code="ITEM-001")
```

### Returns (11 methods)

```python
# Search returns
results = client.returns.search(
    return_type="RTO",
    updated_from="2026-06-01T00:00:00.000Z",
    updated_to="2026-06-21T23:59:59.000Z",
)

# Get return details
ret = client.returns.get(shipment_code="SH-001")
ret = client.returns.get(reverse_pickup_code="RP-001")

# Create reverse pickup
client.returns.create_reverse_pickup(
    sale_order_code="SO-12345",
    sale_order_items=[{"code": "SOI-001", "reason": "DAMAGED"}],
)

# Edit reverse pickup
client.returns.edit_reverse_pickup(reverse_pickup_code="RP-001", courierCode="DELHIVERY")

# Approve / cancel reverse pickups
client.returns.approve_reverse_pickup(reverse_pickup_codes=["RP-001", "RP-002"])
client.returns.cancel_reverse_pickup(reverse_pickup_code="RP-001")

# Allocate courier for reverse pickup
client.returns.allocate_courier_for_reverse_pickup(reverse_pickup_codes=["RP-001"])

# Mark items as returned
client.returns.mark_returned(
    sale_order_code="SO-12345",
    sale_order_items=[{"code": "SOI-001"}],
    return_reason="DAMAGED",
)

# Mark returned with inventory type
client.returns.mark_returned_with_inventory_type(
    sale_order_code="SO-12345",
    sale_order_items=[{"code": "SOI-001", "inventoryType": "GOOD_INVENTORY"}],
)

# Alternate item handling
client.returns.create_alternate_item(
    sale_order_items=[{"code": "SOI-001"}],
    sale_order_item_alternates=[{"skuCode": "SKU-ALT"}],
)
client.returns.accept_alternate_item(
    sale_order_code="SO-12345",
    sale_order_item_codes=["SOI-001"],
    selected_alternate_item_sku="SKU-ALT",
)
```

### Outbound / Gatepass (9 methods)

```python
# Create gatepass
gp = client.outbound.create_gatepass(type="OUTBOUND", party_code="PARTY-001")

# Edit gatepass
client.outbound.edit_gatepass(gate_pass_code="GP-001", ws_gate_pass={...})

# Scan item into gatepass
client.outbound.scan_item(gate_pass_code="GP-001", item_code="ITEM-001")

# Add non-traceable item
client.outbound.add_nontraceable_item(
    gate_pass_code="GP-001",
    item_sku="SKU-100",
    inventory_type="GOOD_INVENTORY",
    quantity=5,
    unit_price=100.0,
    shelf_code="DEFAULT",
)

# Remove item from gatepass
client.outbound.remove_gatepass_item(gate_pass_code="GP-001", item_code="ITEM-001")

# Complete / discard gatepass
client.outbound.complete_gatepass(gate_pass_code="GP-001")
client.outbound.discard_gatepass(gate_pass_code="GP-001")

# Search gatepasses
results = client.outbound.search_gatepass(from_date="2026-06-01", to_date="2026-06-21")

# Get gatepass details
gp = client.outbound.get_gatepass(gate_pass_codes=["GP-001"])
```

### Facilities (2 methods)

```python
# Search facilities
results = client.facilities.search(
    from_date="2026-06-01T00:00:00.000Z",
    to_date="2026-06-21T23:59:59.000Z",
    date_type="CREATED",
)

# Get facility details
facility = client.facilities.get_details(facility_code="WAREHOUSE-1")
print(facility.name, facility.gst_number)
```

### Export Jobs (2 methods)

```python
# Create a bulk export job
job = client.export_jobs.create(
    export_job_type_name="Inventory Snapshot",
    export_columns=["inventory"],
    frequency="ONETIME",
)
print(job.job_code)

# Check export job status
status = client.export_jobs.get_status(job_code=job.job_code)
print(status.status, status.file_path)  # COMPLETE, https://...csv
```

## Error Handling

```python
from unicommerce.exceptions import (
    UnicommerceError,    # base for all errors
    AuthenticationError, # 401 - bad credentials
    AuthorizationError,  # 403 - insufficient permissions
    ValidationError,     # request validation failed
    RateLimitError,      # 429 - too many requests
    ApiError,            # API returned successful=false
    ServerError,         # 5xx
    NetworkError,        # connection failed
    TimeoutError,        # request timed out
)

try:
    order = client.sale_orders.get(code="SO-INVALID")
except AuthenticationError:
    print("Bad credentials")
except ApiError as e:
    print(f"API error: {e.errors}")
except UnicommerceError as e:
    print(f"Something went wrong: {e}")
```

## Raw Response Access

Every response model exposes the raw API response via `.raw`:

```python
order = client.sale_orders.get(code="SO-12345")
raw = order.raw  # dict with full unprocessed API response
print(raw["saleOrderDTO"]["channel"])
```

## License

MIT
