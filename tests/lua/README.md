# Headless Lua plugin harness

Runs the real `resources/plugins/**/*.lua` scripts on Lua 5.1 — the dialect DCS
embeds — inside the normal pytest run, against a faked mission-scripting
sandbox (`dcs_stubs.lua`). No DCS install involved.

## Why

A Lua syntax check (`luac -p`) catches parse errors; nothing before this caught
the next failure class up: **the script loads, errors at file scope or inside
its first scheduled tick, and the feature silently never starts** — no crash,
no CI signal, just a plugin that does nothing in the mission. The harness runs
the plugin exactly as the mission would (config table first, then the script),
drives a virtual clock through `timer.scheduleFunction`, and records every
`trigger.action.*` side effect for assertions.

## What it models — and what it doesn't

Modeled: the sandbox API surface (env/timer/world/land/trigger/coalition/
Group/Unit/StaticObject/missionCommands), a tiny test-populated unit world,
weapon SHOT→track→impact fakes, and a minimal MOOSE facade for plugins that
touch a few MOOSE classes. **Not modeled:** DCS AI, physics, weapons flight,
LoS, or the real MOOSE runtime. A green harness test means "the script runs
and does what it schedules"; whether the *sim* behaves still needs a fly.

## Running

```
pytest tests/lua
```

The only dependency is `lupa` (already in requirements.txt).

## Extending

1. Build a `DcsPluginHarness`, emit the plugin's config with
   `set_retribution_config(plugin_options={"<plugin>": {...}})`, then
   `load_plugin_script(...)` in the same order the mission's work orders would.
2. Populate the world (`add_group`/`add_airbase`/`add_static`), advance the
   clock (`advance_to`), fire events (`fire_shot`/`fire_birth`/`fire_hit`).
3. Assert on `records(...)` (explosions, texts, marks, menus, spawns, roe…)
   and finish with `assert_no_lua_errors()` — scheduled-function and event
   errors are captured, never swallowed.

When a plugin needs a sandbox call the stubs lack, add a minimal, DCS-shaped
fake to `dcs_stubs.lua` (keep the DCS conventions documented in its header:
Vec3 `{x, y=up, z}`, `land.getHeight` takes a Vec2, scheduler return-time
semantics).

`test_splashdamage_runtime.py` is the reference consumer.
