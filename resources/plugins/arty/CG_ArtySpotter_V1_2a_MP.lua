-- Artillery Spotter script - Multiplayer version
-- by Carsten Gurk aka Don Rudi

-- Map for passing settings from Retribution
cg_arty_options = {
  ["user_fireDelay"] = 10,
  ["user_quantity"] = 20,
  ["user_spread"] = 50,
  ["user_spottingDistance"] = 15,
}

local version = "MP 1.2"

-- User configurable variables

local user_fireDelay = cg_arty_options.user_fireDelay					-- time to impcat of the rounds
local user_quantity = cg_arty_options.user_quantity						-- how many rounds will be fired in a fire for effect task
local user_spread = cg_arty_options.user_spread							-- impact radius of the rounds during fire for effect
local user_spottingDistance = cg_arty_options.user_spottingDistance		-- max allowable distance from player to target to prevent cheating. In kilometers.
local user_restrictByType = ""        									-- Restriction by type ("", "helo", etc.)
local user_restrictByUnitName = "" 										-- Restriction by unit name ("", "spotter", etc.), not case sensitive
local user_markerPrefix = ""     										-- Prefix for marker text, for instance "#arty"

-- end of user block

-- Script variables

local SINGLE_ROUND = false  			-- pilot called single round on marker (from F10 menu)

local artyCall     = 0 					-- pilot called arty (from F10 menu)
local artyRadius   = user_spread		-- Artillery Radius
local adjustRadius = 20  				-- fire adjustment 
local quantity     = 1   				-- Rounds expanded 
local quantity_effect = user_quantity	-- Rounds expanded during fire for effect
local tntEquivalent = 12				-- TNT equivalent for explosion
local fireDelay = user_fireDelay		-- delay til artillery fires in seconds

local firstShotFired = true

local markerSet = false

local pos = { x = 0, y = 0, z = 0 }
local playerPos = { x = 0, y = 0, z = 0 }

local target = {}

local adjustX = 0
local adjustZ = 0

local adjustDistance = 0				-- Adjust fire (from F10 menu)
local adjustDirection = 0				-- Adjust fire (from F10 menu)

local position = ""

local markerText = ""

local artyTasks = {}

local menuItems = false

-- optional arty enabled user flag, for use in triggers, if the player wants to

trigger.action.setUserFlag( "artyEnabled", 1 )


-- select format of target coordinates MGRS or LAT/LONG

local outputFormat = "MGRS"
--local outputFormat = "LL"


-- set values selected by player through F10 menu

local function setValue( _valueType, _value, _initiatorName )

	if _valueType == "arty" then
	
		artyCall = _value
				
	end
	
	if _valueType == "dist" then
	
		adjustDistance = _value
		
		trigger.action.outText("Fire adjusted by "..adjustDistance.." meters", 10)
		
	end
	
	if _valueType == "dir" then
	
		adjustDirection = _value
		
	end

	artyAction( _initiatorName )
	
end


-- Function to add F10 menu items for a specific group and store references

local function addMenuItems(groupId, initiatorName)

	menuItems = true

    local artyTask = artyTasks[initiatorName]
	
    artyTask.ArtyMenu = missionCommands.addSubMenuForGroup(groupId, 'Artillery Commands')
    artyTask.AdjustDistance = missionCommands.addSubMenuForGroup(groupId, 'Adjust distance', artyTask.ArtyMenu)
    artyTask.AdjustDirection = missionCommands.addSubMenuForGroup(groupId, 'Adjust direction', artyTask.ArtyMenu)

    artyTask.commands = {}
	artyTask.commands[#artyTask.commands + 1] = missionCommands.addCommandForGroup(groupId, 'request single round', artyTask.ArtyMenu, function() setValue("arty", 1, initiatorName) end)
    artyTask.commands[#artyTask.commands + 1] = missionCommands.addCommandForGroup(groupId, 'request fire for effect', artyTask.ArtyMenu, function() setValue("arty", 2, initiatorName) end)
    artyTask.commands[#artyTask.commands + 1] = missionCommands.addCommandForGroup(groupId, 'adjust fire by 20m', artyTask.AdjustDistance, function() setValue("dist", 20, initiatorName) end)
    artyTask.commands[#artyTask.commands + 1] = missionCommands.addCommandForGroup(groupId, 'adjust fire by 50m', artyTask.AdjustDistance, function() setValue("dist", 50, initiatorName) end)
    artyTask.commands[#artyTask.commands + 1] = missionCommands.addCommandForGroup(groupId, 'adjust fire by 100m', artyTask.AdjustDistance, function() setValue("dist", 100, initiatorName) end)
    artyTask.commands[#artyTask.commands + 1] = missionCommands.addCommandForGroup(groupId, 'adjust fire by 200m', artyTask.AdjustDistance, function() setValue("dist", 200, initiatorName) end)
    artyTask.commands[#artyTask.commands + 1] = missionCommands.addCommandForGroup(groupId, 'adjust fire by 500m', artyTask.AdjustDistance, function() setValue("dist", 500, initiatorName) end)
    
    artyTask.commands[#artyTask.commands + 1] = missionCommands.addCommandForGroup(groupId, 'adjust fire North', artyTask.AdjustDirection, function() setValue("dir", 360, initiatorName) end)
    artyTask.commands[#artyTask.commands + 1] = missionCommands.addCommandForGroup(groupId, 'adjust fire North-East', artyTask.AdjustDirection, function() setValue("dir", 45, initiatorName) end)
    artyTask.commands[#artyTask.commands + 1] = missionCommands.addCommandForGroup(groupId, 'adjust fire East', artyTask.AdjustDirection, function() setValue("dir", 90, initiatorName) end)
    artyTask.commands[#artyTask.commands + 1] = missionCommands.addCommandForGroup(groupId, 'adjust fire South-East', artyTask.AdjustDirection, function() setValue("dir", 135, initiatorName) end)
    artyTask.commands[#artyTask.commands + 1] = missionCommands.addCommandForGroup(groupId, 'adjust fire South', artyTask.AdjustDirection, function() setValue("dir", 180, initiatorName) end)
    artyTask.commands[#artyTask.commands + 1] = missionCommands.addCommandForGroup(groupId, 'adjust fire South-West', artyTask.AdjustDirection, function() setValue("dir", 225, initiatorName) end)
    artyTask.commands[#artyTask.commands + 1] = missionCommands.addCommandForGroup(groupId, 'adjust fire West', artyTask.AdjustDirection, function() setValue("dir", 270, initiatorName) end)
    artyTask.commands[#artyTask.commands + 1] = missionCommands.addCommandForGroup(groupId, 'adjust fire North-West', artyTask.AdjustDirection, function() setValue("dir", 315, initiatorName) end)
end

-- Function to remove F10 menu items for a specific group

local function removeMenuItems(initiatorName)

    local artyTask = artyTasks[initiatorName]
	
    if artyTask then
	
        for _, command in ipairs(artyTask.commands) do
            missionCommands.removeItemForGroup(artyTasks[initiatorName].groupID, command)
        end
        missionCommands.removeItemForGroup(artyTasks[initiatorName].groupID, artyTask.AdjustDistance)
        missionCommands.removeItemForGroup(artyTasks[initiatorName].groupID, artyTask.AdjustDirection)
        missionCommands.removeItemForGroup(artyTasks[initiatorName].groupID, artyTask.ArtyMenu)
    end
	
	menuItems = false
	
end

-- Calculate distance

local function getDist(_point1, _point2)

    local xUnit = _point1.x
    local yUnit = _point1.z
    local xZone = _point2.x
    local yZone = _point2.z

    local xDiff = xUnit - xZone
    local yDiff = yUnit - yZone

    return math.sqrt(xDiff * xDiff + yDiff * yDiff)

end

-- Shelling Zone

local function shellZone ( _initiatorName )

	trigger.action.outTextForUnit( artyTasks[_initiatorName].unitID, "Arty Task Created - fire incoming "..quantity.." rounds", 10)
	
	if artyCall == 1 then
		artyRadius = 5
	else
		artyRadius = 50
	end
	
	local _shellPos = artyTasks[_initiatorName].pos
	
	if firstShotFired == true then
		_shellPos.x = _shellPos.x + adjustX
		_shellPos.y = _shellPos.y
		_shellPos.z = _shellPos.z + adjustZ
	end 
	
	for i = 1, quantity do
	
		-- Create a random offset within the given radius
		
		local randomX = math.random(-artyRadius, artyRadius)
		local randomZ = math.random(-artyRadius, artyRadius)
		
		local strikePos = {
		  x = _shellPos.x + randomX,
		  y = _shellPos.y,
		  z = _shellPos.z + randomZ
		}
		
		-- Delay the shelling by 1 second for each shell
		
		timer.scheduleFunction(function()
		  trigger.action.explosion(strikePos, tntEquivalent)  -- Create an explosion at the target position with a predefined power
		end, {}, timer.getTime() + i)
	end	
	
	--[[
	if firstShotFired == false then 
		addMenuItems ()
		firstShotFired = true
	end
	]]--
	
end

-- MGRS conversion to LL to x,z

local function convertMGRStoPos ( _mrgs )

	local lat, lon = coord.MGRStoLL( _mgrs )
    local markerPos = coord.LLtoLO( lat, lon, 0 )
	return markerPos

end

-- x,z coordinates conversion to LAT/LONG and MGRS

local function convertPos2Coord ( _pos, _reply )

	local lat, lon, alt = coord.LOtoLL (_pos)
	local lat_degrees = math.floor (lat)
	local lat_minutes = (60 * (lat - lat_degrees))
	local lat_seconds = math.floor(60 * (lat_minutes - math.floor(lat_minutes))) 
	lat_minutes = math.floor(lat_minutes)

	local lon_degrees = math.floor (lon)
	local lon_minutes = (60 * (lon - lon_degrees))
	local lon_seconds = math.floor (60 * (lon_minutes - math.floor(lon_minutes)))
	lon_minutes = math.floor(lon_minutes)
	  
	local coordStringLL = "N" .. lat_degrees .. " " .. lat_minutes .. " " ..lat_seconds.. " E".. lon_degrees .. " " .. lon_minutes .. " ".. lon_seconds
	  
	local targetMGRS = coord.LLtoMGRS(lat, lon)
	targetMGRS.Easting = math.floor (( targetMGRS.Easting /10 ) + 0.5 )
	targetMGRS.Northing = math.floor (( targetMGRS.Northing / 10 ) + 0.5 )
	--local coordStringMGRS = targetMGRS.UTMZone.." "..targetMGRS.MGRSDigraph.." "..string.sub(targetMGRS.Easting, 1, -2).." "..string.sub(targetMGRS.Northing, 1, -2)
	local coordStringMGRS = targetMGRS.UTMZone.." "..targetMGRS.MGRSDigraph.." "..targetMGRS.Easting.." "..targetMGRS.Northing
	  
	if outputFormat == "MGRS" then
		coordString = coordStringMGRS
	else
		coordString = coordStringLL
	end
	  
	-- return either formated string or MGRS coordinate  
	
	if _reply == "string" then
		return coordString
	elseif _reply == "pos" then
		return targetMGRS
	end
end  

-- Who is the player

-- Function to determine which unit is controlled by the player
--[[
local function getPlayerControlledUnit()
	
  local playerUnit = nil
  
  -- Iterate through all coalitions and their respective player units
  
  for coalitionID = 1, 2 do  -- 1 = Red, 2 = Blue
    local playerUnits = coalition.getPlayers(coalitionID)
    for _, unit in ipairs(playerUnits) do
      if unit and unit:getPlayerName() then
        playerUnit = unit
        break
      end
    end
    if playerUnit then
      break
    end
  end
  
  return playerUnit
end
]]--

-- Check if user has created F10 map marker

artyAction = function ( _initiatorName )
	
  -- Check Call for arty - 1 = single round, 2 = fire for effect
  
  if artyCall == 1 or artyCall == 2 then
      
    if MARKER_FOUND == true and artyTasks[_initiatorName] then
	
       -- check if target is within 15km from player
	   
	   --trigger.action.outTextForUnit( artyTasks[_initiatorName].unitID, "Arty action marker found.", 10)
	   
		--local _player = _initiator
		local _playerPos = artyTasks[_initiatorName].playerPos
		local _targetPos = artyTasks[_initiatorName].pos
		
		local _dist = math.floor( getDist ( _targetPos, _playerPos ) / 10 ) / 100
		 
	    if  trigger.misc.getUserFlag( "artyEnabled" ) == 1 and _dist <= user_spottingDistance then
	   
		   position = convertPos2Coord ( _targetPos, "string" )
			
			if artyCall == 1 then
				trigger.action.outTextForUnit( artyTasks[_initiatorName].unitID, "Arty single round requested on "..position, 10)
				quantity = 1
				
			elseif artyCall == 2 then
				trigger.action.outTextForUnit( artyTasks[_initiatorName].unitID, "Arty fire for effect requested on "..position, 10)
				quantity = quantity_effect
			end
			
			timer.scheduleFunction(shellZone, _initiatorName, timer.getTime() + fireDelay)
			trigger.action.setUserFlag( "artyFired", 1 )
		
		else	
			trigger.action.outTextForUnit( artyTasks[_initiatorName].unitID, "Artillery not available", 10)
		end
		
	else
		trigger.action.outTextForUnit( artyTasks[_initiatorName].unitID, "Arty Requested Without Marker", 10)
    end
  
     artyCall = 0
	 
  end
  
  -- Check Call for arty direction correction
  
  if adjustDirection == 360 then
     
	adjustX = adjustDistance
	adjustZ = 0
	artyRadius = 5
				
	trigger.action.outTextForUnit( artyTasks[_initiatorName].unitID, "Fire adjusted to the North", 10)
	
    adjustDirection = 0
  end
  
  if adjustDirection == 45 then
     
	adjustX = adjustDistance
	adjustZ = adjustDistance
	artyRadius = 5
				
    adjustDirection = 0
  end
  
  if adjustDirection == 90 then
     
	adjustX = 0
	adjustZ = adjustDistance
	artyRadius = 5
				
	trigger.action.outTextForUnit( artyTasks[_initiatorName].unitID, "Fire adjusted to the East", 10)
	      
    adjustDirection = 0
  end
  
  if adjustDirection == 135 then
     
	adjustX = -adjustDistance
	adjustZ = adjustDistance
	artyRadius = 5
				
	trigger.action.outTextForUnit( artyTasks[_initiatorName].unitID, "Fire adjusted to the South-East", 10)
	       
    adjustDirection = 0
  end
  
  if adjustDirection == 180 then

	adjustX = -adjustDistance
	adjustZ = 0
	artyRadius = 5
				
	trigger.action.outTextForUnit( artyTasks[_initiatorName].unitID, "Fire adjusted to the South", 10)
	         
    adjustDirection = 0
  end
  
  if adjustDirection == 225 then
     
	adjustX = -adjustDistance
	adjustZ = -adjustDistance
	artyRadius = 5
				
	trigger.action.outTextForUnit( artyTasks[_initiatorName].unitID, "Fire adjusted to the South-West", 10)
	        
    adjustDirection = 0
  end
  
  if adjustDirection == 270 then
     
	adjustX = 0
	adjustZ = -adjustDistance
	artyRadius = 5
				
	trigger.action.outTextForUnit( artyTasks[_initiatorName].unitID, "Fire adjusted meters to the West", 10)
	          
    adjustDirection = 0
  end
  
  if adjustDirection == 315 then
     
	adjustX = adjustDistance
	adjustZ = -adjustDistance
	artyRadius = 5
				
	trigger.action.outTextForUnit( artyTasks[_initiatorName].unitID, "Fire adjusted meters to the North-West", 10)
	          
    adjustDirection = 0
  end

end

-- Main

trigger.action.outText("Arty spotter script "..version.." loaded", 10)


-- Map Marker Text - read and process

-- Function to remove spaces from a string

local function removeSpaces( _text )

	_text = _text:gsub( " ", "" )
	_text = _text:gsub( "-", "" )
	return _text
	
end

-- Function to validate the structure of the MGRS coordinate

local function checkValidMGRS( _mgrs, len)

	if len == 13 then
  
    -- Pattern: 2 digits 1 letter UTM Zone, 2 letters MGRS Digraph, 4 digits Easting, 4 digits Northing
    return _mgrs:match("^%d%d%u%u%u%d%d%d%d%d%d%d%d$")
	
  elseif len == 10 then
  
    -- Pattern: 2 letters MGRS Digraph, 4 digits Easting, 4 digits Northing
    return _mgrs:match("^%u%u%d%d%d%d%d%d%d%d$")
	
  elseif len == 8 then
  
    -- Pattern: 4 digits Easting, 4 digits Northing
    return _mgrs:match("^%d%d%d%d%d%d%d%d$")
	
  else
    return false
  end
end

-- Function to validate and complete MGRS coordinates

local function processMGRS( _text, _playerPos, initiatorName )
  local _cleanedText = string.upper( removeSpaces( _text ) )
  local len = #_cleanedText
  
  local _isValidMGRS = checkValidMGRS( _cleanedText, len)
  
  if _isValidMGRS then
	
	trigger.action.outTextForUnit( artyTasks[initiatorName].unitID, "Processing MGRS: " .. _cleanedText, 10)
	
	if len == 13 then
	
		-- Complete MGRS coordinate
		return _cleanedText
		
	elseif len == 10 then
	  
		-- Add UTM Zone based on player position
		local _utmZone = coord.LLtoMGRS(_playerPos.Lat, _playerPos.Lon).UTMZone
		return _utmZone .. _cleanedText
		
	elseif len == 8 then
	  
		-- Add UTM Zone and MGRS Digraph based on player position
		local _mgrs = coord.LLtoMGRS( _playerPos.Lat, _playerPos.Lon )
		return _mgrs.UTMZone .. _mgrs.MGRSDigraph .. _cleanedText
		
	else
  
		-- Invalid MGRS coordinate
		return nil
	end
	
  else
  
	trigger.action.outTextForUnit( artyTasks[initiatorName].unitID, "Invalid text input: " .. _cleanedText, 10)
	return nil
  
  end
	
  
end

-- Function to convert a valid MGRS to vec3
local function MGRStoVec3( _mgrs )

  local lat, lon = coord.MGRStoLL( _mgrs )
  local vec3 = coord.LLtoLO( lat, lon, 0 )
  return vec3
end

-- Function to check if the initiator is valid based on restrictions

local function isValidInitiator(initiator)
    if not initiator then return false end
    
    -- Check type restriction
	
    if user_restrictByType == "helo" then
	
        if not initiator:getDesc().category == Unit.Category.Helicopter then
            return false
        end
    end

    -- Check name restriction
	
    if user_restrictByUnitName ~= "" then
	
        local name = initiator:getName():lower()
		
        if not name:find(user_restrictByUnitName:lower()) then
            return false
        end
    end

    return true
end

-- Function to check if the marker text has the required prefix and remove it

local function checkAndRemovePrefix(text)

    if user_markerPrefix ~= "" and text:sub(1, #user_markerPrefix) == user_markerPrefix then
	
        return true, text:sub(#user_markerPrefix + 1)
    
	elseif user_markerPrefix == "" then
	
		return true, text
		
	else
	
		return false, text
		
	end
	
end


-- Event handler for map marker creation
local function onPlayerAddMarker(event)

	
	if event.id == world.event.S_EVENT_MARK_ADDED and user_markerPrefix == "" then
	
		 if isValidInitiator(event.initiator) then
		 
			--local hasPrefix, cleanedText = checkAndRemovePrefix(event.text)
			hasPrefix = true
		 
            if hasPrefix then
		
				MARKER_FOUND = true
				pos = event.pos
				
				if event.initiator then
				
					local initiatorName = event.initiator:getName()
					
					local playerUnit = event.initiator
					local playerPos = playerUnit:getPoint()
					
					-- Store position
										
					if not artyTasks[initiatorName] then
						artyTasks[initiatorName] = {}
					end
					
					trigger.action.outTextForUnit( event.initiator:getID(), "Marker added", 5)
					
					artyTasks[initiatorName].playerPos = playerPos
					artyTasks[initiatorName].pos = pos
					artyTasks[initiatorName].unitID = event.initiator:getID()
				
					-- Add menu items for the initiator's group
					local groupId = event.initiator:getGroup():getID()
					artyTasks[initiatorName].groupID = groupId
				
					if menuItems == false then 
						addMenuItems(groupId, initiatorName)
					end
		
				end
				
			end
			
		else
            --trigger.action.outText("You do not have permission to add a marker.", 5)
        end
		    
	elseif event.id == world.event.S_EVENT_MARK_CHANGE then
	 
        if isValidInitiator(event.initiator) then
		
			local hasPrefix, cleanedText = checkAndRemovePrefix(event.text)
			
            if hasPrefix then
			
				MARKER_FOUND = true
		
				local markText = cleanedText
				
				trigger.action.outText("Text: "..markText, 10)
				
				if markText and event.initiator then
				
					local initiatorName = event.initiator:getName()
					local playerUnit = event.initiator
					
					if not artyTasks[initiatorName] then
						artyTasks[initiatorName] = {}
					end
					
					artyTasks[initiatorName].initiator = event.initiator
					artyTasks[initiatorName].unitID = event.initiator:getID()
					
					trigger.action.outTextForUnit( event.initiator:getID(), "Marker changed", 5)
					
					if playerUnit then
					
						local playerPos = playerUnit:getPoint()
						local lat, lon = coord.LOtoLL(playerPos)
						local playerPosition = { Lat = lat, Lon = lon }
						local validMGRS = processMGRS(markText, playerPosition, initiatorName)

						if validMGRS then
						
							trigger.action.outTextForUnit( artyTasks[initiatorName].unitID, "Valid MGRS: " .. validMGRS, 10)
							
							local tmpMGRS = {
								UTMZone = string.sub(validMGRS, 1, 3),
								MGRSDigraph = string.sub(validMGRS, 4, 5),
								Easting = tonumber(string.sub(validMGRS, 6, 9)) * 10,
								Northing = tonumber(string.sub(validMGRS, 10, 13)) * 10
							}
							
							local targetPoint = MGRStoVec3(tmpMGRS)
							targetPoint.y = land.getHeight({ x = targetPoint.x, y = targetPoint.z })

							
							artyTasks[initiatorName].pos = targetPoint
							artyTasks[initiatorName].playerPos = playerPos
							
														
						else
							trigger.action.outTextForUnit( artyTasks[initiatorName].unitID, "Invalid MGRS coordinate entered.", 10)
						end
						
						local groupId = event.initiator:getGroup():getID()
						artyTasks[initiatorName].groupID = groupId
						
						if menuItems == false then 
							addMenuItems(groupId, initiatorName)
						end
					end
				end
			end
		else
            --trigger.action.outText("You do not have permission to change this marker.", 5)
		end
		
    elseif event.id == world.event.S_EVENT_MARK_REMOVED then
	
        trigger.action.outText("Marker removed", 5)
		
        if event.initiator then
		
            local initiatorName = event.initiator:getName()
			
			if artyTasks[initiatorName] then
			
				removeMenuItems(initiatorName)
                artyTasks[initiatorName] = nil
				
            end
			
        end
	end
end

-- Register the event handler
local eventHandler = { f = onPlayerAddMarker }
function eventHandler:onEvent(e)
  self.f(e)
end
world.addEventHandler(eventHandler)




