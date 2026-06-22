def test_get_facility(client):
    facility = client.facilities.get_details(facility_code="YOUR_TENANT")
    assert facility.code == "YOUR_TENANT"
    assert facility.name is not None
    assert facility.enabled is True


def test_facility_has_gst(client):
    facility = client.facilities.get_details(facility_code="YOUR_TENANT")
    assert facility.gst_number is not None
    assert len(facility.gst_number) > 0
