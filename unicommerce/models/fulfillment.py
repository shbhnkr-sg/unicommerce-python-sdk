from pydantic import Field

from unicommerce.models.base import UnicommerceRequest, UnicommerceResponse


class CreateInvoiceRequest(UnicommerceRequest):
    shipping_package_code: str = Field(alias="shippingPackageCode")


class InvoiceResponse(UnicommerceResponse):
    invoice_code: str = Field("", alias="invoiceCode")
    invoice_date: str = Field("", alias="invoiceDate")
    shipping_package_code: str = Field("", alias="shippingPackageCode")
    channel_name: str = Field("", alias="channelName")


class ShippingPackageResponse(UnicommerceResponse):
    code: str | None = Field(None, alias="code")
    channel_shipment_code: str | None = Field(None, alias="channelShipmentCode")
    sale_order_code: str | None = Field(None, alias="saleOrderCode")
    status_code: str | None = Field(None, alias="statusCode")
    shipping_manifest_code: str | None = Field(None, alias="shippingManifestCode")
    actual_weight: float | None = Field(None, alias="actualWeight")
    box_width: int | None = Field(None, alias="boxWidth")
    box_height: int | None = Field(None, alias="boxHeight")
    box_length: int | None = Field(None, alias="boxLength")
    number_of_boxes: int | None = Field(None, alias="numberOfBoxes")
    collectable_amount: float | None = Field(None, alias="collectableAmount")
    shipping_provider: str | None = Field(None, alias="shippingProvider")
    tracking_number: str | None = Field(None, alias="trackingNumber")
    tracking_link: str | None = Field(None, alias="trackingLink")


class ShippingManifestResponse(UnicommerceResponse):
    code: str = Field("", alias="code")
    status: str = Field("", alias="status")
    channel: str = Field("", alias="channel")
    shipping_provider: str = Field("", alias="shippingProvider")
    package_count: int = Field(0, alias="packageCount")


class TrackShipmentResponse(UnicommerceResponse):
    tracking_number: str = Field("", alias="trackingNumber")
    status: str = Field("", alias="status")
    current_location: str = Field("", alias="currentLocation")
    estimated_delivery: str = Field("", alias="estimatedDelivery")
