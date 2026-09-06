-- dcs_atmos_probe.lua — DCS airfield elevation probe (tk dr-g1tk / dr-pu9z).
-- Dumps each airbase's land.getHeight (the QFE ground truth) + a small surface
-- atmosphere sample to dcs.log ([ATMOS] lines) and a JSON file. The Spec 1
-- diagnostic profiles (0–40k ft wind/temp/pressure ladders + map grid) have been
-- removed now that the wind/QNH questions are answered; feed the result to
-- scripts/dcs_airfield_elevations.py (apply). Expects a global `json` (bundled
-- json.lua, prepended by the generator).

local SCHEMA_VERSION = 1
local SURFACE_AGL_M = 10.0       -- match MOOSE ATIS sample height

local function log(msg)
  env.info("[ATMOS] " .. msg)
end

-- Fallback when io is sanitized (default DCS MissionScripting.lua strips io/lfs/os
-- from the mission env): stream the whole JSON to dcs.log in ordered chunks so the
-- run still yields data. Reassemble with `ingest_atmos_probe.py --log <dcs.log>`.
local function dump_to_log(payload)
  local CHUNK = 3000
  local total = #payload
  local n = math.floor((total + CHUNK - 1) / CHUNK)
  log(string.format("JSON-BEGIN bytes=%d chunks=%d", total, n))
  for i = 1, n do
    log(string.format("JSON %d/%d %s", i, n, string.sub(payload, (i - 1) * CHUNK + 1, i * CHUNK)))
  end
  log("JSON-END")
end

-- Resolve an output path, mirroring dcs_retribution.lua's discovery order.
-- Uses backslash path separators to match dcs_retribution.lua's Windows convention.
-- NOTE: unlike dcs_retribution.lua, we do not canWrite()-probe each candidate;
-- we accept the first non-empty candidate and let io.open report the error.
local function output_path()
  local name = "atmos_probe.json"
  local function join(dir)
    if dir:sub(-1) ~= "\\" then dir = dir .. "\\" end
    return dir .. name
  end
  if os then
    local env_dir = os.getenv("RETRIBUTION_EXPORT_DIR")
    if env_dir and #env_dir > 0 then return join(env_dir) end
  end
  if dcsRetribution and dcsRetribution.installPath then
    return join(dcsRetribution.installPath)
  end
  if os then
    local tmp = os.getenv("TEMP")
    if tmp and #tmp > 0 then return join(tmp) end
  end
  -- Last resort: DCS write dir (same as dcs_retribution.lua's final fallback).
  -- NOTE: confirm this path is accessible during TriggerStart in the live run.
  if lfs then
    return join(lfs.writedir() .. "Missions")
  end
  -- Absolute last resort if lfs is unavailable.
  return name
end

-- atmosphere.getWind* return a velocity Vec3 {x=North, y=Up, z=East} in m/s.
-- Convert to aviation "wind from" degrees + speed (m/s). Single helper so the
-- axis/bearing math lives in exactly one place (steady + turbulence share it).
-- bearing = atan2(East, North) = atan2(v.z, v.x); +180 => "from".
-- NOTE: assumes DCS Vec3 x=North, z=East — confirm axis mapping in live run vs ATIS.
local function vec_to_wind_sample(v)
  local speed = math.sqrt(v.x * v.x + v.z * v.z)
  local to_deg = math.deg(math.atan2(v.z, v.x))  -- heading the wind blows TO
  local from_deg = (to_deg + 180.0) % 360.0
  return { dir_from_deg = from_deg, speed_mps = speed }
end

local function wind_sample(point)
  return vec_to_wind_sample(atmosphere.getWind(point))
end

local function wind_turb_sample(point)
  return vec_to_wind_sample(atmosphere.getWindWithTurbulence(point))
end

-- atmosphere.getTemperatureAndPressure takes Vec3 {x, y=MSL alt, z}; returns K, Pa.
local function atmo_sample(x, z, alt_msl)
  local point = { x = x, y = alt_msl, z = z }
  local temp, press = atmosphere.getTemperatureAndPressure(point)  -- Kelvin, Pa
  return {
    alt_msl_m = alt_msl,
    wind = wind_sample(point),
    wind_turb = wind_turb_sample(point),
    temp_c = temp - 273.15,
    pressure_hpa = press / 100.0,
  }
end

-- pydcs/DCS wind layers as stored in the mission, read back for comparison.
-- NOTE: env.mission.weather.wind.atGround/at2000/at8000 keys verified against
-- pydcs mission XML; dir is "wind blows TO" in DCS, so +180 gives "from" degrees.
local function configured_weather()
  local w = env.mission.weather
  local function layer(l) return { dir_from_deg = (l.dir + 180.0) % 360.0, speed_mps = l.speed } end
  return {
    qnh_mmhg = w.qnh,
    qnh_inhg = w.qnh / 25.400002776728,
    temperature_c = (w.season and w.season.temperature) or 0,
    wind = {
      at_0m = layer(w.wind.atGround),
      at_2000m = layer(w.wind.at2000),
      at_8000m = layer(w.wind.at8000),
    },
  }
end

local function run()
  local airbases = {}
  -- world.getAirbases() returns a table of Airbase objects.
  -- NOTE: verify that pairs() iterates all entries (some DCS versions use
  -- consecutive integer keys; pairs vs ipairs both work for that case).
  for _, ab in pairs(world.getAirbases()) do
    local p = ab:getPoint()                 -- {x,y,z} world coords (y=MSL elev)
    local x, z = p.x, p.z
    -- land.getHeight takes Vec2 {x, y} where y is the world z-axis.
    -- NOTE: confirm this axis convention in the live run vs. known airbase elevations.
    local h = land.getHeight({ x = x, y = z })
    airbases[#airbases + 1] = {
      id = tostring(ab:getID()),
      name = ab:getName(),
      x = x, z = z,
      land_height_m = h,
      surface = atmo_sample(x, z, h + SURFACE_AGL_M),
    }
    log(string.format("airbase %s elev=%.1fm", ab:getName(), h))
  end

  -- Elevation-only probe: the per-altitude wind/temp/pressure ladders + map-grid
  -- columns (Spec 1 diagnosis) are no longer collected; `columns` stays empty so
  -- the dump schema is unchanged and the ingest/apply tools parse it as before.
  local dump = {
    schema_version = SCHEMA_VERSION,
    terrain = env.mission.theatre,
    configured_weather = configured_weather(),
    airbases = airbases,
    columns = {},
  }

  -- json:encode uses method-call syntax, matching dcs_retribution.lua's convention.
  local payload = json:encode(dump)

  -- io is nil when MissionScripting.lua sanitizes the mission env (DCS default).
  -- Don't crash: fall back to streaming the JSON into dcs.log.
  if io == nil then
    log("io is sanitized — cannot write a file from the mission environment.")
    log("For a JSON FILE: replace <DCS>/Scripts/MissionScripting.lua with")
    log("<retribution>/resources/scripts/MissionScripting.lua, then restart DCS.")
    log("For NOW: streaming the dump to this log; apply with: dcs_airfield_elevations.py apply --log <dcs.log>")
    dump_to_log(payload)
    return
  end

  local path = output_path()
  local fh, err = io.open(path, "w")
  if not fh then
    log("ERROR opening " .. tostring(path) .. ": " .. tostring(err))
    log("Streaming the dump to this log instead; apply with: dcs_airfield_elevations.py apply --log <dcs.log>")
    dump_to_log(payload)
    return
  end
  fh:write(payload)
  fh:close()
  log(string.format("wrote %d airbases, %d columns -> %s", #airbases, #columns, path))
end

local ok, err = pcall(run)
if not ok then log("FATAL: " .. tostring(err)) end
