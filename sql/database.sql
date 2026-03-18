DROP TABLE IF EXISTS expenses;
DROP TABLE IF EXISTS budgets;
DROP TABLE IF EXISTS categories;

-- Script di creazione del database
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- PRIMARY KEY
    name TEXT NOT NULL UNIQUE             -- NOT NULL
);

CREATE TABLE budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month TEXT NOT NULL,
    amount REAL NOT NULL CHECK(amount > 0),
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    UNIQUE(month, category_id)
);

CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    amount REAL NOT NULL CHECK(amount > 0),
    description TEXT,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Script di inserimento dati di esempio
INSERT INTO categories (name) VALUES ('Alimentari'), ('Trasporti'), ('Svago');

INSERT INTO budgets (month, amount, category_id) VALUES
('2025-01', 300.00, 1),
('2025-01', 100.00, 2);

INSERT INTO expenses (date, amount, description, category_id) VALUES
('2025-01-15', 25.00, 'Pranzo', 1),
('2025-01-16', 320.50, 'Spesa settimanale', 1),
('2025-01-18', 50.00, 'Benzina', 2);
