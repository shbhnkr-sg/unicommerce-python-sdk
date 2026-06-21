import json
from pathlib import Path
from unittest.mock import AsyncMock, patch

import httpx
import pytest
from pydantic import BaseModel, ConfigDict

from unicommerce.config import UnicommerceConfig
from unicommerce.auth import AuthManager
from unicommerce.transport.async_transport import AsyncTransport
from unicommerce.exceptions import ApiError, AuthenticationError, NetworkError, ServerError

FIXTURES = Path(__file__).parent / "fixtures"


class SampleResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    successful: bool = True
    message: str = ""


@pytest.fixture
def config():
    return UnicommerceConfig(
        tenant="testco",
        username="admin@testco.com",
        password="secret123",
        client_id="my-trusted-client",
        max_retries=2,
        retry_base_delay=0.01,
        retry_max_delay=0.05,
    )


@pytest.fixture
def token_data():
    return json.loads((FIXTURES / "token_response.json").read_text())


@pytest.fixture
def error_data():
    return json.loads((FIXTURES / "error_response.json").read_text())


@pytest.fixture
def auth(config):
    auth_mgr = AuthManager(config)
    # Pre-set a valid token so we don't need to mock the OAuth endpoint
    auth_mgr._access_token = "valid-test-token"
    auth_mgr._refresh_token = "valid-refresh-token"
    import time
    auth_mgr._expires_at = time.monotonic() + 99999
    return auth_mgr


@pytest.fixture
def transport(config, auth):
    return AsyncTransport(config, auth)


@pytest.mark.asyncio
async def test_successful_request(transport, httpx_mock):
    """Mock a 200 response with successful=True, verify model returned."""
    response_data = {"successful": True, "message": "OK", "orderCode": "SO-123"}

    httpx_mock.add_response(
        method="POST",
        url="https://testco.unicommerce.com/services/rest/v1/oms/order/get",
        json=response_data,
    )

    result = await transport.request("/oms/order/get", body={"code": "SO-123"}, response_model=SampleResponse)

    assert isinstance(result, SampleResponse)
    assert result.successful is True
    assert result._raw == response_data


@pytest.mark.asyncio
async def test_api_error_on_successful_false(transport, error_data, httpx_mock):
    """Mock 200 with successful=False, verify ApiError raised."""
    httpx_mock.add_response(
        method="POST",
        url="https://testco.unicommerce.com/services/rest/v1/oms/order/get",
        json=error_data,
    )

    with pytest.raises(ApiError) as exc_info:
        await transport.request("/oms/order/get", body={"code": "SO-999"})

    assert "Sale order not found" in str(exc_info.value)
    assert exc_info.value.errors[0]["code"] == 40001


@pytest.mark.asyncio
async def test_authentication_error_triggers_refresh(config, token_data, httpx_mock):
    """Mock 401 then 200, verify token refresh + replay."""
    auth = AuthManager(config)
    import time
    auth._access_token = "expired-token"
    auth._refresh_token = "old-refresh"
    auth._expires_at = time.monotonic() + 99999  # Token looks valid to _is_token_valid

    transport = AsyncTransport(config, auth)

    # First POST returns 401
    httpx_mock.add_response(
        method="POST",
        url="https://testco.unicommerce.com/services/rest/v1/oms/order/get",
        json={"error": "unauthorized"},
        status_code=401,
    )

    # Auth refresh call
    httpx_mock.add_response(
        method="GET",
        json=token_data,
    )

    # Second POST returns success
    httpx_mock.add_response(
        method="POST",
        url="https://testco.unicommerce.com/services/rest/v1/oms/order/get",
        json={"successful": True, "message": "OK"},
    )

    result = await transport.request("/oms/order/get", body={"code": "SO-123"})
    assert result["successful"] is True


@pytest.mark.asyncio
async def test_server_error_no_retry_on_unsafe(transport, httpx_mock):
    """Mock 503, safe_to_retry=False, verify ServerError raised immediately."""
    httpx_mock.add_response(
        method="POST",
        url="https://testco.unicommerce.com/services/rest/v1/oms/order/create",
        json={"error": "service unavailable"},
        status_code=503,
    )

    with pytest.raises(ServerError) as exc_info:
        await transport.request("/oms/order/create", body={"data": "test"}, safe_to_retry=False)

    assert exc_info.value.status_code == 503
    # Only one request should have been made (no retry)
    assert len(httpx_mock.get_requests()) == 1


@pytest.mark.asyncio
async def test_server_error_retries_on_safe(transport, httpx_mock):
    """Mock 503 then 200, safe_to_retry=True, verify success."""
    # First call returns 503
    httpx_mock.add_response(
        method="POST",
        url="https://testco.unicommerce.com/services/rest/v1/oms/order/get",
        json={"error": "service unavailable"},
        status_code=503,
    )

    # Second call succeeds
    httpx_mock.add_response(
        method="POST",
        url="https://testco.unicommerce.com/services/rest/v1/oms/order/get",
        json={"successful": True, "message": "OK"},
    )

    result = await transport.request("/oms/order/get", body={"code": "SO-123"}, safe_to_retry=True)
    assert result["successful"] is True
    assert len(httpx_mock.get_requests()) == 2


@pytest.mark.asyncio
async def test_network_error_retries(transport, httpx_mock):
    """Mock network failure then success, safe_to_retry=True."""
    # First call raises network error
    httpx_mock.add_exception(
        httpx.ConnectError("Connection refused"),
        url="https://testco.unicommerce.com/services/rest/v1/oms/order/get",
    )

    # Second call succeeds
    httpx_mock.add_response(
        method="POST",
        url="https://testco.unicommerce.com/services/rest/v1/oms/order/get",
        json={"successful": True, "message": "OK"},
    )

    result = await transport.request("/oms/order/get", body={"code": "SO-123"}, safe_to_retry=True)
    assert result["successful"] is True
