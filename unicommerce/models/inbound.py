from pydantic import Field

from unicommerce.models.base import UnicommerceRequest, UnicommerceResponse


class VendorResponse(UnicommerceResponse):
    code: str | None = Field(None, alias="code")
    name: str | None = Field(None, alias="name")
    pan: str | None = Field(None, alias="pan")
    gst_number: str | None = Field(None, alias="gstNumber")
    website: str | None = Field(None, alias="website")
    enabled: bool | None = Field(None, alias="enabled")
    tax_exempted: bool | None = Field(None, alias="taxExempted")


class PurchaseOrderResponse(UnicommerceResponse):
    code: str | None = Field(None, alias="code")
    purchase_order_code: str | None = Field(None, alias="purchaseOrderCode")
    vendor_code: str | None = Field(None, alias="vendorCode")
    vendor_name: str | None = Field(None, alias="vendorName")
    status_code: str | None = Field(None, alias="statusCode")
    created: str | None = Field(None, alias="created")
    expiry_date: str | None = Field(None, alias="expiryDate")
    delivery_date: str | None = Field(None, alias="deliveryDate")


class GrnResponse(UnicommerceResponse):
    code: str | None = Field(None, alias="code")
    status_code: str | None = Field(None, alias="statusCode")
    created: str | None = Field(None, alias="created")
    vendor_invoice_number: str | None = Field(None, alias="vendorInvoiceNumber")
    total_quantity: int | None = Field(None, alias="totalQuantity")
    vendor_code: str | None = Field(None, alias="vendorCode")


class VendorBackorderResponse(UnicommerceResponse):
    total_records: int | None = Field(None, alias="totalRecords")
    elements: list[dict] | None = Field(None, alias="elements")


class PurchaseOrderSearchResponse(UnicommerceResponse):
    purchase_order_codes: list[str] | None = Field(None, alias="purchaseOrderCodes")


class PurchaseOrderCreateResponse(UnicommerceResponse):
    purchase_order_code: str | None = Field(None, alias="purchaseOrderCode")


class GrnSearchResponse(UnicommerceResponse):
    inflow_receipt_codes: list[str] | None = Field(None, alias="inflowReceiptCodes")
