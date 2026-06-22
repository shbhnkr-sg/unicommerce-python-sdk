from pydantic import Field

from unicommerce.models.base import UnicommerceResponse


class ProductResponse(UnicommerceResponse):
    id: int | None = Field(None, alias="id")
    sku_code: str | None = Field(None, alias="skuCode")
    category_code: str | None = Field(None, alias="categoryCode")
    name: str | None = Field(None, alias="name")
    description: str | None = Field(None, alias="description")
    scan_identifier: str | None = Field(None, alias="scanIdentifier")
    length: int | None = Field(None, alias="length")
    width: int | None = Field(None, alias="width")
    height: int | None = Field(None, alias="height")
    weight: float | None = Field(None, alias="weight")
    color: str | None = Field(None, alias="color")
    size: str | None = Field(None, alias="size")
    brand: str | None = Field(None, alias="brand")
    ean: str | None = Field(None, alias="ean")
    upc: str | None = Field(None, alias="upc")
    isbn: str | None = Field(None, alias="isbn")
    hsn_code: str | None = Field(None, alias="hsnCode")
    max_retail_price: float | None = Field(None, alias="maxRetailPrice")
    base_price: float | None = Field(None, alias="basePrice")
    cost_price: float | None = Field(None, alias="costPrice")
    type: str | None = Field(None, alias="type")
    enabled: bool | None = Field(None, alias="enabled")
    min_order_size: int | None = Field(None, alias="minOrderSize")
    sku_type: str | None = Field(None, alias="skuType")
    fragile: bool | None = Field(None, alias="fragile")
    dangerous_good: bool | None = Field(None, alias="dangerousGood")
    tags: list | None = Field(None, alias="tags")
