-- qra_filter_test.lua
--
-- Standalone unit test for the task-type reaction filter in
-- resources/plugins/intercept/intercept-config.lua. QRA must react only to
-- air-to-ground taskings (Strike/BAI/OCA-Runway/OCA-Aircraft/Anti-ship/Armed
-- Recon) and ignore
-- CAP/sweep/escort/intercept/SEAD/CAS/DEAD/Air Assault/support, based on the
-- DCS group name.
--
-- Not run by CI (CI has no Lua). Run locally with:
--   lua    tests/missiongenerator/qra_filter_test.lua
--   luajit tests/missiongenerator/qra_filter_test.lua

local SCRIPT = "resources/plugins/intercept/intercept-config.lua"

-- Minimal global stubs the script touches at load time. We deliberately do NOT
-- set dcsRetribution.Intercept, so the module-level build block is skipped and
-- no Moose/mist machinery runs — the load just defines the helpers and returns
-- the test-export table.
dcsRetribution = {}
mist = { scheduleFunction = function() end }
timer = { getTime = function() return 0 end }
env = { info = function() end, warning = function() end }
BASE = { CreateEventTakeoff = function() end }

local M = assert(loadfile(SCRIPT))()
assert(M, "intercept-config.lua did not return its test-export table")
assert(type(M.group_reacts) == "function", "missing group_reacts export")
assert(type(M.cluster_has_react) == "function", "missing cluster_has_react export")

local failures = 0
local function check(label, got, want)
    if got ~= want then
        failures = failures + 1
        print(string.format("FAIL: %s -> got %s, want %s",
            label, tostring(got), tostring(want)))
    end
end

-- group_reacts: react-types => true
check("Strike",       M.group_reacts("TIGER Strike|5|8|F-16C_50|"), true)
check("BAI",          M.group_reacts("COLT BAI|5|3|0|"),            true)
check("OCA/Runway",   M.group_reacts("HAWK OCA/Runway|5|1|0|"),     true)
check("OCA/Aircraft", M.group_reacts("HAWK OCA/Aircraft|5|1|0|"),   true)
check("Anti-ship",    M.group_reacts("VIPER Anti-ship|5|2|0|"),     true)
check("Armed Recon",  M.group_reacts("SCOUT Armed Recon|5|5|0|"),   true)
-- custom-named flight: naming.py appends the task type, so it still classifies
check("custom-name-strike", M.group_reacts("Alpha Strike|5|8|0|"),  true)

-- group_reacts: ignore-types => false
check("TARCAP",        M.group_reacts("EAGLE TARCAP|5|7|0|"),        false)
check("BARCAP",        M.group_reacts("EAGLE BARCAP|5|7|0|"),        false)
check("SEAD",          M.group_reacts("WEASEL SEAD|5|4|0|"),         false)
check("CAS",           M.group_reacts("HOG CAS|5|6|0|"),             false)
check("Fighter sweep", M.group_reacts("EAGLE Fighter sweep|5|9|0|"), false)
check("Escort",        M.group_reacts("EAGLE Escort|5|9|0|"),        false)
check("Intercept",     M.group_reacts("Intercept|Tiyas|sq-abc|"),    false)
check("AEW&C",         M.group_reacts("SENTRY AEW&C|5|1|0|"),        false)
check("DEAD",          M.group_reacts("WEASEL DEAD|5|4|0|"),         false)
check("Air Assault",   M.group_reacts("HERC Air Assault|5|6|0|"),    false)

-- group_reacts: multi-word target name still parses the type suffix
check("multiword-strike", M.group_reacts("Al Dhafra Strike|5|8|0|"), true)
check("multiword-tarcap", M.group_reacts("Al Dhafra TARCAP|5|8|0|"), false)

-- group_reacts: malformed / no match => false
check("no-pipe",       M.group_reacts("garbage"),          false)
check("empty",         M.group_reacts(""),                 false)
check("nil",           M.group_reacts(nil),                false)
check("no-type-match", M.group_reacts("SomeGroup|5|1|0|"), false)
-- type word without the leading-space separator must NOT match
check("no-separator",  M.group_reacts("BAI|5|1|0|"),       false)
-- non-namegen name (no "|") that coincidentally ends in a react word must NOT
-- match — only pipe-delimited namegen ATO flights are classifiable
check("no-pipe-strike-suffix", M.group_reacts("Eagle Strike"),   false)
check("no-pipe-bai-suffix",    M.group_reacts("Reserve BAI"),    false)
check("leading-pipe",          M.group_reacts("|Strike|5|1|0|"), false)

-- cluster_has_react: fake DetectedItem whose Set:ForEachUnit iterates units,
-- each resolving to a group with GetName().
local function fake_item(group_names)
    local units = {}
    for _, gname in ipairs(group_names) do
        units[#units + 1] = {
            GetGroup = function()
                return { GetName = function() return gname end }
            end,
        }
    end
    return {
        Set = {
            ForEachUnit = function(_, fn)
                for _, u in ipairs(units) do fn(u) end
            end,
        },
    }
end

check("cluster-lone-cap",
    M.cluster_has_react(fake_item({ "EAGLE TARCAP|5|7|0|", "EAGLE BARCAP|5|1|0|" })),
    false)
check("cluster-escorted-strike",
    M.cluster_has_react(fake_item({ "EAGLE Escort|5|9|0|", "TIGER Strike|5|8|0|" })),
    true)
check("cluster-empty", M.cluster_has_react(fake_item({})), false)
check("cluster-nil",   M.cluster_has_react({}),            false)

-- pattern_escape: Retribution IADS group names contain "(" / ")" / "-" that
-- break Moose's pattern-based FilterPrefixes. Replicate Moose's matcher
-- (string.find with its own "-" -> "%-" gsub applied to the prefix) and assert
-- an escaped prefix matches the literal name while the raw prefix does not.
local function moose_matches(name, prefix)
    -- Mirror Moose SET_GROUP:FilterPrefixes (Moose.lua): string.find(name,
    -- gsub(prefix, "-", "%-"), 1) — NOT plain, so prefix is a Lua pattern.
    return string.find(name, (prefix:gsub("%-", "%%-")), 1) ~= nil
end

local paren_names = {
    "0041 | LION (EWR)",
    "0035 | ELEPHANT (Naval Two Ship)",
    "0114 | LORIKEET (S-300)",
    "0178 | OPOSSUM (Patriot)",
}
for _, name in ipairs(paren_names) do
    -- raw (unescaped) prefix fails to match because "(" / ")" are pattern captures
    check("raw-nomatch:" .. name, moose_matches(name, name), false)
    -- escaped prefix matches the literal name -> sensor lands in the SET_GROUP
    check("escaped-match:" .. name, moose_matches(name, M.pattern_escape(name)), true)
end

if failures == 0 then
    print("OK: all QRA filter assertions passed")
    os.exit(0)
else
    print(string.format("%d assertion(s) failed", failures))
    os.exit(1)
end
