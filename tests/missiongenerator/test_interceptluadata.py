from game.missiongenerator.interceptluadata import (
    InterceptEntry,
    populate_intercept_lua,
)
from game.missiongenerator.luagenerator import LuaData


def _entry(**kw: object) -> InterceptEntry:
    base = dict(
        squadron_id="sq-1",
        squadron_name="12th FS",
        airbase_name="Batumi",
        template_prefix="Intercept|Batumi|sq-1",
        coalition="BLUE",
        resource_count=4,
        engagement_range_nm=60,
        gci_max_radius_nm=100,
        comms_enabled=True,
    )
    base.update(kw)
    return InterceptEntry(**base)  # type: ignore[arg-type]


def test_empty_entries_creates_blue_and_red_buckets() -> None:
    root = LuaData("dcsRetribution")
    populate_intercept_lua(root, [])
    serialized = root.serialize()
    assert "Intercept" in serialized
    assert "BLUE" in serialized
    assert "RED" in serialized


def test_entry_is_grouped_under_its_coalition() -> None:
    root = LuaData("dcsRetribution")
    populate_intercept_lua(root, [_entry(coalition="RED")])

    intercept = root.get_item("Intercept")
    assert isinstance(intercept, LuaData)
    red_bucket = intercept.get_item("RED")
    blue_bucket = intercept.get_item("BLUE")
    assert isinstance(red_bucket, LuaData)
    assert isinstance(blue_bucket, LuaData)

    # Entry must land in the RED bucket, not in BLUE.
    assert len(red_bucket.objects) == 1
    assert len(blue_bucket.objects) == 0

    # Spot-check the record's content via the bucket's own serialization.
    red_serialized = red_bucket.serialize()
    assert "Intercept|Batumi|sq-1" in red_serialized
    assert "12th FS" in red_serialized


def test_resource_count_and_ranges_are_serialized() -> None:
    root = LuaData("dcsRetribution")
    populate_intercept_lua(root, [_entry(resource_count=4, engagement_range_nm=60)])
    serialized = root.serialize()
    assert "resourceCount" in serialized
    assert "engagementRangeNm" in serialized
    assert "gciMaxRadiusNm" in serialized
    assert "commsEnabled" in serialized
