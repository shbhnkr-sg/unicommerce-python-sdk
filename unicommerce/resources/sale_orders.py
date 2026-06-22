from unicommerce.models.sale_orders import (
    CancelResponse,
    CreateSaleOrderRequest,
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

    async def edit(self, *, sale_order_code: str, addresses: list[dict], **kwargs) -> None:
        body: dict = {"saleOrderAddress": {"saleOrderCode": sale_order_code, "addresses": addresses, **kwargs}}
        return await self._transport.request(
            path="/oms/saleOrder/edit",
            body=body,
            response_model=None,
            safe_to_retry=False,
        )

    async def verify(self, *, sale_order_code: str) -> None:
        return await self._transport.request(
            path="/oms/saleOrder/verify",
            body={"saleOrderCode": sale_order_code},
            response_model=None,
            safe_to_retry=False,
        )

    async def set_priority(self, *, sale_order_code: str, priority: int) -> None:
        return await self._transport.request(
            path="/oms/saleOrder/setPriority",
            body={"saleOrderCode": sale_order_code, "priority": priority},
            response_model=None,
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

    def edit(self, *, sale_order_code: str, addresses: list[dict], **kwargs) -> None:
        body: dict = {"saleOrderAddress": {"saleOrderCode": sale_order_code, "addresses": addresses, **kwargs}}
        return self._transport.request(
            path="/oms/saleOrder/edit",
            body=body,
            response_model=None,
            safe_to_retry=False,
        )

    def verify(self, *, sale_order_code: str) -> None:
        return self._transport.request(
            path="/oms/saleOrder/verify",
            body={"saleOrderCode": sale_order_code},
            response_model=None,
            safe_to_retry=False,
        )

    def set_priority(self, *, sale_order_code: str, priority: int) -> None:
        return self._transport.request(
            path="/oms/saleOrder/setPriority",
            body={"saleOrderCode": sale_order_code, "priority": priority},
            response_model=None,
            safe_to_retry=False,
        )
