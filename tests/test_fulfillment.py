def test_get_shipping_package(client):
    results = client.sale_orders.search(fromDate="2026-06-20", toDate="2026-06-22")
    order = client.sale_orders.get(code=results.sale_orders[0].code)
    packages = order.raw.get("saleOrderDTO", {}).get("shippingPackages", [])
    assert len(packages) > 0

    sp = client.fulfillment.get_shipping_package(shipping_package_code=packages[0]["code"])
    assert sp.code is not None
    assert sp.shipping_provider is not None
    assert sp.tracking_number is not None
