"""Tests for Pydantic models across all resource domains."""

import pytest
from pydantic import ValidationError

from unicommerce.models.base import UnicommerceRequest, UnicommerceResponse
from unicommerce.models.inventory import AdjustInventoryRequest
from unicommerce.models.sale_orders import SaleOrderResponse


class TestUnicommerceRequest:
    """Tests for UnicommerceRequest base model."""

    def test_rejects_unknown_fields(self):
        """UnicommerceRequest with extra='forbid' should reject unknown fields."""
        with pytest.raises(ValidationError) as exc_info:
            # Create a minimal subclass to test
            class TestRequest(UnicommerceRequest):
                name: str = ""

            TestRequest(name="test", unknown_field="oops")

        assert "extra_forbidden" in str(exc_info.value)

    def test_accepts_known_fields(self):
        """UnicommerceRequest should accept defined fields."""

        class TestRequest(UnicommerceRequest):
            name: str = ""

        req = TestRequest(name="hello")
        assert req.name == "hello"


class TestUnicommerceResponse:
    """Tests for UnicommerceResponse base model."""

    def test_allows_unknown_fields(self):
        """UnicommerceResponse with extra='allow' should accept unknown fields."""
        resp = UnicommerceResponse.model_validate({"unknownField": "value", "anotherOne": 42})
        assert resp.model_extra == {"unknownField": "value", "anotherOne": 42}

    def test_raw_private_attr(self):
        """UnicommerceResponse._raw and .raw property should work correctly."""
        resp = UnicommerceResponse()
        assert resp.raw == {}

        resp._raw = {"key": "value"}
        assert resp.raw == {"key": "value"}

    def test_raw_initialized_empty(self):
        """UnicommerceResponse._raw should default to empty dict."""
        resp = UnicommerceResponse()
        assert resp._raw == {}
        assert resp.raw == {}


class TestSaleOrderResponse:
    """Tests for SaleOrderResponse model with camelCase aliases."""

    def test_create_from_camel_case_dict(self):
        """SaleOrderResponse can be created from a dict with camelCase keys."""
        data = {
            "code": "SO-001",
            "displayOrderCode": "ORD-001",
            "displayOrderDateTime": 1705312200000,
            "channel": "SHOPIFY",
            "source": "API",
            "status": "CREATED",
            "cod": True,
            "priority": 0,
            "currencyCode": "INR",
            "totalDiscount": 10.0,
            "totalShippingCharges": 5.0,
            "customerCode": "CUST-001",
            "notificationEmail": "john@example.com",
            "notificationMobile": "9876543210",
            "created": 1705312200000,
            "updated": 1705312200000,
            "fulfillmentTat": 1705571400000,
            "thirdPartyShipping": False,
            "addresses": [
                {
                    "id": "1",
                    "name": "John Doe",
                    "addressLine1": "123 Main St",
                    "addressLine2": "Apt 4",
                    "city": "Mumbai",
                    "state": "Maharashtra",
                    "pincode": "400001",
                    "country": "IN",
                    "phone": "9876543210",
                    "email": "john@example.com",
                }
            ],
            "saleOrderItems": [
                {
                    "code": "SOI-001",
                    "itemSku": "SKU-100",
                    "itemName": "Widget",
                    "sellingPrice": 50.0,
                    "totalPrice": 50.0,
                    "discount": 0,
                    "shippingCharges": 5.0,
                    "quantity": 1,
                    "statusCode": "CREATED",
                }
            ],
        }

        order = SaleOrderResponse.model_validate(data)

        assert order.code == "SO-001"
        assert order.display_order_code == "ORD-001"
        assert order.display_order_date_time == 1705312200000
        assert order.channel == "SHOPIFY"
        assert order.cod is True
        assert order.priority == 0
        assert order.currency_code == "INR"
        assert order.customer_code == "CUST-001"
        assert len(order.addresses) == 1
        assert order.addresses[0].city == "Mumbai"
        assert order.addresses[0].address_line1 == "123 Main St"
        assert len(order.sale_order_items) == 1
        assert order.sale_order_items[0].item_sku == "SKU-100"
        assert order.sale_order_items[0].status == "CREATED"

    def test_default_values(self):
        """SaleOrderResponse should have sensible defaults (all None)."""
        order = SaleOrderResponse()
        assert order.code is None
        assert order.cod is None
        assert order.total_discount is None
        assert order.addresses is None
        assert order.sale_order_items is None

    def test_allows_extra_fields(self):
        """SaleOrderResponse should allow extra unknown fields from API."""
        data = {"code": "SO-001", "someNewApiField": "surprise"}
        order = SaleOrderResponse.model_validate(data)
        assert order.code == "SO-001"
        assert order.model_extra == {"someNewApiField": "surprise"}


class TestAdjustInventoryRequest:
    """Tests for AdjustInventoryRequest model."""

    def test_serializes_to_camel_case(self):
        """AdjustInventoryRequest should serialize to camelCase via model_dump(by_alias=True)."""
        req = AdjustInventoryRequest(
            item_sku="SKU-001",
            quantity=10,
            shelf_code="SHELF-A1",
            adjustment_type="ADD",
            inventory_type="GOOD_INVENTORY",
        )

        dumped = req.model_dump(by_alias=True)

        assert dumped["itemSKU"] == "SKU-001"
        assert dumped["quantity"] == 10
        assert dumped["shelfCode"] == "SHELF-A1"
        assert dumped["adjustmentType"] == "ADD"
        assert dumped["inventoryType"] == "GOOD_INVENTORY"
        assert dumped["transferToShelfCode"] is None
        assert dumped["remarks"] is None

    def test_rejects_unknown_fields(self):
        """AdjustInventoryRequest should reject unknown fields."""
        with pytest.raises(ValidationError):
            AdjustInventoryRequest(
                item_sku="SKU-001",
                quantity=10,
                shelf_code="SHELF-A1",
                adjustment_type="ADD",
                unknown="bad",
            )

    def test_round_trip(self):
        """Round-trip: create model from dict, dump to dict, verify camelCase keys."""
        input_data = {
            "itemSKU": "SKU-999",
            "quantity": 5,
            "shelfCode": "SHELF-B2",
            "adjustmentType": "REMOVE",
            "inventoryType": "GOOD_INVENTORY",
        }

        # Create from camelCase dict
        req = AdjustInventoryRequest.model_validate(input_data)

        # Verify Python attribute access
        assert req.item_sku == "SKU-999"
        assert req.quantity == 5
        assert req.shelf_code == "SHELF-B2"
        assert req.adjustment_type == "REMOVE"

        # Dump back to camelCase
        output_data = req.model_dump(by_alias=True, exclude_none=True)

        assert output_data["itemSKU"] == "SKU-999"
        assert output_data["quantity"] == 5
        assert output_data["shelfCode"] == "SHELF-B2"
        assert output_data["adjustmentType"] == "REMOVE"
        assert output_data["inventoryType"] == "GOOD_INVENTORY"
        # Keys should be camelCase
        assert "item_sku" not in output_data
        assert "shelf_code" not in output_data
