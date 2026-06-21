from pydantic import Field

from unicommerce.models.base import UnicommerceRequest, UnicommerceResponse


class AdjustInventoryRequest(UnicommerceRequest):
    item_sku: str = Field(alias="itemSKU")
    quantity: int = Field(alias="quantity")
    shelf_code: str = Field(alias="shelfCode")
    adjustment_type: str = Field(alias="adjustmentType")  # ADD, REMOVE, REPLACE, TRANSFER
    inventory_type: str = Field("GOOD_INVENTORY", alias="inventoryType")
    transfer_to_shelf_code: str | None = Field(None, alias="transferToShelfCode")
    remarks: str | None = Field(None, alias="remarks")


class AdjustInventoryResponse(UnicommerceResponse):
    item_sku: str = Field("", alias="itemSKU")
    quantity: int = Field(0, alias="quantity")


class InventorySnapshotItem(UnicommerceResponse):
    item_sku: str = Field("", alias="itemSKU")
    shelf_code: str = Field("", alias="shelfCode")
    quantity: int = Field(0, alias="quantity")
    inventory_type: str = Field("", alias="inventoryType")


class InventorySnapshotResponse(UnicommerceResponse):
    inventory_items: list[InventorySnapshotItem] = Field(default_factory=list, alias="inventorySnapshots")
