"""End-to-end integration tests exercising full stack:
client -> resource -> transport -> mocked HTTP -> response model
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from unicommerce import AsyncUnicommerce, Unicommerce
from unicommerce.exceptions import ApiError

FIXTURES = Path(__file__).parent / "fixtures"

TOKEN_RESPONSE = {
    "access_token": "test-token-123",
    "refresh_token": "test-refresh-456",
    "expires_in": 3600,
    "token_type": "bearer",
}

FRESH_TOKEN_RESPONSE = {
    "access_token": "fresh-token-789",
    "refresh_token": "fresh-refresh-012",
    "expires_in": 3600,
    "token_type": "bearer",
}


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text())


class TestSyncClientGetSaleOrder:
    """Test the full sync flow: Unicommerce -> SaleOrders.get -> SyncTransport -> httpx -> model."""

    def test_sync_client_get_sale_order(self, httpx_mock):
        # Mock the OAuth token endpoint
        httpx_mock.add_response(
            url="https://testtenant.unicommerce.com/oauth/token?grant_type=password&client_id=my-trusted-client&username=testuser&password=testpass",
            json=TOKEN_RESPONSE,
        )

        # Mock the sale order get API
        fixture = load_fixture("sale_order_get.json")
        httpx_mock.add_response(
            url="https://testtenant.unicommerce.com/services/rest/v1/oms/saleorder/get",
            json=fixture,
        )

        client = Unicommerce(
            tenant="testtenant",
            username="testuser",
            password="testpass",
        )

        result = client.sale_orders.get("SO-001")

        # The model was parsed from the full response (extra="allow" captures saleOrderDTO)
        assert result is not None
        # The raw dict should be stored
        assert result.raw == fixture
        client.close()


class TestAsyncClientGetSaleOrder:
    """Test the full async flow: AsyncUnicommerce -> AsyncSaleOrders.get -> httpx."""

    @pytest.mark.asyncio
    async def test_async_client_get_sale_order(self, httpx_mock):
        # Mock the OAuth token endpoint
        httpx_mock.add_response(
            url="https://testtenant.unicommerce.com/oauth/token?grant_type=password&client_id=my-trusted-client&username=testuser&password=testpass",
            json=TOKEN_RESPONSE,
        )

        # Mock the sale order get API
        fixture = load_fixture("sale_order_get.json")
        httpx_mock.add_response(
            url="https://testtenant.unicommerce.com/services/rest/v1/oms/saleorder/get",
            json=fixture,
        )

        client = AsyncUnicommerce(
            tenant="testtenant",
            username="testuser",
            password="testpass",
        )

        result = await client.sale_orders.get("SO-001")

        assert result is not None
        assert result.raw == fixture
        await client.close()


class TestErrorHandlingFlow:
    """Test that a 200 with successful=False raises ApiError through the full stack."""

    def test_error_handling_flow(self, httpx_mock):
        # Mock token
        httpx_mock.add_response(
            url="https://testtenant.unicommerce.com/oauth/token?grant_type=password&client_id=my-trusted-client&username=testuser&password=testpass",
            json=TOKEN_RESPONSE,
        )

        # Mock API returning successful=False
        error_response = {
            "successful": False,
            "message": "Sale order not found",
            "code": 1001,
            "errors": [{"code": "NOT_FOUND", "message": "Order does not exist"}],
            "warnings": None,
        }
        httpx_mock.add_response(
            url="https://testtenant.unicommerce.com/services/rest/v1/oms/saleorder/get",
            json=error_response,
        )

        client = Unicommerce(
            tenant="testtenant",
            username="testuser",
            password="testpass",
        )

        with pytest.raises(ApiError) as exc_info:
            client.sale_orders.get("SO-NONEXIST")

        assert "Sale order not found" in str(exc_info.value)
        assert exc_info.value.code == 1001
        assert len(exc_info.value.errors) == 1
        client.close()


class TestRetryFlow:
    """Test that a 503 followed by 200 retries correctly when safe_to_retry=True."""

    def test_retry_flow(self, httpx_mock):
        # Mock token
        httpx_mock.add_response(
            url="https://testtenant.unicommerce.com/oauth/token?grant_type=password&client_id=my-trusted-client&username=testuser&password=testpass",
            json=TOKEN_RESPONSE,
        )

        # First request returns 503
        httpx_mock.add_response(
            url="https://testtenant.unicommerce.com/services/rest/v1/oms/saleorder/get",
            status_code=503,
            json={"successful": False, "message": "Service unavailable"},
        )

        # Second request succeeds
        fixture = load_fixture("sale_order_get.json")
        httpx_mock.add_response(
            url="https://testtenant.unicommerce.com/services/rest/v1/oms/saleorder/get",
            json=fixture,
        )

        client = Unicommerce(
            tenant="testtenant",
            username="testuser",
            password="testpass",
        )

        # Patch time.sleep to avoid actual waiting
        with patch("time.sleep"):
            result = client.sale_orders.get("SO-001")

        assert result is not None
        assert result.raw == fixture
        client.close()


class TestAuthRefreshFlow:
    """Test transparent auth refresh: token -> 401 -> refresh -> 200."""

    def test_auth_refresh_flow(self, httpx_mock):
        # Initial token
        httpx_mock.add_response(
            url="https://testtenant.unicommerce.com/oauth/token?grant_type=password&client_id=my-trusted-client&username=testuser&password=testpass",
            json=TOKEN_RESPONSE,
        )

        # First API call returns 401
        httpx_mock.add_response(
            url="https://testtenant.unicommerce.com/services/rest/v1/oms/saleorder/get",
            status_code=401,
            json={"successful": False, "message": "Unauthorized"},
        )

        # Refresh token call
        httpx_mock.add_response(
            url="https://testtenant.unicommerce.com/oauth/token?grant_type=refresh_token&client_id=my-trusted-client&refresh_token=test-refresh-456",
            json=FRESH_TOKEN_RESPONSE,
        )

        # Second API call with fresh token succeeds
        fixture = load_fixture("sale_order_get.json")
        httpx_mock.add_response(
            url="https://testtenant.unicommerce.com/services/rest/v1/oms/saleorder/get",
            json=fixture,
        )

        client = Unicommerce(
            tenant="testtenant",
            username="testuser",
            password="testpass",
        )

        result = client.sale_orders.get("SO-001")

        assert result is not None
        assert result.raw == fixture
        client.close()
