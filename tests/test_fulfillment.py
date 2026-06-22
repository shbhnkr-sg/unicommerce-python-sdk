import pytest


@pytest.fixture(scope="module")
def shipping_package(client):
    """Find a real shipping package from recent orders."""
    results = client.sale_orders.search(fromDate="2026-06-20", toDate="2026-06-22")
    for so_summary in results.sale_orders:
        order = client.sale_orders.get(code=so_summary.code)
        packages = order.raw.get("saleOrderDTO", {}).get("shippingPackages", [])
        if packages:
            return packages[0]["code"]
    pytest.skip("No shipping packages found in recent orders")


def test_get_shipping_package(client, shipping_package):
    sp = client.fulfillment.get_shipping_package(shipping_package_code=shipping_package)
    assert sp.code is not None
    assert sp.shipping_provider is not None
    assert sp.tracking_number is not None


def test_get_invoice_details(client, shipping_package):
    result = client.fulfillment.get_invoice_details(shipping_package_code=shipping_package)
    assert result.successful is True
    assert result.invoice is not None
    assert result.invoice["shippingPackageCode"] == shipping_package


def test_get_invoice_label(client, shipping_package):
    result = client.fulfillment.get_invoice_label(shipping_package_code=shipping_package)
    assert result.successful is True
    assert result.invoice_code is not None
    assert result.label is not None
    assert len(result.label) > 100


def test_update_tracking_rejects_invalid(client):
    from unicommerce.exceptions import ApiError

    with pytest.raises(ApiError):
        client.fulfillment.update_tracking_status(
            provider_code="FAKE",
            tracking_number="FAKE",
            tracking_status="DELIVERED",
        )
