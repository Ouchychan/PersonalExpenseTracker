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
            amount REAL NOT NULL,
            category TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    
def add_expense(name, amount, category):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO expenses (name, amount, category) VALUES (?, ?, ?)",
        (name, amount, category)
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

def update_expense(expense_id, name, amount, category):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE expenses SET name = ?, amount = ?, category = ? WHERE id = ?",
        (name, amount, category, expense_id)
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
    
def get_category_totals():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT category, SUM(amount) FROM expenses GROUP BY category"
    )

    category_totals = cursor.fetchall()
    
    conn.close()

    return category_totals