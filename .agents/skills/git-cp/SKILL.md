---
name: git-cp
description: >-
  Executes git commit and git push when the user types 'CP' or requests a commit and push.
---

# Git Commit & Push (CP) Workflow

Quando l'utente scrive **`CP`** (oppure "cp", "fai CP", "esegui CP"), significa **Commit & Push**.

## Procedura da Eseguire

1. **Verifica dello Stato Git**:
   Esegui `git status` per controllare i file modificati, aggiunti o eliminati.

2. **Staging delle Modifiche**:
   Aggiungi tutti i file di progetto modificati:
   ```bash
   git add -A
   ```

3. **Commit con Messaggio Dettagliato**:
   Crea un messaggio di commit professionale e descrittivo in italiano, che riassuma con precisione i cambiamenti apportati:
   ```bash
   git commit -m "<tipo>: <descrizione sintetica ma completa>"
   ```

4. **Push su Remote**:
   Invia le modifiche al branch remoto principale:
   ```bash
   git push origin main
   ```

5. **Riepilogo all'Utente**:
   Comunica all'utente l'avvenuto commit (con hash) e la conferma del push con l'elenco dei file aggiornati.

