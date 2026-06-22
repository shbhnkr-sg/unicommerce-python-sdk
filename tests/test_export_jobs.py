import time

import pytest


@pytest.fixture(scope="module")
def export_job(client):
    """Create a single export job shared across all tests in this module."""
    result = client.export_jobs.create(
        export_job_type_name="Inventory Snapshot",
        export_columns=["inventory"],
        frequency="ONETIME",
    )
    return result


def test_create_returns_job_code(export_job):
    assert export_job.job_code is not None
    assert len(export_job.job_code) > 0


def test_create_returns_export_job_id(export_job):
    assert export_job.export_job_id is not None
    assert len(export_job.export_job_id) > 0


def test_get_status(client, export_job):
    status = client.export_jobs.get_status(job_code=export_job.job_code)
    assert status.status is not None
    assert status.status in ("SCHEDULED", "RUNNING", "IN_PROGRESS", "COMPLETE", "SUCCESSFUL", "FAILED")


def test_completed_export_has_csv_link(client, export_job):
    for _ in range(10):
        status = client.export_jobs.get_status(job_code=export_job.job_code)
        if status.status in ("COMPLETE", "SUCCESSFUL"):
            break
        time.sleep(2)

    assert status.status in ("COMPLETE", "SUCCESSFUL")
    assert status.file_path is not None
    assert status.file_path.endswith(".csv")
