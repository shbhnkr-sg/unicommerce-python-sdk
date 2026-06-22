from unicommerce.models.facilities import (
    FacilityResponse,
    FacilitySearchResponse,
)
from unicommerce.resources.base import AsyncBaseResource, BaseResource


class AsyncFacilities(AsyncBaseResource):
    async def search(
        self,
        *,
        from_date: str,
        to_date: str,
        date_type: str = "CREATED",
        facility_status: str = "ALL",
    ) -> FacilitySearchResponse:
        return await self._transport.request(
            path="/facility/search",
            body={
                "fromDate": from_date,
                "toDate": to_date,
                "dateType": date_type,
                "facilityStatus": facility_status,
            },
            response_model=FacilitySearchResponse,
            safe_to_retry=True,
        )

    async def get_details(self, *, facility_code: str) -> FacilityResponse:
        return await self._transport.request(
            path="/facility/get",
            body={"facilityCode": facility_code},
            response_model=FacilityResponse,
            dto_key="facility",
            safe_to_retry=True,
        )


class Facilities(BaseResource):
    def search(
        self,
        *,
        from_date: str,
        to_date: str,
        date_type: str = "CREATED",
        facility_status: str = "ALL",
    ) -> FacilitySearchResponse:
        return self._transport.request(
            path="/facility/search",
            body={
                "fromDate": from_date,
                "toDate": to_date,
                "dateType": date_type,
                "facilityStatus": facility_status,
            },
            response_model=FacilitySearchResponse,
            safe_to_retry=True,
        )

    def get_details(self, *, facility_code: str) -> FacilityResponse:
        return self._transport.request(
            path="/facility/get",
            body={"facilityCode": facility_code},
            response_model=FacilityResponse,
            dto_key="facility",
            safe_to_retry=True,
        )
