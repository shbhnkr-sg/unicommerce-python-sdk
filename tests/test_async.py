import pytest


@pytest.mark.asyncio
async def test_async_search(async_client):
    async with async_client as ac:
        results = await ac.sale_orders.search(fromDate="2026-06-20", toDate="2026-06-22")
        assert results.sale_orders is not None
        assert len(results.sale_orders) > 0


@pytest.mark.asyncio
async def test_async_get_product(async_client):
    async with async_client as ac:
        product = await ac.products.get(sku_code="10001394-3XL")
        assert product.sku_code == "10001394-3XL"


@pytest.mark.asyncio
async def test_async_inventory_snapshot(async_client):
    async with async_client as ac:
        snapshot = await ac.inventory.get_snapshot(updated_since_in_minutes=1440)
        assert snapshot.inventory_snapshots is not None
