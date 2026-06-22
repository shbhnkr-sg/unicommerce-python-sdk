def test_search_rto_returns(client):
    result = client.returns.search(
        return_type="RTO",
        updated_from="2026-06-01T00:00:00.000Z",
        updated_to="2026-06-22T00:00:00.000Z",
    )
    assert result.return_type == "RTO"
    assert result.return_orders is not None
    assert len(result.return_orders) > 0


def test_search_return_has_fields(client):
    result = client.returns.search(
        return_type="RTO",
        updated_from="2026-06-01T00:00:00.000Z",
        updated_to="2026-06-22T00:00:00.000Z",
    )
    order = result.return_orders[0]
    assert order.code is not None
    assert order.created is not None


def test_get_return_by_shipment_code(client):
    search = client.returns.search(
        return_type="RTO",
        updated_from="2026-06-01T00:00:00.000Z",
        updated_to="2026-06-22T00:00:00.000Z",
    )
    code = search.return_orders[0].code
    result = client.returns.get(shipment_code=code)
    assert result.return_sale_order_items is not None
    assert len(result.return_sale_order_items) > 0


def test_get_return_has_sale_order_value(client):
    search = client.returns.search(
        return_type="RTO",
        updated_from="2026-06-01T00:00:00.000Z",
        updated_to="2026-06-22T00:00:00.000Z",
    )
    code = search.return_orders[0].code
    result = client.returns.get(shipment_code=code)
    assert result.return_sale_order_value is not None
    assert "saleOrderCode" in result.return_sale_order_value
