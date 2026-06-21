from pydantic import Field

from unicommerce.models.base import UnicommerceRequest, UnicommerceResponse


class Address(UnicommerceResponse):
    id: int | None = Field(None, alias="id")
    name: str = Field("", alias="name")
    address_line1: str = Field("", alias="addressLine1")
    address_line2: str = Field("", alias="addressLine2")
    city: str = Field("", alias="city")
    state: str = Field("", alias="state")
    pincode: str = Field("", alias="pincode")
    country: str = Field("", alias="country")
    phone: str = Field("", alias="phone")
    email: str = Field("", alias="email")


class SaleOrderItem(UnicommerceResponse):
    code: str = Field("", alias="code")
    item_sku: str = Field("", alias="itemSku")
    item_name: str = Field("", alias="itemName")
    selling_price: float = Field(0, alias="sellingPrice")
    total_price: float = Field(0, alias="totalPrice")
    discount: float = Field(0, alias="discount")
    shipping_charges: float = Field(0, alias="shippingCharges")
    quantity: int = Field(0, alias="quantity")
    status: str = Field("", alias="statusCode")


class CreateSaleOrderRequest(UnicommerceRequest):
    sale_order: dict = Field(alias="saleOrder")


class SaleOrderResponse(UnicommerceResponse):
    code: str = Field("", alias="code")
    display_order_code: str = Field("", alias="displayOrderCode")
    display_order_date_time: str = Field("", alias="displayOrderDateTime")
    channel: str = Field("", alias="channel")
    status: str = Field("", alias="status")
    cash_on_delivery: bool = Field(False, alias="cashOnDelivery")
    total_prepaid_amount: float = Field(0, alias="totalPrepaidAmount")
    total_discount: float = Field(0, alias="totalDiscount")
    total_shipping_charges: float = Field(0, alias="totalShippingCharges")
    customer_name: str = Field("", alias="customerName")
    customer_code: str = Field("", alias="customerCode")
    addresses: list[Address] = Field(default_factory=list, alias="addresses")
    sale_order_items: list[SaleOrderItem] = Field(default_factory=list, alias="saleOrderItems")


class SaleOrderSearchResponse(UnicommerceResponse):
    sale_orders: list[SaleOrderResponse] = Field(default_factory=list, alias="elements")
    total_count: int = Field(0, alias="totalCount")


class CancelResponse(UnicommerceResponse):
    code: str = Field("", alias="code")
    status: str = Field("", alias="status")
