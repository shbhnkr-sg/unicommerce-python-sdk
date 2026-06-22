from unicommerce.models.products import ProductResponse
from unicommerce.resources.base import AsyncBaseResource, BaseResource


class AsyncProducts(AsyncBaseResource):
    async def get(self, sku_code: str) -> ProductResponse:
        return await self._transport.request(
            path="/catalog/itemType/get",
            body={"skuCode": sku_code},
            response_model=ProductResponse,
            dto_key="itemTypeDTO",
            safe_to_retry=True,
        )


class Products(BaseResource):
    def get(self, sku_code: str) -> ProductResponse:
        return self._transport.request(
            path="/catalog/itemType/get",
            body={"skuCode": sku_code},
            response_model=ProductResponse,
            dto_key="itemTypeDTO",
            safe_to_retry=True,
        )
