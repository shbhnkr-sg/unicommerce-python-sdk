from unicommerce.models.export_jobs import (
    CreateExportJobRequest,
    CreateExportJobResponse,
    ExportJobStatusResponse,
)
from unicommerce.resources.base import AsyncBaseResource, BaseResource


class AsyncExportJobs(AsyncBaseResource):
    async def create(
        self,
        *,
        export_job_type_name: str,
        export_columns: list[str],
        export_filters: list[dict] | None = None,
        frequency: str = "ONETIME",
        notification_email: str | None = None,
        schedule_time: str | None = None,
        cron_expression: str | None = None,
        report_name: str | None = None,
    ) -> CreateExportJobResponse:
        body: dict = {
            "exportJobTypeName": export_job_type_name,
            "exportColums": export_columns,
            "frequency": frequency,
        }
        if export_filters is not None:
            body["exportFilters"] = export_filters
        if notification_email is not None:
            body["notificationEmail"] = notification_email
        if schedule_time is not None:
            body["scheduleTime"] = schedule_time
        if cron_expression is not None:
            body["cronExpression"] = cron_expression
        if report_name is not None:
            body["reportName"] = report_name
        return await self._transport.request(
            path="/export/job/create",
            body=body,
            response_model=CreateExportJobResponse,
            safe_to_retry=False,
        )

    async def get_status(self, *, job_code: str) -> ExportJobStatusResponse:
        return await self._transport.request(
            path="/export/job/status",
            body={"jobCode": job_code},
            response_model=ExportJobStatusResponse,
            safe_to_retry=True,
        )


class ExportJobs(BaseResource):
    def create(
        self,
        *,
        export_job_type_name: str,
        export_columns: list[str],
        export_filters: list[dict] | None = None,
        frequency: str = "ONETIME",
        notification_email: str | None = None,
        schedule_time: str | None = None,
        cron_expression: str | None = None,
        report_name: str | None = None,
    ) -> CreateExportJobResponse:
        body: dict = {
            "exportJobTypeName": export_job_type_name,
            "exportColums": export_columns,
            "frequency": frequency,
        }
        if export_filters is not None:
            body["exportFilters"] = export_filters
        if notification_email is not None:
            body["notificationEmail"] = notification_email
        if schedule_time is not None:
            body["scheduleTime"] = schedule_time
        if cron_expression is not None:
            body["cronExpression"] = cron_expression
        if report_name is not None:
            body["reportName"] = report_name
        return self._transport.request(
            path="/export/job/create",
            body=body,
            response_model=CreateExportJobResponse,
            safe_to_retry=False,
        )

    def get_status(self, *, job_code: str) -> ExportJobStatusResponse:
        return self._transport.request(
            path="/export/job/status",
            body={"jobCode": job_code},
            response_model=ExportJobStatusResponse,
            safe_to_retry=True,
        )
