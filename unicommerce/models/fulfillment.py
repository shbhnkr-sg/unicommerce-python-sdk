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
    code: str = Field("", alias="code")
    status: str = Field("", alias="status")
    shipping_provider: str = Field("", alias="shippingProvider")
    tracking_number: str = Field("", alias="trackingNumber")
    invoice_code: str = Field("", alias="invoiceCode")


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
