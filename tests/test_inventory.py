def test_get_snapshot(client):
    snapshot = client.inventory.get_snapshot(updated_since_in_minutes=1440)
    assert snapshot.inventory_snapshots is not None
    assert len(snapshot.inventory_snapshots) > 0


def test_snapshot_item_fields(client):
    snapshot = client.inventory.get_snapshot(updated_since_in_minutes=1440)
    item = snapshot.inventory_snapshots[0]
    assert item.item_type_sku is not None
    assert item.inventory is not None
    assert isinstance(item.inventory, int)


def test_adjust_noop(client):
    result = client.inventory.adjust(
        item_sku="10001394-3XL",
        quantity=0,
        shelf_code="DEFAULT",
        adjustment_type="ADD",
    )
    assert result is not None
