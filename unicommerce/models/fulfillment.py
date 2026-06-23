from pydantic import Field

from unicommerce.models.base import UnicommerceResponse


class InvoiceDetailResponse(UnicommerceResponse):
    code: str | None = Field(None, alias="code")
    display_code: str | None = Field(None, alias="displayCode")
    shipping_package_code: str | None = Field(None, alias="shippingPackageCode")
    reverse_pickup_code: str | None = Field(None, alias="reversePickupCode")
    total_quantity: int | None = Field(None, alias="totalQuantity")
    payment_mode: str | None = Field(None, alias="paymentMode")
    selling_price: float | None = Field(None, alias="sellingPrice")
    subtotal: float | None = Field(None, alias="subtotal")
    total: float | None = Field(None, alias="total")
    vat: float | None = Field(None, alias="vat")
    cst: float | None = Field(None, alias="cst")
    integrated_gst: float | None = Field(None, alias="integratedGst")
    state_gst: float | None = Field(None, alias="stateGst")
    central_gst: float | None = Field(None, alias="centralGst")
    union_territory_gst: float | None = Field(None, alias="unionTerritoryGst")
    compensation_cess: float | None = Field(None, alias="compensationCess")
    additional_tax: float | None = Field(None, alias="additionalTax")
    prepaid_amount: float | None = Field(None, alias="prepaidAmount")
    store_credit: float | None = Field(None, alias="storeCredit")
    discount: float | None = Field(None, alias="discount")
    shipping_charges: float | None = Field(None, alias="shippingCharges")
    shipping_method_charges: float | None = Field(None, alias="shippingMethodCharges")
    cash_on_delivery_charges: float | None = Field(None, alias="cashOnDeliveryCharges")
    gift_wrap_charges: float | None = Field(None, alias="giftWrapCharges")
    channel_created: int | str | None = Field(None, alias="channelCreated")
    created: int | str | None = Field(None, alias="created")
    invoice_items: list[dict] | None = Field(None, alias="invoiceItems")
    is_return: bool | None = Field(None, alias="return")
    payment_detail: dict | None = Field(None, alias="paymentDetail")
    tcs_amount: float | None = Field(None, alias="tcsAmount")
    gst_number: str | None = Field(None, alias="gstNumber")
    invoice_link: str | None = Field(None, alias="invoiceLink")
    irn: str | None = Field(None, alias="irn")


class GetInvoiceDetailResponse(UnicommerceResponse):
    invoice: dict | None = Field(None, alias="invoice")


class InvoiceLabelResponse(UnicommerceResponse):
    invoice_code: str | None = Field(None, alias="invoiceCode")
    invoice_display_code: str | None = Field(None, alias="invoiceDisplayCode")
    label: str | None = Field(None, alias="label")


class CreateInvoiceAndLabelResponse(UnicommerceResponse):
    invoice_code: str | None = Field(None, alias="invoiceCode")
    shipping_package_code: str | None = Field(None, alias="shippingPackageCode")
    shipping_provider_code: str | None = Field(None, alias="shippingProviderCode")
    tracking_number: str | None = Field(None, alias="trackingNumber")
    shipping_label_link: str | None = Field(None, alias="shippingLabelLink")
    label: str | None = Field(None, alias="label")
    tracking_link: str | None = Field(None, alias="trackingLink")
    invoice_display_code: str | None = Field(None, alias="invoiceDisplayCode")


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


class CreateShippingPackageResponse(UnicommerceResponse):
    shipping_package_code: str | None = Field(None, alias="shippingPackageCode")


class ShippingManifestResponse(UnicommerceResponse):
    code: str = Field("", alias="code")
    status: str = Field("", alias="status")
    channel: str = Field("", alias="channel")
    shipping_provider: str = Field("", alias="shippingProvider")
    package_count: int = Field(0, alias="packageCount")


class UpdateTrackingStatusResponse(UnicommerceResponse):
    total_polled: int | None = Field(None, alias="totalPolled")
    failures: int | None = Field(None, alias="failures")
    total_changed: int | None = Field(None, alias="totalChanged")


class ShippingPackageSearchResponse(UnicommerceResponse):
    total_records: int | None = Field(None, alias="totalRecords")
    elements: list[dict] | None = Field(None, alias="elements")
