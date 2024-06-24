
--assert(loadfile("C:\\Users\\spenc\\OneDrive\\Documents\\Eclipe_LDT\\dcs splash damage\\src\\mist.lua"))()
--[[
2 October 2020
FrozenDroid:
- Added error handling to all event handler and scheduled functions. Lua script errors can no longer bring the server down.
- Added some extra checks to which weapons to handle, make sure they actually have a warhead (how come S-8KOM's don't have a warhead field...?)

28 October 2020
FrozenDroid:
- Uncommented error logging, actually made it an error log which shows a message box on error.
- Fixed the too restrictive weapon filter (took out the HE warhead requirement)

21 December 2021
spencershepard (GRIMM):
 SPLASH DAMAGE 2.0:
 -Added blast wave effect to add timed and scaled secondary explosions on top of game objects
 -object geometry within blast wave changes damage intensity
 -damage boost for structures since they are hard to kill, even if very close to large explosions
 -increased some rocket values in explTable
 -missing weapons from explTable will display message to user and log to DCS.log so that we can add what's missing
 -damage model for ground units that will disable their weapons and ability to move with partial damage before they are killed
 -added options table to allow easy adjustments before release
 -general refactoring and restructure

 31 December 2021
 spencershepard (GRIMM):
-added many new weapons
-added filter for weapons.shells events
-fixed mission weapon message option
-changed default for damage_model option

 16 April 2022
 spencershepard (GRIMM):
 added new/missing weapons to explTable
 added new option rocket_multiplier

 29 May 2022
 Ghosti (MetalStormGhost):
 - Implemented generating extra explosions near BLU-97/B hits to simulate the missing submunitions which are omitted by ED
  due to performance reasons. This is an attempt at making the A-model JSOW more useful against groups of soft targets.

 3 August 2022
 Ghosti (MetalStormGhost):
 SPLASH DAMAGE WITH CLUSTERS AND SHIP RADAR EFFECTS:
 -damage boost for parked aircraft since they are hard to kill (DCS: Retribution OCA/Aircraft mission improvement)
 -additional cluster weapons support
 -helicopter gunship autocannon fragmentation effect support
 -napalm will now spawn fire on impact
 -ship radars might turn off when hit with anti-radiation missiles
 -BDA messages for splash damage

 12 November 2023
 Raffson:
 - integrate Ghosti's implementation into original script

--]]

----[[ ##### SCRIPT CONFIGURATION ##### ]]----

splash_damage_options = {
  ["static_damage_boost"] = 2000, --apply extra damage to Unit.Category.STRUCTUREs with wave explosions
  ["oca_aircraft_damage_boost"] = 3000, --apply extra damage to parked Unit.Category.AIRPLANEs and Unit.Category.HELICOPTERs with wave explosions
  ["wave_explosions"] = true, --secondary explosions on top of game objects, radiating outward from the impact point and scaled based on size of object and distance from weapon impact point
  ["larger_explosions"] = true, --secondary explosions on top of weapon impact points, dictated by the values in the explTable
  ["damage_model"] = false, --allow blast wave to affect ground unit movement and weapons
  ["blast_search_radius"] = 100, --this is the max size of any blast wave radius, since we will only find objects within this zone
  ["cascade_damage_threshold"] = 0.1, --if the calculated blast damage doesn't exeed this value, there will be no secondary explosion damage on the unit.  If this value is too small, the appearance of explosions far outside of an expected radius looks incorrect.
  ["firebomb_splash_factor"] = 8, --apply a multiplier to thermobaric and napalm bombs so it matches the visual effect
  ["game_messages"] = true, --enable some messages on screen
  ["message_time"] = 20, --BDA messages remain this time on the screen, in seconds, if the option is enabled
  ["blast_stun"] = false, --not implemented
  ["unit_disabled_health"] = 30, --if health is below this value after our explosions, disable its movement
  ["unit_cant_fire_health"] = 50, --if health is below this value after our explosions, set ROE to HOLD to simulate damage weapon systems
  ["infantry_cant_fire_health"] = 90,  --if health is below this value after our explosions, set ROE to HOLD to simulate severe injury
  ["debug"] = false,  --enable debugging messages
  ["weapon_missing_message"] = false, --false disables messages alerting you to weapons missing from the explTable
  ["rocket_multiplier"] = 1.3, --multiplied by the explTable value for rockets
  ["explTable_multiplier"] = 1.0, --overall multiplier for explTable
  ["cluster_multiplier"] = 1.0, --overall multiplier for clusterDamage
  ["clusterEffectsEnable"] = false,
  ["shipRadarDamageEnable"] = false,
  ["cluster_munition_distribution_radius"] = 75, --distribution radius of submunition explosions, in meters, TODO: make this depend on the weapon type
}

local script_enable = 1
refreshRate = 0.1

----[[ ##### End of SCRIPT CONFIGURATION ##### ]]----

----[[ ##### explTable defines the values for the warhead of each explosive system in kg. This is where new weapons must be declared.  ##### ]]----
explTable = {
  ["FAB_100"] = 103,
  ["FAB_250"] = 238,
  ["FAB_250M54TU"]= 238,
  ["FAB_500"] = 506,
  ["FAB_1500"]  = 1500,
  ["BAP_100"] = 100,
  ["BetAB_500"] = 98,
  ["BetAB_500ShP"]= 107,
  ["KH-66_Grom"]  = 108,
  ["M_117"] = 201,
  ["AN_M64"]  = 121,                            --
  ["Mk_81"] = 118,                               --
  ["Mk_82"] = 241,
  ["Mk_83"] = 447,
  ["Mk_84"] = 874,                              --
  ["MK_82AIR"]  = 241,
  ["MK_82SNAKEYE"]= 241,                        --
  ["HB_F4E_GBU_8_HOBOS"]  = 874,                -- Heatblur F-4E HOBOS 
  ["GBU_10"]  = 874,                            --
  ["GBU_12"]  = 241,                            --
  ["HB_F4E_GBU15V1"] = 874,                     -- Heatblur F-4E GBU-15 
  ["GBU_16"]  = 447,                    --
  ["GBU_31"]  = 874,
  ["GBU_31_V_3B"] = 874,                        --
  ["GBU_31_V_2B"] = 874,
  ["GBU_31_V_4B"] = 874,                        --
  ["GBU_32_V_2B"] = 874,
  ["GBU_38"]  = 241,                            --
  ["GBU_54_V_1B"] = 241,
  ["GBU_24"]  = 874,                            --
  ["KAB_1500Kr"]  = 1500,                        --
  ["KAB_500Kr"] = 560,
  ["KAB_500"] = 534,        
  ["AGM_62"]  = 424,                            -- Walleye II 
  ["AGM_62_I"]  = 202,                          -- Walleye I
  ["X_23"]  = 111,                              -- Kh-23 Grom anti-radar (AS-7 'Kerry')
  ["X_23L"] = 111,                              -- Kh-23L Grom laser (AS-7 'Kerry')
  ["X_28"]  = 160,                              -- Kh-28 anti-radar (AS-9 'Kyle')
  ["X_25ML"]  = 89,                             -- Kh-25ML laser (AS-10 'Karen')
  ["X_25MP"]  = 89,                             -- Kh-25MP anti-radar (AS-12 'Kegler')
  ["X_25MR"]  = 140,                            -- Kh-25MR TV (AS-12 'Kegler')
  ["X_58"]  = 140,                              -- Kh-58 anti-radar (AS-11 'Kilter')
  ["X_29L"] = 320,                              -- Kh-29L laser (AS-14 'Kedge')
  ["X_29T"] = 320,                              -- Kh-29T TV (AS-14 'Kedge')
  ["X_29TE"]  = 320,                            -- Kh_29TE export (AS-14 'Kedge')
  ["X_31P"]  = 87,                              -- Kh-31P (AS-17 Krypton)
  ["X_65"]  = 410,                              -- Kh-65 (AS-15B Kent)
  ["Rb 04E"] = 300,
  ["Rb 15F"] = 200,
  ["Rb 15F (for A.I.)"] = 200,
  ["RB75"] = 57,
  ["RB75B"] = 57,
  ["RB75T"] = 136,
  ["AGM_12A"] = 113,                            -- Bullpup A
  ["AGM_12B"] = 113,                            -- Bullpup B
  ["AGM_12C"] = 454,                            -- Bullpup C
  ["HB_F4E_AGM_12C"] = 454,                     -- Bullpup C - Heatblur
  ["AGM_45A"] = 66,                             -- Shrike A
  ["AGM_45B"] = 66,                             -- Shrike B
  ["AGM_65A"] = 57,                             
  ["AGM_65B"] = 57,                             
  ["AGM_65D"] = 57,
  ["AGM_65E"] = 136,
  ["AGM_65F"] = 136,
  ["AGM_65G"] = 136,
  ["AGM_65H"] = 57,
  ["AGM_65K"] = 136,
  ["AGM_65L"] = 136,
  ["AGM_78A"] = 97,
  ["AGM_78B"] = 97,
  ["AGM_84A"] = 221,
  ["AGM_84D"] = 221,
  ["AGM_84S"] = 221,
  ["AGM_84E"] = 221,
  ["AGM_84H"] = 360,
  ["AGM_86"] = 908,
  ["AGM_86C"] = 908,
  ["AGM_88"] = 89,
  ["AGM_88C"] = 89,
  ["AGM_114K"] = 8,
  ["AGM_114L"] = 8,
  ["AGM_122"] = 15,
  ["AGM_123"] = 274,
  ["AGM_130"] = 874,
  ["AGM_119"] = 176,
  ["AGM_154"]  = 305,                            -- AGM-154C - JSOW Unitary BROACH
  ["AGM_154C"]  = 305,                           -- AGM-154C - JSOW Unitary BROACH
  ["S-24A"] = 24,                                --
  ["S-24B"] = 123,                               --
  ["S-25OF"]  = 194,                             --
  ["S-25OFM"] = 150,                             --
  ["S-25O"] = 150,                               --
  ["S_25L"] = 190,                               --
  ["S-5M"]  = 5,                                 --
  ["C_5"]  = 5,                                  -- S-5
  ["C_8"]   = 8,                                 -- S-8
  ["C_8CM"] = 8,                                 -- S-8CM (с цветным дымом / with colored smoke )
  ["C_8OFP2"] = 8,                               -- S-8OFP2
  ["C_13"]  = 21,                                -- S-13
  ["C_24"]  = 123,                               -- S-24
  ["C_25"]  = 151,                               -- S-25
  ["HVAR"] = 13,
  ["Zuni_127"]  = 13,
  ["Zuni_127CM"]  = 13,
  ["ARAKM70BHE"]  = 14,
  ["BR_500"]  = 118,
  ["Rb 05A"]  = 217,
  ["HEBOMB"]  = 120,
  ["HEBOMBD"] = 120,
  ["MK-81SE"] = 60,
  ["AGR_20A"] = 8,                               -- A10C Laser-guided M151
  ["AGR_20_M282"] = 8,                           -- A10C APKWS Laser-guided M282
  ["HYDRA_70"] = 7,                              -- Hydra 70 2.75-inch/70mm rocket
  ["HYDRA_70_M151"] = 7,                         -- Hydra 70 2.75-inch/70mm rocket, M151 HEDP warhead
  ["HYDRA_70_M229"] = 7,                         -- Hydra 70 2.75-inch/70mm rocket, M229 HEDP warhead
  ["HYDRA_70_M282"] = 7,                         -- Hydra 70 2.75-inch/70mm rocket, M282 MPP (penetrator) warhead
  ["HYDRA_70_MK5"] = 7,                          -- Hydra 70 2.75-inch/70mm rocket, Mk5 HEAT warhead
  ["FFAR Mk1 HE"] = 8,
  ["FFAR Mk5 HEAT"] = 8,
  ["SNEB68_EAP"] = 7,
  ["SNEB_TYPE253_H1"] = 7,
  ["SNEB_TYPE251_F1B"] = 7,
  ["MALUTKA"] = 4,                               -- AT-3 Sagger / 9M14 Malyutka
  ["KONKURS"] = 3,                               -- AT-5 Spandrel / 9M113 Konkurs
  ["AT_6"] = 6,                                  -- AT-6 Spiral / 9K114 Shturm
  ["Ataka_9M120"] = 8,                           -- AT-9 Spiral-2 / 9M120 Ataka
  ["Ataka_9M120F"] = 8 * splash_damage_options.firebomb_splash_factor, -- AT-9 Spiral-2 / 9M120F Ataka (thermobaric)
  ["P_9M117"] = 3,                               -- AT-10 Stabber / 9M117 Bastion
  ["SVIR"] = 5,                                  -- AT-11 Sniper / 9M119 Svir
  ["REFLEX"] = 5,                                -- AT-11 Sniper / 9M119M Refleks
  ["Vikhr_M"] = 12,                              -- AT-16 Scallion / 9K121 Vikhr
  ["HOT2"] = 15,
  ["HOT3"] = 15,
  ["TOW2"] = 15,
  ["TOW"] = 15,
  ["URAGAN_9M27F"] = 100,                        -- BM-27 Uragan / 9M27F (220mm HE)
  ["SMERCH_9M55F"] = 243,                        -- BM-30 Smerch / 9M55F (300mm HE)
  ["ALARM"] = 66,                                -- ALARM (Air-Launched Anti-Radiation Missile) - 146lbs (66kg) direct fragmentation with proximity/contact fuse
  ["Sea_Eagle"] = 230,
  ["YJ-83K"] = 165,                              -- Air-launched YJ-83 anti-ship missile
  ["250-3"] = 100,                               --("250 lb GP")
  ["British_GP_250LB_Bomb_Mk1"] = 100,           --("250 lb GP Mk.I")
  ["British_GP_250LB_Bomb_Mk4"] = 100,           --("250 lb GP Mk.IV")
  ["British_GP_250LB_Bomb_Mk5"] = 100,           --("250 lb GP Mk.V")
  ["British_GP_500LB_Bomb_Mk1"] = 213,           --("500 lb GP Mk.I")
  ["British_GP_500LB_Bomb_Mk4"] = 213,           --("500 lb GP Mk.IV")
  ["British_GP_500LB_Bomb_Mk4_Short"] = 213,     --("500 lb GP Short tail")
  ["British_GP_500LB_Bomb_Mk5"] = 213,           --("500 lb GP Mk.V")
  ["British_MC_250LB_Bomb_Mk1"] = 100,           --("250 lb MC Mk.I")
  ["British_MC_250LB_Bomb_Mk2"] = 100,           --("250 lb MC Mk.II")
  ["British_MC_500LB_Bomb_Mk1_Short"] = 213,     --("500 lb MC Short tail")
  ["British_MC_500LB_Bomb_Mk2"] = 213,           --("500 lb MC Mk.II")
  ["British_SAP_250LB_Bomb_Mk5"] = 100,          --("250 lb S.A.P.")
  ["British_SAP_500LB_Bomb_Mk5"] = 213,          --("500 lb S.A.P.")
  ["British_AP_25LBNo1_3INCHNo1"] = 4,           --("RP-3 25lb AP Mk.I")
  ["British_HE_60LBSAPNo2_3INCHNo1"] = 4,        --("RP-3 60lb SAP No2 Mk.I")
  ["British_HE_60LBFNo1_3INCHNo1"] = 4,          --("RP-3 60lb F No1 Mk.I")
  ["WGr21"] = 21,                                --("Werfer-Granate 21 - 21 cm UnGd air-to-air rocket")
  ["3xM8_ROCKETS_IN_TUBES"] = 12,                --("4.5 inch M8 UnGd Rocket")
  ["AN_M30A1"] = 45,                             --("AN-M30A1 - 100lb GP Bomb LD")
  ["AN-M57"] = 100,                              --("AN-M57 - 250lb GP Bomb LD")
  ["AN-M64"] = 213,                              --("AN-M64 - 500lb GP Bomb LD")
  ["AN-M65"] = 400,                              --("AN-M65 - 1000lb GP Bomb LD")
  ["AN-M66A2"] = 536,                            --("AN-M66A2 - 2000lb GP Bomb LD")
  ["AN_M57"] = 100,                              --("AN-M57 - 250lb GP Bomb LD")
  ["AN_M65"] = 400,                              --("AN-M65 - 1000lb GP Bomb LD")
  ["AN_M66"] = 536,                              --("AN-M66 - 2000lb GP Bomb LD")
  ["AN_M66A2"] = 536,                            --("AN-M66 - 2000lb GP Bomb LD")
  ["AN_M81"] = 110,                              --("AN-M81 - 260lb GP Bomb LD")
  ["AN_M88"] = 97,                               --("AN-M88 - 216lb GP Bomb LD")
  ["SC_50"] = 20,                                --("SC 50 - 50kg GP Bomb LD")
  ["ER_4_SC50"] = 20,                            --("4 x SC 50 - 50kg GP Bomb LD")
  ["SC_250_T1_L2"] = 100,                        --("SC 250 Type 1 L2 - 250kg GP Bomb LD")
  ["SC_501_SC250"] = 100,                        --("SC 250 Type 3 J - 250kg GP Bomb LD")
  ["Schloss500XIIC1_SC_250_T3_J"] = 100,         --("SC 250 Type 3 J - 250kg GP Bomb LD")
  ["SC_501_SC500"] = 213,                        --("SC 500 J - 500kg GP Bomb LD")
  ["SC_500_J"] = 213,                            --("SC 500 J - 500kg GP Bomb LD")
  ["SC_500_L2"] = 213,                           --("SC 500 L2 - 500kg GP Bomb LD")
  ["SD_250_Stg"] = 100,                          --("SD 250 Stg - 250kg GP Bomb LD")
  ["SD_500_A"] = 213,                            --("SD 500 A - 500kg GP Bomb LD")
  ["LTF_5B"] = 100,                              --("LTF 5b Aerial Torpedo")
  ["BL_755"] = 132,                              --("BL755 - 147 x parachute-retarded HEAT submunitions, 264kg")
  ["MK77mod0-WPN"] = 110 * splash_damage_options.firebomb_splash_factor, --("Mk 77 Mod 0 - 750 lb (340 kg) with 110 U.S. gallons (416 L; 92 imp gal) of petroleum oil.")
  ["MK77mod1-WPN"] = 75 * splash_damage_options.firebomb_splash_factor,  --("Mk 77 Mod 1 - 500 lb (230 kg) with 75 U.S. gallons (284 L; 62 imp gal) of petroleum oil.")
  ["BIN_200"] = 75 * splash_damage_options.firebomb_splash_factor,     --("BIN-200 - 200 kg Spanish liquid incendiary Napalm filled bomb.")
  ["M_230_new"] = 3,                             --30mm M230 autocannon (AH-64)
  ["2A42"] = 3,                                  --30mm Shipunov 2A42 autocannon (Ka-50)
  ["GSh_23_UPK"] = 2.3,                          --23mm GSh-23 autocannon (Ka-50)
  ["GSh_30_2K"] = 3,                             --30mm GSh-30 autocannon (Mi-24P)
  --["BLU-97/B"] = 10,
  --["BLU-97B"] = 10,
  --["MK118"] = 8,
}

clusterDamage = {
  ["BK90_MJ1"] = 3,                              -- BK-90 MJ1 (72 x MJ1 HE-FRAG Bomblets)
  ["BK90_MJ2"] = 10,                             -- BK-90 MJ2 (24 x MJ2 HEAT Bomblets)
  ["BK90_MJ1_MJ2"] = 8,                          -- BK-90 MJ1+2 (12x MJ2 HEAT / 36x MJ1 HE-FRAG Bomblets)
  ["BLG-66"] = 0.51,                             -- BLG-66 Belouga AC - 305kg CBU, 151 x HEAT Bomblets
  ["GR_66_AC"] = 0.51,                           -- BLG-66 Belouga AC - 305kg CBU, 151 x HEAT Bomblets
  --["ROCKEYE"] = 0.18,                            -- ("Mk-20 - 247 x Mk 118 Mod 1 bomblets, 222kg")
  --["CBU_87"] = 0.287,                            -- CBU-87 - 202 x CEM Cluster Bomb
  --["CBU_99"] = 0.18,                             -- CBU-99 - 247 x CEM Cluster Bomb
  ["Mk 118"] = 0.18,                             -- CBU-99 - 247 x CEM Cluster Bomb
  ["MK118"] = 0.18,                              -- CBU-99 - 247 x CEM Cluster Bomb
  ["BLU-97B"] = 0.287,                           -- CBU-87/103 - 202 x CEM, CBU with WCMD
  ["BLU-97/B"]  = 0.287,                         -- AGM-154A - JSOW CEB (CBU-type) - 145 BLU-97/B Combined Effects Bomb (CEB) submunitions
  --["AGM_154A"]  = 0.287,                         -- AGM-154A - JSOW CEB (CBU-type) - 145 BLU-97/B Combined Effects Bomb (CEB) submunitions
  ["BLU-108"] = 10,
  ["PTAB-2.5KO"]= 10,                            -- BKF - 12 x PTAB-2.5KO
  ["AO-2.5RT"]= 10,                              -- BKF - 12 x AO-2.5RT
  ["AO-1SCh"] = 1.67,                            -- RBK-250-275 - 150 x AO-1SCh, 250kg CBU HE/Frag
  ["PTAB-2-5"] = 5.95,                           -- RBK-250 - 42 x PTAB-2.5M, 250kg CBU Medium HEAT/AP
  ["PTAB-10-5"] = 16.67,                         -- RBK-500-255 - 30 x PTAB-10-5 CBU Heavy HEAT/AP
  ["PTAB-1M"] = 1.75,                            -- RBK-500U - 268 x PTAB-1M CBU Light HEAT/AP
  ["OAB_2_5RT"] = 3.97,                          -- RBK-500U - 126 x OAB-2.5RT, 500kg CBU HE/Frag
  ["SD-2"] = 1.73,                               --("AB 250-2 - 144 x SD-2, 250kg CBU with HE submunitions")
  ["SD-10A"] = 10,                               --("AB 250-2/1 - 17/34 x SD-10A, 250/500kg CBU with 10kg Frag/HE submunitions")
}

clusterWeaps = {
  ["BK90_MJ1"] = 72,                             -- BK-90 MJ1 (72 x MJ1 HE-FRAG Bomblets)
  ["BK90_MJ2"] = 24,                             -- BK-90 MJ2 (24 x MJ2 HEAT Bomblets)
  ["BK90_MJ1_MJ2"] = 48,                         -- BK-90 MJ1+2 (12x MJ2 HEAT / 36x MJ1 HE-FRAG Bomblets)
  ["BLG-66"] = 151,                              -- BLG-66 Belouga AC - 305kg CBU, 151 x HEAT Bomblets
  ["GR_66_AC"] = 151,                            -- BLG-66 Belouga AC - 305kg CBU, 151 x HEAT Bomblets
  --["ROCKEYE"] = 247,                             -- ("Mk-20 - 247 x Mk 118 Mod 1 bomblets, 222kg")
  --["CBU_87"] = 202,                              -- CBU-87 - 202 x CEM Cluster Bomb
  --["CBU_99"] = 247,                              -- CBU-99 - 247 x CEM Cluster Bomb
  ["Mk 118"] = 247,                              -- CBU-99 - 247 x CEM Cluster Bomb
  ["MK118"] = 247,                               -- CBU-99 - 247 x CEM Cluster Bomb
  ["BLU-97B"] = 202,                             -- CBU-87/103 - 202 x CEM, CBU with WCMD
  ["BLU-97/B"]  = 145,                           -- AGM-154A - JSOW CEB (CBU-type) - 145 BLU-97/B Combined Effects Bomb (CEB) submunitions
  --["AGM_154A"]  = 145,                           -- AGM-154A - JSOW CEB (CBU-type) - 145 BLU-97/B Combined Effects Bomb (CEB) submunitions
  ["BLU-108"] = 30,
  ["PTAB-2.5KO"] = 12,                           -- BKF - 12 x PTAB-2.5KO
  ["AO-2.5RT"] = 12,                             -- BKF - 12 x AO-2.5RT
  ["AO-1SCh"] = 150,                             -- RBK-250-275 - 150 x AO-1SCh, 250kg CBU HE/Frag
  ["PTAB-2-5"] = 42,                             -- RBK-250 - 42 x PTAB-2.5M, 250kg CBU Medium HEAT/AP
  ["PTAB-10-5"] = 30,                            -- RBK-500-255 - 30 x PTAB-10-5 CBU Heavy HEAT/AP
  ["PTAB-1M"] = 268,                             -- RBK-500U - 268 x PTAB-1M CBU Light HEAT/AP
  ["OAB_2_5RT"] = 126,                           -- RBK-500U - 126 x OAB-2.5RT, 500kg CBU HE/Frag
  ["SD-2"] = 144,                                --("AB 250-2 - 144 x SD-2, 250kg CBU with HE submunitions")
  ["SD-10A"] = 17,                               --("AB 250-2/1 - 17/34 x SD-10A, 250/500kg CBU with 10kg Frag/HE submunitions")
  -- can't really model AB 250-1 since it uses exactly the same submunitions as AB 250-2
}

antiRadiationMissile = {
  ["AGM_45A"] = 1,
  ["AGM_88"] = 1,
  ["AGM_88C"] = 1,
  ["AGM-88C"] = 1,
  ["AGM_122"] = 1,
  ["ALARM"] = 1,
  ["X_25MP"]  = 1,
  ["X_28"]  = 1,
  ["X_58"]  = 1,
}

ignoredWeaps = {
  ["AK_74"] = 1,                                  --5.45mm
  ["M4"] = 1,                                     --5.56mm
  ["M249"] = 1,                                   --5.56mm
  ["7_62_MG"] = 1,                                --7.62mm
  ["7_62_PKT"] = 1,                               --7.62mm
  ["7_62_L94A1"] = 1,                             --7.62mm
  ["M_134"] = 1,                                  --7.62mm
  ["M240"] = 1,                                   --7.62mm
  ["PK-3"] = 1,                                   --7.62mm, PK-3 GPMG
  ["SHKAS_GUN"] = 1,                              --7.62mm, ShKAS machine gun
  ["M1 Garand .30 cal"] = 1,                      --7.62mm, .30-06
  ["Browning .30 cal"] = 1,                       --7.62mm, .30-06
  ["Browning303MkII"] = 1,                        --7.7 mm, .303
  ["Lee-Enfield SMLE No.4 Mk.1"] = 1,             --7.7 mm, .303
  ["MG34"] = 1,                                   --7.92mm
  ["Besa"] = 1,                                   --7.92mm
  ["12_7_MG"] = 1,                                --12.7mm
  ["A20_TopTurret_M2_L"] = 1,                     --12.7mm
  ["A20_TopTurret_M2_R"] = 1,                     --12.7mm
  ["M2_Browning"] = 1,                            --12.7mm
  ["BrowningM2"] = 1,                             --12.7mm
  ["m3_browning"] = 1,                            --12.7mm
  ["m3_f84g"] = 1,                                --12.7mm
  ["KORD_12_7"] = 1,                              --12.7mm
  ["KPVT"] = 1,                                   --14.5mm
  ["coltMK12"] = 1,                               --20mm
  ["HispanoMkII"] = 1,                            --20mm
  ["2A14_2"] = 1,                                 --23mm, ZU-23
  ["2A14_4"] = 1,                                 --23mm, ZSU-23
  ["NR-23"] = 1,                                  --23mm, NR-23
  ["GSH_23"] = 1,                                 --23mm
  ["M242_Bushmaster"] = 1,                        --25mm
  ["2A38"] = 1,                                   --30mm, 2S6 Tunguska
  ["2A72"] = 1,                                   --30mm, BMP-2
  ["DEFA 554"] = 1,                               --30mm
  ["NR-30"] = 1,                                  --30mm
  ["GSh_30_2"] = 1,                               --30mm
  ["GSh_30_6"] = 1,                               --30mm
  ["GSh-6-30K"] = 1,                              --30mm
  ["GAU_8"] = 1,                                  --30mm
  ["N-37"] = 1,                                   --37mm
  ["Flak M1 37mm"] = 1,                           --37mm
  ["Bofors 40mm gun"] = 1,                        --40mm
  ["Mk.19"] = 1,                                  --40mm
  ["S_68"] = 1,                                   --57mm
  ["AAA 01"] = 1,
}

----[[ ##### HELPER/UTILITY FUNCTIONS ##### ]]----

local function tableHasKey(table,key)
    return table[key] ~= nil
end

local function debugMsg(str)
  if splash_damage_options.debug == true then
    trigger.action.outText(str , tonumber(splash_damage_options.message_time))
  end
end

local function gameMsg(str)
  if splash_damage_options.game_messages == true then
    trigger.action.outText(str ,tonumber(splash_damage_options.message_time))
  end
end

local function getDistance(point1, point2)
  local x1 = point1.x
  local y1 = point1.y
  local z1 = point1.z
  local x2 = point2.x
  local y2 = point2.y
  local z2 = point2.z
  local dX = math.abs(x1-x2)
  local dZ = math.abs(z1-z2)
  local distance = math.sqrt(dX*dX + dZ*dZ)
  return distance
end

local function getDistance3D(point1, point2)
  local x1 = point1.x
  local y1 = point1.y
  local z1 = point1.z
  local x2 = point2.x
  local y2 = point2.y
  local z2 = point2.z
  local dX = math.abs(x1-x2)
  local dY = math.abs(y1-y2)
  local dZ = math.abs(z1-z2)
  local distance = math.sqrt(dX*dX + dZ*dZ + dY*dY)
  return distance
end

local function vec3Mag(speedVec)
  local mag = speedVec.x*speedVec.x + speedVec.y*speedVec.y+speedVec.z*speedVec.z
  mag = math.sqrt(mag)
  --trigger.action.outText("X = " .. speedVec.x ..", y = " .. speedVec.y .. ", z = "..speedVec.z, 10)
  --trigger.action.outText("Speed = " .. mag, 1)
  return mag
end

local function lookahead(speedVec)
  local speed = vec3Mag(speedVec)
  local dist = speed * refreshRate * 1.5
  return dist
end

----[[ ##### End of HELPER/UTILITY FUNCTIONS ##### ]]----


WpnHandler = {}
tracked_weapons = {}

function track_wpns()
--  env.info("Weapon Track Start")
  for wpn_id_, wpnData in pairs(tracked_weapons) do
    if wpnData.wpn:isExist() then  -- just update speed, position and direction.
      wpnData.pos = wpnData.wpn:getPosition().p
      wpnData.dir = wpnData.wpn:getPosition().x
      wpnData.speed = wpnData.wpn:getVelocity()
      --wpnData.lastIP = land.getIP(wpnData.pos, wpnData.dir, 50)
    else -- wpn no longer exists, must be dead.
--      trigger.action.outText("Weapon impacted, mass of weapon warhead is " .. wpnData.exMass, 2)
      local ip = land.getIP(wpnData.pos, wpnData.dir, lookahead(wpnData.speed))  -- terrain intersection point with weapon's nose.  Only search out 20 meters though.
      local impactPoint
      if not ip then -- use last calculated IP
        impactPoint = wpnData.pos
  --        trigger.action.outText("Impact Point:\nPos X: " .. impactPoint.x .. "\nPos Z: " .. impactPoint.z, 2)
      else -- use intersection point
        impactPoint = ip
  --        trigger.action.outText("Impact Point:\nPos X: " .. impactPoint.x .. "\nPos Z: " .. impactPoint.z, 2)
      end
      --env.info("Weapon is gone") -- Got to here --
      --trigger.action.outText("Weapon Type was: ".. wpnData.name, 20)
      if splash_damage_options.larger_explosions == true then
        --env.info("triggered explosion size: "..getWeaponExplosive(wpnData.name))
        trigger.action.explosion(impactPoint, getWeaponExplosive(wpnData.name))
        --trigger.action.smoke(impactPoint, 0)
      end

      local obj_land_height = land.getHeight({x = impactPoint.x , y = impactPoint.z})
      local impact_ground_pos = {
              x = impactPoint.x,
              y = obj_land_height,
              z = impactPoint.z
            }
      if wpnData.name == "MK77mod1-WPN" or wpnData.name == "BIN_200" then
          trigger.action.effectSmokeBig(impact_ground_pos, 2, 0.5, wpnData.name)
      elseif wpnData.name == "MK77mod0-WPN" then
          trigger.action.effectSmokeBig(impact_ground_pos, 3, 0.5, wpnData.name)
      end

      local explosive = getWeaponExplosive(wpnData.name)
      local weapon = wpnData.wpn
      local player = wpnData.player

      if wpnData.cat == Weapon.Category.ROCKET then
        explosive = explosive * splash_damage_options.rocket_multiplier / 100
      elseif clusterWeaps[wpnData.name] then
        explosive = getClusterExplosive(weapon)
      end

      if splash_damage_options.clusterEffectsEnable and clusterWeaps[wpnData.name] then
        for i=1,clusterWeaps[wpnData.name]
        do
          cluster_radius = math.random(0, splash_damage_options.cluster_munition_distribution_radius)
          cluster_angle = 2 * math.pi * (math.random())
          local X = impactPoint.x + cluster_radius * math.cos(cluster_angle)
          local Z = impactPoint.z + cluster_radius * math.sin(cluster_angle)
          blastPoint = {
            x = X,
            y = land.getHeight({x = X , y = Z}),
            z = Z
          }
          --env.info('Generating cluster bomb explosion at: X: ' .. blastPoint.x .. ' Y: ' .. blastPoint.y .. ' Z: ' .. blastPoint.z)
          --debugMsg('Generating cluster bomb explosion at: X: ' .. blastPoint.x .. ' Y: ' .. blastPoint.y .. ' Z: ' .. blastPoint.z)
          --timer.scheduleFunction(explodeObject, {blastPoint, 0, explosive}, timer.getTime() + math.random(0, 3))
          blastWave(blastPoint, splash_damage_options.blast_search_radius, weapon, getClusterExplosive(wpnData.name), player)
        end
        debugMsg('Cluster explosions generated for ' .. wpnData.name)
      end

      blastWave(impactPoint, splash_damage_options.blast_search_radius, weapon, explosive, player)
      debugMsg('Stop track: '..wpnData.name)
      tracked_weapons[wpn_id_] = nil -- remove from tracked weapons first.
    end
  end
--  env.info("Weapon Track End")
end

function onWpnEvent(event)
  if event.weapon and ignoredWeaps[event.weapon:getTypeName()] then
    return
  end
  if event.weapon and explTable[event.weapon:getTypeName()] == nil and clusterWeaps[event.weapon:getTypeName()] == nil then
    if string.find(event.weapon:getTypeName(), "weapons.shells") then
      debugMsg("event shot, but not tracking: "..event.weapon:getTypeName())
      return  --we wont track these types of weapons, so exit here
    end
    env.info(event.weapon:getTypeName().." missing from Splash Damage script")
    debugMsg(event.weapon:getTypeName().." missing from Splash Damage script")
    if splash_damage_options.weapon_missing_message == true then
      debugMsg(event.weapon:getTypeName().." missing from Splash Damage script")
      debugMsg("desc: "..mist.utils.tableShow(event.weapon:getDesc()))
    end
    return
  end
  if event.id == world.event.S_EVENT_SHOT then
    if event.weapon then
      local ordnance = event.weapon
      local weapon_desc = ordnance:getDesc()

      --trigger.action.outText(ordnance:getTypeName().." found.", 10)
      debugMsg('Weapon shot: ' .. event.weapon:getTypeName())
      if (weapon_desc.category ~= 0) and event.initiator then
        debugMsg('Tracking weapon: ' .. event.weapon:getTypeName())
        tracked_weapons[event.weapon.id_] = { wpn = ordnance, init = event.initiator:getName(), pos = ordnance:getPoint(), dir = ordnance:getPosition().x, name = ordnance:getTypeName(), speed = ordnance:getVelocity(), cat = ordnance:getCategory(), player=event.initiator:getPlayerName() }
      end
    end
  --elseif event.id == world.event.S_EVENT_SHOOTING_START or event.id == world.S_EVENT_SHOOTING_END then
    --debugMsg("Start/Stop shooting with "..event.weapon_name)
  elseif event.id == world.event.S_EVENT_HIT then
    --debugMsg('Hit occurred with '..event.weapon:getTypeName()..' ('..event.weapon:getCategory()..')'..': '..mist.utils.tableShow(event.weapon:getDesc()))
    --debugMsg('Event table: '..mist.utils.tableShow(event))
    if event.weapon and event.target then
      local weapon = event.weapon:getTypeName()
      if splash_damage_options.shipRadarDamageEnable and event.target:getDesc().category == Unit.Category.SHIP and antiRadiationMissile[weapon] ~= nil then
        event.target:enableEmission(false)
        env.info("BDA: "..event.target:getTypeName().." radar destroyed")
        if event.initiator then
          if event.initiator:getPlayerName() ~= nil then
            gameMsg("BDA: "..event.target:getTypeName().." radar destroyed")
          end
        end
      end

      local player = event.initiator
      local targetName = event.target:getTypeName()
      local impactPoint = event.target:getPosition().p
      if weapon and targetName then
        env.info(weapon.." hit "..targetName)
        debugMsg(weapon.." hit "..targetName)
      end
      --env.info('Impact point was at: X: ' .. impactPoint.x .. ' Y: ' .. impactPoint.y .. ' Z: ' .. impactPoint.z)
      if clusterWeaps[weapon] then
        local ordnance = event.weapon
        tracked_weapons[event.weapon.id_] = { wpn = ordnance, init = event.initiator:getName(), pos = ordnance:getPoint(), dir = ordnance:getPosition().x, name = ordnance:getTypeName(), speed = ordnance:getVelocity(), cat = ordnance:getCategory(), player=event.initiator }
      else
        blastWave(impactPoint, splash_damage_options.blast_search_radius, event.weapon, getWeaponExplosive(weapon), player)
      end
    end
  elseif event.id == world.event.S_EVENT_KILL and event.initiator ~= nil then
    destroyedBda(event.target)
  end
end

local function protectedCall(...)
  local status, retval = pcall(...)
  if not status then
    env.warning("Splash damage script error... gracefully caught! " .. retval, true)
  end
end


function WpnHandler:onEvent(event)
  protectedCall(onWpnEvent, event)
end



function explodeObject(table)
  local point = table[1]
  local distance = table[2]
  local power = table[3]
  trigger.action.explosion(point, power)
end


function getClusterExplosive(name)
  if clusterWeaps[name] then
    return clusterDamage[name] * splash_damage_options.cluster_multiplier / 100
  else
    return 0
  end
end


function getWeaponExplosive(name)
  if explTable[name] then
    return explTable[name] * splash_damage_options.explTable_multiplier / 100
  else
    return 0
  end
end

--controller is only at group level for ground units.  we should itterate over the group and only apply effects if health thresholds are met by all units in the group
function modelUnitDamage(table)
  local units = table[1]
  local player = table[2]
  --debugMsg("units table: "..mist.utils.tableShow(units))
  for i, unit in ipairs(units)
  do
    --debugMsg("unit table: "..mist.utils.tableShow(unit))
    if unit:isExist() then  --if units are not already dead
      local health = (unit:getLife() / unit:getDesc().life) * 100
      --debugMsg(unit:getTypeName().." health %"..health)

      if player ~= nil and health < 100 then
        gameMsg("BDA: "..unit:getTypeName().." damaged: "..100-health.."%")
      end

      if unit:hasAttribute("Infantry") == true and health > 0 then  --if infantry
        if health <= splash_damage_options.infantry_cant_fire_health then
          ---disable unit's ability to fire---
          unit:getController():setOption(AI.Option.Ground.id.ROE , AI.Option.Ground.val.ROE.WEAPON_HOLD)
        end
      elseif unit:getDesc().category == Unit.Category.GROUND_UNIT == true and unit:hasAttribute("Infantry") == false and health > 0 then  --if ground unit but not infantry
        if health <= splash_damage_options.unit_cant_fire_health then
          ---disable unit's ability to fire---
          unit:getController():setOption(AI.Option.Ground.id.ROE , AI.Option.Ground.val.ROE.WEAPON_HOLD)

          if player ~= nil then
            gameMsg("Critical hit: "..unit:getTypeName().." weapons disabled")
          end
        end
        if health <= splash_damage_options.unit_disabled_health and health > 0 then
          ---disable unit's ability to move---
          unit:getController():setTask({id = 'Hold', params = { }} )
          unit:getController():setOnOff(false)

          if player ~= nil and health < 100 then
            gameMsg("Critical hit: "..unit:getTypeName().." disabled")
          end
        end
      end
    else
      --debugMsg("unit no longer exists")
      --pcall(destroyedBda, unit)
    end
  end
end

-- This is run inside a function with a protected call (pcall),
-- so we allow the unit to have been destroyed and cleaned up
-- between the start and finish of the function when calling unit:getName()
-- This allows us to avoid "Unit does not exist" errors in the log.
function destroyedBda(unit)
  if unit == nil then
    gameMsg("BDA: target destroyed")
  elseif unit:getTypeName() == nil then
    gameMsg("BDA: target destroyed")
  else
    gameMsg("BDA: "..unit:getTypeName().." critically damaged")
  end
end

function blastWave(_point, _radius, weapon, power, player)
  local foundUnits = {}
  local volS = {
   id = world.VolumeType.SPHERE,
   params = {
     point = _point,
     radius = _radius
   }
  }

  local ifFound = function(foundObject, val)
    if foundObject:getDesc().category == Unit.Category.GROUND_UNIT and foundObject:getCategory() == Object.Category.UNIT then
      foundUnits[#foundUnits + 1] = foundObject
    end
    if foundObject:getDesc().category == Unit.Category.GROUND_UNIT then --if ground unit
      if splash_damage_options.blast_stun == true then
        --suppressUnit(foundObject, 2, weapon)
      end
    end
    if splash_damage_options.wave_explosions == true then
      local obj = foundObject
      local obj_location = obj:getPoint()
      local distance = getDistance(_point, obj_location)
      local timing = distance/500
      if obj:isExist() then

        local damage_for_surface = 0

        if tableHasKey(obj:getDesc(), "box") then
          local length = (obj:getDesc().box.max.x + math.abs(obj:getDesc().box.min.x))
          local height = (obj:getDesc().box.max.y + math.abs(obj:getDesc().box.min.y))
          local depth = (obj:getDesc().box.max.z + math.abs(obj:getDesc().box.min.z))
          local _length = length
          local _depth = depth
          if depth > length then
            _length = depth
            _depth = length
          end
          local surface_distance = distance - _depth/2
          local scaled_power_factor = 0.006 * power + 1 --this could be reduced into the calc on the next line
          local intensity = (power * scaled_power_factor) / (4 * 3.14 * surface_distance * surface_distance )
          local surface_area = _length * height --Ideally we should roughly calculate the surface area facing the blast point, but we'll just find the largest side of the object for now
          damage_for_surface = intensity * surface_area
          --debugMsg(obj:getTypeName().." sa:"..surface_area.." distance:"..surface_distance.." dfs:"..damage_for_surface)
          if damage_for_surface > splash_damage_options.cascade_damage_threshold then
            local explosion_size = damage_for_surface
            if obj:getDesc().category == Unit.Category.STRUCTURE then
              explosion_size = intensity * splash_damage_options.static_damage_boost --apply an extra damage boost for static objects. should we factor in surface_area?
              --debugMsg("static obj :"..obj:getTypeName())
            end

            local obj_altitude_ground = getAGL(obj)
            -- Deal extra damage to parked airplanes and helicopters to make OCA/Aircraft missions more viable
            if (obj:getDesc().category == Unit.Category.AIRPLANE or obj:getDesc().category == Unit.Category.HELICOPTER) and (obj:inAir() == false or obj_altitude_ground < 50) then
              explosion_size = intensity * splash_damage_options.oca_aircraft_damage_boost --apply an extra damage boost for aircraft to increase kill probability on OCA/Aircraft missions.
              --debugMsg("static obj :"..obj:getTypeName())
            end
            -- According to toutenglisse on DCS World forums (2022-06-11), ships do not have sensors attributes and therefore obj:hasSensors(Unit.SensorType.RADAR) cannot be used
            -- "I don't know why, but no Ship in DCS has ["sensors"] in its attributes (while obviously they have and can use them in game...). No way to use Ship with getDetectedTargets function (except for visual detection)."
            if splash_damage_options.shipRadarDamageEnable and obj:getDesc().category == Unit.Category.SHIP and antiRadiationMissile[weapon:getTypeName()] ~= nil then
              obj:enableEmission(false)
              env.info("BDA: "..event.target:getTypeName().." radar destroyed")
              if player ~= nil then
                gameMsg("BDA: "..obj:getTypeName().." radar destroyed")
              end
            end

            if explosion_size > power then explosion_size = power end --secondary explosions should not be larger than the explosion that created it
            local id = timer.scheduleFunction(explodeObject, {obj_location, distance, explosion_size}, timer.getTime() + timing)  --create the explosion on the object location

            if player ~= nil then
              gameMsg("BDA: "..obj:getTypeName().." damaged: "..damage_for_surface)
            end
          end
        else
          debugMsg(obj:getTypeName().." object does not have box property")  -- should never happen...
        end
      end
    end
    return true
  end

  world.searchObjects(Object.Category.UNIT, volS, ifFound)
  world.searchObjects(Object.Category.STATIC, volS, ifFound)
  world.searchObjects(Object.Category.SCENERY, volS, ifFound)
  world.searchObjects(Object.Category.CARGO, volS, ifFound)
  --world.searchObjects(Object.Category.BASE, volS, ifFound)

  if splash_damage_options.damage_model == true then
    local id = timer.scheduleFunction(modelUnitDamage, {foundUnits, player}, timer.getTime() + 1.5) --allow some time for the game to adjust health levels before running our function
  end
end


function getAGL(obj)
  -- Object's altitude from ground
  local obj_vec3 = obj:getPoint()
  local obj_land_height = land.getHeight({x = obj_vec3.x , y = obj_vec3.z})
  -- Altitude from ground in meters
  local obj_altitude_MSL = obj:getPoint().y -- Altitude MSL, in meters
  return obj_altitude_MSL - obj_land_height
end


if (script_enable == 1) then
  gameMsg("SPLASH DAMAGE 2 SCRIPT RUNNING")
  env.info("SPLASH DAMAGE 2 SCRIPT RUNNING")
  timer.scheduleFunction(function()
      protectedCall(track_wpns)
      return timer.getTime() + refreshRate
    end, 
    {}, 
    timer.getTime() + refreshRate
  )
  world.addEventHandler(WpnHandler)
end
