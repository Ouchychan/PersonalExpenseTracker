import sqlite3

#Connect to the database (creates the file if it doesn't exist)
conn = sqlite3.connect("expenses.db")

#Create a cursor object to execute SQL commands
cursor = conn.cursor()

#Write and execute the SQL query to create a table
# Using "IF NOT EXISTS" prevents errors if the script runs multiple times
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        amount REAL NOT NULL
    )
"""
)

expense_name = "Groceries"
expense_amount = 150.75

#Insertion data into the table
cursor.execute(
    "INSERT INTO expenses (name, amount) VALUES (?, ?)",
    (expense_name, expense_amount)
)

#Update data in the table
expense_id_to_update = 1
new_expense_name = "Dinner"
new_expense_amount = 85.50
cursor.execute(
    "UPDATE expenses SET name = ?, amount = ? WHERE id = ?",
    (new_expense_name, new_expense_amount, expense_id_to_update)
)

#Delete data from the table
expense_id_to_delete = 1
cursor.execute(
    "DELETE FROM expenses WHERE id = ?",
    (expense_id_to_delete,)
)

#Selecting data from the table
cursor.execute("SELECT * FROM expenses")
expenses = cursor.fetchall()
print("Expenses in the database:")
for expense in expenses:
    print(f"{expense[0]} - {expense[1]}: RM{expense[2]:.2f}")



#Commit changes to save them to the database
conn.commit()

#Close the connection
conn.close()

print("Table created successfully!")