if dcsRetribution then

    if dcsRetribution.plugins then
        if dcsRetribution.plugins.airboss then
            env.info("MGC DCSRetribution|Airboss - Setting Up")

            enableRescueHelo = dcsRetribution.plugins.airboss.enableRescueHelo or false
            env.info("MGC DCSRetribution|Airboss - Rescue Helo - %s" .. tostring(enableRescueHelo))

        end
    end
end
