from pydantic import Field

from unicommerce.models.base import UnicommerceResponse


class ReturnOrderSummary(UnicommerceResponse):
    code: str | None = Field(None, alias="code")
    created: int | str | None = Field(None, alias="created")
    updated: int | str | None = Field(None, alias="updated")


class ReturnSearchResponse(UnicommerceResponse):
    return_type: str | None = Field(None, alias="returnType")
    return_orders: list[ReturnOrderSummary] | None = Field(None, alias="returnOrders")


class ReturnGetResponse(UnicommerceResponse):
    return_sale_order_items: list[dict] | None = Field(None, alias="returnSaleOrderItems")
    return_address_details_list: list[dict] | None = Field(None, alias="returnAddressDetailsList")
    return_sale_order_value: dict | None = Field(None, alias="returnSaleOrderValue")


class ReversePickupResponse(UnicommerceResponse):
    reverse_pickup_code: str | None = Field(None, alias="reversePickupCode")
    sale_order_item_codes: list[str] | None = Field(None, alias="saleOrderItemCodes")


class AllocateCourierResponse(UnicommerceResponse):
    assigned_rvp: list[dict] | None = Field(None, alias="assignedRVP")
    already_assigned_rvp: list[dict] | None = Field(None, alias="alreadyAssignedRVP")
    manual_rvps: list[dict] | None = Field(None, alias="manualRVPS")
    erroneous_rvp: list[dict] | None = Field(None, alias="errorneousRVP")
