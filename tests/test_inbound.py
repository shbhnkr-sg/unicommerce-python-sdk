import pytest

from unicommerce.exceptions import ApiError


def test_get_purchase_order_rejects_invalid_code(client):
    with pytest.raises(ApiError) as exc_info:
        client.inbound.get_purchase_order(purchase_order_code="NONEXISTENT")
    assert "Invalid purchase order code" in str(exc_info.value) or exc_info.value.errors


def test_get_grn_rejects_invalid_code(client):
    with pytest.raises(ApiError) as exc_info:
        client.inbound.get_grn(inflow_receipt_code="NONEXISTENT")
    assert "Invalid" in str(exc_info.value) or exc_info.value.errors


def test_create_purchase_order_requires_vendor(client):
    with pytest.raises(ApiError) as exc_info:
        client.inbound.create_purchase_order(vendor_code="FAKE_VENDOR")
    assert exc_info.value.errors
