import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import database
from datetime import datetime, timezone

database.create_table()

categories = [
    "Food",
    "Transport",
    "Shopping",
    "Bills",
    "Entertainment",
    "Healthcare",
    "Education",
    "Other"
]

total_expenses = 0.0
expenses = []

def get_expense():
    global expenses, total_expenses

    expenses = database.get_expenses()

    for item in expense_list.get_children():
        expense_list.delete(item)
    total_expenses = 0

    for expense in expenses:
        dt = datetime.strptime(
            expense[4], "%Y-%m-%d %H:%M:%S"
        ).replace(tzinfo=timezone.utc)

        local_timestamp = dt.astimezone().strftime("%d/%m/%Y %I:%M %p")
        
        expense_list.insert(
            "",
            tk.END,
            values=(
                expense[0],
                expense[1],
                f"RM {expense[2]:.2f}",
                expense[3],
                local_timestamp
        )
    )

        total_expenses += expense[2]

    total_label.config(text=f"Total: RM {total_expenses:.2f}")
        
def add_expense():
    global total_expenses
    expense_name = expenseentry.get().strip() #strip whitespace from the input
    expense_amount = amountentry.get().strip() 
    expense_category = category_dropdown.get()
    
    if expense_name == "" or expense_amount == "":
        messagebox.showerror("Invalid Input", "Please fill in all fields.")
        return
    try:
        expense_amount = float(expense_amount)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid amount.")
        return
    if expense_amount <= 0:
        messagebox.showerror("Invalid Input", "Amount must be greater than zero.")
        return

    database.add_expense(expense_name, expense_amount, expense_category)

    # Refresh the expense list after adding a new expense
    get_expense() 
    
    expenseentry.delete(0, tk.END)
    amountentry.delete(0, tk.END)
    
def delete_expense():
    selected_items = expense_list.selection()

    if not selected_items:
        messagebox.showwarning(
            "Warning",
            "Please select an expense to delete."
        )
        return

    for item in selected_items:
        values = expense_list.item(item, "values")
        expense_id = values[0]

        database.delete_expense(expense_id)

    get_expense()
    messagebox.showinfo(
            "Expense Deleted",
            f"{len(selected_items)} expense(s) have been deleted successfully."
        )    

def edit_expense():
    selected_items = expense_list.selection()

    if len(selected_items) != 1:
        messagebox.showwarning(
            "Warning",
            "Please select exactly one expense to edit."
        )
        return

    selected_item = selected_items[0]
    expense = expense_list.item(selected_item, "values")

    expense_id = expense[0]
    expense_name = expense[1]
    expense_amount = float(expense[2].replace("RM ", ""))
    expense_category = expense[3]

    edit_window = tk.Toplevel(root) 
    edit_window.title("Edit Expense")
    edit_window.geometry("600x600")
    edit_window.resizable(False, False)

    edit_expense_label = tk.Label(
        edit_window,
        text="Expense Name:",
        font=("Arial", 14)
    )
    edit_expense_entry = tk.Entry(
        edit_window,
        font=("Arial", 14),
        width=20
    )
    edit_expense_entry.insert(0, expense_name)
    
    edit_amount_label = tk.Label(
        edit_window,
        text="Amount (RM):",
        font=("Arial", 14)
    )
    edit_amount_entry = tk.Entry(
        edit_window,
        font=("Arial", 14),
        width=15
    )
    edit_amount_entry.insert(0, f"{expense_amount:.2f}")

    edit_category_dropdown = ttk.Combobox(
        edit_window,
        values=categories,
        state="readonly",
        font=("Arial", 14)
    )
    edit_category_dropdown.set(expense_category) 

    save_button = tk.Button(
        edit_window,
        text="Save Changes",
        font=("Arial", 12),
        command=lambda: save_changes(
            edit_expense_entry,
            edit_amount_entry,
            edit_category_dropdown,
            expense_id,
            edit_window
        ) #lambda delays the execution of save_changes until the button is clicked
    )
    
    edit_expense_label.pack(pady=5)
    edit_expense_entry.pack(pady=5) 
    edit_amount_label.pack(pady=5)
    edit_amount_entry.pack(pady=5)
    edit_category_dropdown.pack(pady=5) 
    save_button.pack(pady=10)    
    
def save_changes(edit_expense_entry, edit_amount_entry, edit_category_dropdown, expense_id, edit_window):
    edited_expense_name = edit_expense_entry.get().strip()
    edited_amount = edit_amount_entry.get().strip()
    edited_category = edit_category_dropdown.get()

    if not edited_expense_name or not edited_amount or not edited_category:
        messagebox.showerror("Invalid Input", "Please fill in all fields.")
        return

    try:
        edited_amount = float(edited_amount)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid amount.")
        return

    if edited_amount <= 0:
        messagebox.showerror("Invalid Input", "Amount must be greater than zero.")
        return

    # Update the database
    database.update_expense(
        expense_id,
        edited_expense_name,
        edited_amount,
        edited_category
    )

    # Refresh the Treeview and total
    get_expense()

    edit_window.destroy()

    messagebox.showinfo(
        "Expense Updated",
        f"Expense '{edited_expense_name}' has been updated successfully."
    )

def show_category_summary():
    category_totals = database.get_category_totals()

    summary_window = tk.Toplevel(root)
    summary_window.title("Category Summary")
    summary_window.geometry("400x500")
    summary_window.resizable(False, False)

    summary_label = tk.Label(
        summary_window,
        text="Category Summary",
        font=("Arial", 16, "bold")
    )
    summary_label.pack(pady=10)

    for category in category_totals:
        category_name = category[0]
        total_amount = category[1]
        category_label = tk.Label(
            summary_window,
            text=f"{category_name}: RM {total_amount:.2f}",
            font=("Arial", 14)
        )
        category_label.pack(pady=5)
    
    overall_total = sum(category[1] for category in category_totals)

    overall_label = tk.Label(
        summary_window,
        text=f"Overall Total: RM {overall_total:.2f}",
        font=("Arial", 14, "bold")
    )
    overall_label.pack(pady=15)
    
def clear_search():
    searchentry.delete(0, tk.END)
    category_filter_dropdown.set("All Categories")
    get_expense()
    messagebox.showinfo(
        "Search Cleared",   
        "Search and filter have been cleared. Displaying all expenses."
    )
  
def apply_filters(keyword, category, start_date, end_date):
    global expenses, total_expenses
    
    if start_date > end_date:
        messagebox.showerror(
            "Invalid Date Range",
            "Start date cannot be later than end date."
        )
        return

    expenses = database.filter_expenses(keyword, category, start_date, end_date)

    for item in expense_list.get_children():
        expense_list.delete(item)
    total_expenses = 0
    
    for expense in expenses:
        dt = datetime.strptime(
            expense[4], "%Y-%m-%d %H:%M:%S"
        ).replace(tzinfo=timezone.utc)

        local_timestamp = dt.astimezone().strftime("%d/%m/%Y %I:%M %p")
        
        expense_list.insert(
            "",
            tk.END,
            values=(
                expense[0],
                expense[1],
                f"RM {expense[2]:.2f}",
                expense[3],
                local_timestamp
            )
        )
        total_expenses += expense[2]
        
    total_label.config(text=f"Total: RM {total_expenses:.2f}")
    
    messagebox.showinfo(
            "Filter Results",
            f"Found {len(expenses)} expense(s) matching your criteria."
        )

# Create the main application window
root = tk.Tk()

main_frame = tk.Frame(root)
main_frame.columnconfigure(0, minsize=150)
main_frame.columnconfigure(1, minsize=200)
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)

filter_frame = tk.Frame(main_frame)
filter_frame.columnconfigure(0, minsize=150)
filter_frame.columnconfigure(1, weight=1)

control_frame = tk.Frame(main_frame)
control_frame.columnconfigure(0, minsize=150)
control_frame.columnconfigure(1, weight=1)
control_frame.columnconfigure(2, weight=1)

expense_frame = tk.Frame(
    root,
    width=900,
    height=200
)
expense_frame.pack_propagate(False)

# Configure the window
root.title("My Expense Manager")
root.geometry("1000x700")
root.resizable(True, True)

# Create a heading
heading = tk.Label(
    root,
    text="Personal Expense Tracker",
    font=("Arial", 24, "bold")
)

#search frame
searchlabel = tk.Label(
    filter_frame,
    text="Search Expense:",
    font=("Arial", 14)
)
searchentry = tk.Entry(
    filter_frame,
    font=("Arial", 14),  
)
category_filter_label = tk.Label(
    filter_frame,
    text="Filter by Category:",
    font=("Arial", 14)
)
category_filter_dropdown = ttk.Combobox(
    filter_frame,
    values=["All Categories"] + categories,
    font=("Arial", 14),
    state="readonly"
)
category_filter_dropdown.set("All Categories")
clear_button = tk.Button(
    filter_frame,
    text="Clear",
    font=("Arial", 14),
    command=clear_search
)
start_date_label = tk.Label(
    filter_frame,
    text="Start Date",
    font=("Arial", 14)
)
start_date_entry = DateEntry(
    filter_frame,
    width=15,
    date_pattern="yyyy-mm-dd"
)
end_date_label = tk.Label(
    filter_frame,
    text="End Date:",
    font=("Arial", 14)
)
end_date_entry = DateEntry(
    filter_frame,
    width=15,
    date_pattern="yyyy-mm-dd"
)
filter_button = tk.Button(
    filter_frame,
    text="Filter",
    font=("Arial", 14),
    command=lambda: apply_filters(
        keyword=searchentry.get().strip(),
        category=category_filter_dropdown.get(),
        start_date = start_date_entry.get_date().isoformat(),
        end_date = end_date_entry.get_date().isoformat()
    )
)

#input frame labels and entries
expenselabel = tk.Label(
    control_frame,
    text="Expense Name:",
    font=("Arial", 14)
)
expenseentry = tk.Entry(
    control_frame,
    font=("Arial", 14),
    width=20
)
amountlabel = tk.Label(
    control_frame,
    text="Amount (RM):",
    font=("Arial", 14)
)
amountentry = tk.Entry(
    control_frame,
    font=("Arial", 14),
    width=15
)
categorylabel = tk.Label(
    control_frame,
    text="Category:",
    font=("Arial", 14)
)
category_dropdown = ttk.Combobox(
    control_frame,
    values=categories,
    font=("Arial", 14),
    width=15,
    state="readonly"
)
addbutton = tk.Button(
    control_frame,
    text="Add Expense",
    font=("Arial", 14),
    command=add_expense
)
deletebutton = tk.Button(
    control_frame,
    text="Delete Expense",
    font=("Arial", 14),
    command=delete_expense
)
editbutton = tk.Button(
    control_frame,
    text="Edit Expense",
    font=("Arial", 14),
    command=edit_expense
)
show_summary_button = tk.Button(
    control_frame,
    text="Show Summary",
    font=("Arial", 14),
    command=show_category_summary
)

# Set default value for the category dropdown
category_dropdown.set("Food")


# Create an expense list
expense_list = ttk.Treeview(
    expense_frame,
    columns=("ID", "Name", "Amount", "Category", "Timestamp"),
    show="headings",
    selectmode="extended",
    height=5
)
expense_list.heading("ID", text="ID")
expense_list.heading("Name", text="Expense")
expense_list.heading("Amount", text="Amount")
expense_list.heading("Category", text="Category")
expense_list.heading("Timestamp", text="Date & Time")

expense_list.column("ID", width=50, anchor="center")
expense_list.column("Name", width=200)
expense_list.column("Amount", width=130, anchor="center")
expense_list.column("Category", width=150, anchor="center")
expense_list.column("Timestamp", width=200, anchor="center")

expense_scrollbar = ttk.Scrollbar(
    expense_frame,
    orient="vertical",
    command=expense_list.yview
)

expense_list.configure(yscrollcommand=expense_scrollbar.set)

total_label = tk.Label(
    root,
    text="Total Expenses: RM 0.00",
    font=("Arial", 16, "bold")
)

# Heading
heading.pack(pady=20)

#Expense input
expenselabel.grid(row=0, column=0, padx=5, pady=5, sticky="w")
expenseentry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

#Amount input
amountlabel.grid(row=1, column=0, padx=5, pady=5, sticky="w")
amountentry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

#Category input
categorylabel.grid(row=2, column=0, padx=5, pady=5, sticky="w")
category_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

#Controls (CRUD)
addbutton.grid(row=0, column=2, padx=5, pady=5, sticky="w")
deletebutton.grid(row=1, column=2, padx=5, pady=5, sticky="w")
editbutton.grid(row=2, column=2, padx=5, pady=5, sticky="w")
show_summary_button.grid(row=3, column=2, padx=5, pady=5, sticky="w")

# Search
searchlabel.grid(row=0, column=0, padx=5, pady=5, sticky="w")
searchentry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# Category
category_filter_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
category_filter_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# Start Date
start_date_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
start_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

# End Date
end_date_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
end_date_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

# Buttons
clear_button.grid(row=4, column=0, padx=5, pady=10, sticky="ew")
filter_button.grid(row=4, column=1, padx=5, pady=10, sticky="ew")

# Nested frame
control_frame.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
filter_frame.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

# Display through pack
main_frame.pack(pady=10)

expense_frame.pack(pady=10)
expense_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
expense_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Total expenses
total_label.pack(pady=10)

# Start the application 
get_expense()
root.mainloop()

