from dcs.point import MovingPoint
from dcs.task import (
    OptECMUsing,
    OptFormation,
    RunScript,
    SetUnlimitedFuelCommand,
    SwitchWaypoint,
    RunScript,
    OptReactOnThreat,
)

from game.utils import knots
from .pydcswaypointbuilder import PydcsWaypointBuilder

from game.ato import FlightType
from game.data.weapons import WeaponType

class SplitPointBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        # List of specific aircraft types that should get their own ewrj_menu_trigger and be excluded from needing a jammer
        specific_aircraft_types = ["CLP_E7A" , "CLP_P8" , "CLP_TU214R" , "CLP_TU214"]  # Replace with aircraft types e.g. E-3A

        # List of excluded aircraft types that should not get any triggers
        excluded_aircraft_types = ["F-16C_50"]  # Replace with aircraft types with working ECM

        # Unlimited fuel option : enable at split. Must be first option to work.
        if self.flight.squadron.coalition.game.settings.ai_unlimited_fuel:
            waypoint.tasks.insert(0, SetUnlimitedFuelCommand(True))

        if not self.flight.flight_type.is_air_to_air:
            # Capture any non A/A type to avoid issues with SPJs that use the primary radar such as the F/A-18C.
            # You can bully them with STT to not be able to fire radar guided missiles at you,
            # so best choice is to not let them perform jamming for now.

            # Let the AI use ECM to defend themselves.
            ecm_option = OptECMUsing(value=OptECMUsing.Values.UseIfOnlyLockByRadar)
            waypoint.tasks.append(ecm_option)

        if self.flight.is_helo:
            waypoint.tasks.append(OptFormation.rotary_wedge())
        else:
            waypoint.tasks.append(OptFormation.finger_four_open())
        waypoint.speed_locked = True
        waypoint.ETA_locked = False
        if self.flight.is_helo:
            waypoint.speed = knots(100).meters_per_second
        else:
            waypoint.speed = self.flight.coalition.doctrine.rtb_speed.meters_per_second
        if self.flight is self.package.primary_flight:
            script = RunScript(
                f'trigger.action.setUserFlag("split-{id(self.package)}", true)'
            )
            waypoint.tasks.append(script)

        elif self.flight.flight_type == FlightType.SEAD_SWEEP:
            # Stop Defensive Jamming
            settings = self.flight.coalition.game.settings

            for unit, member in zip(self.group.units, self.flight.iter_members()):
                if not settings.plugins.get("ewrj"):
                    return

                if unit.type in excluded_aircraft_types:
                    return

                if not settings.plugin_option("ewrj.ai_jammer_enabled"):
                    return

                # Check jammer requirement for non-specific aircraft types
                if settings.plugin_option("ewrj.ecm_required"):
                    ecm = WeaponType.JAMMER
                    if not member.loadout.has_weapon_of_type(ecm):
                        return
                if not member.is_player:
                    script_content = f'stopDjamming("{unit.name}")'
                    start_jamming_script = RunScript(script_content)
                    waypoint.tasks.append(start_jamming_script)

                passive_defense = OptReactOnThreat(
                    OptReactOnThreat.Values.PassiveDefense
                )
                waypoint.tasks.append(passive_defense)

        elif self.flight.flight_type == FlightType.SEAD:
            # Stop Defensive Jamming
            settings = self.flight.coalition.game.settings

            for unit, member in zip(self.group.units, self.flight.iter_members()):
                if not settings.plugins.get("ewrj"):
                    return

                if unit.type in excluded_aircraft_types:
                    return

                if not settings.plugin_option("ewrj.ai_jammer_enabled"):
                    return

                # Check jammer requirement for non-specific aircraft types
                if settings.plugin_option("ewrj.ecm_required"):
                    ecm = WeaponType.JAMMER
                    if not member.loadout.has_weapon_of_type(ecm):
                        return
                if not member.is_player:
                    script_content = f'stopDjamming("{unit.name}")'
                    start_jamming_script = RunScript(script_content)
                    waypoint.tasks.append(start_jamming_script)

                passive_defense = OptReactOnThreat(
                    OptReactOnThreat.Values.PassiveDefense
                )
                waypoint.tasks.append(passive_defense),

        elif self.flight.flight_type == FlightType.SEAD_ESCORT:
            # Moved previous escort split tasks
            if self.flight.flight_type.is_escort_type:
                index = len(self.group.points)
                self.group.add_trigger_action(SwitchWaypoint(None, index))

            # Stop Defensive Jamming
            settings = self.flight.coalition.game.settings

            for unit, member in zip(self.group.units, self.flight.iter_members()):
                if not settings.plugins.get("ewrj"):
                    return

                if unit.type in excluded_aircraft_types:
                    return

                if not settings.plugin_option("ewrj.ai_jammer_enabled"):
                    return

                # Check jammer requirement for non-specific aircraft types
                if settings.plugin_option("ewrj.ecm_required"):
                    ecm = WeaponType.JAMMER
                    if not member.loadout.has_weapon_of_type(ecm):
                        return
                if not member.is_player:
                    script_content = f'stopDjamming("{unit.name}")'
                    start_jamming_script = RunScript(script_content)
                    waypoint.tasks.append(start_jamming_script)

                passive_defense = OptReactOnThreat(
                    OptReactOnThreat.Values.PassiveDefense
                )
                waypoint.tasks.append(passive_defense)

