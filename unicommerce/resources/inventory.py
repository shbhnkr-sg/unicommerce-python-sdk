from unicommerce.models.inventory import (
    AdjustInventoryRequest,
    AdjustInventoryResponse,
    InventorySnapshotResponse,
)
from unicommerce.resources.base import AsyncBaseResource, BaseResource


class AsyncInventory(AsyncBaseResource):
    async def adjust(
        self,
        *,
        item_sku: str,
        quantity: int,
        shelf_code: str,
        adjustment_type: str,
        inventory_type: str = "GOOD_INVENTORY",
        transfer_to_shelf_code: str | None = None,
        remarks: str | None = None,
        facility: str | None = None,
    ) -> AdjustInventoryResponse:
        request = AdjustInventoryRequest(
            itemSKU=item_sku,
            quantity=quantity,
            shelfCode=shelf_code,
            adjustmentType=adjustment_type,
            inventoryType=inventory_type,
            transferToShelfCode=transfer_to_shelf_code,
            remarks=remarks,
        )
        return await self._transport.request(
            path="/inventory/adjust",
            body={"inventoryAdjustment": request.model_dump(by_alias=True, exclude_none=True)},
            response_model=AdjustInventoryResponse,
            facility=facility,
            safe_to_retry=False,
        )

    async def adjust_bulk(
        self, *, adjustments: list[dict], facility: str | None = None
    ) -> AdjustInventoryResponse:
        return await self._transport.request(
            path="/inventory/adjust/bulk",
            body={"inventoryAdjustments": adjustments},
            response_model=AdjustInventoryResponse,
            facility=facility,
            safe_to_retry=False,
        )

    async def get_snapshot(
        self, *, item_sku: str | None = None, facility: str | None = None
    ) -> InventorySnapshotResponse:
        body = {}
        if item_sku:
            body["itemSKU"] = item_sku
        return await self._transport.request(
            path="/inventory/inventorySnapshot/get",
            body=body,
            response_model=InventorySnapshotResponse,
            facility=facility,
            safe_to_retry=True,
        )

    async def mark_found(
        self, *, item_sku: str, quantity: int, shelf_code: str, facility: str | None = None
    ) -> AdjustInventoryResponse:
        return await self._transport.request(
            path="/inventory/markFound",
            body={"itemSKU": item_sku, "quantity": quantity, "shelfCode": shelf_code},
            response_model=AdjustInventoryResponse,
            facility=facility,
            safe_to_retry=False,
        )


class Inventory(BaseResource):
    def adjust(
        self,
        *,
        item_sku: str,
        quantity: int,
        shelf_code: str,
        adjustment_type: str,
        inventory_type: str = "GOOD_INVENTORY",
        transfer_to_shelf_code: str | None = None,
        remarks: str | None = None,
        facility: str | None = None,
    ) -> AdjustInventoryResponse:
        request = AdjustInventoryRequest(
            itemSKU=item_sku,
            quantity=quantity,
            shelfCode=shelf_code,
            adjustmentType=adjustment_type,
            inventoryType=inventory_type,
            transferToShelfCode=transfer_to_shelf_code,
            remarks=remarks,
        )
        return self._transport.request(
            path="/inventory/adjust",
            body={"inventoryAdjustment": request.model_dump(by_alias=True, exclude_none=True)},
            response_model=AdjustInventoryResponse,
            facility=facility,
            safe_to_retry=False,
        )

    def adjust_bulk(
        self, *, adjustments: list[dict], facility: str | None = None
    ) -> AdjustInventoryResponse:
        return self._transport.request(
            path="/inventory/adjust/bulk",
            body={"inventoryAdjustments": adjustments},
            response_model=AdjustInventoryResponse,
            facility=facility,
            safe_to_retry=False,
        )

    def get_snapshot(
        self, *, item_sku: str | None = None, facility: str | None = None
    ) -> InventorySnapshotResponse:
        body = {}
        if item_sku:
            body["itemSKU"] = item_sku
        return self._transport.request(
            path="/inventory/inventorySnapshot/get",
            body=body,
            response_model=InventorySnapshotResponse,
            facility=facility,
            safe_to_retry=True,
        )

    def mark_found(
        self, *, item_sku: str, quantity: int, shelf_code: str, facility: str | None = None
    ) -> AdjustInventoryResponse:
        return self._transport.request(
            path="/inventory/markFound",
            body={"itemSKU": item_sku, "quantity": quantity, "shelfCode": shelf_code},
            response_model=AdjustInventoryResponse,
            facility=facility,
            safe_to_retry=False,
        )
