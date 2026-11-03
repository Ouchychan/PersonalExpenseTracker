import database

database.delete_expense(1)

saved_expenses = database.get_expenses()

for expense in saved_expenses:
    print(expense)