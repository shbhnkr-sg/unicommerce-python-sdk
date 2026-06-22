from pydantic import Field

from unicommerce.models.base import UnicommerceRequest, UnicommerceResponse


class AdjustInventoryRequest(UnicommerceRequest):
    item_sku: str = Field(alias="itemSKU")
    quantity: int = Field(alias="quantity")
    shelf_code: str = Field(alias="shelfCode")
    adjustment_type: str = Field(alias="adjustmentType")
    inventory_type: str = Field("GOOD_INVENTORY", alias="inventoryType")
    transfer_to_shelf_code: str | None = Field(None, alias="transferToShelfCode")
    remarks: str | None = Field(None, alias="remarks")


class AdjustInventoryResponse(UnicommerceResponse):
    inventory_adjustment_responses: list[dict] | None = Field(
        None, alias="inventoryAdjustmentResponses"
    )


class InventorySnapshotItem(UnicommerceResponse):
    item_type_sku: str | None = Field(None, alias="itemTypeSKU")
    inventory: int | None = Field(None, alias="inventory")
    open_sale: int | None = Field(None, alias="openSale")
    open_purchase: int | None = Field(None, alias="openPurchase")
    putaway_pending: int | None = Field(None, alias="putawayPending")
    inventory_blocked: int | None = Field(None, alias="inventoryBlocked")
    pending_stock_transfer: int | None = Field(None, alias="pendingStockTransfer")
    vendor_inventory: int | None = Field(None, alias="vendorInventory")
    virtual_inventory: int | None = Field(None, alias="virtualInventory")
    pending_inventory_assessment: int | None = Field(None, alias="pendingInventoryAssessment")
    bad_inventory: int | None = Field(None, alias="badInventory")


class InventorySnapshotResponse(UnicommerceResponse):
    inventory_snapshots: list[InventorySnapshotItem] | None = Field(
        None, alias="inventorySnapshots"
    )


class MarkFoundResponse(UnicommerceResponse):
    item_quantity_not_found_dto: list[dict] | None = Field(
        None, alias="itemQuantityNotFoundDTO"
    )


class NearbyInventoryResponse(UnicommerceResponse):
    facility_wise_nearby_inventory_snapshot_dto_list: list[dict] | None = Field(
        None, alias="facilityWiseNearbyInventorySnapshotDTOList"
    )
