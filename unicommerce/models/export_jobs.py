from pydantic import Field

from unicommerce.models.base import UnicommerceRequest, UnicommerceResponse


class CreateExportJobRequest(UnicommerceRequest):
    export_job_type: str = Field(alias="exportJobType")
    filters: dict = Field(default_factory=dict, alias="filters")


class ExportJobResponse(UnicommerceResponse):
    code: str = Field("", alias="code")
    status: str = Field("", alias="status")
    download_url: str = Field("", alias="downloadUrl")
    created_date: str = Field("", alias="createdDate")
