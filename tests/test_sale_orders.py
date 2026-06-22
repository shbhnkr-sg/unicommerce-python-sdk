import pytest


def test_search_returns_orders(client):
    results = client.sale_orders.search(fromDate="2026-06-20", toDate="2026-06-22")
    assert results.sale_orders is not None
    assert len(results.sale_orders) > 0


def test_search_result_fields(client):
    results = client.sale_orders.search(fromDate="2026-06-20", toDate="2026-06-22")
    order = results.sale_orders[0]
    assert order.code is not None
    assert order.channel is not None
    assert order.status is not None
    assert isinstance(order.display_order_date_time, int)


def test_get_returns_full_order(client):
    results = client.sale_orders.search(fromDate="2026-06-20", toDate="2026-06-22")
    code = results.sale_orders[0].code
    order = client.sale_orders.get(code=code)
    assert order.code == code
    assert order.channel is not None
    assert order.status is not None


def test_get_includes_items(client):
    results = client.sale_orders.search(fromDate="2026-06-20", toDate="2026-06-22")
    code = results.sale_orders[0].code
    order = client.sale_orders.get(code=code)
    assert order.sale_order_items is not None
    assert len(order.sale_order_items) > 0
    item = order.sale_order_items[0]
    assert item.item_sku is not None


def test_get_raw_contains_dto(client):
    results = client.sale_orders.search(fromDate="2026-06-20", toDate="2026-06-22")
    code = results.sale_orders[0].code
    order = client.sale_orders.get(code=code)
    assert "saleOrderDTO" in order.raw
    assert order.raw["successful"] is True


def test_search_with_no_params_raises_error(client):
    from unicommerce.exceptions import ApiError

    with pytest.raises(ApiError):
        client.sale_orders.search()
