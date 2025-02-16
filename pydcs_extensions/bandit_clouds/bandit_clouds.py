from enum import unique, Enum

from dcs.weather import CloudPreset

from pydcs_extensions.cloud_injector import inject_cloud_presets, eject_cloud_presets


@unique
class BanditClouds(Enum):
    ScatteredShowers1 = CloudPreset(
        name="Preset35",
        ui_name="Scattered Showers 1 [Bandit648]",
        description="35 ##Scattered Showers \nMETAR: RA SCT SCT BKN",
        min_base=200.0,
        max_base=7000.0,
    )

    ScatteredShowers2 = CloudPreset(
        name="Preset36",
        ui_name="Scattered Showers 2 [Bandit648]",
        description="36 ##Scattered Showers \nMETAR: RA SCT SCT BKN ",
        min_base=200.0,
        max_base=14000.0,
    )

    ScatteredShowers3 = CloudPreset(
        name="Preset37",
        ui_name="Scattered Showers 3 [Bandit648]",
        description="37 ##Scattered Showers  \nMETAR: RA SCT BKN ",
        min_base=200.0,
        max_base=10000.0,
    )

    ScatteredShowers4 = CloudPreset(
        name="Preset38",
        ui_name="Scattered Showers 4 [Bandit648]",
        description="38 ##Scattered Showers \nMETAR: RA SCT BKN",
        min_base=200.0,
        max_base=10000.0,
    )

    ScatteredShowers5 = CloudPreset(
        name="Preset39",
        ui_name="Scattered Showers 5 [Bandit648]",
        description="39 ##Scattered Showers  \nMETAR: RA SCT BKN BKN",
        min_base=200.0,
        max_base=10000.0,
    )

    OvercastLightRain1 = CloudPreset(
        name="Preset40",
        ui_name="Overcast Light Rain 1 [Bandit648]",
        description="40 ##Overcast light rain \nMETAR: -RA BKN BKN",
        min_base=200.0,
        max_base=10000.0,
    )

    OvercastLightRain2 = CloudPreset(
        name="Preset41",
        ui_name="Overcast Light Rain 2 [Bandit648]",
        description="41 ##Overcast light rain \nMETAR: RA OVC BKN",
        min_base=200.0,
        max_base=10000.0,
    )

    OvercastAndModerateRain1 = CloudPreset(
        name="Preset42",
        ui_name="Overcast And Moderate Rain 1 [Bandit648]",
        description="42 ##Overcast with Rain \nMETAR: RA OVC BKN OVC",
        min_base=200.0,
        max_base=10000.0,
    )

    ScatteredCumulus1 = CloudPreset(
        name="Preset43",
        ui_name="Scattered Cumulus 1 [Bandit648]",
        description="43 ##One Layer Scattered \nMETAR: FEW/SCT ",
        min_base=200.0,
        max_base=10000.0,
    )

    ScatteredCumulus2 = CloudPreset(
        name="Preset44",
        ui_name="Scattered Cumulus 2 [Bandit648]",
        description="44 ##One Layer Scattered \nMETAR: SCT 6/10",
        min_base=200.0,
        max_base=15000.0,
    )

    ScatteredCumulus3 = CloudPreset(
        name="Preset45",
        ui_name="Scattered Cumulus 3 [Bandit648]",
        description="45 ##Two Layer Scattered \nMETAR: SCT SCT",
        min_base=200.0,
        max_base=10000.0,
    )

    ScatteredCumulus4 = CloudPreset(
        name="Preset46",
        ui_name="Scattered Cumulus 4 [Bandit648]",
        description="46 ##Two Layer Scattered \nMETAR: SCT SCT",
        min_base=200.0,
        max_base=10000.0,
    )

    ScatteredCumulus5 = CloudPreset(
        name="Preset47",
        ui_name="Scattered Cumulus 5 [Bandit648]",
        description="47 ##Three Layer Scattered \nMETAR: SCT BKN OVC",
        min_base=200.0,
        max_base=15000.0,
    )

    OvercastCumulusLightMist = CloudPreset(
        name="Preset48",
        ui_name="Overcast Cumulus Light Mist [Bandit648]",
        description="48 ##Overcast Light Rain \nMETAR: -RA OVC FEW",
        min_base=200.0,
        max_base=10000.0,
    )

    Lowlevelstratus1 = CloudPreset(
        name="Preset49",
        ui_name="Low level stratus 1 [Bandit648]",
        description="49 ##Single layer stratus \nMETAR: BKN",
        min_base=0.0,
        max_base=1524.0,
    )

    Lowlevelstratus2 = CloudPreset(
        name="Preset50",
        ui_name="Low level stratus 2 [Bandit648]",
        description="50 ##Single layer stratus \nMETAR: BKN",
        min_base=0.0,
        max_base=1524.0,
    )

    Lowlevelstratus3 = CloudPreset(
        name="Preset51",
        ui_name="Low level stratus 3 [Bandit648]",
        description="51 ##Single layer stratus \nMETAR: BKN",
        min_base=0.0,
        max_base=1524.0,
    )

    Lowlevelstratus4 = CloudPreset(
        name="Preset52",
        ui_name="Low level stratus 4 [Bandit648]",
        description="52 ##Single layer stratus \nMETAR: BKN",
        min_base=0.0,
        max_base=1524.0,
    )

    Lowlevelstratus5 = CloudPreset(
        name="Preset53",
        ui_name="Low level stratus 5 [Bandit648]",
        description="53 ##Low stratus with thick overcast clouds \nMETAR: OVC SCT",
        min_base=0.0,
        max_base=1524.0,
    )

    Lowlevelstratus6 = CloudPreset(
        name="Preset54",
        ui_name="Low level stratus 6 [Bandit648]",
        description="54 ##Low level stratus with big puffy cumulus \nMETAR: OVC BKN",
        min_base=0.0,
        max_base=3048.0,
    )

    Lowlevelstratus7 = CloudPreset(
        name="Preset55",
        ui_name="Low level stratus 7 [Bandit648]",
        description="55 ##Low level stratus with light scattered cumulus \nMETAR: BKN SCT",
        min_base=0.0,
        max_base=3048.0,
    )

    Altotratus1 = CloudPreset(
        name="Preset56",
        ui_name="Altotratus 1 [Bandit648]",
        description="56 ##Mid level Altostratus Overcast \nMETAR: OVC/BKN",
        min_base=3000.0,
        max_base=6096.0,
    )

    Altostratus2 = CloudPreset(
        name="Preset57",
        ui_name="Altostratus 2 [Bandit648]",
        description="57 ##Altostratus Scattered \nMETAR: OVC/SCT",
        min_base=1828.0,
        max_base=6096.0,
    )

    Altostratus3 = CloudPreset(
        name="Preset58",
        ui_name="Altostratus 3 [Bandit648]",
        description="58 ##Altostratus Scattered \nMETAR: OVC/SCT",
        min_base=1828.0,
        max_base=6096.0,
    )

    Altostratus4 = CloudPreset(
        name="Preset59",
        ui_name="Altostratus 4 [Bandit648]",
        description="59 ##Altostratus Broken \nMETAR: OVC/BKN",
        min_base=1828.0,
        max_base=6096.0,
    )

    Altocumulus1 = CloudPreset(
        name="Preset60",
        ui_name="Altocumulus 1 [Bandit648]",
        description="60 ##Altocumulus scattered \nMETAR: OVC/SCT",
        min_base=500.0,
        max_base=7620.0,
    )

    Altocumulus2 = CloudPreset(
        name="Preset61",
        ui_name="Altocumulus 2 [Bandit648]",
        description="61 ##Mid Level Altocumulus Few \nMETAR: SCT/FEW",
        min_base=500.0,
        max_base=7620.0,
    )

    Altocumulus3 = CloudPreset(
        name="Preset62",
        ui_name="Altocumulus 3 [Bandit648]",
        description="62 ##Altocumulus broken \nMETAR: OVC/BKN",
        min_base=500.0,
        max_base=7620.0,
    )

    Altocumulus4 = CloudPreset(
        name="Preset63",
        ui_name="Altocumulus 4 [Bandit648]",
        description="63 ##Altocumulus broken \nMETAR: OVC/BKN",
        min_base=500.0,
        max_base=7620.0,
    )

    Nimbostratuswithheavyrain = CloudPreset(
        name="Preset64",
        ui_name="Nimbostratus with heavy rain [Bandit648]",
        description="64 ##Heavy rain with thick overcast cloud layer \nMETAR: RA OVC BKN",
        min_base=609.0,
        max_base=6096.0,
    )

    Cirrocumulus1 = CloudPreset(
        name="Preset65",
        ui_name="Cirrocumulus 1 [Bandit648]",
        description="65 ##High level cirrcumulus clouds \nMETAR: SCT/BKN",
        min_base=300.0,
        max_base=18288.0,
    )

    Cirrocumulus2 = CloudPreset(
        name="Preset66",
        ui_name="Cirrocumulus 2 [Bandit648]",
        description="66 ##High level cirrcumulus clouds \nMETAR: SCT/BKN",
        min_base=300.0,
        max_base=18288.0,
    )

    Cirrocumulus3 = CloudPreset(
        name="Preset67",
        ui_name="Cirrocumulus 3 [Bandit648]",
        description="67 ##High level cirrocumulus scattered \nMETAR: SCT",
        min_base=300.0,
        max_base=18288.0,
    )

    Cirrostratus1 = CloudPreset(
        name="Preset68",
        ui_name="Cirrostratus 1 [Bandit648]",
        description="68 ##High level cirrostratus clouds \nMETAR: SCT/BKN",
        min_base=300.0,
        max_base=18288.0,
    )

    Cirrostratus2 = CloudPreset(
        name="Preset69",
        ui_name="Cirrostratus 2 [Bandit648]",
        description="69 ##High level cirrostratus overcast \nMETAR: OVC/BKN",
        min_base=0.0,
        max_base=18288.0,
    )

    Cirrostratus3 = CloudPreset(
        name="Preset70",
        ui_name="Cirrostratus 3 [Bandit648]",
        description="70 ##High level cirrostratus overcast \nMETAR: OVC/BKN",
        min_base=300.0,
        max_base=18288.0,
    )

    Cirrostratus4 = CloudPreset(
        name="Preset71",
        ui_name="Cirrostratus 4 [Bandit648]",
        description="71 ##High level cirrostratus overcast \nMETAR: OVC/BKN",
        min_base=300.0,
        max_base=18288.0,
    )

    @staticmethod
    def activate() -> None:
        inject_cloud_presets(BANDIT_CLOUDS)

    @staticmethod
    def deactivate() -> None:
        eject_cloud_presets(BANDIT_CLOUDS)


BANDIT_CLOUDS = {
    "Preset35": BanditClouds.ScatteredShowers1,
    "Preset36": BanditClouds.ScatteredShowers2,
    "Preset37": BanditClouds.ScatteredShowers3,
    "Preset38": BanditClouds.ScatteredShowers4,
    "Preset39": BanditClouds.ScatteredShowers5,
    "Preset40": BanditClouds.OvercastLightRain1,
    "Preset41": BanditClouds.OvercastLightRain2,
    "Preset42": BanditClouds.OvercastAndModerateRain1,
    "Preset43": BanditClouds.ScatteredCumulus1,
    "Preset44": BanditClouds.ScatteredCumulus2,
    "Preset45": BanditClouds.ScatteredCumulus3,
    "Preset46": BanditClouds.ScatteredCumulus4,
    "Preset47": BanditClouds.ScatteredCumulus5,
    "Preset48": BanditClouds.OvercastCumulusLightMist,
    "Preset49": BanditClouds.Lowlevelstratus1,
    "Preset50": BanditClouds.Lowlevelstratus2,
    "Preset51": BanditClouds.Lowlevelstratus3,
    "Preset52": BanditClouds.Lowlevelstratus4,
    "Preset53": BanditClouds.Lowlevelstratus5,
    "Preset54": BanditClouds.Lowlevelstratus6,
    "Preset55": BanditClouds.Lowlevelstratus7,
    "Preset56": BanditClouds.Altotratus1,
    "Preset57": BanditClouds.Altostratus2,
    "Preset58": BanditClouds.Altostratus3,
    "Preset59": BanditClouds.Altostratus4,
    "Preset60": BanditClouds.Altocumulus1,
    "Preset61": BanditClouds.Altocumulus2,
    "Preset62": BanditClouds.Altocumulus3,
    "Preset63": BanditClouds.Altocumulus4,
    "Preset64": BanditClouds.Nimbostratuswithheavyrain,
    "Preset65": BanditClouds.Cirrocumulus1,
    "Preset66": BanditClouds.Cirrocumulus2,
    "Preset67": BanditClouds.Cirrocumulus3,
    "Preset68": BanditClouds.Cirrostratus1,
    "Preset69": BanditClouds.Cirrostratus2,
    "Preset70": BanditClouds.Cirrostratus3,
    "Preset71": BanditClouds.Cirrostratus4,
}
