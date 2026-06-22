from pydantic import Field

from unicommerce.models.base import UnicommerceRequest, UnicommerceResponse


class Address(UnicommerceResponse):
    id: str | None = Field(None, alias="id")
    name: str | None = Field(None, alias="name")
    address_line1: str | None = Field(None, alias="addressLine1")
    address_line2: str | None = Field(None, alias="addressLine2")
    city: str | None = Field(None, alias="city")
    state: str | None = Field(None, alias="state")
    pincode: str | None = Field(None, alias="pincode")
    country: str | None = Field(None, alias="country")
    phone: str | None = Field(None, alias="phone")
    email: str | None = Field(None, alias="email")


class SaleOrderItem(UnicommerceResponse):
    id: int | None = Field(None, alias="id")
    code: str | None = Field(None, alias="code")
    item_sku: str | None = Field(None, alias="itemSku")
    item_name: str | None = Field(None, alias="itemName")
    selling_price: float | None = Field(None, alias="sellingPrice")
    total_price: float | None = Field(None, alias="totalPrice")
    discount: float | None = Field(None, alias="discount")
    shipping_charges: float | None = Field(None, alias="shippingCharges")
    quantity: int | None = Field(None, alias="quantity")
    status: str | None = Field(None, alias="statusCode")
    shipping_package_code: str | None = Field(None, alias="shippingPackageCode")
    shipping_package_status: str | None = Field(None, alias="shippingPackageStatus")
    facility_code: str | None = Field(None, alias="facilityCode")
    channel_sale_order_item_code: str | None = Field(None, alias="channelSaleOrderItemCode")


class CreateSaleOrderRequest(UnicommerceRequest):
    sale_order: dict = Field(alias="saleOrder")


class SaleOrderResponse(UnicommerceResponse):
    code: str | None = Field(None, alias="code")
    display_order_code: str | None = Field(None, alias="displayOrderCode")
    display_order_date_time: int | None = Field(None, alias="displayOrderDateTime")
    channel: str | None = Field(None, alias="channel")
    source: str | None = Field(None, alias="source")
    status: str | None = Field(None, alias="status")
    cod: bool | None = Field(None, alias="cod")
    priority: int | None = Field(None, alias="priority")
    currency_code: str | None = Field(None, alias="currencyCode")
    total_discount: float | None = Field(None, alias="totalDiscount")
    total_shipping_charges: float | None = Field(None, alias="totalShippingCharges")
    customer_code: str | None = Field(None, alias="customerCode")
    notification_email: str | None = Field(None, alias="notificationEmail")
    notification_mobile: str | None = Field(None, alias="notificationMobile")
    created: int | None = Field(None, alias="created")
    updated: int | None = Field(None, alias="updated")
    fulfillment_tat: int | None = Field(None, alias="fulfillmentTat")
    third_party_shipping: bool | None = Field(None, alias="thirdPartyShipping")
    addresses: list[Address] | None = Field(None, alias="addresses")
    sale_order_items: list[SaleOrderItem] | None = Field(None, alias="saleOrderItems")


class SaleOrderSearchResponse(UnicommerceResponse):
    sale_orders: list[SaleOrderResponse] | None = Field(None, alias="elements")
    total_records: int | None = Field(None, alias="totalRecords")


class CancelResponse(UnicommerceResponse):
    code: str | None = Field(None, alias="code")
    status: str | None = Field(None, alias="status")
