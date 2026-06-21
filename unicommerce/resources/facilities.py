from unicommerce.resources.base import BaseResource, AsyncBaseResource
from unicommerce.models.facilities import (
    FacilityResponse,
    FacilitySearchResponse,
)


class AsyncFacilities(AsyncBaseResource):
    async def search(self, **filters) -> FacilitySearchResponse:
        return await self._transport.request(
            path="/facility/search",
            body=filters,
            response_model=FacilitySearchResponse,
            safe_to_retry=True,
        )

    async def get_details(self, code: str) -> FacilityResponse:
        return await self._transport.request(
            path="/facility/get",
            body={"code": code},
            response_model=FacilityResponse,
            safe_to_retry=True,
        )


class Facilities(BaseResource):
    def search(self, **filters) -> FacilitySearchResponse:
        return self._transport.request(
            path="/facility/search",
            body=filters,
            response_model=FacilitySearchResponse,
            safe_to_retry=True,
        )

    def get_details(self, code: str) -> FacilityResponse:
        return self._transport.request(
            path="/facility/get",
            body={"code": code},
            response_model=FacilityResponse,
            safe_to_retry=True,
        )
