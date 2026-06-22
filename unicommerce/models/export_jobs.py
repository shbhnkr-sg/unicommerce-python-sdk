from pydantic import Field

from unicommerce.models.base import UnicommerceRequest, UnicommerceResponse


class ExportFilter(UnicommerceRequest):
    id: int = Field(alias="id")
    text: str | None = Field(None, alias="text")
    selected_values: list[str] | None = Field(None, alias="selectedValues")
    selected_value: str | None = Field(None, alias="selectedValue")
    date_time: str | None = Field(None, alias="dateTime")
    date_range: dict | None = Field(None, alias="dateRange")
    checked: bool | None = Field(None, alias="checked")


class CreateExportJobRequest(UnicommerceRequest):
    export_job_type_name: str = Field(alias="exportJobTypeName")
    export_columns: list[str] = Field(alias="exportColums")
    export_filters: list[ExportFilter] | None = Field(None, alias="exportFilters")
    schedule_time: str | None = Field(None, alias="scheduleTime")
    notification_email: str | None = Field(None, alias="notificationEmail")
    frequency: str = Field("ONETIME", alias="frequency")
    cron_expression: str | None = Field(None, alias="cronExpression")
    report_name: str | None = Field(None, alias="reportName")


class CreateExportJobResponse(UnicommerceResponse):
    export_job_id: str | None = Field(None, alias="exportJobId")
    job_code: str | None = Field(None, alias="jobCode")


class ExportJobStatusResponse(UnicommerceResponse):
    status: str | None = Field(None, alias="status")
    file_path: str | None = Field(None, alias="filePath")
