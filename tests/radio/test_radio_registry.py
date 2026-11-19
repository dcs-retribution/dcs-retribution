from game.radio.radios import RadioRegistry


def test_alloc_vhf_returns_distinct_reserved_vhf_channel() -> None:
    registry = RadioRegistry()
    vhf = registry.alloc_vhf()
    # VHF AM band 118-144 MHz
    assert 118_000_000 <= vhf.hertz <= 144_000_000
    # reserved: a second alloc differs
    vhf2 = registry.alloc_vhf()
    assert vhf2.hertz != vhf.hertz
    # distinct band from UHF
    uhf = registry.alloc_uhf()
    assert uhf.hertz != vhf.hertz
