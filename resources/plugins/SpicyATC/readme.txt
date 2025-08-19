Hi, thank you for using my tool. I have worked hard on this and I hope it at least improves your experience. If you have any issues/suggestions, message me on discord @spicy2160

Instructions:
-Copy the script into your DCS mission’s Scripts folder or another location of your choice. (C:\Users{user}\Saved Games\DCS\Scripts)

-In the DCS Mission Editor, add a trigger at mission start (i use the following):

Trigger: ONCE, NO EVENT

Condition: Time More (1 second)

Action: "Do Script File" and point it to spicyATC.lua

-Save and run your mission. (Script should work on start-up)
No additional mods or tools are required.

Usage:
-When you start the mission, open the F10 menu and select SpicyATC. You will see submenus for Ground, Tower, and Slasher (idk what this is called in BMS, for now pretend it is your overlord). I have tested it for jets and know that it works for now. Helicopters are most likely not full function. I have tested on red and blue coalition.

At any point, under the ground menu, hit refresh airbase list, and then return to ground menu, to change your home airbase.

Follow the sequence of calls:

Ground → Request Startup Clears you (or your flight) to start engines.

Ground → Request Taxi Provides taxi instructions and hands you off to the tower.

Tower → Request Takeoff Places you in the takeoff queue; when first in line, you are cleared to depart and told to contact again for hand‑off.

Tower → Request Handoff After becoming airborne, triggers a hand‑off to Slasher, advises you to check in.

Slasher → Check In Acknowledge the hand‑off; Slasher tells you to fly your mission.

Slasher → Request Inbound On your way back, request inbound; Slasher confirms and tells you to call for approach clearance. (I also have auto detection logic. If you are within 10 NMs you can call in, or watch for approach alert)

Slasher → Request Approach This is automatic, or if you feel the need to do it, it will work within 10nms, otherwise will tell you that you are too far.

Tower → Request Landing Clears you to land or informs you of your position in the landing queue, Tells u to contact ground for taxi.

Ground → Taxi to Parking Once landed and stopped off of runway, call for taxi clearance and instructions.

Ground → Shutdown The ground crew will tell you that you are cleared for shutdown, and sign off.

If you call a step out of sequence (e.g., request taxi before startup), the script will let you know.