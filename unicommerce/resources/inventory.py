from unicommerce.models.inventory import (
    AdjustInventoryRequest,
    AdjustInventoryResponse,
    InventorySnapshotResponse,
    MarkFoundResponse,
    NearbyInventoryResponse,
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
        self, *, updated_since_in_minutes: int = 60, facility: str | None = None
    ) -> InventorySnapshotResponse:
        return await self._transport.request(
            path="/inventory/inventorySnapshot/get",
            body={"updatedSinceInMinutes": updated_since_in_minutes},
            response_model=InventorySnapshotResponse,
            facility=facility,
            safe_to_retry=True,
        )

    async def mark_found(
        self,
        *,
        item_sku: str,
        shelf_code: str,
        quantity_found: int,
        ageing_start_date: str | None = None,
        facility: str | None = None,
    ) -> MarkFoundResponse:
        body: dict = {
            "itemSku": item_sku,
            "shelfCode": shelf_code,
            "quantityFound": quantity_found,
        }
        if ageing_start_date is not None:
            body["ageingStartDate"] = ageing_start_date
        return await self._transport.request(
            path="/inventory/markQuantityFound",
            body=body,
            response_model=MarkFoundResponse,
            facility=facility,
            safe_to_retry=False,
        )

    async def get_nearby_store_inventory(
        self,
        *,
        customer_pincode: str,
        facility_search_radius: str,
        facility_operational_type: str,
        facility_status: str,
        sku_code: str,
        quantity: int,
    ) -> NearbyInventoryResponse:
        return await self._transport.request(
            path="/oms/nearbyInventory/get",
            body={
                "customerPincode": customer_pincode,
                "facilitySearchRadius": facility_search_radius,
                "facilityOperationalType": facility_operational_type,
                "facilityStatus": facility_status,
                "itemType": {"skuCode": sku_code, "quantity": quantity},
            },
            response_model=NearbyInventoryResponse,
            safe_to_retry=True,
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
        self, *, updated_since_in_minutes: int = 60, facility: str | None = None
    ) -> InventorySnapshotResponse:
        return self._transport.request(
            path="/inventory/inventorySnapshot/get",
            body={"updatedSinceInMinutes": updated_since_in_minutes},
            response_model=InventorySnapshotResponse,
            facility=facility,
            safe_to_retry=True,
        )

    def mark_found(
        self,
        *,
        item_sku: str,
        shelf_code: str,
        quantity_found: int,
        ageing_start_date: str | None = None,
        facility: str | None = None,
    ) -> MarkFoundResponse:
        body: dict = {
            "itemSku": item_sku,
            "shelfCode": shelf_code,
            "quantityFound": quantity_found,
        }
        if ageing_start_date is not None:
            body["ageingStartDate"] = ageing_start_date
        return self._transport.request(
            path="/inventory/markQuantityFound",
            body=body,
            response_model=MarkFoundResponse,
            facility=facility,
            safe_to_retry=False,
        )

    def get_nearby_store_inventory(
        self,
        *,
        customer_pincode: str,
        facility_search_radius: str,
        facility_operational_type: str,
        facility_status: str,
        sku_code: str,
        quantity: int,
    ) -> NearbyInventoryResponse:
        return self._transport.request(
            path="/oms/nearbyInventory/get",
            body={
                "customerPincode": customer_pincode,
                "facilitySearchRadius": facility_search_radius,
                "facilityOperationalType": facility_operational_type,
                "facilityStatus": facility_status,
                "itemType": {"skuCode": sku_code, "quantity": quantity},
            },
            response_model=NearbyInventoryResponse,
            safe_to_retry=True,
        )
