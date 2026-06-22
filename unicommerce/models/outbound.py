from pydantic import Field

from unicommerce.models.base import UnicommerceResponse


class GatepassScanResponse(UnicommerceResponse):
    scanned_item: dict | None = Field(None, alias="scannedItem")


class GatepassCreateResponse(UnicommerceResponse):
    gate_pass_code: str | None = Field(None, alias="gatePassCode")


class GatepassSearchResponse(UnicommerceResponse):
    total_records: int | None = Field(None, alias="totalRecords")
    elements: list[dict] | None = Field(None, alias="elements")


class GatepassGetResponse(UnicommerceResponse):
    elements: list[dict] | None = Field(None, alias="elements")
    gate_pass_item_dtos: list[dict] | None = Field(None, alias="gatePassItemDTOs")
