# Personal Expense System

Un sistema di gestione delle spese personali basato su console, progettato per registrare spese, gestire categorie, definire budget mensili e generare report riepilogativi.

## Requisiti per l'esecuzione
* **Interprete:** Python 3.10 o versioni successive (richiesto per l'utilizzo del costrutto `match-case`).
* **Database:** SQLite3 (incluso nella libreria standard di Python).
* **Librerie Standard:** `sqlite3`, `os`, `sys` (nessuna installazione di pacchetti esterni richiesta).

## Istruzioni per l'esecuzione
Il database verrà generato automaticamente al primo avvio leggendo lo script `database.sql`.

1.  Aprire il terminale (o Prompt dei Comandi).
2.  Navigare nella cartella radice del progetto:
    ```bash
    cd percorso/del/progetto/PersonalExpenseSystem
    ```
3.  Avviare il programma eseguendo il file `main.py` contenuto all'interno della cartella `src`:
    ```bash
    python src/main.py
    ```
    *(Nota: su alcuni sistemi operativi potrebbe essere necessario utilizzare il comando `python3 src/main.py`)*

## Demo
Il video dimostrativo `demo_video.mp4` è reperibile nella cartella `demo/`.