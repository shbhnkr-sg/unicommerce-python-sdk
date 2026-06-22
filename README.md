# unicommerce

A modern, async-first Python SDK for the [Unicommerce](https://www.unicommerce.com/) REST API.

- Python 3.12+
- Sync and async clients (powered by [httpx](https://www.python-httpx.org/))
- Pydantic v2 models for all responses
- OAuth 2.0 with automatic token refresh
- Retry with exponential backoff
- Custom exception hierarchy

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

### Sale Orders

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
```

### Inventory

```python
# Get inventory snapshot
snapshot = client.inventory.get_snapshot(updated_since_in_minutes=60)
for item in snapshot.inventory_snapshots:
    print(item.item_sku, item.quantity)

# Adjust inventory
client.inventory.adjust(
    item_sku="SKU-100",
    quantity=5,
    shelf_code="DEFAULT",
    adjustment_type="ADD",          # ADD, REMOVE, TRANSFER
    inventory_type="GOOD_INVENTORY",
)

# Bulk adjust
client.inventory.adjust_bulk(adjustments=[...])
```

### Products

```python
product = client.products.get(sku="SKU-100")
print(product.name, product.category_name)
```

### Fulfillment

```python
# Get shipping package details
sp = client.fulfillment.get_shipping_package(shipping_package_code="SP-001")

# Create shipping package
client.fulfillment.create_shipping_package(
    sale_order_code="SO-12345",
    sale_order_item_codes=["SOI-001", "SOI-002"],
)

# Create invoice
client.fulfillment.create_invoice(shipping_package_code="SP-001")

# Get invoice details (full breakdown with taxes, items, etc.)
invoice = client.fulfillment.get_invoice_details(shipping_package_code="SP-001")
print(invoice.invoice["total"], invoice.invoice["paymentMode"])

# Get invoice label as base64 PDF
label = client.fulfillment.get_invoice_label(shipping_package_code="SP-001")
import base64
pdf_bytes = base64.b64decode(label.label)

# Create invoice + shipping label in one call
result = client.fulfillment.create_invoice_and_label(
    shipping_package_code="SP-001",
    generate_uniware_shipping_label=True,
)
print(result.tracking_number, result.shipping_label_link)

# Manifests
manifest = client.fulfillment.create_manifest(
    channel="MYNTRA",
    third_party_shipping=True,
    shipping_provider_code="DELHIVERY",
)
manifest = client.fulfillment.get_manifest(shipping_manifest_code="SM-001")

# Update tracking status
client.fulfillment.update_tracking_status(
    provider_code="DELHIVERY",
    tracking_number="AWB123456",
    tracking_status="DELIVERED",
)
```

### Inbound (Purchase Orders & GRN)

```python
# Create vendor
client.inbound.create_vendor(vendor={"code": "V-001", "name": "Acme Corp"})

# Create purchase order
client.inbound.create_purchase_order(vendor_code="V-001")

# Get purchase order details
po = client.inbound.get_purchase_order(purchase_order_code="PO-001")

# Create GRN (Goods Receipt Note)
client.inbound.create_grn(purchase_order_code="PO-001")

# Get GRN details
grn = client.inbound.get_grn(inflow_receipt_code="IR-001")

# Add item to GRN
client.inbound.add_item_to_grn(inflow_receipt_code="IR-001", item_sku="SKU-100", quantity=10)
```

### Returns

```python
# Search returns (RTO, customer returns, etc.)
results = client.returns.search(
    return_type="RTO",
    from_date="2026-06-01T00:00:00.000Z",
    to_date="2026-06-21T23:59:59.000Z",
)

# Get return details
ret = client.returns.get(shipment_code="SH-001")
# or by reverse pickup code:
ret = client.returns.get(reverse_pickup_code="RP-001")

# Create reverse pickup
client.returns.create_reverse_pickup(
    sale_order_code="SO-12345",
    sale_order_items=[{"code": "SOI-001", "reason": "DAMAGED"}],
)

# Mark items as returned
client.returns.mark_returned(
    sale_order_code="SO-12345",
    sale_order_items=[{"code": "SOI-001"}],
    return_reason="DAMAGED",
)
```

### Facilities

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

### Export Jobs

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

Every response model exposes the raw API response via `._raw`:

```python
order = client.sale_orders.get(code="SO-12345")
raw = order.raw  # dict with full unprocessed API response
print(raw["saleOrderDTO"]["channel"])
```

## License

MIT
