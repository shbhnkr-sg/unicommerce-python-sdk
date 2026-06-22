import httpx

from conftest import TENANT, USERNAME, PASSWORD


def test_password_grant_returns_token():
    resp = httpx.get(
        f"https://{TENANT}.unicommerce.com/oauth/token",
        params={
            "grant_type": "password",
            "client_id": "my-trusted-client",
            "username": USERNAME,
            "password": PASSWORD,
        },
        timeout=30,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]
    assert data["refresh_token"]
    assert data["expires_in"] > 0


def test_client_authenticates_on_first_request(client):
    results = client.sale_orders.search(fromDate="2026-06-20", toDate="2026-06-22")
    assert results is not None
