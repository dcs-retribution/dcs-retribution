from enum import unique, Enum

from dcs.weather import CloudPreset

from pydcs_extensions.cloud_injector import inject_cloud_presets, eject_cloud_presets


@unique
class AtmosXClouds(Enum):
    ScatteredShowers1 = CloudPreset(
        name="Preset35",
        ui_name="Scattered Showers 1 [ATMOS-X]",
        description="35 ##Scattered Showers \nMETAR: RA SCT SCT BKN",
        min_base=200.0,
        max_base=7000.0,
    )

    ScatteredShowers2 = CloudPreset(
        name="Preset36",
        ui_name="Scattered Showers 2 [ATMOS-X]",
        description="36 ##Scattered Showers \nMETAR: RA SCT SCT BKN",
        min_base=200.0,
        max_base=14000.0,
    )

    ScatteredShowers3 = CloudPreset(
        name="Preset37",
        ui_name="Scattered Showers 3 [ATMOS-X]",
        description="37 ##Scattered Showers  \nMETAR: RA SCT BKN ",
        min_base=200.0,
        max_base=10000.0,
    )

    ScatteredShowers4 = CloudPreset(
        name="Preset38",
        ui_name="Scattered Showers 4 [ATMOS-X]",
        description="38 ##Scattered Showers \nMETAR: RA SCT BKN",
        min_base=200.0,
        max_base=10000.0,
    )

    ScatteredShowers5 = CloudPreset(
        name="Preset39",
        ui_name="Scattered Showers 5 [ATMOS-X]",
        description="39 ##Scattered Showers  \nMETAR: RA SCT BKN BKN",
        min_base=200.0,
        max_base=10000.0,
    )

    ScatteredShowers6 = CloudPreset(
        name="Preset40",
        ui_name="Scattered Showers 6 [ATMOS-X]",
        description="40 ##Low clounds w/Scattered Showers",
        min_base=200.0,
        max_base=10000.0,
    )

    OvercastLightRain1 = CloudPreset(
        name="Preset41",
        ui_name="Overcast Light Rain 1 [ATMOS-X]",
        description="41 ##Overcast light rain \nMETAR: -RA BKN BKN",
        min_base=200.0,
        max_base=10000.0,
    )

    OvercastLightRain2 = CloudPreset(
        name="Preset42",
        ui_name="Overcast Light Rain 2 [ATMOS-X]",
        description="42 ##Overcast light rain \nMETAR: RA OVC BKN",
        min_base=200.0,
        max_base=10000.0,
    )

    OvercastAndModerateRain1 = CloudPreset(
        name="Preset43",
        ui_name="Overcast And Moderate Rain 1 [ATMOS-X]",
        description="43 ##Overcast with Rain \nMETAR: RA OVC BKN OVC",
        min_base=200.0,
        max_base=10000.0,
    )

    ScatteredCumulus1 = CloudPreset(
        name="Preset44",
        ui_name="Scattered Cumulus 1 [ATMOS-X]",
        description="44 ##One Layer Scattered \nMETAR: FEW/SCT ",
        min_base=200.0,
        max_base=10000.0,
    )

    ScatteredCumulus2 = CloudPreset(
        name="Preset45",
        ui_name="Scattered Cumulus 2 [ATMOS-X]",
        description="45 ##One Layer Scattered \nMETAR: SCT 6/10",
        min_base=200.0,
        max_base=15000.0,
    )

    ScatteredCumulus3 = CloudPreset(
        name="Preset46",
        ui_name="Scattered Cumulus 3 [ATMOS-X]",
        description="46 ##Two Layer Scattered \nMETAR: SCT SCT",
        min_base=200.0,
        max_base=10000.0,
    )

    ScatteredCumulus4 = CloudPreset(
        name="Preset47",
        ui_name="Scattered Cumulus 4 [ATMOS-X]",
        description="47 ##Two Layer Scattered \nMETAR: SCT SCT",
        min_base=200.0,
        max_base=10000.0,
    )

    ScatteredCumulus5 = CloudPreset(
        name="Preset48",
        ui_name="Scattered Cumulus 5 [ATMOS-X]",
        description="48 ##Three Layer Scattered \nMETAR: SCT BKN OVC",
        min_base=200.0,
        max_base=15000.0,
    )

    OvercastCumulusLightMist = CloudPreset(
        name="Preset49",
        ui_name="Overcast Cumulus Light Mist [ATMOS-X]",
        description="49 ##Overcast Light Rain \nMETAR: -RA OVC FEW",
        min_base=200.0,
        max_base=10000.0,
    )

    Lowlevelstratus1 = CloudPreset(
        name="Preset50",
        ui_name="Low level stratus 1 [ATMOS-X]",
        description="50 ##Single layer stratus \nMETAR: BKN",
        min_base=0.0,
        max_base=10000.0,
    )

    Lowlevelstratus2 = CloudPreset(
        name="Preset51",
        ui_name="Low level stratus 2 [ATMOS-X]",
        description="51 ##Single layer stratus \nMETAR: BKN",
        min_base=0.0,
        max_base=10000.0,
    )

    Lowlevelstratus3 = CloudPreset(
        name="Preset52",
        ui_name="Low level stratus 3 [ATMOS-X]",
        description="52 ##Single layer stratus \nMETAR: BKN",
        min_base=0.0,
        max_base=10000.0,
    )

    Lowlevelstratus4 = CloudPreset(
        name="Preset53",
        ui_name="Low level stratus 4 [ATMOS-X]",
        description="53 ##Single layer stratus \nMETAR: BKN",
        min_base=0.0,
        max_base=10000.0,
    )

    Lowlevelstratus5 = CloudPreset(
        name="Preset54",
        ui_name="Low level stratus 5 [ATMOS-X]",
        description="54 ##Low stratus with broken clouds \nMETAR: BKN SCT",
        min_base=0.0,
        max_base=10000.0,
    )

    Lowlevelstratus6 = CloudPreset(
        name="Preset55",
        ui_name="Low level stratus 6 [ATMOS-X]",
        description="55 ##Low level stratus with big puffy cumulus \nMETAR: BKN BKN",
        min_base=200.0,
        max_base=10000.0,
    )

    Lowlevelstratus7 = CloudPreset(
        name="Preset56",
        ui_name="Low level stratus 7 [ATMOS-X]",
        description="56 ##Low level stratus with light scattered cumulus \nMETAR: BKN SCT",
        min_base=200.0,
        max_base=10000.0,
    )

    Altotratus1 = CloudPreset(
        name="Preset57",
        ui_name="Altotratus 1 [ATMOS-X]",
        description="57 ##Mid level Altostratus \nMETAR: SCT",
        min_base=2000.0,
        max_base=6096.0,
    )

    Altostratus2 = CloudPreset(
        name="Preset58",
        ui_name="Altostratus 2 [ATMOS-X]",
        description="58 ##Altostratus Scattered \nMETAR: BKN",
        min_base=1828.0,
        max_base=6096.0,
    )

    Altostratus3 = CloudPreset(
        name="Preset59",
        ui_name="Altostratus 3 [ATMOS-X]",
        description="59 ##Altostratus Scattered \nMETAR: BKN/SCT",
        min_base=1828.0,
        max_base=6096.0,
    )

    Altostratus4 = CloudPreset(
        name="Preset60",
        ui_name="Altostratus 4 [ATMOS-X]",
        description="60 ##Altostratus Broken \nMETAR: OVC/BKN",
        min_base=1828.0,
        max_base=6096.0,
    )

    Altocumulus1 = CloudPreset(
        name="Preset61",
        ui_name="Altocumulus 1 [ATMOS-X]",
        description="61 ##Altocumulus scattered \nMETAR: SCT",
        min_base=2000.0,
        max_base=7620.0,
    )

    Altocumulus2 = CloudPreset(
        name="Preset62",
        ui_name="Altocumulus 2 [ATMOS-X]",
        description="62 ##Mid Level Altocumulus Few \nMETAR: SCT",
        min_base=2000.0,
        max_base=7620.0,
    )

    Altocumulus3 = CloudPreset(
        name="Preset63",
        ui_name="Altocumulus 3 [ATMOS-X]",
        description="63 ##Altocumulus broken \nMETAR: OVC/BKN",
        min_base=2000.0,
        max_base=7620.0,
    )

    Altocumulus4 = CloudPreset(
        name="Preset64",
        ui_name="Altocumulus 4 [ATMOS-X]",
        description="64 ##Altocumulus broken \nMETAR: OVC/BKN",
        min_base=2000.0,
        max_base=7620.0,
    )

    Nimbostratuswithheavyrain = CloudPreset(
        name="Preset65",
        ui_name="Nimbostratus with heavy rain [ATMOS-X]",
        description="65 ##Heavy rain with thick overcast cloud layer \nMETAR: RA OVC BKN",
        min_base=609.0,
        max_base=6096.0,
    )

    Cirrocumulus1 = CloudPreset(
        name="Preset66",
        ui_name="Cirrocumulus 1 [ATMOS-X]",
        description="66 ##High level cirrocumulus clouds \nMETAR: SCT/BKN",
        min_base=5000.0,
        max_base=18288.0,
    )

    Cirrocumulus2 = CloudPreset(
        name="Preset67",
        ui_name="Cirrocumulus 2 [ATMOS-X]",
        description="67 ##High level cirrocumulus clouds \nMETAR: SCT/BKN",
        min_base=5000.0,
        max_base=18288.0,
    )

    Cirrocumulus3 = CloudPreset(
        name="Preset68",
        ui_name="Cirrocumulus 3 [ATMOS-X]",
        description="68 ##High level cirrocumulus scattered \nMETAR: SCT",
        min_base=5000.0,
        max_base=18288.0,
    )

    Cirrostratus1 = CloudPreset(
        name="Preset69",
        ui_name="Cirrostratus 1 [ATMOS-X]",
        description="69 ##High level cirrostratus clouds \nMETAR: FEW",
        min_base=5000.0,
        max_base=12192.0,
    )

    Cirrostratus2 = CloudPreset(
        name="Preset70",
        ui_name="Cirrostratus 2 [ATMOS-X]",
        description="70 ##High level cirrostratus overcast \nMETAR: SCT",
        min_base=5000.0,
        max_base=12192.0,
    )

    Cirrostratus3 = CloudPreset(
        name="Preset71",
        ui_name="Cirrostratus 3 [ATMOS-X]",
        description="71 ##High level cirrostratus overcast \nMETAR: BKN",
        min_base=5000.0,
        max_base=18288.0,
    )

    Cirrostratus4 = CloudPreset(
        name="Preset72",
        ui_name="Cirrostratus 4 [ATMOS-X]",
        description="72 ##High level cirrostratus overcast \nMETAR: OVC",
        min_base=5000.0,
        max_base=18288.0,
    )

    ScatteredThunderstorms1 = CloudPreset(
        name="Preset73",
        ui_name="Scattered Thunderstorms 1 [ATMOS-X]",
        description="73 ##Scattered Thunderstorms \nMETAR: RA SCT TS",
        min_base=200.0,
        max_base=10000.0,
    )

    ScatteredThunderstorms2 = CloudPreset(
        name="Preset74",
        ui_name="Scattered Thunderstorms 2 [ATMOS-X]",
        description="74 ##Scattered Thunderstorms \nMETAR: RA SCT TS",
        min_base=200.0,
        max_base=10000.0,
    )

    CumulusandAltocumulus1 = CloudPreset(
        name="Preset75",
        ui_name="Cumulus and Altocumulus 1 [ATMOS-X]",
        description="75 ##Cumulus and Altocumulus scattered \nMETAR: OVC/SCT",
        min_base=500.0,
        max_base=7620.0,
    )

    BrokenCumulusNoRain1 = CloudPreset(
        name="Preset76",
        ui_name="Broken Cumulus No Rain 1 [ATMOS-X]",
        description="76 ##Broken Thick Clouds \nMETAR: SCT BKN",
        min_base=200.0,
        max_base=7000.0,
    )

    BrokenCumulusNoRain2 = CloudPreset(
        name="Preset77",
        ui_name="Broken Cumulus No Rain 2 [ATMOS-X]",
        description="77 ##Broken Thick Clouds \nMETAR: SCT SCT BKN ",
        min_base=200.0,
        max_base=14000.0,
    )

    BrokenCumulusNoRain3 = CloudPreset(
        name="Preset78",
        ui_name="Broken Cumulus No Rain 3 [ATMOS-X]",
        description="78 ##Broken Thick Clouds  \nMETAR: SCT BKN ",
        min_base=200.0,
        max_base=10000.0,
    )

    BrokenCumulusNoRain4 = CloudPreset(
        name="Preset79",
        ui_name="Broken Cumulus No Rain 4 [ATMOS-X]",
        description="79 ##Broken Thick Clouds \nMETAR: SCT BKN",
        min_base=200.0,
        max_base=10000.0,
    )

    BrokenCumulusNoRain5 = CloudPreset(
        name="Preset80",
        ui_name="Broken Cumulus No Rain 5 [ATMOS-X]",
        description="80 ##Broken Thick Clouds  \nMETAR: SCT BKN BKN",
        min_base=200.0,
        max_base=10000.0,
    )

    CumulusAltocumulus1 = CloudPreset(
        name="Preset81",
        ui_name="Cumulus & Altocumulus 1 [ATMOS-X]",
        description="81 ##2 layers, low and mid level",
        min_base=610.0,
        max_base=11500.0,
    )

    CumulusAltocumulus2 = CloudPreset(
        name="Preset82",
        ui_name="Cumulus & Altocumulus 2 [ATMOS-X]",
        description="82 ##2 layers, low/mid",
        min_base=620.0,
        max_base=8561.0,
    )

    ScatteredShowers7 = CloudPreset(
        name="Preset83",
        ui_name="Scattered Showers 7 [ATMOS-X]",
        description="83 ##Building cumulonimbus, scattered showers",
        min_base=460.0,
        max_base=2438.0,
    )

    AltocumulusCirrocumulus1 = CloudPreset(
        name="Preset84",
        ui_name="Altocumulus & Cirrocumulus 1 [ATMOS-X]",
        description="84 ##3 layers mid level and upper level ",
        min_base=2438.0,
        max_base=8108.0,
    )

    AltostratusAltocumulus = CloudPreset(
        name="Preset85",
        ui_name="Altostratus & Altocumulus [ATMOS-X]",
        description="85 ##2 layers mid level",
        min_base=2438.0,
        max_base=8108.0,
    )

    FewAltocumulus = CloudPreset(
        name="Preset86",
        ui_name="Few Altocumulus [ATMOS-X]",
        description="86 ##2 layers mid level",
        min_base=2438.0,
        max_base=8108.0,
    )

    Altocumulus3layers = CloudPreset(
        name="Preset87",
        ui_name="Altocumulus 3 layers [ATMOS-X]",
        description="87 ##3 layers mid level",
        min_base=2438.0,
        max_base=6157.0,
    )

    AltostratusAltocumulus88 = CloudPreset(
        name="Preset88",
        ui_name="Altostratus & Altocumulus [ATMOS-X]",
        description="88 ##3 layers mid and upper level",
        min_base=3658.0,
        max_base=8382.0,
    )

    @staticmethod
    def activate() -> None:
        inject_cloud_presets(ATMOSX_CLOUDS)

    @staticmethod
    def deactivate() -> None:
        eject_cloud_presets(ATMOSX_CLOUDS)


ATMOSX_CLOUDS = {
    "Preset35": AtmosXClouds.ScatteredShowers1,
    "Preset36": AtmosXClouds.ScatteredShowers2,
    "Preset37": AtmosXClouds.ScatteredShowers3,
    "Preset38": AtmosXClouds.ScatteredShowers4,
    "Preset39": AtmosXClouds.ScatteredShowers5,
    "Preset40": AtmosXClouds.ScatteredShowers6,
    "Preset41": AtmosXClouds.OvercastLightRain1,
    "Preset42": AtmosXClouds.OvercastLightRain2,
    "Preset43": AtmosXClouds.OvercastAndModerateRain1,
    "Preset44": AtmosXClouds.ScatteredCumulus1,
    "Preset45": AtmosXClouds.ScatteredCumulus2,
    "Preset46": AtmosXClouds.ScatteredCumulus3,
    "Preset47": AtmosXClouds.ScatteredCumulus4,
    "Preset48": AtmosXClouds.ScatteredCumulus5,
    "Preset49": AtmosXClouds.OvercastCumulusLightMist,
    "Preset50": AtmosXClouds.Lowlevelstratus1,
    "Preset51": AtmosXClouds.Lowlevelstratus2,
    "Preset52": AtmosXClouds.Lowlevelstratus3,
    "Preset53": AtmosXClouds.Lowlevelstratus4,
    "Preset54": AtmosXClouds.Lowlevelstratus5,
    "Preset55": AtmosXClouds.Lowlevelstratus6,
    "Preset56": AtmosXClouds.Lowlevelstratus7,
    "Preset57": AtmosXClouds.Altotratus1,
    "Preset58": AtmosXClouds.Altostratus2,
    "Preset59": AtmosXClouds.Altostratus3,
    "Preset60": AtmosXClouds.Altostratus4,
    "Preset61": AtmosXClouds.Altocumulus1,
    "Preset62": AtmosXClouds.Altocumulus2,
    "Preset63": AtmosXClouds.Altocumulus3,
    "Preset64": AtmosXClouds.Altocumulus4,
    "Preset65": AtmosXClouds.Nimbostratuswithheavyrain,
    "Preset66": AtmosXClouds.Cirrocumulus1,
    "Preset67": AtmosXClouds.Cirrocumulus2,
    "Preset68": AtmosXClouds.Cirrocumulus3,
    "Preset69": AtmosXClouds.Cirrostratus1,
    "Preset70": AtmosXClouds.Cirrostratus2,
    "Preset71": AtmosXClouds.Cirrostratus3,
    "Preset72": AtmosXClouds.Cirrostratus4,
    "Preset73": AtmosXClouds.ScatteredThunderstorms1,
    "Preset74": AtmosXClouds.ScatteredThunderstorms2,
    "Preset75": AtmosXClouds.CumulusandAltocumulus1,
    "Preset76": AtmosXClouds.BrokenCumulusNoRain1,
    "Preset77": AtmosXClouds.BrokenCumulusNoRain2,
    "Preset78": AtmosXClouds.BrokenCumulusNoRain3,
    "Preset79": AtmosXClouds.BrokenCumulusNoRain4,
    "Preset80": AtmosXClouds.BrokenCumulusNoRain5,
    "Preset81": AtmosXClouds.CumulusAltocumulus1,
    "Preset82": AtmosXClouds.CumulusAltocumulus2,
    "Preset83": AtmosXClouds.ScatteredShowers7,
    "Preset84": AtmosXClouds.AltocumulusCirrocumulus1,
    "Preset85": AtmosXClouds.AltostratusAltocumulus,
    "Preset86": AtmosXClouds.FewAltocumulus,
    "Preset87": AtmosXClouds.Altocumulus3layers,
    "Preset88": AtmosXClouds.AltostratusAltocumulus88,
}
