from game.dcs.beacons import Beacon, BeaconType
from game.radio.tacan import TacanBand, TacanChannel


def make_beacon(
    beacon_type: BeaconType, channel: int | None = 40, hertz: int | None = None
) -> Beacon:
    return Beacon(
        name="Test",
        callsign="TST",
        beacon_type=beacon_type,
        hertz=hertz,
        channel=channel,
    )


def test_tacan_and_vortac_occupy_tacan_channel() -> None:
    assert make_beacon(BeaconType.BEACON_TYPE_TACAN).occupies_tacan_channel
    assert make_beacon(BeaconType.BEACON_TYPE_VORTAC).occupies_tacan_channel


def test_dme_and_vor_dme_occupy_tacan_channel() -> None:
    """DME/VOR-DME share TACAN's channelization, so they must be blacklisted too."""
    assert make_beacon(BeaconType.BEACON_TYPE_DME).occupies_tacan_channel
    assert make_beacon(BeaconType.BEACON_TYPE_VOR_DME).occupies_tacan_channel


def test_vor_alone_does_not_occupy_tacan_channel() -> None:
    assert not make_beacon(BeaconType.BEACON_TYPE_VOR).occupies_tacan_channel


def test_ils_does_not_occupy_tacan_channel() -> None:
    assert not make_beacon(BeaconType.BEACON_TYPE_ILS_LOCALIZER).occupies_tacan_channel


def test_tacan_channel_falls_back_to_channel_field_outside_vor_band() -> None:
    """No VHF frequency (or one outside the civil VOR band) means we can't derive
    the channel/band from frequency, so fall back to the raw channel field."""
    beacon = make_beacon(BeaconType.BEACON_TYPE_VOR_DME, channel=88, hertz=None)
    assert beacon.tacan_channel == TacanChannel(88, TacanBand.X)


def test_tacan_channel_derived_from_kalde_kad_beacon() -> None:
    """Regression test for #36: KALDE airport's KAD VOR-DME beacon (Syria) has no
    'channel' in the DCS data, but its 112.60 MHz frequency pairs with 73X per the
    standard ICAO VOR/TACAN channelling plan, so it must still be blacklisted."""
    beacon = make_beacon(
        BeaconType.BEACON_TYPE_VOR_DME, channel=None, hertz=112_600_000
    )
    assert beacon.tacan_channel == TacanChannel(73, TacanBand.X)


def test_tacan_channel_frequency_takes_priority_over_channel_field() -> None:
    """The frequency-derived channel/band is authoritative even if DCS also supplied
    a (potentially band-agnostic/incorrect) channel number."""
    beacon = make_beacon(BeaconType.BEACON_TYPE_VOR_DME, channel=88, hertz=112_600_000)
    assert beacon.tacan_channel == TacanChannel(73, TacanBand.X)


def test_tacan_channel_derives_y_band() -> None:
    beacon = make_beacon(
        BeaconType.BEACON_TYPE_VOR_DME, channel=None, hertz=112_650_000
    )
    assert beacon.tacan_channel == TacanChannel(73, TacanBand.Y)


def test_tacan_channel_none_when_unresolvable() -> None:
    beacon = make_beacon(BeaconType.BEACON_TYPE_VOR_DME, channel=None, hertz=None)
    assert beacon.tacan_channel is None
