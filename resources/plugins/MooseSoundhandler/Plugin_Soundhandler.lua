-- Do not edit this line or the following line
-- assert(loadfile("C:\\Users\\Taco\\Documents\\Github\\SoundHandler\\SoundHandlerByTaco.lua"))()
MESSAGE:New("*SOUNDHANDLER 0.1 LOADING*", 5, "MISSION", false):ToAll():ToLog()

Soundhandler_options = {
    ["SoundsToGroupOnly"] = true,
    ["ShipSamSounds"] = false,
    ["RedShootingSounds"] = true,
    ["Debug"] = false
}

-----------------------------------------------------------------------------------------------------------------------------------
-- USER SETTINGS
-----------------------------------------------------------------------------------------------------------------------------------
-- On/Off?
SoundHandler = true
-- Do you want ALL Clients to hear sounds, or only those associated with the sound event?
SoundOnlyToGroup = Soundhandler_options
    .SoundsToGroupOnly -- true means only the affected group will hear the sound.  False will play to all.  If no valid group is associated with the EVENT, sound will play to all.
-- Quick fix: SAMs and Red Missiles will play to Target Group ONLY

-- Do you want ship firing SAMs to play SAM Sounds?
ShipSamSounds = Soundhandler_options.ShipSamSounds -- true means they will play sounds with each missile launched

-- Do you want red airplanes to play sounds when they fire their gun cannons?
PlayRedShootingGuns = Soundhandler_options.RedShootingSounds -- true means they will play sounds with each gun burst

-----------------------------------------------------------------------------------------------------------------------------------
-- DEBUG
-----------------------------------------------------------------------------------------------------------------------------------
SoundDebug = Soundhandler_options.Debug -- Will enable messages on-screen and in log

if SoundDebug then
    trigger.action.outText("---SOUND DEBUG IS ON!---", 10)

    if SoundHandler then
        trigger.action.outText("Soundhandler ON!", 10)
    else
        trigger.action.outText("Soundhandler OFF!", 10)
    end

    if SoundOnlyToGroup then
        trigger.action.outText("Sounds will only play to the involved GROUP", 10)
    else
        trigger.action.outText("Sounds will play to ALL Clients", 10)
    end

    if ShipSamSounds then
        trigger.action.outText("Ships firing SAMs will play sounds", 10)
    else
        trigger.action.outText("Ships firing SAMs will NOT play sounds", 10)
    end

    if PlayRedShootingGuns then
        trigger.action.outText("Red Airplane Gun Bursts will play sounds", 10)
    else
        trigger.action.outText("Red Airplane Gun Bursts will NOT play sounds", 10)
    end
end

-- Debug output to DCS log
env.info("--------- SoundsToGroupOnly=" .. tostring(SoundOnlyToGroup) ..
    " | ShipSamSounds=" .. tostring(ShipSamSounds) ..
    " | RedShootingSounds=" .. tostring(PlayRedShootingGuns) ..
    " | Debug=" .. tostring(SoundDebug))

-----------------------------------------------------------------------------------------------------------------------------------
-- SOUNDS FILEPATH
-----------------------------------------------------------------------------------------------------------------------------------
SoundFilePath = ""
-----------------------------------------------------------------------------------------------------------------------------------
-- SOUND FILES
-----------------------------------------------------------------------------------------------------------------------------------
-- Global Sound Tables (make sure you have all these files, named exactly like these, loaded into the .mix file)
Sounds = {}
-- A2A Kill Sound Table
Sounds.Air_Unit_Sound_Table = { "AAGoodKill", "AAKill4", "AAKillGoodhiton1", "AAKillSplash", "AAKillSplashone",
    "AASplashOne", "AASplashOne_2" }
-- Red Jet Missile Sound Table
Sounds.RedMissile_Sound_Table = { "Misil1", "Misil2", "Misil3", "Misil4", "Misil5", "Misil6" }
-- Red Ground Unit Dead Sound Table
Sounds.Ground_Unit_Sound_Table = { "AGKillBOOM1", "AGKillCOMEONBABY", "AGKillGoodBOOM", "AGKillSeeTheSmoke",
    "AGKill_TARGET_DESTROYED", "AGKillBeautiful_beautiful", "AGKillMotherFucker" }
-- SAM Sound Table
Sounds.SamSoundTable = { "SAM1", "SAM2", "SAM3", "SAM4", "SAM5", "SAM6", "SAM7", "Defending", "Singer" }
-- Balistic Missile Launch Table
Sounds.Ballistic = { "SCUD_Long", "Fireball" }
-- AGM_154 Sound Table
Sounds.PigsAway_Sound_Table = { "PigsAway", "PigsAway2" }
-- Paveway_Sound_Table for LGBs
Sounds.Paveway_Sound_Table = { "Paveway" }
-- Bruiser Sound Table for Harpoons
Sounds.Bruiser_Sound_Table = { "Bruiser", "Bruiser2", "Bruiser3" }
-- Fox 2 Sound Table
Sounds.Fox2_Sound_Table = { "Fox2A", "Fox2B", "Fox2C", "Fox2D", "Fox2E" }
-- Fox 3 Sound Table
Sounds.Fox3_Sound_Table = { "Fox3A", "Fox3B", "Fox3C", "Fox3D", "Fox3E", "Fox3F" }
-- Fox 1 Sound Table
Sounds.Fox1_Sound_Table = { "Fox1A", "Fox1B" }
-- Magnum Sound Table
Sounds.Magnum_Sound_Table = { "Magnum", "Magnum2" }
-- Rifle Sound Table
Sounds.Rifle_Sound_Table = { "RifleA", "RifleB", "RifleC", "RifleD", "RifleE" }
-- Pickle Sound Table
Sounds.Pickle_Sound_Table = { "Pickle1", "Pickle2", "Pickle3", "Pickle4", "Pickle5", "Pickle6", "Pickle7" }
-- Blue Air Unit Dead Sound Table
Sounds.Blue_Air_Unit_Sound_Table = { "OhJesus", "SOS_Beacon", "HitEjecting1", "HitEjecting2", "HitEjecting3" } -- just for fun
-- Blue Guns Sounds
Sounds.Blue_Guns_Table = { "BlueGuns1", "BlueGuns2", "BlueGuns3" }
-- Red Guns Sounds
Sounds.Red_Guns_Table = { "Guns_Break_Right", "Guns_Break_Left" }
-- Blue Decoy Sounds
Sounds.Decoy_Table = { "A2G_Duck1" }
-- Blue Cruise Missile Sounds
Sounds.CruiseMissile_Table = { "A2G_Greyhound1" }
-- Red Anti-Ship Missile Sounds
Sounds.Vampires_Table = { "A2G_Vampires1" }
-- Blue Tomahawk/Ship-Launched Cruise Missile Sounds
Sounds.Tomahawk_Table = { "S2G_Tomahawk1" }
-- Friendly Fire Sounds
Sounds.Friendly_Fire_Table = { "FriendlyFire1", "FriendlyFire2" }
-- Friendly SAM Sounds
Sounds.Friendly_SAM_Table = { "BirdsAway" }

-----------------------------------------------------------------------------------------------------------------------------------
-- PRINT SOUNDS
-----------------------------------------------------------------------------------------------------------------------------------
if SoundDebug then
    for _, tbl in pairs(Sounds) do
        local txt = UTILS.OneLineSerialize(tbl)
        env.info("EventData Debug: " .. txt)
        trigger.action.outText("Sounds Loaded: " .. txt, 10)
    end
end

-----------------------------------------------------------------------------------------------------------------------------------
-- EVENT HANDLERS
-----------------------------------------------------------------------------------------------------------------------------------

EventHandler = EVENTHANDLER:New()
EventHandler:HandleEvent(EVENTS.Shot)
EventHandler:HandleEvent(EVENTS.Kill)
EventHandler:HandleEvent(EVENTS.Dead)

-----------------------------------------------------------------------------------------------------------------------------------
-- KILL EVENTS
-----------------------------------------------------------------------------------------------------------------------------------
function EventHandler:OnEventKill(EventData)
    --    UTILS.PrintTableToLog(EventData)

    if SoundHandler then
        if SoundDebug then
            BASE:I("---------KILL DETECTED: EVALUATING FOR COALITION & TYPE----------")
            BASE:I(EventData)
        end

        -- KILL SECTION (BLUE KILLS RED)
        if EventData.IniCoalition == coalition.side.BLUE or EventData.TgtCoalition == coalition.side.RED then
            if SoundDebug then BASE:I("BLUE UNIT KILLED RED...") end
            if (EventData.TgtCategory == 0 or EventData.TgtCategory == 1) and EventData.TgtObjectCategory == 1 and
                GROUP:FindByName(EventData.IniGroupName):IsAirPlane() then -- 0 is plane, 1 is helo https://wiki.hoggitworld.com/view/DCS_Class_Unit
                if SoundDebug then BASE:I("...AIRPLANE") end

                random_Air_Unit_Sound = Sounds.Air_Unit_Sound_Table[math.random(1, #Sounds.Air_Unit_Sound_Table)]
                local Air_Unit_Sound_Ogg = random_Air_Unit_Sound .. ".ogg"
                -- Sound Chosen
                RedA2ASound = USERSOUND:New(SoundFilePath .. Air_Unit_Sound_Ogg)
                -- Determine who to play sound to
                if EventData.IniGroup and SoundOnlyToGroup then
                    local SoundGroup = EventData.IniGroup
                    if SoundDebug then
                        BASE:I("-----SOUNDFILE PLAYED is " ..
                            random_Air_Unit_Sound .. " TO " .. SoundGroup:GetName())
                    end
                    RedA2ASound:ToGroup(SoundGroup)
                    if SoundDebug then
                        trigger.action.outText("-----SOUNDFILE PLAYED is " .. random_Air_Unit_Sound .. " TO " ..
                            SoundGroup:GetName(), 10)
                    end
                else
                    RedA2ASound:ToCoalition(coalition.side.BLUE)
                    if SoundDebug then BASE:I("-----SOUNDFILE PLAYED is " .. random_Air_Unit_Sound .. " TO ALL-----") end
                    if SoundDebug then
                        trigger.action.outText("-----SOUNDFILE PLAYED is " .. random_Air_Unit_Sound .. " TO ALL", 10)
                    end
                end
            end

            if EventData.IniGroupName then                                                                          -- If we don't have an IniGroupName, then don't proceed
                if EventData.TgtCategory == 2 and EventData.IniCoalition ~= EventData.TgtCoalition and
                    GROUP:FindByName(EventData.IniGroupName):IsAirPlane() and EventData.TgtObjectCategory == 1 then -- TgtCategory 2 is Ground, TgtObjectCategory is Unit
                    if SoundDebug then BASE:I("...GROUND UNIT (KILLED BY A BLUE AIRPLANE)") end

                    math.random()
                    random_Ground_Unit_Sound = Sounds.Ground_Unit_Sound_Table[math.random(1,
                        #Sounds.Ground_Unit_Sound_Table)]
                    local Ground_Unit_Sound_Ogg = random_Ground_Unit_Sound .. ".ogg"
                    -- Sound Chosen
                    RedGroundKillSound = USERSOUND:New(SoundFilePath .. Ground_Unit_Sound_Ogg)
                    -- Determine who to play sound to
                    if EventData.IniGroup and SoundOnlyToGroup then
                        local SoundGroup = EventData.IniGroup
                        BASE:I("-----SOUNDFILE PLAYED is " .. random_Ground_Unit_Sound .. " TO " .. SoundGroup:GetName())
                        RedGroundKillSound:ToGroup(SoundGroup)
                        if SoundDebug then
                            trigger.action.outText("-----SOUNDFILE PLAYED is " .. random_Ground_Unit_Sound .. " TO " ..
                                SoundGroup:GetName(), 10)
                        end
                    else
                        RedGroundKillSound:ToCoalition(coalition.side.BLUE)
                        BASE:I("-----SOUNDFILE PLAYED is " .. random_Ground_Unit_Sound .. " TO ALL-----")
                        if SoundDebug then
                            trigger.action.outText("-----SOUNDFILE PLAYED is " .. random_Ground_Unit_Sound .. " TO ALL",
                                10)
                        end
                    end
                end
            else
                env.info("-----No EventData.IniGroupName-----")
            end

            if EventData.IniGroupName then                                     -- If we don't have an IniGroupName, then don't proceed
                if EventData.TgtCategory == 3 and EventData.TgtObjectCategory == 1 and
                    GROUP:FindByName(EventData.IniGroupName):IsAirPlane() then -- 3 is Ship
                    BASE:I("...SHIP")
                    math.random()
                    random_Ground_Unit_Sound = Sounds.Ground_Unit_Sound_Table[math.random(1,
                        #Sounds.Ground_Unit_Sound_Table)]
                    local Ground_Unit_Sound_Ogg = random_Ground_Unit_Sound .. ".ogg"
                    -- Sound Chosen
                    RedGroundKillSound = USERSOUND:New(SoundFilePath .. Ground_Unit_Sound_Ogg)
                    -- Determine who to play sound to
                    if EventData.IniGroup and SoundOnlyToGroup then
                        local SoundGroup = EventData.IniGroup
                        BASE:I("-----SOUNDFILE PLAYED is " .. random_Ground_Unit_Sound .. " TO " .. SoundGroup:GetName())
                        RedGroundKillSound:ToGroup(SoundGroup)
                        if SoundDebug then
                            trigger.action.outText("-----SOUNDFILE PLAYED is " .. random_Ground_Unit_Sound .. " TO " ..
                                SoundGroup:GetName(), 10)
                        end
                    else
                        RedGroundKillSound:ToCoalition(coalition.side.BLUE)
                        BASE:I("-----SOUNDFILE PLAYED is " .. random_Ground_Unit_Sound .. " TO ALL-----")
                        if SoundDebug then
                            trigger.action.outText("-----SOUNDFILE PLAYED is " .. random_Ground_Unit_Sound .. " TO ALL",
                                10)
                        end
                    end
                end
            else
                env.info("-----No EventData.IniGroupName-----")
            end
        end

        -- Blue Dead, and/or Initiated by Red, and its a Plane
        if (EventData.IniCoalition == coalition.side.RED and EventData.TgtCoalition == coalition.side.BLUE) and
            EventData.TgtCategory == 0 then
            if EventData.TgtGroupName then
                BASE:I("---------BLUE UNIT GOT KILLED---------(" .. EventData.TgtGroupName .. ")")
            else
                BASE:I("---------BLUE UNIT GOT KILLED--------- (No Name)")
            end
            random_Blue_Air_Unit_Sound = Sounds.Blue_Air_Unit_Sound_Table[math.random(1,
                #Sounds.Blue_Air_Unit_Sound_Table)]
            local Blue_Air_Unit_Sound_Ogg = random_Blue_Air_Unit_Sound .. ".ogg"

            A2GSound = USERSOUND:New(SoundFilePath .. Blue_Air_Unit_Sound_Ogg)
            A2GSound:ToCoalition(coalition.side.BLUE)
            BASE:I("---------SOUNDFILE PLAYED---------is " .. Blue_Air_Unit_Sound_Ogg)
            if SoundDebug then
                trigger.action.outText("-----SOUNDFILE PLAYED is " .. Blue_Air_Unit_Sound_Ogg .. " TO ALL", 10)
            end
        end

        -- Blue Dead, and Initiated by Blue, and its a Plane
        if (EventData.IniCoalition == coalition.side.BLUE and EventData.TgtCoalition == coalition.side.BLUE) and
            EventData.TgtCategory == 0 then
            if EventData.TgtGroupName then
                BASE:I("---------BLUE ON BLUE---------(" .. EventData.TgtGroupName .. ")")
            else
                BASE:I("---------BLUE ON BLUE--------- (No Name)")
            end
            random_Friendly_Fire_Sound = Sounds.Friendly_Fire_Table[math.random(1, #Sounds.Friendly_Fire_Table)]
            local Friendly_Fire_Sound_Ogg = random_Friendly_Fire_Sound .. ".ogg"
            FFSound = USERSOUND:New(SoundFilePath .. Friendly_Fire_Sound_Ogg)

            if EventData.IniGroup and SoundOnlyToGroup then
                local SoundGroup = EventData.IniGroup
                BASE:I("-----SOUNDFILE PLAYED is " .. random_Friendly_Fire_Sound .. " TO " .. SoundGroup:GetName())
                FFSound:ToGroup(SoundGroup)
                if SoundDebug then
                    trigger.action.outText("-----SOUNDFILE PLAYED is " .. random_Friendly_Fire_Sound .. " TO " ..
                        SoundGroup:GetName(), 10)
                end
            else
                FFSound:ToCoalition(coalition.side.BLUE)
                BASE:I("-----SOUNDFILE PLAYED is " .. random_Friendly_Fire_Sound .. " TO ALL-----")
                if SoundDebug then
                    trigger.action.outText("-----SOUNDFILE PLAYED is " .. random_Friendly_Fire_Sound .. " TO ALL", 10)
                end
            end
        end
    end -- end of If SoundHandler
end     -- KILL EventHandler Function End

-----------------------------------------------------------------------------------------------------------------------------------
-- DEAD EVENTS
-----------------------------------------------------------------------------------------------------------------------------------
function EventHandler:OnEventDead(EventData)
    if SoundHandler then
        if SoundDebug then
            BASE:I("---------DEAD DETECTED: EVALUATING FOR COALITION & TYPE----------")
            BASE:I(EventData)
        end

        -- STATIC SECTION
        if EventData.IniObjectCategory == 3 then -- STATIC DEAD
            if EventData.IniCoalition == 1 then  -- RED STATIC DEAD
                BASE:I("RED STATIC DEAD")
                random_Ground_Unit_Sound =
                    Sounds.Ground_Unit_Sound_Table[math.random(1, #Sounds.Ground_Unit_Sound_Table)]
                local Ground_Unit_Sound_Ogg = random_Ground_Unit_Sound .. ".ogg"
                -- Sounnd Chosen
                RedStaticKillSound = USERSOUND:New(SoundFilePath .. Ground_Unit_Sound_Ogg)
                -- Determine who to play sound to
                if EventData.IniGroup and SoundOnlyToGroup then
                    local SoundGroup = EventData.IniGroup
                    BASE:I("-----SOUNDFILE PLAYED is " .. random_Ground_Unit_Sound .. " TO " .. SoundGroup:GetName())
                    RedStaticKillSound:ToGroup(SoundGroup)
                    if SoundDebug then
                        trigger.action.outText("-----SOUNDFILE PLAYED is " .. random_Ground_Unit_Sound .. " TO " ..
                            SoundGroup:GetName(), 10)
                    end
                elseif not EventData.IniGroup and SoundOnlyToGroup then
                    env.info("-----NO EventData.IniGroup Available-----")
                end

                if not SoundOnlyToGroup then
                    env.info("-----SOUND INTENDED FOR ALL-----")
                    RedStaticKillSound:ToCoalition(coalition.side.BLUE)
                    BASE:I("-----SOUNDFILE PLAYED is " .. random_Ground_Unit_Sound .. " TO ALL-----")
                    if SoundDebug then
                        trigger.action.outText("-----SOUNDFILE PLAYED is " .. random_Ground_Unit_Sound .. " TO ALL", 10)
                    end
                end
            end

            if EventData.IniCoalition == 2 then -- BLUE STATIC DEAD
                -- Consider if we want sounds for this
                BASE:I("---------BLUE STATIC DEAD, NO SOUND FOR NOW----------")
            end
        end -- Static Logic End
    end     -- End of If Soundhandler
end         -- DEAD EventHandler Function End

-----------------------------------------------------------------------------------------------------------------------------------
-- SHOT EVENTS
-----------------------------------------------------------------------------------------------------------------------------------
function EventHandler:OnEventShot(EventData)
    if SoundDebug then
        BASE:I("---------SHOT DETECTED: EVALUATING FOR COALITION & WEAPON----------")
        -- UTILS.PrintTableToLog(EventData)
        BASE:I(EventData)
    end
    math.random()
    local WeaponDesc = EventData.Weapon:getDesc()
    if SoundDebug then
        BASE:I({ WeaponDesc })
    end
    local Brevity = "none"
    soundDelay = false
    if SoundHandler then
        -- Weapon data.
        local _weapon = EventData.Weapon:getTypeName() -- should be the same as Event.WeaponTypeName
        local _weaponStrArray = UTILS.Split(_weapon, "%.")
        local _weaponName = _weaponStrArray[#_weaponStrArray]

        -- Weapon descriptor.
        local desc = EventData.Weapon:getDesc()

        -- Weapon category: 0=SHELL, 1=MISSILE, 2=ROCKET, 3=BOMB (Weapon.Category.X)
        local weaponcategory = desc.category
        local weaponguidance = WeaponDesc.guidance

        -- Debug info.

        if SoundDebug then
            BASE:I("-----PREPARING GENERAL SHOT INFORMATION...------")

            if EventData.IniUnitName then
                BASE:I("EVENT SHOT: Ini unit    = " .. EventData.IniUnitName)
            end
            if EventData.IniGroupName then
                BASE:I("EVENT SHOT: Ini group   = " .. EventData.IniGroupName)
            end

            BASE:I("EVENT SHOT: Weapon type = " .. _weapon)
            BASE:I("EVENT SHOT: Weapon name = " .. _weaponName)

            if weaponcategory then
                BASE:I("EVENT SHOT: Weapon category = " .. weaponcategory)
            else
                BASE:I('NO WEAPON CATEGORY VALUE')
            end
            if weaponguidance then
                BASE:I("EVENT SHOT: Weapon guidance = " .. weaponguidance)
            else
                BASE:I('NO WEAPON GUIDANCE VALUE')
            end
        end

        -- Blue and a SAM

        if EventData.IniCoalition == 2 and GROUP:FindByName(EventData.IniGroupName):IsSAM() then
            BASE:I("BLUE SAM SHOT CONFIRMED")
            RandomBlueSamSound = Sounds.Friendly_SAM_Table[math.random(1, #Sounds.Friendly_SAM_Table)]
            Brevity = tostring(RandomBlueSamSound)
            BASE:I("---------RANDOM FRIENDLY SAM SOUND IS " .. Brevity)
        end

        -- Blue and an Airplane
        if EventData.IniCoalition == 2 and GROUP:FindByName(EventData.IniGroupName):IsAirPlane() then
            BASE:I("BLUE AIRPLANE SHOT CONFIRMED")

            -- We want a specific sound for a glide weapon, so it needs to be added manually.
            if _weapon == "AGM_154" or _weapon == "AGM_154A" then
                math.random()
                RandomPigsAwaySound = Sounds.PigsAway_Sound_Table[math.random(1, #Sounds.PigsAway_Sound_Table)]
                Brevity = tostring(RandomPigsAwaySound)
                BASE:I("---------RANDOM PIGS AWAY SOUND IS " .. Brevity)

                -- DCS mis-classifies the GBU_32_V_2B, so it needs to be added manually.

                -- Duck for ADMs
            elseif string.find(_weapon, "ADM", 1, true) then
                math.random()
                RandomDuckSound = Sounds.Decoy_Table[math.random(1, #Sounds.Decoy_Table)]
                Brevity = tostring(RandomDuckSound)
                BASE:I("---------RANDOM DUCK SOUND IS " .. Brevity)
            elseif WeaponDesc.category == 3 and WeaponDesc.guidance == 1 or _weapon == "GBU_32_V_2B" or
                string.find(_weapon, "MK", 1, true) or string.find(_weapon, "ROCKEYE", 1, true) then
                math.random()
                math.random()
                RandomPickleSound = Sounds.Pickle_Sound_Table[math.random(1, #Sounds.Pickle_Sound_Table)]
                Brevity = tostring(RandomPickleSound)
                BASE:I("---------RANDOM PICKLE SOUND (3, 1, Specific) IS " .. Brevity)
            elseif WeaponDesc.category == 3 and WeaponDesc.guidance == 7 then
                -- LASER GUIDED SOUND TABLES
                math.random()
                RandomPavewaySound = Sounds.Paveway_Sound_Table[math.random(1, #Sounds.Paveway_Sound_Table)]
                Brevity = tostring(RandomPavewaySound)
                BASE:I("---------RANDOM PAVEWAY SOUND IS " .. Brevity)

                -- DCS mis-classifies the Harpoon, so it needs to be added manually.
            elseif _weapon == "AGM_84D" then
                math.random()
                RandomBruiserSound = Sounds.Bruiser_Sound_Table[math.random(1, #Sounds.Bruiser_Sound_Table)]
                Brevity = tostring(RandomBruiserSound)
                BASE:I("---------RANDOM BRUISER SOUND IS " .. Brevity)

                -- Cruise Missiles are "Greyhound".
            elseif _weapon == "AGM_84H" or string.find(_weapon, "84E", 1, true) then
                math.random()
                RandomGreyhoundSound = Sounds.CruiseMissile_Table[math.random(1, #Sounds.CruiseMissile_Table)]
                Brevity = tostring(RandomGreyhoundSound)
                BASE:I("---------RANDOM GREYHOUND SOUND IS " .. Brevity)
            elseif WeaponDesc.category == 1 and WeaponDesc.guidance == 2 then
                math.random()
                RandomFox2Sound = Sounds.Fox2_Sound_Table[math.random(1, #Sounds.Fox2_Sound_Table)]
                Brevity = tostring(RandomFox2Sound)
                BASE:I("---------FOX 2 SOUND----------" .. Brevity)
            elseif WeaponDesc.category == 1 and WeaponDesc.guidance == 3 then
                math.random()
                RanddomFox3Sound = Sounds.Fox3_Sound_Table[math.random(1, #Sounds.Fox3_Sound_Table)]
                Brevity = tostring(RanddomFox3Sound)
                BASE:I("---------FOX 3 SOUND----------" .. Brevity)
            elseif WeaponDesc.category == 1 and WeaponDesc.guidance == 4 then
                math.random()
                RanddomFox1Sound = Sounds.Fox1_Sound_Table[math.random(1, #Sounds.Fox1_Sound_Table)]
                Brevity = tostring(RanddomFox1Sound)
                BASE:I("---------Fox 1 SOUND----------")
            elseif WeaponDesc.category == 1 and WeaponDesc.guidance == 5 and WeaponDesc.missileCategory == 6 then
                RandomMagnumSound = Sounds.Magnum_Sound_Table[math.random(1, #Sounds.Magnum_Sound_Table)]
                Brevity = tostring(RandomMagnumSound)
                BASE:I("---------MAGNUM SOUND IS " .. Brevity)
            elseif WeaponDesc.category == 1 and WeaponDesc.guidance == 7 or string.find(_weapon, "65", 1, true) then
                math.random()
                RandomRifleSound = Sounds.Rifle_Sound_Table[math.random(1, #Sounds.Rifle_Sound_Table)]
                Brevity = tostring(RandomRifleSound)
                BASE:I("---------RIFLE SOUND (Includes Zuni Rockets)----------")

                -- "0" = Shells
            elseif WeaponDesc.category == 0 then
                math.random()
                RandomRifleSound = Sounds.Rifle_Sound_Table[math.random(1, #Sounds.Rifle_Sound_Table)]
                Brevity = tostring(RandomRifleSound)
                BASE:I("---------GUNS SOUND----------")

                -- If we still don't know what kind it is, and its a missile, let's call it a Rifle
            elseif WeaponDesc.category == 1 then
                math.random()
                RandomRifleSound = Sounds.Rifle_Sound_Table[math.random(1, #Sounds.Rifle_Sound_Table)]
                Brevity = tostring(RandomRifleSound)
                BASE:I("---------RIFLE SOUND (UNKNOWN MISSILE)----------")

                -- Rockets = Rifle (for lack of a better brevity code)
            elseif WeaponDesc.category == 2 then
                math.random()
                RandomRifleSound = Sounds.Rifle_Sound_Table[math.random(1, #Sounds.Rifle_Sound_Table)]
                Brevity = tostring(RandomRifleSound)
                BASE:I("---------ROCKET SOUND (RIFLE FOR NOW))----------")

                -- If we still don't know what kind it is, and its a bomb, let's call it a Pickle
            elseif WeaponDesc.category == 3 then
                math.random()
                RandomPickleSound = Sounds.Pickle_Sound_Table[math.random(1, #Sounds.Pickle_Sound_Table)]
                Brevity = tostring(RandomPickleSound)
                BASE:I("---------RANDOM PICKLE (UNKNOWN) SOUND IS " .. Brevity)
            end
        end

        if EventData.IniCoalition == 2 and GROUP:FindByName(EventData.IniGroupName):IsShip() then
            BASE:I("BLUE NAVAL SHOT CONFIRMED")

            if string.find(_weapon, "BGM_109B", 1, true) then
                RandomTomahawkSound = Sounds.Tomahawk_Table[math.random(1, #Sounds.Tomahawk_Table)]
                Brevity = tostring(RandomTomahawkSound)
                BASE:I("---------BLUE TOMAHAWK SOUND IS: " .. Brevity)
            end
        end

        -- LOGIC FOR RED AIRPLANE SHOTS
        -- if Red and an Airplane
        if EventData.IniCoalition == 1 and GROUP:FindByName(EventData.IniGroupName):IsAirPlane() then
            BASE:I("RED PLANE SHOT CONFIRMED")
            soundDelay = true
            BASE:I("DELAY ACTIVATED")

            if WeaponDesc.category == 1 and WeaponDesc.guidance == 2 then
                RandomRedMissileSound = Sounds.RedMissile_Sound_Table[math.random(1, #Sounds.RedMissile_Sound_Table)]
                Brevity = tostring(RandomRedMissileSound)
                BASE:I("---------RED MISSILE (Fox2) SOUND----------" .. Brevity)
            elseif WeaponDesc.category == 1 and WeaponDesc.guidance == 3 then
                RandomRedMissileSound = Sounds.RedMissile_Sound_Table[math.random(1, #Sounds.RedMissile_Sound_Table)]
                Brevity = tostring(RandomRedMissileSound)
                BASE:I("---------RED MISSILE (Fox2) SOUND----------" .. Brevity)
            elseif WeaponDesc.category == 1 and WeaponDesc.guidance == 4 then
                RandomRedMissileSound = Sounds.RedMissile_Sound_Table[math.random(1, #Sounds.RedMissile_Sound_Table)]
                Brevity = tostring(RandomRedMissileSound)
                BASE:I("---------RED MISSILE (Fox1) SOUND----------")
            elseif (WeaponDesc.category == 1 and WeaponDesc.missileCategory == 4) or
                string.find(_weapon, "X_22", 1, true) or string.find(_weapon, "X_35", 1, true) or
                string.find(_weapon, "X_31A", 1, true) or string.find(_weapon, "YJ_83K", 1, true) or
                string.find(_weapon, "YJ_12", 1, true) or _weapon == "AGM_84D" then
                RandomRedAntiShipSound = Sounds.Vampires_Table[math.random(1, #Sounds.Vampires_Table)]
                Brevity = tostring(RandomRedAntiShipSound)
                BASE:I("---------RED VAMPIRES SOUND----------")
            end -- End of Red Shot Classification
        end     -- End of Red Aerial Shot Logic

        -- LOGIC FOR RED GROUND MISSILES
        if ShipSamSounds then
            if EventData.IniCoalition == 1 and
                (GROUP:FindByName(EventData.IniGroupName):IsGround() or
                    GROUP:FindByName(EventData.IniGroupName):IsShip()) and WeaponDesc.category == 1 and
                not string.find(_weapon, "SA48N6", 1, true) and not string.find(_weapon, "SCUD_RAKETA", 1, true) then
                BASE:I("RED GROUND OR SHIP SHOT CONFIRMED")
                soundDelay = true
                BASE:I("DELAY ACTIVATED")

                -- if string.find(_weapon, "SA48N6", 1, true) then
                --  BASE:I("-----WEAPON SOUND KNOWN BUT SUPPRESSED-----")
                -- BASE:I("DELAY ACTIVATED, BUT NO SOUND")
                -- end

                RandomSamSound = Sounds.SamSoundTable[math.random(1, #Sounds.SamSoundTable)]
                Brevity = tostring(RandomSamSound)
                BASE:I("---------RED SAM SOUND----------" .. Brevity)
            end
        else
            if EventData.IniCoalition == 1 and GROUP:FindByName(EventData.IniGroupName):IsGround() and
                WeaponDesc.category == 1 and not string.find(_weapon, "SA48N6", 1, true) and
                not string.find(_weapon, "SCUD_RAKETA", 1, true) then
                BASE:I("RED GROUND (NOT SHIP) SHOT CONFIRMED")
                soundDelay = true
                BASE:I("DELAY ACTIVATED")

                --            if string.find(_weapon, "SA48N6", 1, true) then
                --              BASE:I("-----WEAPON SOUND KNOWN BUT SUPPRESSED-----")
                --        end

                if string.find(_weapon, "SCUD_RAKETA", 1, true) then
                    BASE:I("-----SCUD LAUNCH (NO SOUND PROGRAMMED)-----")
                end

                RandomSamSound = Sounds.SamSoundTable[math.random(1, #Sounds.SamSoundTable)]
                Brevity = tostring(RandomSamSound)
                BASE:I("---------RED SAM SOUND----------" .. Brevity)
            end
        end

        -- LOGIC FOR RED SCUD / BALLISTIC MISSILE LAUNCHES
        -- if Red and an Airplane
        if EventData.IniCoalition == 1 and string.find(_weapon, "SCUD_RAKETA", 1, true) then
            BASE:I("RED SCUD LAUNCH CONFIRMED")

            RandomBallisticMissileSound = Sounds.Ballistic[math.random(1, #Sounds.Ballistic)]
            Brevity = tostring(RandomBallisticMissileSound)
            BASE:I("---------RED BALLISTIC MISSILE SOUND----------" .. Brevity)
        end -- End of Red Scud Launch

        -- Let's put it into Sound
        if Brevity ~= "none" then
            BASE:I("-----soundDelay value = " .. tostring(soundDelay) .. "-----")

            -- Its a Blue Weapon Event
            if EventData.IniCoalition == 2 and EventData.IniGroup then
                local BrevitySound = Brevity .. ".ogg"
                WeaponSound = USERSOUND:New(SoundFilePath .. BrevitySound)

                -- Determine Who to Play Sound to
                if SoundOnlyToGroup then
                    local SoundGroup = EventData.IniGroup
                    WeaponSound:ToGroup(SoundGroup)

                    if SoundDebug then
                        BASE:I("---------SOUNDFILE PLAYED---------is " .. Brevity .. " TO " .. SoundGroup:GetName())
                        trigger.action.outText("-----SOUNDFILE PLAYED is " .. Brevity .. " TO " .. SoundGroup:GetName(),
                            10)
                    end
                else
                    WeaponSound:ToCoalition(coalition.side.BLUE)

                    if SoundDebug then
                        BASE:I("---------SOUNDFILE PLAYED---------is " .. Brevity .. " TO ALL")
                        trigger.action.outText("-----SOUNDFILE PLAYED is " .. Brevity .. " TO ALL", 10)
                    end
                end
            end

            -- Excluded Sounds, sounds we want to play to all Blue clients regardless of who fires
            if EventData.IniCoalition == 2 and EventData.IniGroup:IsShip() then
                WeaponSound:ToCoalition(coalition.side.BLUE)
                if SoundDebug then
                    BASE:I("--------- (EXCLUDED EVENT) SOUNDFILE PLAYED---------is " .. Brevity .. " TO ALL")
                end
            end

            -- Its a Red Weapon Event (SAM, on incoming missile)
            if EventData.IniCoalition == 1 then
                env.info("-----Red Shot-----")
                if EventData.TgtGroup then
                    env.info("-----TargetGroup Object Available-----")
                    local BrevitySound = Brevity .. ".ogg"
                    WeaponSound = USERSOUND:New(SoundFilePath .. BrevitySound)

                    local function DelayedSound()
                        local SoundGroup = EventData.TgtGroup
                        if SoundGroup then
                            WeaponSound:ToGroup(SoundGroup)
                        end
                    end
                    local soundDelayTime = math.random(3, 7)
                    env.info("-----soundDelayTime =" .. soundDelayTime .. "-----")
                    TIMER:New(DelayedSound):Start(soundDelayTime)

                    if SoundDebug then
                        BASE:I("---------SOUNDFILE PLAYED---------is " .. Brevity .. " TO " .. SoundGroup:GetName() ..
                            " ONLY")
                        trigger.action.outText("-----SOUNDFILE PLAYED is " .. Brevity .. " TO " .. SoundGroup:GetName(),
                            10)
                    end

                    -- Sound can play if its SCUD (but not other un-guided things like Artillery)
                elseif string.find(_weapon, "SCUD_RAKETA", 1, true) then
                    env.info("-----TargetGroup Object NOT Available Sound ToAll(Must be a SCUD) -----")

                    local BrevitySound = Brevity .. ".ogg"
                    WeaponSound = USERSOUND:New(SoundFilePath .. BrevitySound)
                    WeaponSound:ToCoalition(coalition.side.BLUE)

                    if SoundDebug then
                        BASE:I("---------SOUNDFILE PLAYED---------is " .. Brevity .. " TO All")
                        trigger.action.outText("-----SOUNDFILE PLAYED is " .. Brevity .. " TO All", 10)
                    end
                end
            end            -- End of Red Shot Event
        end                -- Sound Action End
        soundDelay = false -- reset value
        if SoundDebug then
            env.info("-----soundDelay value reset to false-----")
        end
    else
        env.info("-----SOUNDHANDLER OFF------")
    end
end -- Function End

BASE:I("-----MISSILE/BOMB SOUNDS SET------")

-----------------------------------------------------------------------------------------------------------------------------------
-- SHOOTING (RAPID FIRE) EVENT
-----------------------------------------------------------------------------------------------------------------------------------

ShootingEventHandler = EVENTHANDLER:New()
ShootingEventHandler:HandleEvent(EVENTS.ShootingStart)

function ShootingEventHandler:OnEventShootingStart(EventData)
    if SoundDebug then
        BASE:I("-----RAPID GUNS SHOOTING START, EVALUATING------")
    end
    local txt = UTILS.OneLineSerialize(EventData)
    env.info("Guns Shooting EventData Debug: " .. txt)
    local ShooterGroupName = EventData.IniGroupName
    local ShooterUnitName = EventData.IniUnitName
    if ShooterGroupName ~= nil and ShooterUnitName ~= nil then
        ShooterGroup = GROUP:FindByName(ShooterGroupName)
        ShooterUnit = UNIT:FindByName(ShooterUnitName)
    end

    if ShooterGroup:IsAirPlane() and ShooterUnit:IsClient() then
        BASE:I("BLUE AIRPLANE GUNS DETECTED (FROM CLIENT)")
        math.random()
        Blue_Guns_Sound = Sounds.Blue_Guns_Table[math.random(1, #Sounds.Blue_Guns_Table)]
        Brevity = tostring(Blue_Guns_Sound)
        BASE:I("---------RANDOM BLUE GUNS SOUND SELECTED IS: " .. Brevity)

        local GunsSound = Brevity .. ".ogg"
        -- Sound Chosen
        GunsSound = USERSOUND:New(SoundFilePath .. GunsSound)

        -- Determine Who to Play Sound to
        if SoundOnlyToGroup and EventData.IniGroup then
            local SoundGroup = EventData.IniGroup
            GunsSound:ToGroup(SoundGroup)
            BASE:I("---------SOUNDFILE PLAYED---------is " .. Brevity .. " TO " .. SoundGroup:GetName())
            if SoundDebug then
                trigger.action.outText("-----SOUNDFILE PLAYED is " .. Brevity .. " TO " .. SoundGroup:GetName(), 10)
            end
        else
            GunsSound:ToCoalition(coalition.side.BLUE)
            BASE:I("---------SOUNDFILE PLAYED---------is " .. Brevity .. " TO ALL")
            if SoundDebug then
                trigger.action.outText("-----SOUNDFILE PLAYED is " .. Brevity .. " TO ALL", 10)
            end
        end
    end

    if ShooterGroup:IsAirPlane() and EventData.IniCoalition == 1 and PlayRedShootingGuns then
        BASE:I("-----RED AIRPLANE GUNS DETECTED (AT CLIENT)------")
        math.random()
        Red_Guns_Sound = Sounds.Red_Guns_Table[math.random(1, #Sounds.Red_Guns_Table)]
        Brevity = tostring(Red_Guns_Sound)
        BASE:I("---------RANDOM RED GUNS SOUND SELECTED IS: " .. Brevity)

        local GunsSound = Brevity .. ".ogg"
        -- Sound Chosen
        GunsSound = USERSOUND:New(SoundFilePath .. GunsSound)
        -- Determine Who to Play Sound to
        if SoundOnlyToGroup and EventData.TgtGroup then
            local SoundGroup = EventData.TgtGroup
            GunsSound:ToGroup(SoundGroup)
            BASE:I("---------SOUNDFILE PLAYED---------is " .. Brevity .. " TO " .. SoundGroup:GetName())
            if SoundDebug then
                trigger.action.outText("-----SOUNDFILE PLAYED is " .. Brevity .. " TO " .. SoundGroup:GetName(), 10)
            end
        else
            GunsSound:ToCoalition(coalition.side.BLUE)
            BASE:I("---------SOUNDFILE PLAYED---------is " .. Brevity .. " TO ALL")
            if SoundDebug then
                trigger.action.outText("-----SOUNDFILE PLAYED is " .. Brevity .. " TO ALL", 10)
            end
        end
    end
end

BASE:I("-----GUN SHOOTING SOUNDS SET------")


-----------------------------------------------------------------
-- MENU FOR SETTINGS
-----------------------------------------------------------------

-- PARENT MENU ENTRY

local SettingsMenu = MENU_MISSION:New("SoundHandler Settings")

-- Toggle Debug On/Off
local function SoundhandlerOnOff(boolean)
    SoundHandler = boolean
    env.info("-----SoundHandler On = " .. tostring(boolean) .. "-----")

    if boolean == true then
        trigger.action.outText("**Soundhandler ON**", 5)
    end
    if boolean == false then
        trigger.action.outText("--Soundhandler OFF--", 5)
    end
end

local OnOrOff = MENU_MISSION:New("On or Off", SettingsMenu)
local SoundHandlerOn = MENU_MISSION_COMMAND:New("On", OnOrOff, SoundhandlerOnOff, true)    -- #MENU
local SoundHandlerOff = MENU_MISSION_COMMAND:New("Off", OnOrOff, SoundhandlerOnOff, false) -- #MENU

-- Toggle Debug On/Off
local function SwitchDebug(boolean)
    SoundDebug = boolean
    env.info("-----SoundDebug Now = " .. tostring(boolean) .. "-----")
end

local SoundDebugMenu = MENU_MISSION:New("Sound Debug", SettingsMenu)
local SoundDebugMenuTrue = MENU_MISSION_COMMAND:New("On", SoundDebugMenu, SwitchDebug, true)    -- #MENU
local SoundDebugMenuFalse = MENU_MISSION_COMMAND:New("Off", SoundDebugMenu, SwitchDebug, false) -- #MENU

-- Switch To Whom Sounds Play To
local function SwitchSoundsToGroup(boolean)
    SoundOnlyToGroup = boolean
    env.info("-----SoundOnlyToGroup Now = " .. tostring(boolean) .. "-----")

    if boolean == true then
        -- trigger.action.outText("**Sounds Play To Group Only**", 5)
    end
    if boolean == false then
        trigger.action.outText("--Sounds Play To All--", 5)
    end
end

local SoundsToGroupAll = MENU_MISSION:New("Sounds To Group or All", SettingsMenu)
local GroupTrue = MENU_MISSION_COMMAND:New("Play Sounds to Group Only", SoundsToGroupAll, SwitchSoundsToGroup, true) -- #MENU
local GroupFalse = MENU_MISSION_COMMAND:New("Play Sounds to All", SoundsToGroupAll, SwitchSoundsToGroup, false)      -- #MENU

BASE:I("-----SOUNDHANDLER SETTING SET------")

MESSAGE:New("*SOUNDHANDLER LOADED*", 5, "MISSION", false):ToAll():ToLog()
