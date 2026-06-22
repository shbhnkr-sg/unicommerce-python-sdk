from unicommerce.models.base import UnicommerceResponse
from unicommerce.models.inbound import (
    GrnResponse,
    GrnSearchResponse,
    PurchaseOrderCreateResponse,
    PurchaseOrderResponse,
    PurchaseOrderSearchResponse,
    VendorBackorderResponse,
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

    async def create_or_edit_vendor_catalog(
        self, *, vendor_item_type: dict
    ) -> UnicommerceResponse:
        return await self._transport.request(
            path="/purchase/vendorItemType/createOrEdit",
            body={"vendorItemType": vendor_item_type},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def get_vendor_backorder_items(self, **filters) -> VendorBackorderResponse:
        return await self._transport.request(
            path="/purchase/getVendorBackOrderItems",
            body=filters,
            response_model=VendorBackorderResponse,
            safe_to_retry=True,
        )

    async def search_purchase_orders(self, **filters) -> PurchaseOrderSearchResponse:
        return await self._transport.request(
            path="/purchase/purchaseOrder/getPurchaseOrders",
            body=filters,
            response_model=PurchaseOrderSearchResponse,
            safe_to_retry=True,
        )

    async def approve_purchase_order(
        self, *, purchase_order_code: str
    ) -> UnicommerceResponse:
        return await self._transport.request(
            path="/purchase/purchaseOrder/approve",
            body={"purchaseOrderCode": purchase_order_code},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def create_and_approve_purchase_order(
        self,
        *,
        vendor_code: str,
        user_id: str,
        purchase_order_items: list[dict],
        **kwargs,
    ) -> PurchaseOrderCreateResponse:
        return await self._transport.request(
            path="/purchase/purchaseOrder/createApproved",
            body={
                "vendorCode": vendor_code,
                "userId": user_id,
                "purchaseOrderItems": purchase_order_items,
                **kwargs,
            },
            response_model=PurchaseOrderCreateResponse,
            safe_to_retry=False,
        )

    async def close_purchase_order(
        self, *, purchase_order_code: str
    ) -> UnicommerceResponse:
        return await self._transport.request(
            path="/purchase/purchaseOrder/close",
            body={"purchaseOrderCode": purchase_order_code},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def add_item_to_grn_by_code(
        self,
        *,
        inflow_receipt_code: str,
        item_code: str,
        manufacturing_date: str | None = None,
    ) -> UnicommerceResponse:
        body: dict = {
            "inflowReceiptCode": inflow_receipt_code,
            "itemCode": item_code,
        }
        if manufacturing_date is not None:
            body["manufacturingDate"] = manufacturing_date
        return await self._transport.request(
            path="/purchase/inflowReceipt/addItem",
            body=body,
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def search_grns(self, **filters) -> GrnSearchResponse:
        return await self._transport.request(
            path="/purchase/inflowReceipt/getInflowReceipts",
            body=filters,
            response_model=GrnSearchResponse,
            safe_to_retry=True,
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

    def create_or_edit_vendor_catalog(
        self, *, vendor_item_type: dict
    ) -> UnicommerceResponse:
        return self._transport.request(
            path="/purchase/vendorItemType/createOrEdit",
            body={"vendorItemType": vendor_item_type},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def get_vendor_backorder_items(self, **filters) -> VendorBackorderResponse:
        return self._transport.request(
            path="/purchase/getVendorBackOrderItems",
            body=filters,
            response_model=VendorBackorderResponse,
            safe_to_retry=True,
        )

    def search_purchase_orders(self, **filters) -> PurchaseOrderSearchResponse:
        return self._transport.request(
            path="/purchase/purchaseOrder/getPurchaseOrders",
            body=filters,
            response_model=PurchaseOrderSearchResponse,
            safe_to_retry=True,
        )

    def approve_purchase_order(
        self, *, purchase_order_code: str
    ) -> UnicommerceResponse:
        return self._transport.request(
            path="/purchase/purchaseOrder/approve",
            body={"purchaseOrderCode": purchase_order_code},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def create_and_approve_purchase_order(
        self,
        *,
        vendor_code: str,
        user_id: str,
        purchase_order_items: list[dict],
        **kwargs,
    ) -> PurchaseOrderCreateResponse:
        return self._transport.request(
            path="/purchase/purchaseOrder/createApproved",
            body={
                "vendorCode": vendor_code,
                "userId": user_id,
                "purchaseOrderItems": purchase_order_items,
                **kwargs,
            },
            response_model=PurchaseOrderCreateResponse,
            safe_to_retry=False,
        )

    def close_purchase_order(
        self, *, purchase_order_code: str
    ) -> UnicommerceResponse:
        return self._transport.request(
            path="/purchase/purchaseOrder/close",
            body={"purchaseOrderCode": purchase_order_code},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def add_item_to_grn_by_code(
        self,
        *,
        inflow_receipt_code: str,
        item_code: str,
        manufacturing_date: str | None = None,
    ) -> UnicommerceResponse:
        body: dict = {
            "inflowReceiptCode": inflow_receipt_code,
            "itemCode": item_code,
        }
        if manufacturing_date is not None:
            body["manufacturingDate"] = manufacturing_date
        return self._transport.request(
            path="/purchase/inflowReceipt/addItem",
            body=body,
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def search_grns(self, **filters) -> GrnSearchResponse:
        return self._transport.request(
            path="/purchase/inflowReceipt/getInflowReceipts",
            body=filters,
            response_model=GrnSearchResponse,
            safe_to_retry=True,
        )
