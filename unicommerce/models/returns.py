from pydantic import Field

from unicommerce.models.base import UnicommerceRequest, UnicommerceResponse


class ReturnResponse(UnicommerceResponse):
    code: str = Field("", alias="code")
    sale_order_code: str = Field("", alias="saleOrderCode")
    shipment_code: str = Field("", alias="shipmentCode")
    status: str = Field("", alias="status")
    return_reason: str = Field("", alias="returnReason")


class CreateReversePickupRequest(UnicommerceRequest):
    reverse_pickup: dict = Field(alias="reversePickup")


class ReversePickupResponse(UnicommerceResponse):
    code: str = Field("", alias="code")
    status: str = Field("", alias="status")
    pickup_date: str = Field("", alias="pickupDate")
