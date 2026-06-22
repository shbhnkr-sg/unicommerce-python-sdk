from pydantic import Field

from unicommerce.models.base import UnicommerceResponse


class FacilityResponse(UnicommerceResponse):
    type: str | None = Field(None, alias="type")
    display_name: str | None = Field(None, alias="displayName")
    operational_type: str | None = Field(None, alias="operationalType")
    name: str | None = Field(None, alias="name")
    code: str | None = Field(None, alias="code")
    alternate_code: str | None = Field(None, alias="alternateCode")
    pan: str | None = Field(None, alias="pan")
    gst_number: str | None = Field(None, alias="gstNumber")
    enabled: bool | None = Field(None, alias="enabled")
    tax_exempted: bool | None = Field(None, alias="taxExempted")
    website: str | None = Field(None, alias="website")
    billing_address: dict | None = Field(None, alias="billingAddress")
    shipping_address: dict | None = Field(None, alias="shippingAddress")


class FacilitySearchResponse(UnicommerceResponse):
    parties: list[FacilityResponse] | None = Field(None, alias="parties")
