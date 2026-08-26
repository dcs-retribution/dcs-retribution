from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from game.missiongenerator.luagenerator import LuaData


@dataclass(frozen=True)
class InterceptEntry:
    squadron_id: str
    squadron_name: str
    airbase_name: str
    template_prefix: str
    coalition: str  # "BLUE" or "RED"
    resource_count: int
    engagement_range_nm: int
    gci_max_radius_nm: int
    comms_enabled: bool


def populate_intercept_lua(root: "LuaData", entries: Iterable[InterceptEntry]) -> None:
    """Build the ``dcsRetribution.Intercept`` subtree (mirrors the IADS pattern).

    Always creates BLUE and RED buckets so the Lua side can iterate them
    unconditionally, then appends one record per reserved squadron.
    """
    intercept = root.add_item("Intercept")
    buckets = {
        "BLUE": intercept.get_or_create_item("BLUE"),
        "RED": intercept.get_or_create_item("RED"),
    }
    for entry in entries:
        record = buckets[entry.coalition].add_item()
        record.add_key_value("squadronId", entry.squadron_id)
        record.add_key_value("squadronName", entry.squadron_name)
        record.add_key_value("airbaseName", entry.airbase_name)
        record.add_key_value("templatePrefix", entry.template_prefix)
        record.add_key_value("resourceCount", str(entry.resource_count))
        record.add_key_value("engagementRangeNm", str(entry.engagement_range_nm))
        record.add_key_value("gciMaxRadiusNm", str(entry.gci_max_radius_nm))
        record.add_key_value("commsEnabled", "true" if entry.comms_enabled else "false")
