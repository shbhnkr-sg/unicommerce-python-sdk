# Unicommerce Python SDK

A modern, async-first Python SDK for the [Unicommerce](https://www.unicommerce.com/) API. Provides a clean, type-safe interface with automatic authentication, retry logic, and Pydantic models for all request/response types.

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

# Get a sale order
order = client.sale_orders.get("SO-001")
print(order.status)

# Search sale orders
results = client.sale_orders.search(status="CREATED", channel="AMAZON")

# Adjust inventory
client.inventory.adjust(item_sku="SKU-100", quantity=10, facility="WAREHOUSE-1")

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
        order = await client.sale_orders.get("SO-001")
        print(order.status)

asyncio.run(main())
```

## Error Handling

```python
from unicommerce import Unicommerce
from unicommerce.exceptions import (
    ApiError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
)

client = Unicommerce(tenant="t", username="u", password="p")

try:
    order = client.sale_orders.get("SO-INVALID")
except AuthenticationError:
    print("Invalid credentials")
except RateLimitError as e:
    print(f"Rate limited, retry after {e.retry_after}s")
except ValidationError as e:
    print(f"Validation failed: {e.errors}")
except ApiError as e:
    print(f"API error {e.code}: {e}")
```

## Available Resources

| Resource | Description |
|----------|-------------|
| `client.sale_orders` | Create, get, search, cancel, edit, verify sale orders |
| `client.inventory` | Adjust inventory, get snapshots, mark found |
| `client.products` | Create, get, search product catalog |
| `client.fulfillment` | Invoices, shipping packages, manifests, tracking |
| `client.inbound` | Vendors, purchase orders, GRN management |
| `client.returns` | Return processing and reverse pickups |
| `client.facilities` | Facility search and details |
| `client.export_jobs` | Create and track bulk export jobs |

## Features

- OAuth 2.0 authentication with automatic token refresh
- Both sync and async client support
- Automatic retry with exponential backoff for safe operations
- Pydantic v2 models for type-safe request/response handling
- Custom exception hierarchy for granular error handling
- PII redaction in logs

## License

MIT
