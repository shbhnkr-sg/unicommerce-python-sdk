from unicommerce.resources.base import BaseResource, AsyncBaseResource
from unicommerce.models.export_jobs import (
    CreateExportJobRequest,
    ExportJobResponse,
)


class AsyncExportJobs(AsyncBaseResource):
    async def create(self, request: CreateExportJobRequest) -> ExportJobResponse:
        return await self._transport.request(
            path="/exportJob/create",
            body=request,
            response_model=ExportJobResponse,
            safe_to_retry=False,
        )

    async def get_status(self, code: str) -> ExportJobResponse:
        return await self._transport.request(
            path="/exportJob/get",
            body={"code": code},
            response_model=ExportJobResponse,
            safe_to_retry=True,
        )


class ExportJobs(BaseResource):
    def create(self, request: CreateExportJobRequest) -> ExportJobResponse:
        return self._transport.request(
            path="/exportJob/create",
            body=request,
            response_model=ExportJobResponse,
            safe_to_retry=False,
        )

    def get_status(self, code: str) -> ExportJobResponse:
        return self._transport.request(
            path="/exportJob/get",
            body={"code": code},
            response_model=ExportJobResponse,
            safe_to_retry=True,
        )
