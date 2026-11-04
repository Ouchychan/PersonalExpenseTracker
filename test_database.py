import database

category_totals = database.get_category_totals()

for category in category_totals:
    print(category[0], category[1])