from game.ato.loadouts import Loadout

GBU_16 = "{0D33DDAE-524F-4A4E-B5B8-621754FE3ADE}"


def test_empty_pylon_does_not_invalidate_a_payload() -> None:
    """A pylon carrying nothing is not a pylon carrying something unknown.

    The Tornado IDS "STRIKE" payload leaves stations 5-8 free, so rejecting it
    left the aircraft planned with no loadout at all instead of its GBU-16s.
    """
    assert Loadout.valid_payload({1: {"CLSID": GBU_16}, 5: {"CLSID": ""}})


def test_unknown_store_still_invalidates_a_payload() -> None:
    assert not Loadout.valid_payload(
        {1: {"CLSID": GBU_16}, 5: {"CLSID": "{NOT-A-REAL-WEAPON}"}}
    )
