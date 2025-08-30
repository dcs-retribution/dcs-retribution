env.info("-----DCSRetribution|MOOSE Tiresias plugin - configuration start ------")

local exceptionset = SET_GROUP:New():FilterPrefixes({ "Convoy", "convoy", "FRONTLINE" }):FilterStart()
local blinder = TIRESIAS:New()
-- Setup different radius for activation around helo and airplane groups (applies to AI and humans)
blinder:SetActivationRanges(10, 25) -- defaults are 10, and 25
-- Setup engagement ranges for AAA (non-advanced SAM units like Flaks etc) and if you want them to be AIOff
blinder:SetAAARanges(60, true) -- defaults are 60, and true
blinder:AddExceptionSet(exceptionset)