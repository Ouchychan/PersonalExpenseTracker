import database

results = database.filter_expenses(
    "",
    "All Categories",
    "2026-11-01",
    "2026-11-05"
)

for expense in results:
    print(expense)