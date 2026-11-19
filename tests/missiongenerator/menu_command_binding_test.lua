-- Lua 5.1 supplies MOOSE's legacy implicit vararg arg table; no source adapter.
-- Execute only inspected definitions, not the full mission/MOOSE initialization.
local function extract(first, last)
  local start = assert(MOOSE_SOURCE:find(first, 1, true), first)
  local finish = assert(MOOSE_SOURCE:find(last, start + #first, true), last)
  return MOOSE_SOURCE:sub(start, finish - 1)
end
local function run(first, last)
  assert(loadstring(extract(first, last), '@Moose.lua:' .. first))()
end
local errors, registrations, calls = {}, {}, {}
UTILS = {}
_ClassID = 0
BASE = { ClassName = 'BASE' }
function BASE:F() end
function BASE:E(value) errors[#errors + 1] = value end
function BASE:IsInstanceOf(name) return self.ClassName == name end
coalition = { side = { BLUE = 2, RED = 1 } }
timer = { getTime = function() return 1 end }
env = { info = function(message) errors[#errors + 1] = message end }
run('UTILS.DeepCopy=function(object)', 'UTILS.OneLineSerialize=function(tbl)')
run('function BASE:New()', 'local function getParent(Child)')
-- Include complete do/end blocks from MENU_BASE through delayed group commands.
run('MENU_INDEX={}', '\ndo\nMENU_BASE=')
run('do\nMENU_BASE={', '\nZONE_BASE={')

local function path(parent, text)
  local p = {}; for _, part in ipairs(parent or {}) do p[#p + 1] = part end
  p[#p + 1] = text; return p
end
local function register(scope, text, parent, callback)
  local p = path(parent, text)
  registrations[scope .. ':' .. table.concat(p, '/')] = callback
  return p
end
missionCommands = {
  addCommand = function(text, parent, fn) return register('mission', text, parent, fn) end,
  addCommandForCoalition = function(side, text, parent, fn) return register('coalition' .. side, text, parent, fn) end,
  addCommandForGroup = function(id, text, parent, fn) return register('group' .. id, text, parent, fn) end,
  addSubMenu = function(text, parent) return path(parent, text) end,
  addSubMenuForCoalition = function(_, text, parent) return path(parent, text) end,
  addSubMenuForGroup = function(_, text, parent) return path(parent, text) end,
  removeItem = function() end,
  removeItemForCoalition = function() end,
  removeItemForGroup = function() end,
}
local group = { GetID = function() return 17 end, GetName = function() return 'players' end, IsAlive = function() return true end }
local pilot1, pilot2 = {name='Pilot 1'}, {name='Pilot 2'}
local jtac1, jtac2 = {code=1687,target='A'}, {code=1681,target='B'}
local function handler(tag)
  return function(instance, pilot)
    calls[#calls + 1] = {tag=tag, instance=instance, pilot=pilot, code=instance.code, target=instance.target}
  end
end
local constructors = {
  {scope='mission', new=function(text, fn, ...) return MENU_MISSION_COMMAND:New(text, nil, fn, ...) end},
  {scope='coalition2', new=function(text, fn, ...) return MENU_COALITION_COMMAND:New(2, text, nil, fn, ...) end},
  {scope='group17', new=function(text, fn, ...) return MENU_GROUP_COMMAND:New(group, text, nil, fn, ...) end},
  {scope='group17', delayed=true, new=function(text, fn, ...) return MENU_GROUP_COMMAND_DELAYED:New(group, text, nil, fn, ...) end},
}
for index, case in ipairs(constructors) do
  local text = 'Status' .. index
  local command = case.new(text, handler('original'), jtac1, pilot1)
  if case.delayed then command:Set() end
  local callback = assert(registrations[case.scope .. ':' .. text])
  callback()
  assert(calls[#calls].instance == jtac1 and calls[#calls].pilot == pilot1, 'initial identity')
  assert(calls[#calls].tag == 'original', 'initial function')
  local reused = case.new(text, handler('replacement'), jtac2, pilot2)
  assert(reused == command, 'constructor must reuse same indexed command')
  assert(command.MenuCallHandler == callback, 'reuse must not replace registered callback')
  callback()
  assert(calls[#calls].tag == 'replacement', 'registered callback must use replacement function')
  assert(calls[#calls].instance == jtac2 and calls[#calls].pilot == pilot2, 'registered callback must use replacement arguments')
  jtac2.code = jtac2.code + 1; jtac2.target = 'changed' .. index
  callback()
  assert(calls[#calls].code == jtac2.code and calls[#calls].target == jtac2.target, 'current data, not a copied instance')
  local other = case.new('Other' .. index, handler('independent'), jtac1, pilot1)
  if case.delayed then other:Set() end
  registrations[case.scope .. ':Other' .. index]()
  assert(calls[#calls].instance == jtac1 and calls[#calls].pilot == pilot1, 'independent command')
  callback()
  assert(calls[#calls].instance == jtac2 and calls[#calls].pilot == pilot2 and calls[#calls].tag == 'replacement', 'no cross-command sharing')
  command:Refresh()
  registrations[case.scope .. ':' .. text]()
  assert(calls[#calls].instance == jtac2 and calls[#calls].pilot == pilot2, 'refresh preserves current binding')
end
assert(#errors == 0, 'unexpected MOOSE callback/menu error')
assert(#calls == 24, 'all four command types must execute six assertions each')
