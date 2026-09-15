# Proposta Architetturale: Gestione di `Core.lua` e Duplicazione Scansioni nei Moduli

## Contesto e Diagnosi

Dall'analisi del codice della suite `FireMageHUD-335`, è emerso che `Core.lua` (298 righe) definisce una ricca libreria condivisa di utility e funzioni di scansione (`FireMageHUD_Core`), tra cui:
* `Core:FindBuff(unit, nameOrId, ownOnly)`
* `Core:FindDebuff(unit, nameOrId, ownOnly)`
* `Core:CheckMoltenArmor()`
* `Core:CheckArcaneIntellect()`
* `Core:GetEquipSlotStatus(slotId)`
* `Core:GetGCD()`
* `Core:FormatTime(seconds)`
* `Core:FormatNumber(value, mode)`

Tuttavia, **nessun modulo nella cartella `modules/` richiama mai `Core` o `FireMageHUD_Core`** (zero occorrenze nel progetto al di fuori di `Core.lua`). Ciascun file in `modules/` reimplementa da zero il proprio ciclo `for i = 1, 40 do UnitBuff/UnitDebuff`, portando a:
1. **Oltre 37 cicli di scansione duplicati** tra i vari file Lua.
2. **Piccole incoerenze logiche**: per esempio, `MoltenArmor.lua` verifica unicamente il Rank 3 (spell ID 43046), mentre `Core:CheckMoltenArmor()` include tutti e tre i rank (Rank 1 ID 30482, Rank 2 ID 31256, Rank 3 ID 43046).
3. **Dicotomia architetturale**: la suite nasce con una duplice natura:
   - **WeakAura 100% Pura** (`IMPORT_STRING.txt`): i chunk Lua devono essere per definizione auto-consistenti e indipendenti da addon esterni.
   - **Addon Companion Standalone** (`FireMageHUD.toc` + `modules/`): qui l'uso di una libreria `Core.lua` condivisa è il paradigma standard di WoW.

---

## Opzioni di Risoluzione Proposte

### Opzione A: Refactoring dei Moduli verso `Core.lua` (Consigliata se si mantiene l'Addon Standalone)

Sostituire progressivamente le scansioni duplicate e le funzioni di formattazione nei file in `modules/` con chiamate dirette a `FireMageHUD_Core`.

* **Vantaggi**:
  - **DRY (Don't Repeat Yourself)**: centralizza la logica di scansione aure, gestione rank e formattazione temporale.
  - **Manutenibilità**: modifiche future ai debuff/buff (es. nuovi rank o eccezioni core) si applicano in un solo file (`Core.lua`).
  - **Coerenza**: risolve incongruenze come i rank mancanti in `MoltenArmor.lua`.
  - **Prestazioni**: possibilità di introdurre caching a livello di Core per l'intero frame (es. una sola scansione `UnitBuff` per frame condivisa tra tutti i moduli dell'addon).
* **Svantaggi / Attenzioni**:
  - Richiede la modifica di 10+ file in `modules/`.
  - Crea una divergenza tra il codice dei file `.lua` dell'addon e i blocchi Lua generati dentro `generate_import_string.py` per WeakAuras (che devono rimanere a sé stanti a meno di non rendere l'addon obbligatorio per la WA).

### Opzione B: Rimozione di `Core.lua` (Consigliata se il focus è la WeakAura Pura)

Eliminare completamente `Core.lua` e rimuoverlo da `FireMageHUD.toc`. Ciascun modulo in `modules/` rimane un file autonomo e auto-consistente.

* **Vantaggi**:
  - **Zero codice morto**: elimina 300 righe di funzioni non utilizzate, evitando dubbi e fraintendimenti futuri durante la lettura del repository.
  - **Simmetria 1:1 con WeakAuras**: il codice in `modules/*.lua` rispecchia fedelmente la logica dei singoli trigger di WeakAuras (self-contained).
  - **Zero rischio di regressioni**: nessun modulo esistente viene modificato, azzerando il rischio di rompere comportamenti attuali dell'addon.
* **Svantaggi**:
  - Rimangono i pattern duplicati `for i = 1, 40` nei singoli moduli dell'addon.
  - Piccole correzioni (es. supporto a tutti i rank di un buff) vanno applicate file per file.

---

## Decisione Richiesta

> [!IMPORTANT]
> **In attesa di conferma da parte dell'utente prima di procedere.**
> * Indicare se procedere con l'**Opzione A** (Refactoring verso Core) o con l'**Opzione B** (Rimozione di Core.lua).
