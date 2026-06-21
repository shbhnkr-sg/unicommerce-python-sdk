from pydantic import Field

from unicommerce.models.base import UnicommerceRequest, UnicommerceResponse


class CreateProductRequest(UnicommerceRequest):
    item_type: dict = Field(alias="itemType")


class ProductResponse(UnicommerceResponse):
    sku_code: str = Field("", alias="skuCode")
    name: str = Field("", alias="name")
    category_code: str = Field("", alias="categoryCode")
    item_type_code: str = Field("", alias="itemTypeCode")
    description: str = Field("", alias="description")
    max_retail_price: float = Field(0, alias="maxRetailPrice")
    enabled: bool = Field(True, alias="enabled")


class ProductSearchResponse(UnicommerceResponse):
    products: list[ProductResponse] = Field(default_factory=list, alias="elements")
    total_count: int = Field(0, alias="totalCount")
