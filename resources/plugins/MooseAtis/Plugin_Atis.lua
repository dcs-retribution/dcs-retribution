env.info("-----DCSRetribution|MOOSE ATIS plugin - start -----")

local announceFieldName = true
local atisDebug = false
if dcsRetribution and dcsRetribution.plugins and dcsRetribution.plugins.MooseAtis then
    local cfg = dcsRetribution.plugins.MooseAtis
    if cfg.AnnounceFieldName ~= nil then announceFieldName = cfg.AnnounceFieldName end
    if cfg.AtisDebug ~= nil then atisDebug = cfg.AtisDebug end
end

if not (dcsRetribution and dcsRetribution.Atis) then
    env.info("-----dcsRetribution.Atis NOT FOUND -- no ATIS stations created")
    return
end

for _, entry in pairs(dcsRetribution.Atis) do
    local ok, err = pcall(function()
        local atis = ATIS:New(entry.name, entry.freq, entry.modulation or 0)
        -- pydcs stores bundled resources flat by basename under l10n/DEFAULT,
        -- so point all three MOOSE soundfile sub-paths there. DCS resolves
        -- transmission files relative to the .miz root; a bare basename (empty
        -- path) does not resolve and the ATIS plays silently.
        local soundPath = "l10n/DEFAULT/"
        atis:SetSoundfilesPath(soundPath, soundPath, soundPath)
        -- Field-name suppression is best-effort: this MOOSE build exposes no
        -- such setter, so the guard never fires here (AnnounceFieldName is
        -- advisory). Guarded so a future MOOSE that adds one Just Works.
        if (not announceFieldName) and atis.SetReportName then
            atis:SetReportName(false)
        end
        atis:Start()
        env.info(string.format(
            "DCSRetribution|MOOSE ATIS: started %s on %.3f MHz", entry.name, entry.freq
        ))
    end)
    if not ok then
        env.info("DCSRetribution|MOOSE ATIS: failed to start a station: " .. tostring(err))
    end
end
