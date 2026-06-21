from pydantic import Field

from unicommerce.models.base import UnicommerceResponse


class FacilityResponse(UnicommerceResponse):
    code: str = Field("", alias="code")
    name: str = Field("", alias="name")
    city: str = Field("", alias="city")
    state: str = Field("", alias="state")
    country: str = Field("", alias="country")
    enabled: bool = Field(True, alias="enabled")


class FacilitySearchResponse(UnicommerceResponse):
    facilities: list[FacilityResponse] = Field(default_factory=list, alias="elements")
