def test_get_product(client):
    product = client.products.get(sku_code="10001394-3XL")
    assert product.sku_code == "10001394-3XL"
    assert product.name is not None
    assert len(product.name) > 0


def test_product_has_dimensions(client):
    product = client.products.get(sku_code="10001394-3XL")
    assert product.weight is not None
    assert product.length is not None
    assert product.width is not None
    assert product.height is not None
