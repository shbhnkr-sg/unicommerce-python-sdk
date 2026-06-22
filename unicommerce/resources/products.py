from unicommerce.models.products import (
    CategoryResponse,
    ChannelItemTypeResponse,
    CreateOrEditItemResponse,
    ProductResponse,
    ProductSearchResponse,
)
from unicommerce.resources.base import AsyncBaseResource, BaseResource


class AsyncProducts(AsyncBaseResource):
    async def get(self, *, sku_code: str) -> ProductResponse:
        return await self._transport.request(
            path="/catalog/itemType/get",
            body={"skuCode": sku_code},
            response_model=ProductResponse,
            dto_key="itemTypeDTO",
            safe_to_retry=True,
        )

    async def get_by_item_code(self, *, item_code: str) -> ProductResponse:
        return await self._transport.request(
            path="/product/item/get",
            body={"itemCode": item_code},
            response_model=ProductResponse,
            dto_key="itemTypeDTO",
            safe_to_retry=True,
        )

    async def search(self, **filters) -> ProductSearchResponse:
        return await self._transport.request(
            path="/product/itemType/search",
            body=filters,
            response_model=ProductSearchResponse,
            safe_to_retry=True,
        )

    async def create_or_edit(self, *, item_type: dict) -> CreateOrEditItemResponse:
        return await self._transport.request(
            path="/catalog/itemType/createOrEdit",
            body={"itemType": item_type},
            response_model=CreateOrEditItemResponse,
            safe_to_retry=False,
        )

    async def create_or_edit_bulk(self, *, item_types: list[dict]) -> CreateOrEditItemResponse:
        return await self._transport.request(
            path="/catalog/itemTypes/createOrEdit",
            body={"itemTypes": item_types},
            response_model=CreateOrEditItemResponse,
            safe_to_retry=False,
        )

    async def create_or_edit_category(self, *, category: dict) -> CategoryResponse:
        return await self._transport.request(
            path="/product/category/addOrEdit",
            body={"category": category},
            response_model=CategoryResponse,
            safe_to_retry=False,
        )

    async def create_channel_item_type(self, **kwargs) -> ChannelItemTypeResponse:
        return await self._transport.request(
            path="/channel/createChannelItemType",
            body=kwargs,
            response_model=ChannelItemTypeResponse,
            safe_to_retry=False,
        )


class Products(BaseResource):
    def get(self, *, sku_code: str) -> ProductResponse:
        return self._transport.request(
            path="/catalog/itemType/get",
            body={"skuCode": sku_code},
            response_model=ProductResponse,
            dto_key="itemTypeDTO",
            safe_to_retry=True,
        )

    def get_by_item_code(self, *, item_code: str) -> ProductResponse:
        return self._transport.request(
            path="/product/item/get",
            body={"itemCode": item_code},
            response_model=ProductResponse,
            dto_key="itemTypeDTO",
            safe_to_retry=True,
        )

    def search(self, **filters) -> ProductSearchResponse:
        return self._transport.request(
            path="/product/itemType/search",
            body=filters,
            response_model=ProductSearchResponse,
            safe_to_retry=True,
        )

    def create_or_edit(self, *, item_type: dict) -> CreateOrEditItemResponse:
        return self._transport.request(
            path="/catalog/itemType/createOrEdit",
            body={"itemType": item_type},
            response_model=CreateOrEditItemResponse,
            safe_to_retry=False,
        )

    def create_or_edit_bulk(self, *, item_types: list[dict]) -> CreateOrEditItemResponse:
        return self._transport.request(
            path="/catalog/itemTypes/createOrEdit",
            body={"itemTypes": item_types},
            response_model=CreateOrEditItemResponse,
            safe_to_retry=False,
        )

    def create_or_edit_category(self, *, category: dict) -> CategoryResponse:
        return self._transport.request(
            path="/product/category/addOrEdit",
            body={"category": category},
            response_model=CategoryResponse,
            safe_to_retry=False,
        )

    def create_channel_item_type(self, **kwargs) -> ChannelItemTypeResponse:
        return self._transport.request(
            path="/channel/createChannelItemType",
            body=kwargs,
            response_model=ChannelItemTypeResponse,
            safe_to_retry=False,
        )
