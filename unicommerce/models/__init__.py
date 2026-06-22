"""Pydantic models for all Unicommerce API resource domains."""

from unicommerce.models.auth import TokenResponse
from unicommerce.models.base import UnicommerceRequest, UnicommerceResponse
from unicommerce.models.common import ApiErrorDetail, ApiWarning
from unicommerce.models.pdf import PdfResponse
from unicommerce.models.export_jobs import (
    CreateExportJobRequest,
    CreateExportJobResponse,
    ExportJobStatusResponse,
)
from unicommerce.models.facilities import (
    FacilityResponse,
    FacilitySearchResponse,
)
from unicommerce.models.fulfillment import (
    CreateInvoiceAndLabelResponse,
    CreateShippingPackageResponse,
    GetInvoiceDetailResponse,
    InvoiceDetailResponse,
    InvoiceLabelResponse,
    ShippingManifestResponse,
    ShippingPackageResponse,
    ShippingPackageSearchResponse,
    UpdateTrackingStatusResponse,
)
from unicommerce.models.inbound import (
    GrnResponse,
    GrnSearchResponse,
    PurchaseOrderCreateResponse,
    PurchaseOrderResponse,
    PurchaseOrderSearchResponse,
    VendorBackorderResponse,
    VendorResponse,
)
from unicommerce.models.inventory import (
    AdjustInventoryRequest,
    AdjustInventoryResponse,
    InventorySnapshotItem,
    InventorySnapshotResponse,
    MarkFoundResponse,
    NearbyInventoryResponse,
)
from unicommerce.models.outbound import (
    GatepassCreateResponse,
    GatepassGetResponse,
    GatepassScanResponse,
    GatepassSearchResponse,
)
from unicommerce.models.products import (
    CategoryResponse,
    ChannelItemTypeResponse,
    CreateOrEditItemResponse,
    ProductResponse,
    ProductSearchResponse,
)
from unicommerce.models.returns import (
    AllocateCourierResponse,
    ReturnGetResponse,
    ReturnOrderSummary,
    ReturnSearchResponse,
    ReversePickupResponse,
)
from unicommerce.models.sale_orders import (
    Address,
    CancelResponse,
    CreateSaleOrderRequest,
    CustomerResponse,
    ItemDetailBulkResponse,
    ItemDetailResponse,
    SaleOrderItem,
    SaleOrderResponse,
    SaleOrderSearchResponse,
)

__all__ = [
    "UnicommerceRequest",
    "UnicommerceResponse",
    "ApiErrorDetail",
    "ApiWarning",
    "TokenResponse",
    "PdfResponse",
    "Address",
    "SaleOrderItem",
    "CreateSaleOrderRequest",
    "SaleOrderResponse",
    "SaleOrderSearchResponse",
    "CancelResponse",
    "CustomerResponse",
    "ItemDetailResponse",
    "ItemDetailBulkResponse",
    "AdjustInventoryRequest",
    "AdjustInventoryResponse",
    "InventorySnapshotItem",
    "InventorySnapshotResponse",
    "MarkFoundResponse",
    "NearbyInventoryResponse",
    "ProductResponse",
    "ProductSearchResponse",
    "CategoryResponse",
    "CreateOrEditItemResponse",
    "ChannelItemTypeResponse",
    "InvoiceDetailResponse",
    "GetInvoiceDetailResponse",
    "InvoiceLabelResponse",
    "CreateInvoiceAndLabelResponse",
    "CreateShippingPackageResponse",
    "ShippingPackageResponse",
    "ShippingPackageSearchResponse",
    "ShippingManifestResponse",
    "UpdateTrackingStatusResponse",
    "VendorResponse",
    "VendorBackorderResponse",
    "PurchaseOrderResponse",
    "PurchaseOrderSearchResponse",
    "PurchaseOrderCreateResponse",
    "GrnResponse",
    "GrnSearchResponse",
    "ReturnGetResponse",
    "ReturnSearchResponse",
    "ReturnOrderSummary",
    "ReversePickupResponse",
    "AllocateCourierResponse",
    "GatepassScanResponse",
    "GatepassCreateResponse",
    "GatepassSearchResponse",
    "GatepassGetResponse",
    "FacilityResponse",
    "FacilitySearchResponse",
    "CreateExportJobRequest",
    "CreateExportJobResponse",
    "ExportJobStatusResponse",
]
