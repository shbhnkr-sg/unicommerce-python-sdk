import json

import pytest

from unicommerce.async_client import AsyncUnicommerce
from unicommerce.models.inventory import AdjustInventoryResponse, InventorySnapshotResponse


@pytest.fixture
def client():
    return AsyncUnicommerce(
        tenant="testco",
        username="admin@testco.com",
        password="secret123",
    )


@pytest.fixture
def token_response():
    return {
        "access_token": "test-access-token-12345",
        "token_type": "bearer",
        "refresh_token": "test-refresh-token-67890",
        "expires_in": 41621,
        "scope": "read trust write",
    }


@pytest.mark.asyncio
async def test_inventory_adjust(client, httpx_mock, token_response):
    """Test that inventory.adjust works with correct parameters."""
    httpx_mock.add_response(
        method="GET",
        url="https://testco.unicommerce.com/oauth/token?grant_type=password&client_id=my-trusted-client&username=admin@testco.com&password=secret123",
        json=token_response,
    )

    adjust_response = {
        "successful": True,
        "message": "Inventory adjusted",
    }

    httpx_mock.add_response(
        method="POST",
        url="https://testco.unicommerce.com/services/rest/v1/inventory/adjust",
        json=adjust_response,
    )

    result = await client.inventory.adjust(
        item_sku="SKU1",
        quantity=5,
        shelf_code="A1",
        adjustment_type="ADD",
    )

    assert isinstance(result, AdjustInventoryResponse)

    await client.close()


@pytest.mark.asyncio
async def test_inventory_adjust_sends_correct_body(client, httpx_mock, token_response):
    """Test that the adjust request body is formed correctly."""
    httpx_mock.add_response(
        method="GET",
        url="https://testco.unicommerce.com/oauth/token?grant_type=password&client_id=my-trusted-client&username=admin@testco.com&password=secret123",
        json=token_response,
    )

    adjust_response = {
        "successful": True,
        "message": "Inventory adjusted",
    }

    httpx_mock.add_response(
        method="POST",
        url="https://testco.unicommerce.com/services/rest/v1/inventory/adjust",
        json=adjust_response,
    )

    await client.inventory.adjust(
        item_sku="SKU1",
        quantity=10,
        shelf_code="B2",
        adjustment_type="REMOVE",
        inventory_type="GOOD_INVENTORY",
        remarks="Damaged items",
    )

    requests = httpx_mock.get_requests()
    post_request = [r for r in requests if r.method == "POST"][0]
    body = json.loads(post_request.content)

    assert "inventoryAdjustment" in body
    adj = body["inventoryAdjustment"]
    assert adj["itemSKU"] == "SKU1"
    assert adj["quantity"] == 10
    assert adj["shelfCode"] == "B2"
    assert adj["adjustmentType"] == "REMOVE"
    assert adj["inventoryType"] == "GOOD_INVENTORY"
    assert adj["remarks"] == "Damaged items"

    await client.close()


@pytest.mark.asyncio
async def test_inventory_adjust_with_facility(client, httpx_mock, token_response):
    """Test that facility header is set when facility is specified."""
    httpx_mock.add_response(
        method="GET",
        url="https://testco.unicommerce.com/oauth/token?grant_type=password&client_id=my-trusted-client&username=admin@testco.com&password=secret123",
        json=token_response,
    )

    adjust_response = {
        "successful": True,
        "message": "Inventory adjusted",
    }

    httpx_mock.add_response(
        method="POST",
        url="https://testco.unicommerce.com/services/rest/v1/inventory/adjust",
        json=adjust_response,
    )

    await client.inventory.adjust(
        item_sku="SKU1",
        quantity=5,
        shelf_code="A1",
        adjustment_type="ADD",
        facility="WH-DELHI",
    )

    requests = httpx_mock.get_requests()
    post_request = [r for r in requests if r.method == "POST"][0]
    assert post_request.headers["Facility"] == "WH-DELHI"

    await client.close()


@pytest.mark.asyncio
async def test_inventory_get_snapshot(client, httpx_mock, token_response):
    """Test that inventory.get_snapshot returns InventorySnapshotResponse with real API fields."""
    httpx_mock.add_response(
        method="GET",
        url="https://testco.unicommerce.com/oauth/token?grant_type=password&client_id=my-trusted-client&username=admin@testco.com&password=secret123",
        json=token_response,
    )

    snapshot_response = {
        "successful": True,
        "message": "Snapshot fetched",
        "inventorySnapshots": [
            {
                "itemTypeSKU": "SKU1",
                "inventory": 50,
                "openSale": 5,
                "openPurchase": 0,
                "putawayPending": 0,
                "inventoryBlocked": 0,
                "pendingStockTransfer": 0,
                "vendorInventory": 0,
                "virtualInventory": 45,
                "pendingInventoryAssessment": 0,
                "badInventory": 2,
            },
            {
                "itemTypeSKU": "SKU2",
                "inventory": 10,
                "openSale": 1,
                "openPurchase": 0,
                "putawayPending": 0,
                "inventoryBlocked": 0,
                "pendingStockTransfer": 0,
                "vendorInventory": 0,
                "virtualInventory": 9,
                "pendingInventoryAssessment": 0,
                "badInventory": 0,
            },
        ],
    }

    httpx_mock.add_response(
        method="POST",
        url="https://testco.unicommerce.com/services/rest/v1/inventory/inventorySnapshot/get",
        json=snapshot_response,
    )

    result = await client.inventory.get_snapshot(updated_since_in_minutes=30)

    assert isinstance(result, InventorySnapshotResponse)
    assert len(result.inventory_snapshots) == 2
    assert result.inventory_snapshots[0].item_type_sku == "SKU1"
    assert result.inventory_snapshots[0].inventory == 50
    assert result.inventory_snapshots[0].open_sale == 5
    assert result.inventory_snapshots[0].bad_inventory == 2
    assert result.inventory_snapshots[1].item_type_sku == "SKU2"
    assert result.inventory_snapshots[1].virtual_inventory == 9

    # Verify the request body uses updatedSinceInMinutes
    requests = httpx_mock.get_requests()
    post_request = [r for r in requests if r.method == "POST"][0]
    body = json.loads(post_request.content)
    assert body["updatedSinceInMinutes"] == 30

    await client.close()
