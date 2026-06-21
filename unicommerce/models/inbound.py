from pydantic import Field

from unicommerce.models.base import UnicommerceRequest, UnicommerceResponse


class CreateVendorRequest(UnicommerceRequest):
    vendor: dict = Field(alias="vendor")


class VendorResponse(UnicommerceResponse):
    code: str = Field("", alias="code")
    name: str = Field("", alias="name")
    email: str = Field("", alias="email")
    phone: str = Field("", alias="phone")
    address: str = Field("", alias="address")


class CreatePurchaseOrderRequest(UnicommerceRequest):
    purchase_order: dict = Field(alias="purchaseOrder")


class PurchaseOrderResponse(UnicommerceResponse):
    code: str = Field("", alias="code")
    vendor_code: str = Field("", alias="vendorCode")
    status: str = Field("", alias="status")
    created_date: str = Field("", alias="createdDate")


class CreateGrnRequest(UnicommerceRequest):
    grn: dict = Field(alias="grn")


class GrnResponse(UnicommerceResponse):
    code: str = Field("", alias="code")
    purchase_order_code: str = Field("", alias="purchaseOrderCode")
    status: str = Field("", alias="status")
    received_date: str = Field("", alias="receivedDate")
