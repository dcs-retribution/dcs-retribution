--[[
Big Eye Early Warning Radar script, moose based

new implementation by quelcertoleo
original EWRS script updated by Apple 30/11/2023
original EWRS concept by Steggles - https://github.com/Bob7heBuilder/EWRS

changelog
1.0.0 - default A2A BRAA instead of BULLS, tune threat levels to report civilian traffic, refactor to Ops.INTEL instead of DETECTION_UNITS
0.0.8 - added option to have either group name or NATO reporting name in report
0.0.7 - target heading to aspect Hot, Cold, Flanking, remove bulls reference, TTS compliant, add altitude cutoff, NCTR
0.0.6 - order contacts by distance
0.0.5 - added Speed cutoff to filter slow movers, Checked for client to be reported to being alive
0.0.4 - remove requirement for ZONE_POLYGON objects defining airspaces
0.0.3 - added GCI and 12-hour report format
0.0.2 - added friendly picture and bogey dope
0.0.1 - initial mvp, supports player preferences and reports contacts on schedule
]]
-- CONSTANTS *************************************************************************************

EWR = {}
EWR.version = "1.0.1-SNAPSHOT"
EWR.debug = false

_SETTINGS:SetPlayerMenuOff()
_SETTINGS:SetEraCold()
_SETTINGS:SetA2A_BRAA()
_SETTINGS:SetA2G_LL_DDM()

--[[
{
k:groupId
v:
[
    clientName,
    playerCoalition,
    reportFrequency,
    reportDistanceCutoff,
    reportEnabled,
    reportUnits,
    playerReportScheduler,
    isGciTaskingAvailable,
    playerGciScheduler,
    gciReportScheduler
]
}
]]
EWR.playerData = {}

EWR.radioMenusAdded = {}

-- Sets of detected groups
EWR.blueDetectedGroups = SET_GROUP:New()
EWR.redDetectedGroups = SET_GROUP:New()

-- Constants
EWR.blueCoalition = "blue"
EWR.redCoalition = "red"
EWR.minThreatLevel = -99
EWR.maxThreatLevel = 99
EWR.unitInternationalSystem = "isu"
EWR.unitImperial = "imp"

-- Report timings and settings
EWR.displayMessageTime = 10
EWR.displayMessageTimeShort = 3
EWR.maxReportUnits = 5
EWR.highReportFrequencyPreference = 15 -- can't be less than EWRS.displayMessageTime
EWR.defaultReportFrequencyPreference = 30
EWR.lowReportFrequencyPreference = 60
EWR.gciReportFrequency = 5
EWR.defaultCutoffDistance = UTILS.NMToMeters(100)
EWR.defaultEnableReportPreference = true

-- GCI
-- {k:playerGroupId, v:[assignedUnit]}
EWR.gciAssignedGroups = {}

-- DETECTION Blue
EWR.blueHasDLINK = false
EWR.blueHasRWR = true
EWR.blueHasIRST = false
-- DETECTION Red
EWR.redHasDLINK = false
EWR.redHasRWR = false
EWR.redHasIRST = false

EWR.isAvailableNCTR = false
EWR.reportUnitNameNATO = true

-- in case of respawned units, use keepUnitNames so that they can be added to the filter dinamically
blueDetectionGroup = SET_GROUP:New():FilterCoalitions(EWR.blueCoalition):FilterStart()
blueIntel = INTEL:New(blueDetectionGroup, EWR.blueCoalition, "Blue BigEye")
blueIntel:SetClusterAnalysis(true, false, false)
blueIntel:SetDetectionTypes(true, true, true, blueHasIRST, blueHasRWR, blueHasDLINK)
blueIntel:SetFilterCategory({ Unit.Category.AIRPLANE, Unit.Category.HELICOPTER })
if EWR.debug then
    blueIntel:SetVerbosity(2)
else
    blueIntel:SetVerbosity(0)
end
blueIntel:__Start(2)

redDetectionGroup = SET_GROUP:New():FilterCoalitions(EWR.redCoalition):FilterStart()
redIntel = INTEL:New(redDetectionGroup, EWR.redCoalition, "Red BigEye")
redIntel:SetClusterAnalysis(true, false, false)
redIntel:SetDetectionTypes(true, true, true, redHasIRST, redHasRWR, redHasDLINK)
redIntel:SetFilterCategory({ Unit.Category.AIRPLANE, Unit.Category.HELICOPTER })
if EWR.debug then
    redIntel:SetVerbosity(2)
else
    redIntel:SetVerbosity(0)
end
redIntel:__Start(2)

-- DETECTION CALLBACKS ***
function blueIntel:OnAfterNewContact(From, Event, To, Contact)
    local detectedGroup = blueIntel:GetContactGroup(Contact)
    if not EWR.blueDetectedGroups:IsInSet(detectedGroup) then
        EWR.blueDetectedGroups:AddGroup(detectedGroup)
    end
    if EWR.debug then
        env.info(string.format("BigEye BLUE detected %s", detectedGroup:GetName()))
    end
end

function redIntel:OnAfterNewContact(From, Event, To, Contact)
    local detectedGroup = redIntel:GetContactGroup(Contact)
    if not EWR.redDetectedGroups:IsInSet(detectedGroup) then
        EWR.redDetectedGroups:AddGroup(detectedGroup)
    end
    if EWR.debug then
        env.info(string.format("BigEye RED detected %s", detectedGroup:GetName()))
    end
end

-- UTILS / MISC (yeah, misc and utils where stuff you don't know the concern goes) ***

-- @param DCS#Vec2 Vec2 objects to calculate distance
-- @return #number distance in meters
function EWR.getDistance(object1Vec2, object2Vec2)
    -- TODO for some reason the input params might be null, reasons are unclear and might be DCS being DCS
    if object1Vec2 == nil or object2Vec2 == nil then
        env.info("BigEye caught null objectvec in EWR.getDistance")
        return 0
    end
    local xDiff = object1Vec2.x - object2Vec2.x
    local yDiff = object1Vec2.y - object2Vec2.y
    local distanceInMeters = math.sqrt(xDiff * xDiff + yDiff * yDiff)
    return distanceInMeters
end

-- @param DCS#Vec2 objectFromVec2 the vertex
-- @param DCS#Vec2 objectToVec2 the destination
-- @return #number angle in degrees
function EWR.getAbsoluteBearing(objectFromVec2, objectToVec2)
    -- TODO for some reason the input params might be null, reasons are unclear and might be DCS being DCS
    if objectFromVec2 == nil or objectToVec2 == nil then
        env.info("BigEye caught null objectvec in EWR.getAbsoluteBearing")
        return 0
    end
    -- Calculate the relative bearing
    local bearing = math.atan2(objectToVec2.y - objectFromVec2.y, objectToVec2.x - objectFromVec2.x)

    -- Convert the bearing to degrees
    bearing = math.deg(bearing)

    -- Make sure the bearing is positive
    bearing = (bearing + 360) % 360
    return UTILS.Round(bearing, -1)
end

-- @param DCS#Vec2 objectFromVec2 the vertex
-- @param DCS#Vec2 objectToVec2 the destination
-- @return #number angle in degrees
function EWR.getRelativeBearing(objectFromVec2, objectToVec2, objectFromHeading)
    -- TODO for some reason the input params might be null, reasons are unclear and might be DCS being DCS
    if objectFromVec2 == nil or objectToVec2 == nil or objectFromHeading == nil then
        env.info("BigEye caught null objectvec in EWR.getRelativeBearing")
        return 0
    end
    -- Calculate the relative bearing
    local bearing = math.atan2(objectToVec2.y - objectFromVec2.y, objectToVec2.x - objectFromVec2.x)
    env.info("bearing " .. bearing)
    -- Convert the bearing to degrees
    bearing = math.deg(bearing)
    env.info("bearing deg " .. bearing)

    -- Make sure the bearing is positive
    bearing = (bearing - objectFromHeading + 360) % 360
    env.info("bearing positive " .. bearing)

    return UTILS.Round(bearing, -1)
end

--- Heading Degrees (0-360) to 12-hour format
-- @param #number bearing is the bearing in degrees
-- @return #string in 12-hour format, e.g. "11 o'clock"
function EWR.getBearingToClockFormat(bearing)

    local bearingClock = math.floor(bearing / 30)

    if bearingClock == 0 then
        bearingClock = 12
    end

    return string.format("%d o'clock", bearingClock)
end

-- @param #SET_UNIT setUnit, in our case the SET_UNITS that contain detected units
-- @return #Wrapper.Unit#UNIT the highest threat in the coalition airspace
function EWR.assignNearestThreatToPlayer(groupId)

    local playerPreferences = EWR.playerData[groupId]
    local playerCoalition = playerPreferences["playerCoalition"]
    local assignedTargetGroup
    if playerCoalition == EWR.blueCoalition then
        assignedTargetGroup = EWR.findAndAssignNearestThreat(groupId, EWR.blueDetectedGroups)
    else
        assignedTargetGroup = EWR.findAndAssignNearestThreat(groupId, EWR.redDetectedGroups)
    end
    if assignedTargetGroup ~= nil then
        trigger.action.outTextForGroup(groupId, string.format("Assigned target %s", assignedTargetGroup:GetID()), 10, false)
        local gciAssignTargetScheduler = EWR.playerData[groupId]["playerGciScheduler"]
        gciAssignTargetScheduler:Stop()
        local gciTargetReportScheduler = EWR.getGciTargetReportSchedulerForPlayerGroup(groupId, assignedTargetGroup)
        gciTargetReportScheduler:Start()
    else
        trigger.action.outTextForGroup(groupId, "Scanning contacts for GCI tasking", 10, false)
    end
end

-- @param #number groupId of client group
-- @param #SET_UNIT setUnit, in our case the SET_UNITS that contain detected units
-- @param #ZONE_POLYGON the airspace zone
-- @return #Wrapper.Unit#UNIT the assigned target unit
function EWR.findAndAssignNearestThreat(playerGroupId, detectedGroup)

    local clientName = EWR.playerData[playerGroupId]["clientName"]
    local clientUnit = UNIT:FindByName(clientName)
    local clientVec2 = clientUnit:GetVec2()

    local clientPreferences = EWR.playerData[playerGroupId]
    local clientDistanceCutoff = clientPreferences["reportDistanceCutoff"]
    local unitDistance = clientDistanceCutoff

    detectedGroup:ForEachGroup(
            function(group)
                if group ~= nil and group:IsAlive() then
                    if group:GetThreatLevel() > EWR.minThreatLevel and
                            unitDistance <= clientDistanceCutoff and
                            EWR.getDistance(clientVec2, group:GetVec2()) < unitDistance then

                        unitDistance = EWR.getDistance(clientVec2, group:GetVec2())
                        EWR.gciAssignedGroups[playerGroupId] = group
                    end
                end
            end
    )

    return EWR.gciAssignedGroups[playerGroupId]
end

-- PREFERENCES ***

-- @param #number groupId of client group
-- @param #number unitPreference EWRS.playerEwrPreferences[groupId]["reportUnits"]
function EWR.setUnitPreference(groupId, unitPreference)
    if EWR.debug then
        env.info(string.format("BigEye group %s set unit preference to %s", groupId, unitPreference))
    end
    local playerPreferences = EWR.playerData[groupId]
    playerPreferences["reportUnits"] = unitPreference
    local newReportScheduler = EWR.getReportSchedulerForPlayerGroup(groupId)
    EWR.replacePlayerReportSchedulerWith(groupId, newReportScheduler)
    trigger.action.outTextForGroup(groupId, string.format("Unit to %s", unitPreference), 10, false)
end

-- @param #number groupId of client group
-- @param #string reportFrequencyPreference EWRS.playerEwrPreferences[groupId]["reportFrequency"]
function EWR.setReportFrequencyPreference(groupId, reportFrequencyPreference)
    if EWR.debug then
        env.info(string.format("BigEye group %s set preference report frequency to %2d", groupId, reportFrequencyPreference))
    end
    local playerPreferences = EWR.playerData[groupId]
    playerPreferences["reportFrequency"] = reportFrequencyPreference
    local newReportScheduler = EWR.getReportSchedulerForPlayerGroup(groupId)
    EWR.replacePlayerReportSchedulerWith(groupId, newReportScheduler)
    trigger.action.outTextForGroup(groupId, string.format("Frequency to %2ds", reportFrequencyPreference), 10, false)
end

-- @param #number groupId of client group
-- @param #string cutoffDistancePreference EWRS.playerEwrPreferences[groupId]["reportDistanceCutoff"]
function EWR.setCutoffDistancePreference(groupId, cutoffDistancePreference)
    if EWR.debug then
        env.info(string.format("BigEye group %s set cutoff distance %2d", groupId, cutoffDistancePreference))
    end
    local playerPreferences = EWR.playerData[groupId]
    playerPreferences["reportDistanceCutoff"] = cutoffDistancePreference
    local newReportScheduler = EWR.getReportSchedulerForPlayerGroup(groupId)
    EWR.replacePlayerReportSchedulerWith(groupId, newReportScheduler)
    trigger.action.outTextForGroup(groupId, "Cutoff distance setting applied", 10, false)
end

-- @param #number groupId of client group
-- @param #boolean reportEnabledPreference boolean, will start or stop player scheduler in EWR.playerEwrPreferences[groupId]["playerReportScheduler"]
function EWR.setReportEnabledPreference(groupId, reportEnabledPreference)
    if EWR.debug then
        env.info(string.format("BigEye group %s set preference report enable %s", groupId, tostring(reportEnabledPreference)))
    end
    local playerReportScheduler = EWR.playerData[groupId]["playerReportScheduler"]
    if reportEnabledPreference then
        trigger.action.outTextForGroup(groupId, "Enable contact report", 10, false)
        playerReportScheduler:Start()
    else
        trigger.action.outTextForGroup(groupId, "Disable contact report", 10, false)
        playerReportScheduler:Stop()
    end
    EWR.playerData[groupId]["reportEnabled"] = reportEnabledPreference
end

-- @param #number groupId of client group
-- @param #boolean reportEnabledPreference boolean, will start or stop player scheduler in EWR.playerEwrPreferences[groupId]["playerReportScheduler"]
function EWR.setGciTaskingAvailablePreference(groupId, gciEnabledPreference)
    if EWR.debug then
        env.info(string.format("BigEye group %s set preference GCI available %s", groupId, tostring(gciEnabledPreference)))
    end
    local playerReportScheduler = EWR.playerData[groupId]["playerReportScheduler"]
    local playerGciAssignTargetScheduler = EWR.playerData[groupId]["playerGciScheduler"]
    local playerGciReportScheduler = EWR.playerData[groupId]["gciReportScheduler"]
    if gciEnabledPreference then
        trigger.action.outTextForGroup(groupId, "Enable GCI tasking, stopping reports", 10, false)
        playerReportScheduler:Stop()
        playerGciAssignTargetScheduler:Start()
    else
        trigger.action.outTextForGroup(groupId, "Disable GCI tasking", 10, false)
        playerGciAssignTargetScheduler:Stop()
        playerGciReportScheduler:Stop()
        EWR.gciAssignedGroups[groupId] = nil
    end
    EWR.playerData[groupId]["isGciTaskingAvailable"] = gciEnabledPreference
end

-- SCHEDULERS ***

-- @param #number groupId of client group
-- @param #table playerPreferences EWR.playerEwrPreferences[groupId]
-- @return #SCHEDULER
function EWR.getReportSchedulerForPlayerGroup(playerGroupId)
    local playerPreferences = EWR.playerData[playerGroupId]
    local playerReportScheduler = SCHEDULER:New(nil,
            function()
                local isOnDemandReport = false
                EWR.printBogeyReport(playerGroupId, isOnDemandReport)
            end, {}, 0, playerPreferences["reportFrequency"], 0)
    return playerReportScheduler
end

-- @param #number groupId of client group
-- @param #table playerPreferences EWR.playerEwrPreferences[groupId]
-- @return #SCHEDULER
function EWR.getGciSchedulerForPlayerGroup(groupId)
    local gciAssignTargetFrequency = 60
    local playerGciScheduler = SCHEDULER:New(nil,
            function()
                EWR.assignNearestThreatToPlayer(groupId)
            end, {}, 0, gciAssignTargetFrequency, 0)
    EWR.playerData[groupId]["playerGciScheduler"] = playerGciScheduler
    return playerGciScheduler
end

-- @param #number groupId of client group
function EWR.getGciTargetReportSchedulerForPlayerGroup(groupId, assignedTargetUnit)
    local playerGciScheduler = SCHEDULER:New(nil,
            function()
                EWR.printGciReport(groupId, assignedTargetUnit)
            end, {}, 0, EWR.displayMessageTimeShort, 0)
    EWR.playerData[groupId]["gciReportScheduler"] = playerGciScheduler
    return playerGciScheduler
end

-- @param #number groupId of client group
-- @param #SCHEDULER the new scheduler with modified player preferences, stop the old one and start a new scheduler
function EWR.replacePlayerReportSchedulerWith(groupId, newReportScheduler)
    local playerPreferences = EWR.playerData[groupId]
    local playerReportScheduler = playerPreferences["playerReportScheduler"]
    playerReportScheduler:Stop()
    playerPreferences["playerReportScheduler"] = newReportScheduler
    playerReportScheduler = playerPreferences["playerReportScheduler"]
    playerReportScheduler:Start()
end

-- REPORTS ***

-- @param #number playerGroupId of client group
-- @param #Wrapper.Unit#UNIT assignedTargetUnit is the unit to generate report of
function EWR.printGciReport(groupId, assignedTargetGroup)
    if assignedTargetGroup == nil or assignedTargetGroup:GetID() == nil then
            env.info("BigEye assignedTargetGroup is null")
        return
    end
    if EWR.debug then
        env.info(string.format("BigEye GCI report for group %3d, %s", groupId, assignedTargetGroup:GetID()))
    end

    local clientName = EWR.playerData[groupId]["clientName"]
    local clientUnit = UNIT:FindByName(clientName)
    local clientVec2 = clientUnit:GetVec2()

    local clientPreferences = EWR.playerData[groupId]
    if assignedTargetGroup ~= nil and assignedTargetGroup:IsAlive() then
        local assignedTargetUnitVec2 = assignedTargetGroup:GetVec2()
        local assignedTargetUnitDistance = EWR.getDistance(clientVec2, assignedTargetUnitVec2)
        local isAltitudeFromGround = false
        local clientAltitude = clientUnit:GetAltitude(isAltitudeFromGround)
        local assignedTargetAltitude = assignedTargetGroup:GetAltitude(isAltitudeFromGround)

        local unitDistanceToString
        if clientPreferences["reportUnits"] == EWR.unitImperial then
            unitDistanceToString = string.format("%03d miles", UTILS.Round(UTILS.MetersToNM(assignedTargetUnitDistance), 0))
        else
            unitDistanceToString = string.format("%03d kilometers", UTILS.Round(assignedTargetUnitDistance / 1000, 0))
        end

        if (assignedTargetUnitDistance <= UTILS.NMToMeters(5)) then

            local bearingInDegrees = EWR.getRelativeBearing(clientVec2, assignedTargetUnitVec2, clientUnit:GetHeading())
            local bearingInClockFormat = EWR.getBearingToClockFormat(bearingInDegrees)

            local relativeAltitude = ""
            if clientAltitude - assignedTargetAltitude > 1000 then
                relativeAltitude = "low"
            elseif clientAltitude - assignedTargetAltitude < -1000 then
                relativeAltitude = "high"
            end

            local unitTextReport = string.format("%s %s | %s", bearingInClockFormat, relativeAltitude, unitDistanceToString)
            trigger.action.outTextForGroup(groupId, unitTextReport, EWR.displayMessageTimeShort, false)
        else
            local altitudeString
            if assignedTargetAltitude == nil then
                altitudeString = "NA"
            elseif assignedTargetAltitude < 1000 then
                altitudeString = "low"
            else
                if clientPreferences["reportUnits"] == EWR.unitImperial then
                    altitudeString = string.format("%02d thousand", UTILS.Round(UTILS.MetersToFeet(assignedTargetAltitude), -3) / 1000)
                else
                    altitudeString = string.format("%02d thousand", UTILS.Round(assignedTargetAltitude, -2) / 1000)
                end
            end

            local bearing = EWR.getAbsoluteBearing(clientVec2, assignedTargetUnitVec2)
            local UnitCoordinate = assignedTargetGroup:GetCoordinate()
            local ReferenceCoordinate = COORDINATE:NewFromVec2(clientVec2)
            local aspect = UnitCoordinate:ToStringAspect(ReferenceCoordinate)

            local unitTextReport = string.format(
                    "%03d | %s | %s | %s",
                    bearing,
                    unitDistanceToString,
                    altitudeString,
                    aspect)

            trigger.action.outTextForGroup(groupId, unitTextReport, EWR.displayMessageTimeShort, false)
        end
    else
        trigger.action.outTextForGroup(groupId, "Target destroyed, good job", EWR.displayMessageTime, false)
        EWR.setGciTaskingAvailablePreference(groupId, false)
    end
end

-- @param #number groupId of client group
-- @param #string clientName string the name of the client group (and unit) as defined in Mission Editor
-- @param #string EWR.blueCoalition / EWR.redCoalition
-- @param #boolean isOnDemand boolean used to print "clean" when report has been explictly requested and no units around, if it's scheduled report then stay quiet
function EWR.printBogeyReport(playerGroupId, isOnDemand)

    local clientName = EWR.playerData[playerGroupId]["clientName"]
    local playerCoalition = EWR.playerData[playerGroupId]["playerCoalition"]

    if EWR.debug then
        env.info(string.format("BigEye report for group %s", playerGroupId))
    end
    local client = CLIENT:FindByName(clientName)
    if not client:IsAlive() then
        return
    end
    if isOnDemand then
        if playerCoalition == EWR.blueCoalition then
            if EWR.blueDetectedGroups:Count() == 0 then
                trigger.action.outTextForGroup(playerGroupId, "clean", EWR.displayMessageTime, false)
                return
            end
        else
            if EWR.redDetectedGroups:Count() == 0 then
                trigger.action.outTextForGroup(playerGroupId, "clean", EWR.displayMessageTime, false)
                return
            end
        end
    end

    local clientPreferences = EWR.playerData[playerGroupId]
    local clientDistanceCutoff = clientPreferences["reportDistanceCutoff"]

    local contactReport = REPORT:New("")
    local clientUnit = UNIT:FindByName(clientName)
    local referenceVec2 = clientUnit:GetVec2()
    local contactsTable = {}
    local contactCounter = 1
    local tableReportCount = 0

    if playerCoalition == EWR.blueCoalition then
        EWR.blueDetectedGroups:ForEachGroup(
                function(group)
                    if group ~= nil and group:IsAlive() then
                        local unitDistance = EWR.getDistance(referenceVec2, group:GetVec2())
                        if group:GetThreatLevel() > EWR.minThreatLevel and unitDistance < clientDistanceCutoff then

                            contactsTable[contactCounter] = {}
                            contactsTable[contactCounter].groupname = group:GetName()
                            contactsTable[contactCounter].distance = unitDistance
                            contactCounter = contactCounter + 1

                            local function sortTableByDistance(unit1, unit2)
                                return unit2.distance > unit1.distance
                            end
                            table.sort(contactsTable, sortTableByDistance)

                        end
                    end
                end
        )
    else
        EWR.redDetectedGroups:ForEachGroup(
                function(group)
                    if group ~= nil and group:IsAlive() then
                        local unitDistance = EWR.getDistance(referenceVec2, group:GetVec2())
                        if group:GetThreatLevel() > EWR.minThreatLevel and unitDistance < clientDistanceCutoff then

                            contactsTable[contactCounter] = {}
                            contactsTable[contactCounter].groupname = group:GetName()
                            contactsTable[contactCounter].distance = unitDistance
                            contactCounter = contactCounter + 1

                            local function sortTableByDistance(unit1, unit2)
                                return unit2.distance > unit1.distance
                            end
                            table.sort(contactsTable, sortTableByDistance)

                        end
                    end
                end
        )
    end

    for i = 1, #contactsTable do
        if i == EWR.maxReportUnits + 1 then
            break
        end
        local bogeyContact = GROUP:FindByName(contactsTable[i].groupname)
        if bogeyContact ~= nil and bogeyContact:IsAlive() then
            local bogeyContactReport = EWR.getTextReportForGroup(bogeyContact, clientPreferences, referenceVec2, false)
            contactReport:Add(bogeyContactReport)
            tableReportCount = tableReportCount + 1
        end
    end

    if playerCoalition == EWR.blueCoalition and tableReportCount > 0 then
        trigger.action.outTextForGroup(playerGroupId, contactReport:Text(), EWR.displayMessageTime, false)
    end
    if playerCoalition == EWR.redCoalition and tableReportCount > 0 then
        trigger.action.outTextForGroup(playerGroupId, contactReport:Text(), EWR.displayMessageTime, false)
    end
end

-- @param #number groupId of client group
-- @param #string clientName string the name of the client group (and unit) as defined in Mission Editor
-- @param #string playerCoalition EWR.redCoalition / EWR.blueCoalition
function EWR.printFriendliesReport(playerGroupId)

    local clientName = EWR.playerData[playerGroupId]["clientName"]
    local playerCoalition = EWR.playerData[playerGroupId]["playerCoalition"]

    if EWR.debug then
        env.info(string.format("BigEye find friendlies for %3d %s", playerGroupId, clientName))
    end
    -- cannot use { Unit.Category.AIRPLANE, Unit.Category.HELICOPTER } here, inconsistent API with others
    local friendlyUnitSet = SET_GROUP
            :New()
            :FilterActive(true)
            :FilterCoalitions(playerCoalition)
            :FilterCategories({ "plane", "helicopter" })
            :FilterOnce()
    -- remove client unit from set
    local clientUnit = UNIT:FindByName(clientName)
    local clientGroupName = clientUnit:GetGroup():GetName()
    friendlyUnitSet:RemoveGroupsByName(clientGroupName)

    if friendlyUnitSet:CountAlive() == 0 then
        trigger.action.outTextForGroup(playerGroupId, "no friendlies", EWR.displayMessageTime, false)
        return
    end

    local clientUnitVec2 = clientUnit:GetVec2()

    local friendliesTable = {}
    local counter = 1
    friendlyUnitSet:ForEachGroup(
            function(group)
                friendliesTable[counter] = {}
                friendliesTable[counter].groupname = group:GetName()
                local unitDistance = EWR.getDistance(clientUnitVec2, group:GetVec2())
                friendliesTable[counter].distance = unitDistance
                counter = counter + 1
            end
    )

    local function sortTableByDistance(unit1, unit2)
        return unit2.distance > unit1.distance
    end
    table.sort(friendliesTable, sortTableByDistance)

    local friendlyReport = REPORT:New("Friendly picture")
    local clientPreferences = EWR.playerData[playerGroupId]
    for i = 1, #friendliesTable do
        if i == EWR.maxReportUnits + 1 then
            break
        end
        local friendlyGroup = GROUP:FindByName(friendliesTable[i].groupname)
        if friendlyGroup ~= nil and friendlyGroup:IsAlive() then
            local friendlyTextReport = EWR.getTextReportForGroup(friendlyGroup, clientPreferences, clientUnitVec2, true)
            friendlyReport:Add(friendlyTextReport)
        end
    end
    trigger.action.outTextForGroup(playerGroupId, friendlyReport:Text(), EWR.displayMessageTime, false)
end

-- @param #Wrapper.Unit#UNIT unit is the unit to generate report of
-- @param #table clientPreferences EWRS.playerEwrPreferences[groupId]
-- @param #DCS#Vec2 referenceVec2 Vec2 used to calculate relative distance, heading, tracking
-- @return #string with report entry for @param unit
function EWR.getTextReportForGroup(group, clientPreferences, referenceVec2, isFriendlyReport)
    if EWR.debug then
        if group == nil or clientPreferences == nil or referenceVec2 == nil then
            env.info("BigEye getTextReportForGroup caught nil object")
            return
        end
        env.info(string.format("BigEye prepare text report for %s", group:GetName()))
    end

    local isAltitudeFromGround = false
    local unitAltitude = group:GetAltitude(isAltitudeFromGround)
    local altitudeString
    if unitAltitude == nil then
        altitudeString = "NA               " -- watch for formatting here, spaces count
    elseif unitAltitude < 1000 then
        altitudeString = "low              " -- watch for formatting here, spaces count
    else
        if clientPreferences["reportUnits"] == EWR.unitImperial then
            altitudeString = string.format("%02d thousand", UTILS.Round(UTILS.MetersToFeet(unitAltitude), -3) / 1000)
        else
            altitudeString = string.format("%02d thousand", UTILS.Round(unitAltitude, -2) / 1000)
        end
    end

    local unitVec2 = group:GetVec2()
    local bearing = EWR.getAbsoluteBearing(referenceVec2, unitVec2)
    local unitDistance = EWR.getDistance(unitVec2, referenceVec2)
    local unitDistanceToString
    if clientPreferences["reportUnits"] == EWR.unitImperial then
        unitDistanceToString = string.format("%03d miles", UTILS.Round(UTILS.MetersToNM(unitDistance), 0))
    else
        unitDistanceToString = string.format("%03d kilometers", UTILS.Round(unitDistance / 1000, 0))
    end

    -- collect group coordinates and defensive logs
    local UnitCoordinate = group:GetCoordinate()
    if UnitCoordinate == nil then
        env.info("BigEye UnitCoordinate is nil")
        return
    end
    if EWR.debug then
        env.info("BigEye UnitCoordinate heading " .. UnitCoordinate:GetHeading())
    end
    local ReferenceCoordinate = COORDINATE:NewFromVec2(referenceVec2)
    local aspect
    if EWR.debug and ReferenceCoordinate == nil then
        env.info("BigEye ReferenceCoordinate is nil")
        aspect = "ERROR"
    else
        aspect = UnitCoordinate:ToStringAspect(ReferenceCoordinate)
    end

    local groupName
    if isFriendlyReport or EWR.isAvailableNCTR then
        if EWR.reportUnitNameNATO then
            groupName = string.format("| %2d %s", group:CountAliveUnits(), group:GetNatoReportingName())
        else
            groupName = string.format("| %2d %s", group:CountAliveUnits(), group:GetTypeName())
        end
    else
        groupName = ""
    end

    local unitTextReport = string.format(
            "%03d | %s | %s | %s %s",
            bearing,
            unitDistanceToString,
            altitudeString,
            aspect,
            groupName)

    return unitTextReport
end

-- SETUP CLIENTS ***
function EWR.setupClients()
    local bluePlayerClients = SET_CLIENT:New():FilterCoalitions(EWR.blueCoalition):FilterActive(true):FilterOnce()
    bluePlayerClients:ForEachClient(
            function(client)
                local playerGroupId = client:GetClientGroupID()
                if EWR.radioMenusAdded[playerGroupId] == nil then
                    EWR.setupClientsHelper(playerGroupId, client, EWR.blueCoalition)
                end
            end
    )
    local redPlayerClients = SET_CLIENT:New():FilterCoalitions(EWR.redCoalition):FilterActive(true):FilterOnce()
    redPlayerClients:ForEachClient(
            function(client)
                local playerGroupId = client:GetClientGroupID()
                if EWR.radioMenusAdded[playerGroupId] == nil then
                    EWR.setupClientsHelper(playerGroupId, client, EWR.redCoalition)
                end
            end
    )
end

function EWR.setupClientsHelper(playerGroupId, client, playerCoalition)
    if EWR.debug then
        env.info(string.format("BigEye client setup for group %s %s", playerGroupId, client:GetName()))
    end

    local reportUnit
    if playerCoalition == EWR.redCoalition then
        reportUnit = EWR.unitInternationalSystem
    else
        reportUnit = EWR.unitImperial
    end

    EWR.playerData[playerGroupId] = {
        groupId = playerGroupId,
        clientName = client:GetName(),
        playerCoalition = playerCoalition,
        reportFrequency = EWR.defaultReportFrequencyPreference,
        reportDistanceCutoff = EWR.defaultCutoffDistance,
        reportEnabled = EWR.defaultEnableReportPreference,
        reportUnits = reportUnit,
        playerReportScheduler = nil,
        isGciTaskingAvailable = false,
        playerGciScheduler = nil,
        gciReportScheduler = nil
    }
    EWR.playerData[playerGroupId]["playerReportScheduler"] = EWR.getReportSchedulerForPlayerGroup(playerGroupId)
    EWR.playerData[playerGroupId]["playerGciScheduler"] = EWR.getGciSchedulerForPlayerGroup(playerGroupId)
    EWR.playerData[playerGroupId]["playerGciScheduler"]:Stop()

    local isOnDemandReport = true

    local MenuRoot = missionCommands.addSubMenuForGroup(playerGroupId, "BigEye EWR")

    missionCommands.addCommandForGroup(
            playerGroupId, "Contact Report", MenuRoot, EWR.printBogeyReport, playerGroupId, isOnDemandReport)
    missionCommands.addCommandForGroup(
            playerGroupId, "Friendly Picture", MenuRoot, EWR.printFriendliesReport, playerGroupId)

    local gciMenuRoot = missionCommands.addSubMenuForGroup(
            playerGroupId, "GCI Tasking", MenuRoot)
    missionCommands.addCommandForGroup(
            playerGroupId, "available for tasking", gciMenuRoot, EWR.setGciTaskingAvailablePreference, playerGroupId, true)
    missionCommands.addCommandForGroup(
            playerGroupId, "tasking out", gciMenuRoot, EWR.setGciTaskingAvailablePreference, playerGroupId, false)

    local ewrsMenuRoot = missionCommands.addSubMenuForGroup(playerGroupId, "Preferences", MenuRoot)

    local ewrsReportsMenuRoot = missionCommands.addSubMenuForGroup(
            playerGroupId, "Reports", ewrsMenuRoot)
    missionCommands.addCommandForGroup(
            playerGroupId, "enable contact reports", ewrsReportsMenuRoot, EWR.setReportEnabledPreference, playerGroupId, true)
    missionCommands.addCommandForGroup(
            playerGroupId, "disable contact reports", ewrsReportsMenuRoot, EWR.setReportEnabledPreference, playerGroupId, false)

    local ewrsUnitsMenuRoot = missionCommands.addSubMenuForGroup(
            playerGroupId, "Units", ewrsMenuRoot)
    missionCommands.addCommandForGroup(
            playerGroupId, "unit imperial", ewrsUnitsMenuRoot, EWR.setUnitPreference, playerGroupId, EWR.unitImperial)
    missionCommands.addCommandForGroup(
            playerGroupId, "unit metric", ewrsUnitsMenuRoot, EWR.setUnitPreference, playerGroupId, EWR.unitInternationalSystem)

    local ewrsFrequencyMenuRoot = missionCommands.addSubMenuForGroup(
            playerGroupId, "Frequency", ewrsMenuRoot)
    missionCommands.addCommandForGroup(
            playerGroupId, "high frequency reports", ewrsFrequencyMenuRoot, EWR.setReportFrequencyPreference, playerGroupId, EWR.highReportFrequencyPreference)
    missionCommands.addCommandForGroup(
            playerGroupId, "default frequency reports", ewrsFrequencyMenuRoot, EWR.setReportFrequencyPreference, playerGroupId, EWR.defaultReportFrequencyPreference)
    missionCommands.addCommandForGroup(
            playerGroupId, "low frequency reports", ewrsFrequencyMenuRoot, EWR.setReportFrequencyPreference, playerGroupId, EWR.lowReportFrequencyPreference)

    local ewrsCutoffDistanceMenuRoot = missionCommands.addSubMenuForGroup(
            playerGroupId, "Cutoff Distance", ewrsMenuRoot)
    missionCommands.addCommandForGroup(
            playerGroupId, "200 nm", ewrsCutoffDistanceMenuRoot, EWR.setCutoffDistancePreference, playerGroupId, UTILS.NMToMeters(200))
    missionCommands.addCommandForGroup(
            playerGroupId, "100 nm", ewrsCutoffDistanceMenuRoot, EWR.setCutoffDistancePreference, playerGroupId, UTILS.NMToMeters(100))
    missionCommands.addCommandForGroup(
            playerGroupId, "50 nm", ewrsCutoffDistanceMenuRoot, EWR.setCutoffDistancePreference, playerGroupId, UTILS.NMToMeters(50))

    EWR.radioMenusAdded[playerGroupId] = true
end

-- reschedule for users that change slot or coalition
local ClientSetupScheduler = TIMER:New(EWR.setupClients)
ClientSetupScheduler:Start(5, 30)

-- cleanup schedulers of users that are dead or left the mission
cleanupScheduler = SCHEDULER:New(nil,
        function()
            for groupId, clientPreferences in pairs(EWR.playerData) do
                local clientName = clientPreferences["clientName"]
                local client = CLIENT:FindByName(clientName, nil, false)
                if client == nil or not client:IsPlayer() then
                    if EWR.debug then
                        env.info(string.format("BigEye client clean up for %s", groupId))
                    end
                    local playerReportScheduler = EWR.getReportSchedulerForPlayerGroup(groupId)
                    playerReportScheduler:Stop()
                    local gciReportScheduler = EWR.getGciSchedulerForPlayerGroup(groupId)
                    gciReportScheduler:Stop()
                    env.info(string.format("BigEye stopping scheduler for %s, %s", clientPreferences["groupId"], clientPreferences["clientName"]))
                    EWR.playerData[groupId] = nil
                    EWR.radioMenusAdded[groupId] = nil
                end
            end
        end, {}, 0, 60, 0)

env.info("Big Eye EWR " .. EWR.version .. " Running")
trigger.action.outText("Big Eye EWR " .. EWR.version .. " Running", 10)
