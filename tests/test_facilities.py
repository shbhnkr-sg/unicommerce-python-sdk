import os

TENANT = os.environ["UNICOMMERCE_TENANT"]


def test_get_facility(client):
    facility = client.facilities.get_details(facility_code=TENANT)
    assert facility.code == TENANT
    assert facility.name is not None
    assert facility.enabled is True


def test_facility_has_gst(client):
    facility = client.facilities.get_details(facility_code=TENANT)
    assert facility.gst_number is not None
    assert len(facility.gst_number) > 0
