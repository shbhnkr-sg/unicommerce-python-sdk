from unicommerce.models.inbound import (
    CreateGrnRequest,
    CreatePurchaseOrderRequest,
    CreateVendorRequest,
    GrnResponse,
    PurchaseOrderResponse,
    VendorResponse,
)
from unicommerce.resources.base import AsyncBaseResource, BaseResource


class AsyncInbound(AsyncBaseResource):
    async def create_vendor(self, vendor: CreateVendorRequest) -> VendorResponse:
        return await self._transport.request(
            path="/vendor/create",
            body=vendor,
            response_model=VendorResponse,
            safe_to_retry=False,
        )

    async def get_vendor(self, code: str) -> VendorResponse:
        return await self._transport.request(
            path="/vendor/get",
            body={"code": code},
            response_model=VendorResponse,
            safe_to_retry=True,
        )

    async def create_purchase_order(self, po: CreatePurchaseOrderRequest) -> PurchaseOrderResponse:
        return await self._transport.request(
            path="/purchaseOrder/create",
            body=po,
            response_model=PurchaseOrderResponse,
            safe_to_retry=False,
        )

    async def get_purchase_order(self, code: str) -> PurchaseOrderResponse:
        return await self._transport.request(
            path="/purchaseOrder/get",
            body={"code": code},
            response_model=PurchaseOrderResponse,
            safe_to_retry=True,
        )

    async def create_grn(self, grn: CreateGrnRequest) -> GrnResponse:
        return await self._transport.request(
            path="/grn/create",
            body=grn,
            response_model=GrnResponse,
            safe_to_retry=False,
        )

    async def get_grn(self, code: str) -> GrnResponse:
        return await self._transport.request(
            path="/grn/get",
            body={"code": code},
            response_model=GrnResponse,
            safe_to_retry=True,
        )

    async def putaway(self, grn_code: str, items: list) -> GrnResponse:
        return await self._transport.request(
            path="/grn/putaway",
            body={"grnCode": grn_code, "items": items},
            response_model=GrnResponse,
            safe_to_retry=False,
        )


class Inbound(BaseResource):
    def create_vendor(self, vendor: CreateVendorRequest) -> VendorResponse:
        return self._transport.request(
            path="/vendor/create",
            body=vendor,
            response_model=VendorResponse,
            safe_to_retry=False,
        )

    def get_vendor(self, code: str) -> VendorResponse:
        return self._transport.request(
            path="/vendor/get",
            body={"code": code},
            response_model=VendorResponse,
            safe_to_retry=True,
        )

    def create_purchase_order(self, po: CreatePurchaseOrderRequest) -> PurchaseOrderResponse:
        return self._transport.request(
            path="/purchaseOrder/create",
            body=po,
            response_model=PurchaseOrderResponse,
            safe_to_retry=False,
        )

    def get_purchase_order(self, code: str) -> PurchaseOrderResponse:
        return self._transport.request(
            path="/purchaseOrder/get",
            body={"code": code},
            response_model=PurchaseOrderResponse,
            safe_to_retry=True,
        )

    def create_grn(self, grn: CreateGrnRequest) -> GrnResponse:
        return self._transport.request(
            path="/grn/create",
            body=grn,
            response_model=GrnResponse,
            safe_to_retry=False,
        )

    def get_grn(self, code: str) -> GrnResponse:
        return self._transport.request(
            path="/grn/get",
            body={"code": code},
            response_model=GrnResponse,
            safe_to_retry=True,
        )

    def putaway(self, grn_code: str, items: list) -> GrnResponse:
        return self._transport.request(
            path="/grn/putaway",
            body={"grnCode": grn_code, "items": items},
            response_model=GrnResponse,
            safe_to_retry=False,
        )
