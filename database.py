import sqlite3

def create_connection():
    conn = sqlite3.connect("expenses.db")
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    
def add_expense(name, amount):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO expenses (name, amount) VALUES (?, ?)",
        (name, amount)
    )

    conn.commit()
    conn.close()
    
def get_expenses():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")

    expenses = cursor.fetchall()

    conn.close()

    return expenses

def update_expense(expense_id, name, amount):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE expenses SET name = ?, amount = ? WHERE id = ?",
        (name, amount, expense_id)
    )

    conn.commit()
    conn.close()
    
def delete_expense(expense_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()