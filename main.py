import sqlite3
import os
import sys

DB_FILE = "expenses.db" #definizione del nome del file del database SQLite
SQL_FILE = os.path.join(os.path.dirname(__file__), '..', 'sql', 'database.sql')

def connect_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = 1")
    return conn


def init_db():
    if not os.path.exists(DB_FILE):
        try:
            with open(SQL_FILE, 'r') as f:
                sql_script = f.read()
            with connect_db() as conn:
                conn.executescript(sql_script)
        except FileNotFoundError:
            print(f"Errore: file {SQL_FILE} non trovato. Assicurati della struttura delle cartelle.")
            sys.exit(1)


#Gestione Categorie
def manage_categories(conn):
    name = input("Inserisci il nome della nuova categoria: ").strip()
    if not name:
        print("Errore: il nome della categoria non puo' essere vuoto.")
        return

    cursor = conn.cursor()
    cursor.execute("SELECT id FROM categories WHERE name = ?", (name,))
    if cursor.fetchone():
        print("Errore: La categoria esiste gia'.")
    else:
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        conn.commit()
        print("Categoria inserita correttamente.")


#Inserimento Spesa
def insert_expense(conn):
    date = input("Data (formato YYYY-MM-DD): ").strip()
    try:
        amount = float(input("Importo: "))
        if amount <= 0:
            print("Errore: l'importo deve essere maggiore di zero.")
            return
    except ValueError:
        print("Errore: inserire un numero valido.")
        return

    category_name = input("Nome della categoria: ").strip()
    description = input("Descrizione facoltativa: ").strip()

    cursor = conn.cursor()
    cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
    cat_row = cursor.fetchone()

    if not cat_row:
        print("Errore: la categoria non esiste.")
        return

    category_id = cat_row[0]
    cursor.execute(
        "INSERT INTO expenses (date, amount, description, category_id) VALUES (?, ?, ?, ?)",
        (date, amount, description, category_id)
    )
    conn.commit()
    print("Spesa inserita correttamente.")


#Definizione Budget
def define_budget(conn):
    month = input("Mese (formato YYYY-MM): ").strip()
    category_name = input("Nome della categoria: ").strip()
    try:
        amount = float(input("Importo del budget: "))
        if amount <= 0:
            print("Errore: l'importo deve essere maggiore di zero.")
            return
    except ValueError:
        print("Errore: inserire un numero valido.")
        return

    cursor = conn.cursor()
    cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
    cat_row = cursor.fetchone()

    if not cat_row:
        print("Errore: la categoria non esiste.")
        return

    category_id = cat_row[0]

    cursor.execute("""
        INSERT INTO budgets (month, amount, category_id) 
        VALUES (?, ?, ?)
        ON CONFLICT(month, category_id) DO UPDATE SET amount = excluded.amount
    """, (month, amount, category_id))
    conn.commit()
    print("Budget mensile salvato correttamente.")


#Report
def view_reports(conn):
    while True:
        print("\n--- Menu dei Report ---")
        print("1. Totale spese per categoria")
        print("2. Spese mensili vs budget")
        print("3. Elenco completo delle spese ordinate per data")
        print("4. Ritorna al menu principale")

        choice = input("Inserisci la tua scelta: ").strip()
        cursor = conn.cursor()

        if choice == '1':
            cursor.execute("""
                SELECT c.name, SUM(e.amount) 
                FROM expenses e 
                JOIN categories c ON e.category_id = c.id 
                GROUP BY c.name
            """)
            print(f"\n{'Categoria':<15} {'Totale Speso':>15}")
            print("-" * 31)
            for row in cursor.fetchall():
                print(f"{row[0]:<15} {row[1]:>15.2f}")

        elif choice == '2':
            cursor.execute("""
                SELECT substr(e.date, 1, 7) as month, c.name, c.id, SUM(e.amount)
                FROM expenses e
                JOIN categories c ON e.category_id = c.id
                GROUP BY month, c.id
            """)
            expenses_data = cursor.fetchall()

            for month, cat_name, cat_id, total_spent in expenses_data:
                cursor.execute("SELECT amount FROM budgets WHERE month = ? AND category_id = ?", (month, cat_id))
                budget_row = cursor.fetchone()

                budget_amt = budget_row[0] if budget_row else 0.0
                status = "SUPERAMENTO BUDGET" if total_spent > budget_amt else "IN REGOLA"

                print(f"\nMese: {month}")
                print(f"Categoria: {cat_name}")
                print(f"Budget: {budget_amt:.2f}")
                print(f"Speso: {total_spent:.2f}")
                print(f"Stato: {status}")

        elif choice == '3':
            cursor.execute("""
                SELECT e.date, c.name, e.amount, e.description 
                FROM expenses e 
                JOIN categories c ON e.category_id = c.id 
                ORDER BY e.date ASC
            """)
            print(f"\n{'Data':<12} {'Categoria':<15} {'Importo':<10} {'Descrizione'}")
            print("-" * 55)
            for row in cursor.fetchall():
                desc = row[3] if row[3] else ""
                print(f"{row[0]:<12} {row[1]:<15} {row[2]:<10.2f} {desc}")

        elif choice == '4':
            break
        else:
            print("Scelta non valida. Riprovare.")


#MAIN LOOP2
def main():
    init_db()
    conn = connect_db()
    print("Benvenuto nel gestionale delle tue spese personali. Cominciamo...\n")

    while True:
        print("=======================\n"
              "SISTEMA SPESE PERSONALI\n"
              "=======================")
        print("1. Gestione Categorie")
        print("2. Inserisci Spesa")
        print("3. Definisci Budget Mensile")
        print("4. Visualizza Report")
        print("5. Esci")

        choice = input("Inserisci la tua scelta: ").strip()

        match choice:
            case '1':
                manage_categories(conn)
            case '2':
                insert_expense(conn)
            case '3':
                define_budget(conn)
            case '4':
                view_reports(conn)
            case '5':
                print("Chiusura del programma...")
                conn.close()
                break
            case _:
                print("Scelta non valida. Riprovare.")


if __name__ == "__main__":
    main()