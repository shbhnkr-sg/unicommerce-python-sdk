import pytest

from unicommerce.async_client import AsyncUnicommerce
from unicommerce.models.sale_orders import SaleOrderResponse


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


@pytest.fixture
def sale_order_response():
    return {
        "successful": True,
        "message": None,
        "errors": None,
        "warnings": None,
        "code": "SO-001",
        "displayOrderCode": "ORD-001",
        "displayOrderDateTime": 1705312200000,
        "channel": "CUSTOM",
        "source": "API",
        "status": "CREATED",
        "cod": False,
        "priority": 0,
        "currencyCode": "INR",
        "totalDiscount": 100.0,
        "totalShippingCharges": 50.0,
        "customerCode": "CUST-001",
        "notificationEmail": "john@example.com",
        "notificationMobile": "9876543210",
        "created": 1705312200000,
        "updated": 1705312200000,
        "fulfillmentTat": None,
        "thirdPartyShipping": False,
        "addresses": [],
        "saleOrderItems": [
            {
                "code": "SOI-001",
                "itemSku": "SKU-ABC",
                "itemName": "Test Product",
                "sellingPrice": 1500.0,
                "totalPrice": 1450.0,
                "discount": 100.0,
                "shippingCharges": 50.0,
                "quantity": 1,
                "statusCode": "CREATED",
            }
        ],
    }


@pytest.mark.asyncio
async def test_sale_order_get(client, httpx_mock, token_response, sale_order_response):
    """Test that sale_orders.get returns a SaleOrderResponse with correct fields."""
    # Mock token endpoint
    httpx_mock.add_response(
        method="GET",
        url="https://testco.unicommerce.com/oauth/token?grant_type=password&client_id=my-trusted-client&username=admin@testco.com&password=secret123",
        json=token_response,
    )

    # Mock sale order get endpoint
    httpx_mock.add_response(
        method="POST",
        url="https://testco.unicommerce.com/services/rest/v1/oms/saleorder/get",
        json=sale_order_response,
    )

    result = await client.sale_orders.get("SO-001")

    assert isinstance(result, SaleOrderResponse)
    assert result.code == "SO-001"
    assert result.display_order_code == "ORD-001"
    assert result.channel == "CUSTOM"
    assert result.status == "CREATED"
    assert result.customer_code == "CUST-001"
    assert result.cod is False
    assert result.total_discount == 100.0
    assert result.display_order_date_time == 1705312200000
    assert len(result.sale_order_items) == 1
    assert result.sale_order_items[0].item_sku == "SKU-ABC"
    assert result.sale_order_items[0].quantity == 1

    await client.close()


@pytest.mark.asyncio
async def test_sale_order_search(client, httpx_mock, token_response, sale_order_response):
    """Test that sale_orders.search returns a SaleOrderSearchResponse."""
    from unicommerce.models.sale_orders import SaleOrderSearchResponse

    httpx_mock.add_response(
        method="GET",
        url="https://testco.unicommerce.com/oauth/token?grant_type=password&client_id=my-trusted-client&username=admin@testco.com&password=secret123",
        json=token_response,
    )

    search_response = {
        "successful": True,
        "message": None,
        "errors": None,
        "warnings": None,
        "elements": [sale_order_response],
        "totalRecords": 1,
    }

    httpx_mock.add_response(
        method="POST",
        url="https://testco.unicommerce.com/services/rest/v1/oms/saleOrder/search",
        json=search_response,
    )

    result = await client.sale_orders.search(status="CREATED")

    assert isinstance(result, SaleOrderSearchResponse)
    assert result.total_records == 1
    assert len(result.sale_orders) == 1
    assert result.sale_orders[0].code == "SO-001"

    await client.close()


@pytest.mark.asyncio
async def test_sale_order_cancel(client, httpx_mock, token_response):
    """Test that sale_orders.cancel returns a CancelResponse."""
    from unicommerce.models.sale_orders import CancelResponse

    httpx_mock.add_response(
        method="GET",
        url="https://testco.unicommerce.com/oauth/token?grant_type=password&client_id=my-trusted-client&username=admin@testco.com&password=secret123",
        json=token_response,
    )

    cancel_response = {
        "successful": True,
        "message": "Cancelled",
        "errors": None,
        "warnings": None,
        "code": "SO-001",
        "status": "CANCELLED",
    }

    httpx_mock.add_response(
        method="POST",
        url="https://testco.unicommerce.com/services/rest/v1/oms/saleOrder/cancel",
        json=cancel_response,
    )

    result = await client.sale_orders.cancel("SO-001")

    assert isinstance(result, CancelResponse)
    assert result.code == "SO-001"
    assert result.status == "CANCELLED"

    await client.close()


@pytest.mark.asyncio
async def test_sale_order_get_sends_correct_body(
    client, httpx_mock, token_response, sale_order_response
):
    """Test that the request body is formed correctly."""
    httpx_mock.add_response(
        method="GET",
        url="https://testco.unicommerce.com/oauth/token?grant_type=password&client_id=my-trusted-client&username=admin@testco.com&password=secret123",
        json=token_response,
    )

    httpx_mock.add_response(
        method="POST",
        url="https://testco.unicommerce.com/services/rest/v1/oms/saleorder/get",
        json=sale_order_response,
    )

    await client.sale_orders.get("SO-001", facility_codes=["FC-001", "FC-002"])

    requests = httpx_mock.get_requests()
    # Second request is the sale order get (first is token)
    post_request = [r for r in requests if r.method == "POST"][0]
    import json

    body = json.loads(post_request.content)
    assert body["code"] == "SO-001"
    assert body["facilityCodes"] == ["FC-001", "FC-002"]

    await client.close()
