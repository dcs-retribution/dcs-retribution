# F-14B(U) Retribution support

This document tracks the work that can be prepared before the DCS F-14B(U) is released. It deliberately does **not** add an aircraft YAML entry or faction references yet: Retribution loads aircraft definitions by the exact class/type exported by pydcs, and the released DCS export is not available at preparation time.

## Current baseline

Retribution already supports the relevant F-14B behavior in:

- `resources/units/aircraft/F-14B.yaml`
  - carrier operation
  - Tomcat radio/channel configuration
  - F-14B task priorities
  - stored INS alignment default
- `game/dcs/aircrafttype.py`
  - discovers DCS aircraft classes from pydcs
  - loads per-variant data from `resources/units/aircraft`
- `game/ato/loadouts.py`
  - reads the aircraft's exported pydcs payloads
  - chooses default payloads by standardized task names
- `resources/factions/*.json`
  - declares which aircraft are available to each faction and era

The F-14B(U) should be treated as a sibling/variant of the existing F-14B for planning purposes, but every pydcs-facing identifier and payload must be verified after release.

## Safe to prepare before DCS release

### 1. Aircraft-data decisions

- [x] Use `F-14B.yaml` as the initial reference for radios, carrier capability, role, and task weighting.
- [ ] Confirm the intended display name and variant name for the F-14B(U).
- [ ] Decide whether the aircraft should have its own YAML file or be a variant in an existing/shared file after the pydcs class is known.
- [ ] Compare the F-14B(U)'s intended introduction date and operator history with existing F-14B faction-era coverage.
- [ ] Revisit price and maximum mission range after release data and community/operator information are available.
- [ ] Determine whether its avionics/options require `default_overrides`, `date_gated_properties`, laser-code configuration, or weapon injections.

### 2. Planner and mission behavior

- [x] Start from the F-14B task-role model rather than inventing a new mission type.
- [ ] Confirm whether the F-14B(U) supports the same planner tasks as the F-14B once pydcs exports its task list.
- [ ] Confirm that normal Tomcat waypoint behavior is sufficient. Add aircraft-specific behavior only if the released module has restrictions not shared by the current F-14B.
- [ ] Check carrier and LHA suitability against the released pydcs dimensions/parking metadata.

### 3. Faction and squadron preparation

- [ ] Make an operator/era matrix before editing faction files. Do not copy every existing F-14B entry automatically.
- [ ] Identify the intended US Navy and any other supported operators for the F-14B(U).
- [ ] Identify likely squadron/livery defaults. Existing F-14B livery overrides are useful references but are not proof that they apply to the new aircraft.
- [ ] After the exact display name is known, add only the relevant faction entries and livery overrides.

### 4. Loadout handoff

- [x] Record that loadouts will be sourced from the pydcs-exported payload table, not guessed in Retribution YAML.
- [ ] After pydcs update, enumerate every exported F-14B(U) payload and compare it with F-14B defaults.
- [ ] Verify standardized payload names for BARCAP, TARCAP, escort, strike, CAS/BAI, DEAD, OCA, and intercept use.
- [ ] Add custom loadout handling or weapon injections only for payloads that are genuinely unique to the U variant.
- [ ] Verify that every selected payload is valid under `Loadout.valid_payload` and spawns correctly in DCS.

### 5. Documentation and assets

- [ ] Prepare a 720x360 JPEG banner and 91x24 JPEG icon once an approved aircraft image is available.
- [ ] Draft the short aircraft description, manufacturer, origin, role, and introduction metadata.
- [ ] Measure fuel consumption using `docs/modding/fuel-consumption-measurement.md` after the aircraft is flyable in the released DCS build.

## Release gate: pydcs/DCS data required

The following cannot be completed reliably before release:

1. Run the latest `pydcs_export.lua` against the released DCS installation.
2. Submit/update pydcs with the aircraft class, pylons, stores, tasks, physical data, radios, properties, and country data.
3. Update Retribution's pydcs dependency.
4. Confirm the exact aircraft class/type ID and variant display names.
5. Add the production aircraft YAML entry.
6. Add faction entries using the exact display name consumed by faction loading.
7. Validate default payload names and unique F-14B(U) stores.
8. Generate representative missions and verify cold, hot, carrier, and ground starts in DCS.
9. Check kneeboard fuel estimates and add measured fuel data.
10. Add final banner/icon assets and run the full aircraft-support checklist.

## Important non-goals for this pre-release change

- Do not guess a pydcs class name or DCS unit ID.
- Do not add a YAML file that cannot be loaded by the current pydcs dependency.
- Do not add F-14B(U) strings to faction files until the released display name is known.
- Do not copy F-14B loadouts into a hand-maintained table when pydcs will be the source of truth.
- Do not add special waypoint code without evidence that the U variant needs it.

## References

- [New aircraft module checklist](https://github.com/dcs-retribution/dcs-retribution/wiki/New-aircraft-module-checklist)
- [`pydcs_export.lua`](https://github.com/dcs-retribution/pydcs/blob/master/tools/pydcs_export.lua)
- `resources/units/aircraft/F-14B.yaml`
- `game/dcs/aircrafttype.py`
- `game/ato/loadouts.py`
- `docs/modding/fuel-consumption-measurement.md`
