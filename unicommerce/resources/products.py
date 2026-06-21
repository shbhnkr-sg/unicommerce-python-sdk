from unicommerce.resources.base import BaseResource, AsyncBaseResource
from unicommerce.models.products import (
    CreateProductRequest,
    ProductResponse,
    ProductSearchResponse,
)


class AsyncProducts(AsyncBaseResource):
    async def create(self, product: CreateProductRequest, *, facility: str | None = None) -> ProductResponse:
        return await self._transport.request(
            path="/catalog/itemType/create",
            body=product,
            response_model=ProductResponse,
            facility=facility,
            safe_to_retry=False,
        )

    async def get(self, sku_code: str) -> ProductResponse:
        return await self._transport.request(
            path="/catalog/itemType/get",
            body={"skuCode": sku_code},
            response_model=ProductResponse,
            safe_to_retry=True,
        )

    async def update(self, product: dict) -> ProductResponse:
        return await self._transport.request(
            path="/catalog/itemType/update",
            body=product,
            response_model=ProductResponse,
            safe_to_retry=False,
        )

    async def search(self, **filters) -> ProductSearchResponse:
        return await self._transport.request(
            path="/catalog/itemType/search",
            body=filters,
            response_model=ProductSearchResponse,
            safe_to_retry=True,
        )


class Products(BaseResource):
    def create(self, product: CreateProductRequest, *, facility: str | None = None) -> ProductResponse:
        return self._transport.request(
            path="/catalog/itemType/create",
            body=product,
            response_model=ProductResponse,
            facility=facility,
            safe_to_retry=False,
        )

    def get(self, sku_code: str) -> ProductResponse:
        return self._transport.request(
            path="/catalog/itemType/get",
            body={"skuCode": sku_code},
            response_model=ProductResponse,
            safe_to_retry=True,
        )

    def update(self, product: dict) -> ProductResponse:
        return self._transport.request(
            path="/catalog/itemType/update",
            body=product,
            response_model=ProductResponse,
            safe_to_retry=False,
        )

    def search(self, **filters) -> ProductSearchResponse:
        return self._transport.request(
            path="/catalog/itemType/search",
            body=filters,
            response_model=ProductSearchResponse,
            safe_to_retry=True,
        )
