import json
import time
from pathlib import Path

import httpx
import pytest

from unicommerce.config import UnicommerceConfig
from unicommerce.auth import AuthManager

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def config():
    return UnicommerceConfig(
        tenant="testco",
        username="admin@testco.com",
        password="secret123",
        client_id="my-trusted-client",
    )


@pytest.fixture
def token_data():
    return json.loads((FIXTURES / "token_response.json").read_text())


@pytest.fixture
def auth(config):
    return AuthManager(config)


@pytest.mark.asyncio
async def test_password_grant_success(config, token_data, httpx_mock):
    """Mock the OAuth endpoint, verify token is returned."""
    httpx_mock.add_response(
        url=httpx.URL(
            f"https://testco.unicommerce.com/oauth/token"
            f"?grant_type=password"
            f"&client_id=my-trusted-client"
            f"&username=admin@testco.com"
            f"&password=secret123"
        ),
        method="GET",
        json=token_data,
    )

    auth = AuthManager(config)
    token = await auth.get_token()

    assert token == "test-access-token-12345"


@pytest.mark.asyncio
async def test_token_caching(config, token_data, httpx_mock):
    """Call get_token twice, verify only one HTTP call made."""
    httpx_mock.add_response(
        method="GET",
        json=token_data,
    )

    auth = AuthManager(config)
    token1 = await auth.get_token()
    token2 = await auth.get_token()

    assert token1 == token2 == "test-access-token-12345"
    # Only one request should have been made
    assert len(httpx_mock.get_requests()) == 1


@pytest.mark.asyncio
async def test_token_refresh_on_expiry(config, token_data, httpx_mock):
    """Simulate expired token, verify refresh is called."""
    auth = AuthManager(config)

    # Manually set an expired token
    auth._access_token = "old-token"
    auth._refresh_token = "old-refresh-token"
    auth._expires_at = time.monotonic() - 10  # Already expired

    # Mock refresh grant endpoint
    refreshed_data = {**token_data, "access_token": "new-access-token"}
    httpx_mock.add_response(
        method="GET",
        json=refreshed_data,
    )

    token = await auth.get_token()
    assert token == "new-access-token"

    # Verify the request was a refresh grant
    request = httpx_mock.get_requests()[0]
    assert "grant_type=refresh_token" in str(request.url)


@pytest.mark.asyncio
async def test_fallback_to_password_on_refresh_failure(config, token_data, httpx_mock):
    """Refresh returns error, verify password grant is retried."""
    auth = AuthManager(config)

    # Manually set an expired token with a refresh token
    auth._access_token = "old-token"
    auth._refresh_token = "old-refresh-token"
    auth._expires_at = time.monotonic() - 10  # Already expired

    # First call (refresh) returns 401
    httpx_mock.add_response(
        method="GET",
        status_code=401,
        json={"error": "invalid_grant"},
    )

    # Second call (password grant) succeeds
    httpx_mock.add_response(
        method="GET",
        json=token_data,
    )

    token = await auth.get_token()
    assert token == "test-access-token-12345"

    # Verify two requests were made
    requests = httpx_mock.get_requests()
    assert len(requests) == 2
    assert "grant_type=refresh_token" in str(requests[0].url)
    assert "grant_type=password" in str(requests[1].url)
