from unicommerce.resources.base import BaseResource, AsyncBaseResource
from unicommerce.models.returns import (
    ReturnResponse,
    CreateReversePickupRequest,
    ReversePickupResponse,
)


class AsyncReturns(AsyncBaseResource):
    async def get_return(self, code: str) -> ReturnResponse:
        return await self._transport.request(
            path="/oms/return/get",
            body={"code": code},
            response_model=ReturnResponse,
            safe_to_retry=True,
        )

    async def create_reverse_pickup(self, request: CreateReversePickupRequest) -> ReversePickupResponse:
        return await self._transport.request(
            path="/oms/return/createReversePickup",
            body=request,
            response_model=ReversePickupResponse,
            safe_to_retry=False,
        )

    async def mark_returned(self, code: str) -> ReturnResponse:
        return await self._transport.request(
            path="/oms/return/markReturned",
            body={"code": code},
            response_model=ReturnResponse,
            safe_to_retry=False,
        )

    async def create_alternate_item(self, return_code: str, alternate_sku: str) -> ReturnResponse:
        return await self._transport.request(
            path="/oms/return/createAlternateItem",
            body={"returnCode": return_code, "alternateSku": alternate_sku},
            response_model=ReturnResponse,
            safe_to_retry=False,
        )


class Returns(BaseResource):
    def get_return(self, code: str) -> ReturnResponse:
        return self._transport.request(
            path="/oms/return/get",
            body={"code": code},
            response_model=ReturnResponse,
            safe_to_retry=True,
        )

    def create_reverse_pickup(self, request: CreateReversePickupRequest) -> ReversePickupResponse:
        return self._transport.request(
            path="/oms/return/createReversePickup",
            body=request,
            response_model=ReversePickupResponse,
            safe_to_retry=False,
        )

    def mark_returned(self, code: str) -> ReturnResponse:
        return self._transport.request(
            path="/oms/return/markReturned",
            body={"code": code},
            response_model=ReturnResponse,
            safe_to_retry=False,
        )

    def create_alternate_item(self, return_code: str, alternate_sku: str) -> ReturnResponse:
        return self._transport.request(
            path="/oms/return/createAlternateItem",
            body={"returnCode": return_code, "alternateSku": alternate_sku},
            response_model=ReturnResponse,
            safe_to_retry=False,
        )
