-- Artillery Spotter script
-- by Carsten Gurk aka Don Rudi

local version = "1.0.3"

-- User configurable variables

local user_fireDelay = 10				-- time to impcat of the rounds
local user_quantity = 20				-- how many rounds will be fired in a fire for effect task
local user_spread = 50					-- impact radius of the rounds during fire for effect
local user_spottingDistance = 15		-- max allowable distance from player to target to prevent cheating. In kilometers.

-- end of user block

-- Script variables

local SINGLE_ROUND = false  			-- pilot called single round on marker (from F10 menu)

local artyCall     = 0 					-- pilot called arty (from F10 menu)
local artyRadius   = user_spread		-- Artillery Radius
local adjustRadius = 20  				-- fire adjustment
local quantity     = 1   				-- Rounds expanded 
local quantity_effect = user_quantity	-- Rounds expanded during fire for effect
local tntEquivalent = 15				-- TNT equivalent for explosion
local fireDelay = user_fireDelay		-- delay til artillery fires in seconds

local firstShotFired = false

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

-- optional arty enabled user flag, for use in triggers, if the player wants to

trigger.action.setUserFlag( "artyEnabled", 1 )


-- select format of target coordinates MGRS or LAT/LONG

local outputFormat = "MGRS"
--local outputFormat = "LL"


-- set values selected by player through F10 menu

local function setValue( _valueType, _value )

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

	artyAction()
	
end


-- F10 menu items


ArtyMenu = missionCommands.addSubMenu('Call Arty')
missionCommands.addCommand('request single round', ArtyMenu, function () setValue ("arty", 1) end)

local function addMenuItems ()

	AdjustDistance = missionCommands.addSubMenu('Adjust distance', ArtyMenu)
	AdjustDirection = missionCommands.addSubMenu('Adjust direction', ArtyMenu)

	missionCommands.addCommand('request fire for effect', ArtyMenu, function () setValue ("arty", 2) end)
	missionCommands.addCommand('adjust fire by 20m', AdjustDistance, function () setValue ("dist", 20) end)
	missionCommands.addCommand('adjust fire by 50m', AdjustDistance, function () setValue ("dist", 50) end)
	missionCommands.addCommand('adjust fire by 100m', AdjustDistance, function ()setValue ("dist", 100) end)
	missionCommands.addCommand('adjust fire by 200m', AdjustDistance, function () setValue ("dist", 200) end)
	missionCommands.addCommand('adjust fire by 500m', AdjustDistance, function () setValue ("dist", 500) end)
	
	missionCommands.addCommand('adjust fire North', AdjustDirection, function () setValue ("dir", 360) end)
	missionCommands.addCommand('adjust fire North-East', AdjustDirection, function () setValue ("dir", 45) end)
	missionCommands.addCommand('adjust fire East', AdjustDirection, function () setValue ("dir", 90) end)
	missionCommands.addCommand('adjust fire South-East', AdjustDirection, function () setValue ("dir", 135) end)
	missionCommands.addCommand('adjust fire South', AdjustDirection, function () setValue ("dir", 180) end)
	missionCommands.addCommand('adjust fire South-West', AdjustDirection, function () setValue ("dir", 225) end)
	missionCommands.addCommand('adjust fire West', AdjustDirection, function () setValue ("dir", 270) end)
	missionCommands.addCommand('adjust fire North-West', AdjustDirection, function () setValue ("dir", 315) end)

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

local function shellZone ( )

	trigger.action.outText("Arty Task Created - fire incoming "..quantity.." rounds", 10)
	
	if artyCall == 1 then
		artyRadius = 5
	else
		artyRadius = 50
	end
	
	if firstShotFired == true then
		pos.x = pos.x + adjustX
		pos.y = pos.y
		pos.z = pos.z + adjustZ
	end 
	
	for i = 1, quantity do
	
		-- Create a random offset within the given radius
		
		local randomX = math.random(-artyRadius, artyRadius)
		local randomZ = math.random(-artyRadius, artyRadius)
		
		local targetPos = {
		  x = pos.x + randomX,
		  y = pos.y,
		  z = pos.z + randomZ
		}
		
		-- Delay the shelling by 1 second for each shell
		
		timer.scheduleFunction(function()
		  trigger.action.explosion(targetPos, tntEquivalent)  -- Create an explosion at the target position with a predefined power
		end, {}, timer.getTime() + i)
	end	
	
	if firstShotFired == false then 
		addMenuItems ()
		firstShotFired = true
	end
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

-- Check if user has created F10 map marker

artyAction = function ()
	
  -- Check Call for arty - 1 = single round, 2 = fire for effect
  
  if artyCall == 1 or artyCall == 2 then
      
    if MARKER_FOUND == true then
	
       -- check if target is within 15km from player
	   
		local _player = getPlayerControlledUnit()
		local _playerPos = _player:getPoint()
		local _dist = math.floor( getDist ( pos, _playerPos ) / 10 ) / 100
		 
	    if  trigger.misc.getUserFlag( "artyEnabled" ) == 1 and _dist <= user_spottingDistance then
	   
		   position = convertPos2Coord ( pos, "string" )
			
			if artyCall == 1 then
				trigger.action.outText("Arty single round requested on "..position, 10)
				quantity = 1
				
			elseif artyCall == 2 then
				trigger.action.outText("Arty fire for effect requested on "..position, 10)
				quantity = quantity_effect
			end
			
			timer.scheduleFunction(shellZone, {}, timer.getTime() + fireDelay)
		
		else	
			trigger.action.outText("Artillery not available", 10)
		end
		
	else
		trigger.action.outText("Arty Requested Without Marker", 10)
    end
  
     artyCall = 0
	 
  end
  
  -- Check Call for arty direction correction
  
  if adjustDirection == 360 then
     
	adjustX = adjustDistance
	adjustZ = 0
	artyRadius = 5
				
	trigger.action.outText("Fire adjusted to the North", 10)
	
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
				
	trigger.action.outText("Fire adjusted to the East", 10)
	      
    adjustDirection = 0
  end
  
  if adjustDirection == 135 then
     
	adjustX = -adjustDistance
	adjustZ = adjustDistance
	artyRadius = 5
				
	trigger.action.outText("Fire adjusted to the South-East", 10)
	       
    adjustDirection = 0
  end
  
  if adjustDirection == 180 then

	adjustX = -adjustDistance
	adjustZ = 0
	artyRadius = 5
				
	trigger.action.outText("Fire adjusted to the South", 10)
	         
    adjustDirection = 0
  end
  
  if adjustDirection == 225 then
     
	adjustX = -adjustDistance
	adjustZ = -adjustDistance
	artyRadius = 5
				
	trigger.action.outText("Fire adjusted to the South-West", 10)
	        
    adjustDirection = 0
  end
  
  if adjustDirection == 270 then
     
	adjustX = 0
	adjustZ = -adjustDistance
	artyRadius = 5
				
	trigger.action.outText("Fire adjusted meters to the West", 10)
	          
    adjustDirection = 0
  end
  
  if adjustDirection == 315 then
     
	adjustX = adjustDistance
	adjustZ = -adjustDistance
	artyRadius = 5
				
	trigger.action.outText("Fire adjusted meters to the North-West", 10)
	          
    adjustDirection = 0
  end

end

-- Main

trigger.action.outText("Arty spotter script v"..version.." loaded", 10)


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

local function processMGRS( _text, _playerPos )
  local cleanedText = string.upper( removeSpaces( _text ) )
  local len = #cleanedText
  
  local _isValidMGRS = checkValidMGRS( cleanedText, len)
  
  if _isValidMGRS then
	
	trigger.action.outText("Processing MGRS: " .. cleanedText, 10)
	
	if len == 13 then
	
		-- Complete MGRS coordinate
		return cleanedText
		
	elseif len == 10 then
	  
		-- Add UTM Zone based on player position
		local _utmZone = coord.LLtoMGRS(_playerPos.Lat, _playerPos.Lon).UTMZone
		return _utmZone .. cleanedText
		
	elseif len == 8 then
	  
		-- Add UTM Zone and MGRS Digraph based on player position
		local _mgrs = coord.LLtoMGRS( _playerPos.Lat, _playerPos.Lon )
		return _mgrs.UTMZone .. _mgrs.MGRSDigraph .. cleanedText
		
	else
  
		-- Invalid MGRS coordinate
		return nil
	end
	
  else
  
	trigger.action.outText("Invalid text input: " .. cleanedText, 10)
	return nil
  
  end
	
  
end

-- Function to convert a valid MGRS to vec3
local function MGRStoVec3( _mgrs )

  local lat, lon = coord.MGRStoLL( _mgrs )
  local vec3 = coord.LLtoLO( lat, lon, 0 )
  return vec3
end


-- Event handler for map marker creation
local function onPlayerAddMarker(event)

	
	if event.id == world.event.S_EVENT_MARK_ADDED then
		
		trigger.action.outText("Marker added", 5)
		MARKER_FOUND = true
		pos = event.pos
		
		if event.initiator then
			trigger.action.outText("User: " .. event.initiator:getName(), 10)
		end
		    
	elseif event.id == world.event.S_EVENT_MARK_CHANGE then
  
		trigger.action.outText("Marker changed", 5)
		
		local _markText = event.text
		local _playerUnit = getPlayerControlledUnit()
		
		if _markText then
				
		  local _playerPos = _playerUnit:getPoint()
		  local lat, lon = coord.LOtoLL( _playerPos )
		  
		  local _playerPosition = { Lat = lat, Lon = lon }
		  local validMGRS = processMGRS( _markText, _playerPosition)

		  if validMGRS then
			-- Valid MGRS coordinate, do something with it
			trigger.action.outText("Valid MGRS: " .. validMGRS, 10)
			
			local _tmpMGRS = {
				UTMZone = string.sub( validMGRS,1 ,3 ),
				MGRSDigraph = string.sub( validMGRS,4 ,5 ),
				Easting = tonumber(string.sub( validMGRS,6 ,9 ))*10,
				Northing = tonumber(string.sub( validMGRS,10 ,13 ))*10
			}
			
			local _targetPoint = MGRStoVec3( _tmpMGRS )
			
			pos = _targetPoint
			pos.y = land.getHeight({x = pos.x, y = pos.z})
			
		  else
			-- Invalid MGRS coordinate
			trigger.action.outText("Invalid MGRS coordinate entered.", 10)
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




