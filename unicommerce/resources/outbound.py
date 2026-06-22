from unicommerce.models.base import UnicommerceResponse
from unicommerce.models.outbound import (
    GatepassCreateResponse,
    GatepassGetResponse,
    GatepassScanResponse,
    GatepassSearchResponse,
)
from unicommerce.resources.base import AsyncBaseResource, BaseResource


class AsyncOutbound(AsyncBaseResource):
    async def scan_item(
        self, *, gate_pass_code: str, item_code: str
    ) -> GatepassScanResponse:
        return await self._transport.request(
            path="/purchase/gatepass/scan/item",
            body={"gatePassCode": gate_pass_code, "itemCode": item_code},
            response_model=GatepassScanResponse,
            safe_to_retry=False,
        )

    async def create_gatepass(
        self, *, type: str, party_code: str, ws_gate_pass: dict | None = None
    ) -> GatepassCreateResponse:
        body: dict = {"type": type, "partyCode": party_code}
        if ws_gate_pass is not None:
            body["wsGatePass"] = ws_gate_pass
        return await self._transport.request(
            path="/purchase/gatepass/create",
            body=body,
            response_model=GatepassCreateResponse,
            safe_to_retry=False,
        )

    async def complete_gatepass(
        self, *, gate_pass_code: str
    ) -> UnicommerceResponse:
        return await self._transport.request(
            path="/purchase/gatepass/complete",
            body={"gatePassCode": gate_pass_code},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def edit_gatepass(
        self, *, gate_pass_code: str, ws_gate_pass: dict | None = None
    ) -> GatepassCreateResponse:
        body: dict = {"gatePassCode": gate_pass_code}
        if ws_gate_pass is not None:
            body["wsGatePass"] = ws_gate_pass
        return await self._transport.request(
            path="/purchase/gatepass/edit",
            body=body,
            response_model=GatepassCreateResponse,
            safe_to_retry=False,
        )

    async def remove_gatepass_item(
        self, *, gate_pass_code: str, item_code: str
    ) -> UnicommerceResponse:
        return await self._transport.request(
            path="/purchase/gatepass/item/remove",
            body={"gatePassCode": gate_pass_code, "itemCode": item_code},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def add_nontraceable_item(
        self,
        *,
        gate_pass_code: str,
        item_sku: str,
        inventory_type: str,
        quantity: int,
        unit_price: float,
        shelf_code: str,
    ) -> UnicommerceResponse:
        return await self._transport.request(
            path="/purchase/gatepass/nontraceable/addItem",
            body={
                "gatePassCode": gate_pass_code,
                "itemSKU": item_sku,
                "inventoryType": inventory_type,
                "quantity": quantity,
                "unitPrice": unit_price,
                "shelfCode": shelf_code,
            },
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def discard_gatepass(
        self, *, gate_pass_code: str
    ) -> UnicommerceResponse:
        return await self._transport.request(
            path="/purchase/gatepass/discard",
            body={"gatePassCode": gate_pass_code},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    async def search_gatepass(
        self, *, from_date: str, to_date: str, **kwargs
    ) -> GatepassSearchResponse:
        return await self._transport.request(
            path="/purchase/gatepass/search",
            body={"fromDate": from_date, "toDate": to_date, **kwargs},
            response_model=GatepassSearchResponse,
            safe_to_retry=True,
        )

    async def get_gatepass(
        self, *, gate_pass_codes: list[str]
    ) -> GatepassGetResponse:
        return await self._transport.request(
            path="/purchase/gatepass/get",
            body={"gatePassCodes": gate_pass_codes},
            response_model=GatepassGetResponse,
            safe_to_retry=True,
        )


class Outbound(BaseResource):
    def scan_item(
        self, *, gate_pass_code: str, item_code: str
    ) -> GatepassScanResponse:
        return self._transport.request(
            path="/purchase/gatepass/scan/item",
            body={"gatePassCode": gate_pass_code, "itemCode": item_code},
            response_model=GatepassScanResponse,
            safe_to_retry=False,
        )

    def create_gatepass(
        self, *, type: str, party_code: str, ws_gate_pass: dict | None = None
    ) -> GatepassCreateResponse:
        body: dict = {"type": type, "partyCode": party_code}
        if ws_gate_pass is not None:
            body["wsGatePass"] = ws_gate_pass
        return self._transport.request(
            path="/purchase/gatepass/create",
            body=body,
            response_model=GatepassCreateResponse,
            safe_to_retry=False,
        )

    def complete_gatepass(
        self, *, gate_pass_code: str
    ) -> UnicommerceResponse:
        return self._transport.request(
            path="/purchase/gatepass/complete",
            body={"gatePassCode": gate_pass_code},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def edit_gatepass(
        self, *, gate_pass_code: str, ws_gate_pass: dict | None = None
    ) -> GatepassCreateResponse:
        body: dict = {"gatePassCode": gate_pass_code}
        if ws_gate_pass is not None:
            body["wsGatePass"] = ws_gate_pass
        return self._transport.request(
            path="/purchase/gatepass/edit",
            body=body,
            response_model=GatepassCreateResponse,
            safe_to_retry=False,
        )

    def remove_gatepass_item(
        self, *, gate_pass_code: str, item_code: str
    ) -> UnicommerceResponse:
        return self._transport.request(
            path="/purchase/gatepass/item/remove",
            body={"gatePassCode": gate_pass_code, "itemCode": item_code},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def add_nontraceable_item(
        self,
        *,
        gate_pass_code: str,
        item_sku: str,
        inventory_type: str,
        quantity: int,
        unit_price: float,
        shelf_code: str,
    ) -> UnicommerceResponse:
        return self._transport.request(
            path="/purchase/gatepass/nontraceable/addItem",
            body={
                "gatePassCode": gate_pass_code,
                "itemSKU": item_sku,
                "inventoryType": inventory_type,
                "quantity": quantity,
                "unitPrice": unit_price,
                "shelfCode": shelf_code,
            },
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def discard_gatepass(
        self, *, gate_pass_code: str
    ) -> UnicommerceResponse:
        return self._transport.request(
            path="/purchase/gatepass/discard",
            body={"gatePassCode": gate_pass_code},
            response_model=UnicommerceResponse,
            safe_to_retry=False,
        )

    def search_gatepass(
        self, *, from_date: str, to_date: str, **kwargs
    ) -> GatepassSearchResponse:
        return self._transport.request(
            path="/purchase/gatepass/search",
            body={"fromDate": from_date, "toDate": to_date, **kwargs},
            response_model=GatepassSearchResponse,
            safe_to_retry=True,
        )

    def get_gatepass(
        self, *, gate_pass_codes: list[str]
    ) -> GatepassGetResponse:
        return self._transport.request(
            path="/purchase/gatepass/get",
            body={"gatePassCodes": gate_pass_codes},
            response_model=GatepassGetResponse,
            safe_to_retry=True,
        )
