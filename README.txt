================================================================================
FIRE MAGE 3.3.5a AM — WEAKAURAS 4.0.0 SUITE COMPLETA (WotLK Build 12340)
================================================================================

GUIDA RAPIDA DI INSTALLAZIONE E AGGIORNAMENTO IN GIOCO:
--------------------------------------------------------------------------------
1. Apri il file IMPORT_STRING.txt e copia tutto il testo (Ctrl+A, poi Ctrl+C).
   (Nota: la versione precedente e' archiviata nel file IMPORT_STRINGOLD.txt).
2. In World of Warcraft, apri WeakAuras digitando in chat:
   /wa
3. Clicca sul pulsante "Import" in alto a sinistra.
4. Incolla il testo con Ctrl+V.
5. Scegli la modalita' di importazione:
   - "Update Auras" (o "Upgrade"): aggiorna la suite preservando le tue impostazioni.
   - "Replace": se vuoi una reinstallazione pulita che ripristini le posizioni base.
6. Chiudi WeakAuras premendo Esc. Fire Mage 3.3.5a AM e' pronto all'uso!

--------------------------------------------------------------------------------
PANORAMICA DELLE FUNZIONALITA' E DEL LAYOUT:
--------------------------------------------------------------------------------

1. BARRA HOT STREAK DINAMICA (Sotto la Barra del Mana a y = -25):
   - 1° Critico Non-Periodico: illumina esattamente meta' barretta a sinistra
     (50%, 130x5px) di colore arancione vivo e RESTA PERSISTENTE nel tempo.
     I DoT periodici (Ignite, tick Living Bomb) non azzerano la serie.
   - 2° Critico Consecutivo (Hot Streak Proc): la meta' barretta sparisce e
     i due segmenti DIVENTANO UN'UNICA BARRA CONTINUA DA 264px a tutta larghezza!
     Attiva il Pixel Glow dorato/arancio e avvia il conto alla rovescia di 10s
     del buff con scorrimento orologio (radial swipe) in tempo reale.
   - Lancio di Pyroblast (o fine 10s): consuma l'effetto e azzera subito la barra.
   - Zero Testo: design puramente visivo, pulito e minimale.

2. GESTIONE DINAMICA TIER 8 & TIER 10 (Praxis +350 SP & Pushing the Limit Haste 12%):
   - Tier 10 (Pushing the Limit - Spell ID 70753/70752):
     * Collocato nella riga superiore procs (01 - Procs, 34x34 px) direttamente
       a SINISTRA di Hot Streak.
     * Quando Hot Streak procca con almeno 2 pezzi T10, il buff (+12% Haste per 5s)
       si attiva con Pixel Glow dorato/arancio, swipe radiale e timer di 5 secondi.
     * Al termine dei 5 secondi, scompare dinamicamente lasciando inalterato l'ordine.
   - Tier 8 (Praxis - Spell ID 64868):
     * Collocato al centro della fila utility inferiore a x = 0 (tra Mantello e Gemma).
     * Mostra il proc +350 SP per 15s con Pixel Glow dorato e ricarica ICD 45s.
   - Le 2 Modalita' Dinamiche della Fila Utility (y = -54, 28x28 px) in base al Gear:
     * Scenario A: Con Tier 8 (>= 2P equipaggiato - Solo T8, T7+T8, T8+T10):
       7 icone a 28px con passo 38px (totale 256px, perfettamente sotto la barra).
       Trinket 1 (-114), Trinket 2 (-76), Mantello (-38), T8 Praxis (0), Gemma (+38),
       Combustione (+76), Mirror Image (+114).
     * Scenario B: Senza Tier 8 (< 2P equipaggiato - Solo T7, Solo T10, no set):
       6 icone a 28px con passo 44px (totale 248px). Configurazione simmetrica standard:
       Trinket 1 (-110), Trinket 2 (-66), Mantello (-22), Gemma (+22), Combustione (+66),
       Mirror Image (+110).
     * Rilevamento in tempo reale a zero persistenza: il cambio layout e' istantaneo
       quando si cambiano pezzi di equipaggiamento (Outfitter, ItemRack, Equipment Manager).

3. BUFF A LUNGA DURATA (Molten Armor, Intellect, Focus Magic):
   - Molten Armor & Arcane Intellect:
     * Invisibili > 5 min: per la massima pulizia dello schermo durante i boss fight.
     * Conto alla rovescia <= 5 min: compaiono con swipe orologio e timer colorato
       (giallo > 60s, rosso <= 60s) solo quando mancano 5 minuti o meno.
     * Allerta OFF: se il buff manca del tutto o e' scaduto, mostra l'icona grigia
       desaturata con avviso rosso "OFF".
   - Focus Magic (04 - Focus Magic):
     * Nascosto se applicato: fintanto che e' attivo sull'alleato (e vivo), rimane
       completamente nascosto per la massima pulizia dello schermo.
     * Proc Personale 10s (+3% Crit): quando l'alleato mette a segno un critico,
       l'icona appare all'istante mostrando il conto alla rovescia dei 10s con swipe.
     * Ritorno a Nascosto: finiti i 10s, torna nascosto se l'alleato ha ancora il buff.
     * Allerta OFF: se non e' applicato a nessuno, o se l'alleato muore in fight o il
       buff scade, mostra subito l'icona grigia desaturata con avviso rosso "OFF".

4. PANNELLO STATISTICHE IN TEMPO REALE (Sotto i 3 Buff a x = -180, y = -54):
   - SP: Spell Power Fuoco in tempo reale (GetSpellBonusDamage(3)), include gear,
     gemme, Flask, pozioni, Demonic Pact, Totem of Wrath/Flametongue, Praxis e T7 2P.
   - Crit: Spell Crit Fuoco con Molten Armor, talenti, proc Focus Magic, stack di
     Combustion (+10% a carica) e debuff boss non cumulabili (+5% Scorch vs Winter's Chill
     vs Shadow and Flame; +3% Heart of the Crusader vs Master Poisoner vs Totem of Wrath).
   - Haste: Spell Haste con rating e moltiplicatori raid anti-conflitto: Bloodlust (+30%),
     Wrath of Air Totem (+5%), 3% Raid Haste (Swift Retribution vs Imp Moonkin Form, max una volta),
     T10 2P (+12% Pushing the Limit), Power Infusion (+20%) e Berserking (+20%).
   - Hit: Spell Hit con rating, talenti Precision (+3%), Draenei (+1%) e debuff boss
     non cumulabile (+3% Misery vs Faerie Fire), con indicatore verde "(Cap)" a >= 17%.

5. ENGINE UNIVERSALE PER TRINKET (SLOT 13 E 14) E MANTELLO (SLOT 15):
   - Database integrato con oltre 40 monili WotLK (DFO, Filatterio, CTS, ecc.).
   - Riconoscimento automatico On-Use e proc passivi con Internal Cooldown (ICD).
   - Pixel Glow dorato durante il proc attivo, seguito dallo swipe a orologio
     e conto alla rovescia del tempo prima del prossimo riproc.
   - Fallback euristico: stima automatica anche per monili non catalogati.

6. GEMMA DEL MANA CON BONUS 2 PEZZI T7 (y = -54):
   - All'uso attiva il proc T7 (+225 SP per 15s) commutando l'icona sul simbolo
     di Mana Surge con Pixel Glow dorato e countdown decimale a sud (%.1fs).
   - Al termine del buff, torna alla gemma mostrando il cooldown di 2 minuti.
   - Cariche residue mostrate in alto a destra (%c, con "0" rosso se esaurite).

7. CLUSTER CENTRALE ERGONOMICO (Larghezza 264px):
   - Castbar (y = +8): icona spell a sinistra, nome spell, tempo residuo a destra.
   - GCD (y = -4): barra bianca sottile per il Global Cooldown.
   - Mana Bar (y = -15): percentuale con 2 decimali (es. 85.24%), rossa se <= 20%.
   - Hot Streak Bar (y = -25): 264x7px a scomparsa dinamica.

8. PROCS & DEBUFF CON TIMER ROSSI IN SCADENZA (y = +52):
   - Include Tier 10 (Pushing the Limit a sx di Hot Streak), Hot Streak, Clearcasting,
     Living Bomb (refresh preventivo <= 3s), Ignite, Scorch, Molten Fury (<= 35% HP).

================================================================================
Repository GitHub: https://github.com/Glacyal/FireMageHUD-335 (Branch: main)
================================================================================
