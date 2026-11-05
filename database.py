import sqlite3
from datetime import datetime, timezone

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
            category TEXT NOT NULL DEFAULT 'Uncategorized',
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()
    
def add_expense(name, amount, category):
    conn = create_connection()
    cursor = conn.cursor()

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute(
        "INSERT INTO expenses (name, amount, category, timestamp) VALUES (?, ?, ?, ?)",
        (name, amount, category, timestamp)
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

def search_and_filter_expenses(keyword, category):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM expenses
        WHERE name LIKE ?
        AND (category = ? OR ? = 'All Categories')
        ORDER BY timestamp DESC
        """, (f"%{keyword}%", category, category)
    )

    expenses = cursor.fetchall()
    conn.close()

    return expenses

def filter_expenses_by_date(start_date, end_date):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM expenses
        WHERE DATE(timestamp) BETWEEN ? AND ?
        ORDER BY timestamp DESC
    """, (start_date, end_date))

    expenses = cursor.fetchall()
    conn.close()

    return expenses

def filter_expenses(keyword, category, start_date, end_date):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM expenses
        WHERE name LIKE ?
        AND (category = ? OR ? = 'All Categories')
        AND DATE(timestamp) BETWEEN ? AND ?
        ORDER BY timestamp DESC
    """, (f"%{keyword}%", category, category, start_date, end_date))

    expenses = cursor.fetchall()
    conn.close()

    return expenses