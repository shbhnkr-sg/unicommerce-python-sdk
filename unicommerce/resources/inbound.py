from unicommerce.models.inbound import (
    GrnResponse,
    PurchaseOrderResponse,
    VendorResponse,
)
from unicommerce.resources.base import AsyncBaseResource, BaseResource


class AsyncInbound(AsyncBaseResource):
    async def create_vendor(self, *, vendor: dict) -> VendorResponse:
        return await self._transport.request(
            path="/purchase/vendor/create",
            body={"vendor": vendor},
            response_model=VendorResponse,
            safe_to_retry=False,
        )

    async def create_purchase_order(
        self,
        *,
        vendor_code: str,
        purchase_order_items: list[dict] | None = None,
        **kwargs,
    ) -> PurchaseOrderResponse:
        body: dict = {"vendorCode": vendor_code, **kwargs}
        if purchase_order_items is not None:
            body["purchaseOrderItems"] = purchase_order_items
        return await self._transport.request(
            path="/purchase/purchaseOrder/create",
            body=body,
            response_model=PurchaseOrderResponse,
            safe_to_retry=False,
        )

    async def get_purchase_order(self, *, purchase_order_code: str) -> PurchaseOrderResponse:
        return await self._transport.request(
            path="/purchase/purchaseOrder/getPurchaseOrderDetails",
            body={"purchaseOrderCode": purchase_order_code},
            response_model=PurchaseOrderResponse,
            safe_to_retry=True,
        )

    async def create_grn(self, *, purchase_order_code: str) -> GrnResponse:
        return await self._transport.request(
            path="/purchase/inflowReceipt/create",
            body={"purchaseOrderCode": purchase_order_code},
            response_model=GrnResponse,
            safe_to_retry=False,
        )

    async def get_grn(self, *, inflow_receipt_code: str) -> GrnResponse:
        return await self._transport.request(
            path="/purchase/inflowReceipt/getInflowReceipt",
            body={"inflowReceiptCode": inflow_receipt_code},
            response_model=GrnResponse,
            dto_key="inflowReceipt",
            safe_to_retry=True,
        )

    async def add_item_to_grn(
        self,
        *,
        inflow_receipt_code: str,
        inflow_receipt_item: dict,
    ) -> GrnResponse:
        return await self._transport.request(
            path="/purchase/inflowReceipt/addItemSKU",
            body={
                "inflowReceiptCode": inflow_receipt_code,
                "inflowReceiptItem": inflow_receipt_item,
            },
            response_model=GrnResponse,
            safe_to_retry=False,
        )


class Inbound(BaseResource):
    def create_vendor(self, *, vendor: dict) -> VendorResponse:
        return self._transport.request(
            path="/purchase/vendor/create",
            body={"vendor": vendor},
            response_model=VendorResponse,
            safe_to_retry=False,
        )

    def create_purchase_order(
        self,
        *,
        vendor_code: str,
        purchase_order_items: list[dict] | None = None,
        **kwargs,
    ) -> PurchaseOrderResponse:
        body: dict = {"vendorCode": vendor_code, **kwargs}
        if purchase_order_items is not None:
            body["purchaseOrderItems"] = purchase_order_items
        return self._transport.request(
            path="/purchase/purchaseOrder/create",
            body=body,
            response_model=PurchaseOrderResponse,
            safe_to_retry=False,
        )

    def get_purchase_order(self, *, purchase_order_code: str) -> PurchaseOrderResponse:
        return self._transport.request(
            path="/purchase/purchaseOrder/getPurchaseOrderDetails",
            body={"purchaseOrderCode": purchase_order_code},
            response_model=PurchaseOrderResponse,
            safe_to_retry=True,
        )

    def create_grn(self, *, purchase_order_code: str) -> GrnResponse:
        return self._transport.request(
            path="/purchase/inflowReceipt/create",
            body={"purchaseOrderCode": purchase_order_code},
            response_model=GrnResponse,
            safe_to_retry=False,
        )

    def get_grn(self, *, inflow_receipt_code: str) -> GrnResponse:
        return self._transport.request(
            path="/purchase/inflowReceipt/getInflowReceipt",
            body={"inflowReceiptCode": inflow_receipt_code},
            response_model=GrnResponse,
            dto_key="inflowReceipt",
            safe_to_retry=True,
        )

    def add_item_to_grn(
        self,
        *,
        inflow_receipt_code: str,
        inflow_receipt_item: dict,
    ) -> GrnResponse:
        return self._transport.request(
            path="/purchase/inflowReceipt/addItemSKU",
            body={
                "inflowReceiptCode": inflow_receipt_code,
                "inflowReceiptItem": inflow_receipt_item,
            },
            response_model=GrnResponse,
            safe_to_retry=False,
        )
