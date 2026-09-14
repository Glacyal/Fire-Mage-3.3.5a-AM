-- =========================================================================
--- Fire Mage HUD 3.3.5a — Modulo: Barra Hot Streak (2 Segmenti)
--- =========================================================================
--- Gestisce il monitoraggio in tempo reale del talento Hot Streak (Lancio Istantaneo)
--- posizionata immediatamente sotto la Barra del Mana (264x7px):
--- - Barretta 1 (Sinistra): si accende al 1° colpo critico diretto e RESTA PERSISTENTE
---   nel tempo. I danni periodici (DoT come Ignite o Living Bomb tick) non la azzerano.
---   Si azzera solo su colpo diretto non-critico o all'uscita dal combattimento.
--- - Barretta 2 (Destra): si accende al 2° colpo critico consecutivo (proc Hot Streak
---   Buff 48108). Mostra il conto alla rovescia dei 10 secondi del buff a scorrere.
--- - Lancio di Pyroblast (o scadenza buff): consuma immediatamente l'effetto
---   e azzera istantaneamente entrambe le barrette a 0.
--- - Zero testo: barra puramente visiva senza percentuali o etichette.
--- =========================================================================

FireMageHUD_HotStreak = FireMageHUD_HotStreak or {
    streak = 0,
    hasBuff = false,
    duration = 10,
    expirationTime = 0,
}

local HS = FireMageHUD_HotStreak

-- Tabella spell valide per Hot Streak (colpi diretti non-periodici)
local QUALIFYING_SPELLS = {
    -- Fireball (tutti i rank)
    [133] = true, [143] = true, [145] = true, [3140] = true, [8400] = true,
    [8401] = true, [8402] = true, [10148] = true, [10149] = true, [10150] = true,
    [10151] = true, [25306] = true, [27070] = true, [38692] = true, [42832] = true, [42833] = true,
    -- Fire Blast (tutti i rank)
    [2136] = true, [2137] = true, [2138] = true, [8412] = true, [8413] = true,
    [10197] = true, [10199] = true, [27078] = true, [27079] = true, [42872] = true, [42873] = true,
    -- Scorch (tutti i rank)
    [2948] = true, [8444] = true, [8445] = true, [8446] = true, [10205] = true,
    [10206] = true, [10207] = true, [27073] = true, [27074] = true, [42858] = true, [42859] = true,
    -- Frostfire Bolt (Rank 1 e 2)
    [44614] = true, [47610] = true,
    -- Living Bomb Esplosione Finale (Rank 1, 2 e 3)
    [44461] = true, [55361] = true, [55362] = true,
}

local QUALIFYING_NAMES = {
    ["Fireball"] = true,
    ["Palla di Fuoco"] = true,
    ["Fire Blast"] = true,
    ["Deflagrazione di Fuoco"] = true,
    ["Scorch"] = true,
    ["Bruciatura"] = true,
    ["Frostfire Bolt"] = true,
    ["Dardo di Fuocogelo"] = true,
}

local function IsQualifyingSpell(spellId, spellName)
    if spellId and QUALIFYING_SPELLS[spellId] then
        return true
    end
    if spellName and QUALIFYING_NAMES[spellName] then
        return true
    end
    return false
end

--- Sincronizza lo stato di Hot Streak con i buff correnti del giocatore.
local function SyncHotStreakBuff()
    local found = false
    for i = 1, 40 do
        local name, _, _, _, _, dur, expTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == 48108 or name == "Hot Streak" or name == "Buona sorte" then
            found = true
            HS.hasBuff = true
            HS.streak = 2
            HS.duration = (dur and dur > 0) and dur or 10
            HS.expirationTime = expTime or (GetTime() + HS.duration)
            break
        end
    end
    if not found and HS.hasBuff then
        -- Il buff Hot Streak e' stato consumato o e' scaduto
        HS.hasBuff = false
        HS.streak = 0
        HS.expirationTime = 0
    end
end

--- Gestione eventi per la barra Hot Streak (CLEU, UNIT_AURA, SPELLCAST, REGEN)
---@param event string Nome evento WoW
---@param ... any Argomenti dell'evento
function FireMageHUD_HotStreak_OnEvent(event, ...)
    if event == "PLAYER_ENTERING_WORLD" then
        HS.streak = 0
        HS.hasBuff = false
        HS.expirationTime = 0
        SyncHotStreakBuff()
    elseif event == "PLAYER_DEAD" or event == "PLAYER_UNGHOST" then
        HS.streak = 0
        HS.hasBuff = false
        HS.expirationTime = 0
    elseif event == "PLAYER_REGEN_ENABLED" then
        -- All'uscita dal combattimento, azzera solo se non si ha il buff Hot Streak attivo
        if not HS.hasBuff then
            HS.streak = 0
        end
    elseif event == "UNIT_AURA" then
        local unit = ...
        if unit == "player" then
            SyncHotStreakBuff()
        end
    elseif event == "UNIT_SPELLCAST_SUCCEEDED" then
        local unit, spellName, _, _, spellId = ...
        if unit == "player" then
            -- Se viene lanciata Pyroblast, il buff Hot Streak viene consumato all'istante
            if spellId == 11366 or spellId == 12505 or spellId == 12522 or spellId == 12523 or
               spellId == 12524 or spellId == 12525 or spellId == 12526 or spellId == 33938 or
               spellId == 42890 or spellId == 42891 or spellName == "Pyroblast" or spellName == "Pirocombustione" then
                HS.hasBuff = false
                HS.streak = 0
                HS.expirationTime = 0
            end
        end
    elseif event == "COMBAT_LOG_EVENT_UNFILTERED" then
        local subEvent = select(2, ...)
        local sourceGUID = select(4, ...)

        -- Solo colpi eseguiti dal giocatore
        if sourceGUID == UnitGUID("player") and subEvent == "SPELL_DAMAGE" then
            -- RIGOROSO: Solo SPELL_DAMAGE diretto! SPELL_PERIODIC_DAMAGE (DoT) viene ignorato!
            local spellId = select(10, ...)
            local spellName = select(11, ...)
            if IsQualifyingSpell(spellId, spellName) then
                local critical = select(19, ...)
                local isCrit = (critical and critical ~= 0 and critical ~= false)
                if isCrit then
                    if not HS.hasBuff then
                        if HS.streak == 0 then
                            -- 1° Critico: persiste nel tempo, illumina metà barretta
                            HS.streak = 1
                        else
                            -- 2° Critico: entra in Hot Streak
                            HS.streak = 2
                        end
                    end
                else
                    -- Colpo non-critico: azzera la serie se non c'e' gia' Hot Streak attivo
                    if not HS.hasBuff then
                        HS.streak = 0
                    end
                end
            end
        end
    end
end

--- Restituisce lo stato corrente della Barretta 1 (Sinistra, 1° Critico).
---@return boolean isVisible True se attiva (piena al 100% e persistente)
---@return number current Valore corrente (1)
---@return number max Valore massimo (1)
function FireMageHUD_HotStreak_Segment1()
    SyncHotStreakBuff()
    local isVisible = (HS.streak >= 1 or HS.hasBuff)
    return isVisible, 1, 1
end

--- Restituisce lo stato corrente della Barretta 2 (Destra, Proc Hot Streak 10s).
---@return boolean isVisible True se Hot Streak proc e' attivo
---@return number remaining Secondi rimanenti prima della scadenza
---@return number duration Durata totale del buff (10.0s)
function FireMageHUD_HotStreak_Segment2()
    SyncHotStreakBuff()
    if HS.hasBuff and HS.expirationTime and HS.expirationTime > GetTime() then
        local rem = math.max(0, HS.expirationTime - GetTime())
        return true, rem, HS.duration or 10.0
    end
    return false, 0, 10.0
end

