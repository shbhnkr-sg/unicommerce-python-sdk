from unicommerce.models.base import UnicommerceResponse
from unicommerce.models.sale_orders import (
    CancelResponse,
    CreateSaleOrderRequest,
    CustomerResponse,
    ItemDetailBulkResponse,
    ItemDetailResponse,
    SaleOrderResponse,
    SaleOrderSearchResponse,
)
from unicommerce.resources.base import AsyncBaseResource, BaseResource


class AsyncSaleOrders(AsyncBaseResource):
    async def create(
        self, order: CreateSaleOrderRequest, *, facility: str | None = None
    ) -> SaleOrderResponse:
        return await self._transport.request(
            path="/oms/saleOrder/create",
            body=order,
            response_model=SaleOrderResponse,
            facility=facility,
            safe_to_retry=False,
        )

    async def get(self, code: str, *, facility_codes: list[str] | None = None) -> SaleOrderResponse:
        body: dict = {"code": code}
        if facility_codes:
            body["facilityCodes"] = facility_codes
        return await self._transport.request(
            path="/oms/saleorder/get",
            body=body,
            response_model=SaleOrderResponse,
            safe_to_retry=True,
            dto_key="saleOrderDTO",
        )

    async def search(self, **filters) -> SaleOrderSearchResponse:
        return await self._transport.request(
            path="/oms/saleOrder/search",
            body=filters,
            response_model=SaleOrderSearchResponse,
            safe_to_retry=True,
        )

    async def cancel(
        self,
        *,
        sale_order_code: str,
        sale_order_item_codes: list[str] | None = None,
        cancellation_reason: str | None = None,
        cancel_partially: bool | None = None,
    ) -> CancelResponse:
        body: dict = {"saleOrderCode": sale_order_code}
        if sale_order_item_codes is not None:
            body["saleOrderItemCodes"] = sale_order_item_codes
        if cancellation_reason is not None:
            body["cancellationReason"] = cancellation_reason
        if cancel_partially is not None:
            body["cancelPartially"] = cancel_partially
        return await self._transport.request(
            path="/oms/saleOrder/cancel",
            body=body,
            response_model=CancelResponse,
            safe_to_retry=False,
        )

    async def edit(self, *, sale_order_code: str, addresses: list[dict], **kwargs) -> UnicommerceResponse:
        body: dict = {"saleOrderAddress": {"saleOrderCode": sale_order_code, "addresses": addresses, **kwargs}}
        return await self._transport.request(
            path="/oms/saleOrder/edit",
            body=body,
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def verify(self, *, sale_order_code: str) -> UnicommerceResponse:
        return await self._transport.request(
            path="/oms/saleOrder/verify",
            body={"saleOrderCode": sale_order_code},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def set_priority(self, *, sale_order_code: str, priority: int) -> UnicommerceResponse:
        return await self._transport.request(
            path="/oms/saleOrder/setPriority",
            body={"saleOrderCode": sale_order_code, "priority": priority},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def create_customer(self, *, customer: dict) -> CustomerResponse:
        return await self._transport.request(
            path="/oms/customer/create",
            body={"customer": customer},
            response_model=CustomerResponse,
            safe_to_retry=False,
        )

    async def edit_customer(self, *, customer: dict) -> CustomerResponse:
        return await self._transport.request(
            path="/oms/customer/edit",
            body={"customer": customer},
            response_model=CustomerResponse,
            safe_to_retry=False,
        )

    async def edit_metadata(
        self,
        *,
        sale_order_code: str,
        priority: int | None = None,
        custom_field_values: list[dict] | None = None,
    ) -> UnicommerceResponse:
        body: dict = {"saleOrderCode": sale_order_code}
        if priority is not None:
            body["priority"] = priority
        if custom_field_values is not None:
            body["customFieldValues"] = custom_field_values
        return await self._transport.request(
            path="/oms/saleOrder/editSaleOrderMetadata",
            body=body,
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def edit_item_metadata(
        self,
        *,
        sale_order_code: str,
        sale_order_item_code: str,
        custom_field_values: list[dict],
    ) -> UnicommerceResponse:
        return await self._transport.request(
            path="/oms/saleOrder/editSaleOrderItemMetadata",
            body={
                "saleOrderCode": sale_order_code,
                "saleOrderItemCode": sale_order_item_code,
                "customFieldValues": custom_field_values,
            },
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def hold(self, *, sale_order_code: str) -> UnicommerceResponse:
        return await self._transport.request(
            path="/oms/saleOrder/hold",
            body={"saleOrderCode": sale_order_code},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def unhold(self, *, sale_order_code: str) -> UnicommerceResponse:
        return await self._transport.request(
            path="/oms/saleOrder/unhold",
            body={"saleOrderCode": sale_order_code},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def hold_items(
        self, *, sale_order_code: str, sale_order_item_codes: list[str]
    ) -> UnicommerceResponse:
        return await self._transport.request(
            path="/oms/saleOrder/holdSaleOrderItems",
            body={
                "saleOrderCode": sale_order_code,
                "saleOrderItemCodes": sale_order_item_codes,
            },
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def unhold_items(
        self, *, sale_order_code: str, sale_order_item_codes: list[str]
    ) -> UnicommerceResponse:
        return await self._transport.request(
            path="/oms/saleOrder/unholdSaleOrderItems",
            body={
                "saleOrderCode": sale_order_code,
                "saleOrderItemCodes": sale_order_item_codes,
            },
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def switch_facility(
        self,
        *,
        facility_code: str,
        sale_order_code: str,
        sale_order_item_codes: list[str],
    ) -> UnicommerceResponse:
        return await self._transport.request(
            path="/oms/saleorder/facility/switch",
            body={
                "facilityCode": facility_code,
                "saleOrderCode": sale_order_code,
                "saleOrderItemCodes": sale_order_item_codes,
            },
            response_model=UnicommerceResponse,
            facility=facility_code,
            safe_to_retry=False,
        )

    async def add_item_detail(
        self,
        *,
        sale_order_code: str,
        sale_order_item_code: str,
        item_details: list[dict],
    ) -> ItemDetailResponse:
        return await self._transport.request(
            path="/oms/inflow/saleOrderItem/detail/add",
            body={
                "saleOrderCode": sale_order_code,
                "saleOrderItemCode": sale_order_item_code,
                "itemDetails": item_details,
            },
            response_model=ItemDetailResponse,
            safe_to_retry=False,
        )

    async def add_item_detail_bulk(
        self,
        *,
        sale_order_code: str,
        sale_order_item_detail_dtos: list[dict],
    ) -> ItemDetailBulkResponse:
        return await self._transport.request(
            path="/oms/inflow/saleOrderItem/detail/add/bulk",
            body={
                "saleOrderCode": sale_order_code,
                "saleOrderItemDetailDTOS": sale_order_item_detail_dtos,
            },
            response_model=ItemDetailBulkResponse,
            safe_to_retry=False,
        )


class SaleOrders(BaseResource):
    def create(
        self, order: CreateSaleOrderRequest, *, facility: str | None = None
    ) -> SaleOrderResponse:
        return self._transport.request(
            path="/oms/saleOrder/create",
            body=order,
            response_model=SaleOrderResponse,
            facility=facility,
            safe_to_retry=False,
        )

    def get(self, code: str, *, facility_codes: list[str] | None = None) -> SaleOrderResponse:
        body: dict = {"code": code}
        if facility_codes:
            body["facilityCodes"] = facility_codes
        return self._transport.request(
            path="/oms/saleorder/get",
            body=body,
            response_model=SaleOrderResponse,
            safe_to_retry=True,
            dto_key="saleOrderDTO",
        )

    def search(self, **filters) -> SaleOrderSearchResponse:
        return self._transport.request(
            path="/oms/saleOrder/search",
            body=filters,
            response_model=SaleOrderSearchResponse,
            safe_to_retry=True,
        )

    def cancel(
        self,
        *,
        sale_order_code: str,
        sale_order_item_codes: list[str] | None = None,
        cancellation_reason: str | None = None,
        cancel_partially: bool | None = None,
    ) -> CancelResponse:
        body: dict = {"saleOrderCode": sale_order_code}
        if sale_order_item_codes is not None:
            body["saleOrderItemCodes"] = sale_order_item_codes
        if cancellation_reason is not None:
            body["cancellationReason"] = cancellation_reason
        if cancel_partially is not None:
            body["cancelPartially"] = cancel_partially
        return self._transport.request(
            path="/oms/saleOrder/cancel",
            body=body,
            response_model=CancelResponse,
            safe_to_retry=False,
        )

    def edit(self, *, sale_order_code: str, addresses: list[dict], **kwargs) -> UnicommerceResponse:
        body: dict = {"saleOrderAddress": {"saleOrderCode": sale_order_code, "addresses": addresses, **kwargs}}
        return self._transport.request(
            path="/oms/saleOrder/edit",
            body=body,
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def verify(self, *, sale_order_code: str) -> UnicommerceResponse:
        return self._transport.request(
            path="/oms/saleOrder/verify",
            body={"saleOrderCode": sale_order_code},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def set_priority(self, *, sale_order_code: str, priority: int) -> UnicommerceResponse:
        return self._transport.request(
            path="/oms/saleOrder/setPriority",
            body={"saleOrderCode": sale_order_code, "priority": priority},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def create_customer(self, *, customer: dict) -> CustomerResponse:
        return self._transport.request(
            path="/oms/customer/create",
            body={"customer": customer},
            response_model=CustomerResponse,
            safe_to_retry=False,
        )

    def edit_customer(self, *, customer: dict) -> CustomerResponse:
        return self._transport.request(
            path="/oms/customer/edit",
            body={"customer": customer},
            response_model=CustomerResponse,
            safe_to_retry=False,
        )

    def edit_metadata(
        self,
        *,
        sale_order_code: str,
        priority: int | None = None,
        custom_field_values: list[dict] | None = None,
    ) -> UnicommerceResponse:
        body: dict = {"saleOrderCode": sale_order_code}
        if priority is not None:
            body["priority"] = priority
        if custom_field_values is not None:
            body["customFieldValues"] = custom_field_values
        return self._transport.request(
            path="/oms/saleOrder/editSaleOrderMetadata",
            body=body,
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def edit_item_metadata(
        self,
        *,
        sale_order_code: str,
        sale_order_item_code: str,
        custom_field_values: list[dict],
    ) -> UnicommerceResponse:
        return self._transport.request(
            path="/oms/saleOrder/editSaleOrderItemMetadata",
            body={
                "saleOrderCode": sale_order_code,
                "saleOrderItemCode": sale_order_item_code,
                "customFieldValues": custom_field_values,
            },
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def hold(self, *, sale_order_code: str) -> UnicommerceResponse:
        return self._transport.request(
            path="/oms/saleOrder/hold",
            body={"saleOrderCode": sale_order_code},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def unhold(self, *, sale_order_code: str) -> UnicommerceResponse:
        return self._transport.request(
            path="/oms/saleOrder/unhold",
            body={"saleOrderCode": sale_order_code},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def hold_items(
        self, *, sale_order_code: str, sale_order_item_codes: list[str]
    ) -> UnicommerceResponse:
        return self._transport.request(
            path="/oms/saleOrder/holdSaleOrderItems",
            body={
                "saleOrderCode": sale_order_code,
                "saleOrderItemCodes": sale_order_item_codes,
            },
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def unhold_items(
        self, *, sale_order_code: str, sale_order_item_codes: list[str]
    ) -> UnicommerceResponse:
        return self._transport.request(
            path="/oms/saleOrder/unholdSaleOrderItems",
            body={
                "saleOrderCode": sale_order_code,
                "saleOrderItemCodes": sale_order_item_codes,
            },
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def switch_facility(
        self,
        *,
        facility_code: str,
        sale_order_code: str,
        sale_order_item_codes: list[str],
    ) -> UnicommerceResponse:
        return self._transport.request(
            path="/oms/saleorder/facility/switch",
            body={
                "facilityCode": facility_code,
                "saleOrderCode": sale_order_code,
                "saleOrderItemCodes": sale_order_item_codes,
            },
            response_model=UnicommerceResponse,
            facility=facility_code,
            safe_to_retry=False,
        )

    def add_item_detail(
        self,
        *,
        sale_order_code: str,
        sale_order_item_code: str,
        item_details: list[dict],
    ) -> ItemDetailResponse:
        return self._transport.request(
            path="/oms/inflow/saleOrderItem/detail/add",
            body={
                "saleOrderCode": sale_order_code,
                "saleOrderItemCode": sale_order_item_code,
                "itemDetails": item_details,
            },
            response_model=ItemDetailResponse,
            safe_to_retry=False,
        )

    def add_item_detail_bulk(
        self,
        *,
        sale_order_code: str,
        sale_order_item_detail_dtos: list[dict],
    ) -> ItemDetailBulkResponse:
        return self._transport.request(
            path="/oms/inflow/saleOrderItem/detail/add/bulk",
            body={
                "saleOrderCode": sale_order_code,
                "saleOrderItemDetailDTOS": sale_order_item_detail_dtos,
            },
            response_model=ItemDetailBulkResponse,
            safe_to_retry=False,
        )
