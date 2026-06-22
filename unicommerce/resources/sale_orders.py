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

    async def cancel(self, code: str, *, items: list[str] | None = None) -> CancelResponse:
        body: dict = {"code": code}
        if items:
            body["saleOrderItems"] = items
        return await self._transport.request(
            path="/oms/saleOrder/cancel",
            body=body,
            response_model=CancelResponse,
            safe_to_retry=False,
        )

    async def edit(self, code: str, *, updates: dict) -> SaleOrderResponse:
        return await self._transport.request(
            path="/oms/saleOrder/edit",
            body={"code": code, **updates},
            response_model=SaleOrderResponse,
            safe_to_retry=False,
        )

    async def verify(self, code: str) -> SaleOrderResponse:
        return await self._transport.request(
            path="/oms/saleOrder/verify",
            body={"code": code},
            response_model=SaleOrderResponse,
            safe_to_retry=False,
        )

    async def set_priority(self, code: str, priority: int) -> SaleOrderResponse:
        return await self._transport.request(
            path="/oms/saleOrder/setPriority",
            body={"code": code, "priority": priority},
            response_model=SaleOrderResponse,
            safe_to_retry=False,
        )

    async def mark_returned(self, code: str) -> SaleOrderResponse:
        return await self._transport.request(
            path="/oms/saleOrder/markReturned",
            body={"code": code},
            response_model=SaleOrderResponse,
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

    def cancel(self, code: str, *, items: list[str] | None = None) -> CancelResponse:
        body: dict = {"code": code}
        if items:
            body["saleOrderItems"] = items
        return self._transport.request(
            path="/oms/saleOrder/cancel",
            body=body,
            response_model=CancelResponse,
            safe_to_retry=False,
        )

    def edit(self, code: str, *, updates: dict) -> SaleOrderResponse:
        return self._transport.request(
            path="/oms/saleOrder/edit",
            body={"code": code, **updates},
            response_model=SaleOrderResponse,
            safe_to_retry=False,
        )

    def verify(self, code: str) -> SaleOrderResponse:
        return self._transport.request(
            path="/oms/saleOrder/verify",
            body={"code": code},
            response_model=SaleOrderResponse,
            safe_to_retry=False,
        )

    def set_priority(self, code: str, priority: int) -> SaleOrderResponse:
        return self._transport.request(
            path="/oms/saleOrder/setPriority",
            body={"code": code, "priority": priority},
            response_model=SaleOrderResponse,
            safe_to_retry=False,
        )

    def mark_returned(self, code: str) -> SaleOrderResponse:
        return self._transport.request(
            path="/oms/saleOrder/markReturned",
            body={"code": code},
            response_model=SaleOrderResponse,
            safe_to_retry=False,
        )
