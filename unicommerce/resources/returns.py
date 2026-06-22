from unicommerce.models.returns import (
    ReturnGetResponse,
    ReturnSearchResponse,
    ReversePickupResponse,
)
from unicommerce.resources.base import AsyncBaseResource, BaseResource


class AsyncReturns(AsyncBaseResource):
    async def search(
        self,
        *,
        return_type: str,
        updated_from: str | None = None,
        updated_to: str | None = None,
        created_from: str | None = None,
        created_to: str | None = None,
        status_code: str | None = None,
    ) -> ReturnSearchResponse:
        body: dict = {"returnType": return_type}
        if updated_from is not None:
            body["updatedFrom"] = updated_from
        if updated_to is not None:
            body["updatedTo"] = updated_to
        if created_from is not None:
            body["createdFrom"] = created_from
        if created_to is not None:
            body["createdTo"] = created_to
        if status_code is not None:
            body["statusCode"] = status_code
        return await self._transport.request(
            path="/oms/return/search",
            body=body,
            response_model=ReturnSearchResponse,
            safe_to_retry=True,
        )

    async def get(
        self,
        *,
        shipment_code: str | None = None,
        reverse_pickup_code: str | None = None,
    ) -> ReturnGetResponse:
        body: dict = {}
        if shipment_code is not None:
            body["shipmentCode"] = shipment_code
        if reverse_pickup_code is not None:
            body["reversePickupCode"] = reverse_pickup_code
        return await self._transport.request(
            path="/oms/return/get",
            body=body,
            response_model=ReturnGetResponse,
            safe_to_retry=True,
        )

    async def create_reverse_pickup(
        self,
        *,
        sale_order_code: str,
        reverse_pick_items: list[dict],
        action_code: str = "WAC",
        **kwargs,
    ) -> ReversePickupResponse:
        body: dict = {
            "saleOrderCode": sale_order_code,
            "reversePickItems": reverse_pick_items,
            "actionCode": action_code,
            **kwargs,
        }
        return await self._transport.request(
            path="/oms/reversePickup/create",
            body=body,
            response_model=ReversePickupResponse,
            safe_to_retry=False,
        )

    async def mark_returned(
        self,
        *,
        sale_order_code: str,
        sale_order_items: list[dict],
        return_reason: str,
        **kwargs,
    ) -> None:
        body: dict = {
            "saleOrderCode": sale_order_code,
            "saleOrderItems": sale_order_items,
            "returnReason": return_reason,
            **kwargs,
        }
        return await self._transport.request(
            path="/saleOrder/markReturned",
            body=body,
            response_model=None,
            safe_to_retry=False,
        )


class Returns(BaseResource):
    def search(
        self,
        *,
        return_type: str,
        updated_from: str | None = None,
        updated_to: str | None = None,
        created_from: str | None = None,
        created_to: str | None = None,
        status_code: str | None = None,
    ) -> ReturnSearchResponse:
        body: dict = {"returnType": return_type}
        if updated_from is not None:
            body["updatedFrom"] = updated_from
        if updated_to is not None:
            body["updatedTo"] = updated_to
        if created_from is not None:
            body["createdFrom"] = created_from
        if created_to is not None:
            body["createdTo"] = created_to
        if status_code is not None:
            body["statusCode"] = status_code
        return self._transport.request(
            path="/oms/return/search",
            body=body,
            response_model=ReturnSearchResponse,
            safe_to_retry=True,
        )

    def get(
        self,
        *,
        shipment_code: str | None = None,
        reverse_pickup_code: str | None = None,
    ) -> ReturnGetResponse:
        body: dict = {}
        if shipment_code is not None:
            body["shipmentCode"] = shipment_code
        if reverse_pickup_code is not None:
            body["reversePickupCode"] = reverse_pickup_code
        return self._transport.request(
            path="/oms/return/get",
            body=body,
            response_model=ReturnGetResponse,
            safe_to_retry=True,
        )

    def create_reverse_pickup(
        self,
        *,
        sale_order_code: str,
        reverse_pick_items: list[dict],
        action_code: str = "WAC",
        **kwargs,
    ) -> ReversePickupResponse:
        body: dict = {
            "saleOrderCode": sale_order_code,
            "reversePickItems": reverse_pick_items,
            "actionCode": action_code,
            **kwargs,
        }
        return self._transport.request(
            path="/oms/reversePickup/create",
            body=body,
            response_model=ReversePickupResponse,
            safe_to_retry=False,
        )

    def mark_returned(
        self,
        *,
        sale_order_code: str,
        sale_order_items: list[dict],
        return_reason: str,
        **kwargs,
    ) -> None:
        body: dict = {
            "saleOrderCode": sale_order_code,
            "saleOrderItems": sale_order_items,
            "returnReason": return_reason,
            **kwargs,
        }
        return self._transport.request(
            path="/saleOrder/markReturned",
            body=body,
            response_model=None,
            safe_to_retry=False,
        )
