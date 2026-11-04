import tkinter as tk
from tkinter import messagebox, ttk
import database

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

    expense_list.delete(0, tk.END)
    total_expenses = 0

    for expense in expenses:
        expense_list.insert(
            tk.END,
            f"{expense[0]}. {expense[1]} - RM {expense[2]:.2f} [{expense[3]}]"
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
    
def select_expense():
    selected = expense_list.curselection()
    messagebox.showinfo(
        "Selected Expenses",
        f"You have selected {len(selected)} expense(s)."
    )
def delete_expense():
    global total_expenses
    selected = expense_list.curselection()
    
    if not selected:
        messagebox.showwarning("Invalid Selection", "Please select an expense to delete.")
        return

    for index in reversed(selected):
        expense_id = expenses[index][0]
        database.delete_expense(expense_id)
    get_expense() 
    
    messagebox.showinfo(
        "Deleted Expenses",
        f"You have deleted {len(selected)} expense(s)."
    )

def edit_expense():
    selected = expense_list.curselection()

    if not selected:
        messagebox.showerror("Invalid Selection", "Please select an expense to edit.")
        return
    if len(selected) > 1:
        messagebox.showerror("Invalid Selection", "Please select only one expense to edit.")
        return
    index = selected[0]
    expense = expenses[index]

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
    edit_expense_entry.insert(0, expense[1])
    
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
    edit_amount_entry.insert(0, str(expense[2]))

    edit_category_dropdown = ttk.Combobox(
        edit_window,
        values=categories,
        state="readonly",
        font=("Arial", 14)
    )
    edit_category_dropdown.set(expense[3]) 

    save_button = tk.Button(
        edit_window,
        text="Save Changes",
        font=("Arial", 12),
        command=lambda: save_changes(
            edit_expense_entry,
            edit_amount_entry,
            edit_category_dropdown,
            index,
            edit_window
        ) #lambda delays the execution of save_changes until the button is clicked
    )
    
    edit_expense_label.pack(pady=5)
    edit_expense_entry.pack(pady=5) 
    edit_amount_label.pack(pady=5)
    edit_amount_entry.pack(pady=5)
    edit_category_dropdown.pack(pady=5) 
    save_button.pack(pady=10)    
    
def save_changes(edit_expense_entry, edit_amount_entry, edit_category_dropdown, index, edit_window):
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

    # Retrieve the database ID
    expense_id = expenses[index][0]

    # Update the database
    database.update_expense(
        expense_id,
        edited_expense_name,
        edited_amount,
        edited_category
    )

    # Refresh the Listbox and total
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
    
# Create the main application window

root = tk.Tk()
input_frame = tk.Frame(root)

control_frame = tk.Frame(root)

expense_frame = tk.Frame(root)

# Configure the window
root.title("My Expense Manager")
root.geometry("1100x600")
root.resizable(True, True)

# Create a heading
heading = tk.Label(
    root,
    text="Welcome To My Expense Tracker",
    font=("Arial", 24, "bold")
)
# Create a subheading
subheading = tk.Label(
    root,
    text="Track your spending, manage your expenses.",
    font=("Arial", 16)
)

#input frame labels and entries
expenselabel = tk.Label(
    input_frame,
    text="Expense Name:",
    font=("Arial", 14)
)
expenseentry = tk.Entry(
    input_frame,
    font=("Arial", 14),
    width=20
)
amountlabel = tk.Label(
    input_frame,
    text="Amount (RM):",
    font=("Arial", 14)
)
amountentry = tk.Entry(
    input_frame,
    font=("Arial", 14),
    width=15
)
#Category label and dropdown
categorylabel = tk.Label(
    input_frame,
    text="Category:",
    font=("Arial", 14)
)
category_dropdown = ttk.Combobox(
    input_frame,
    values=categories,
    font=("Arial", 14),
    width=15,
    state="readonly"
)
# Set default value for the category dropdown
category_dropdown.set("Food")


# Create an expense list
expense_scrollbar = ttk.Scrollbar(
    expense_frame,
    orient="vertical"
)

expense_list = tk.Listbox(
    expense_frame,
    font=("Arial", 14),
    selectmode=tk.EXTENDED,
    width=40,
    height=10,
    yscrollcommand=expense_scrollbar.set
)

expense_scrollbar.config(command=expense_list.yview)

total_label = tk.Label(
    root,
    text="Total Expenses: RM 0.00",
    font=("Arial", 16, "bold")
)

addbutton = tk.Button(
    control_frame,
    text="Add Expense",
    font=("Arial", 14),
    command=add_expense
)
selectbutton = tk.Button(
    control_frame,
    text="Check Selection",
    font=("Arial", 14),
    command=select_expense
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
    text="Show Category Summary",
    font=("Arial", 14),
    command=show_category_summary
)

# Heading and subheading
heading.pack(pady=20)
subheading.pack(pady=10)

# Input frame
input_frame.pack(pady=10)

expenselabel.pack(side=tk.LEFT, padx=5)
expenseentry.pack(side=tk.LEFT, padx=5)
amountlabel.pack(side=tk.LEFT, padx=5)
amountentry.pack(side=tk.LEFT, padx=5)
categorylabel.pack(side=tk.LEFT, padx=5)
category_dropdown.pack(side=tk.LEFT, padx=5)

# Control frame
control_frame.pack(pady=10)

addbutton.pack(side=tk.LEFT, padx=5)
selectbutton.pack(side=tk.LEFT, padx=5)
deletebutton.pack(side=tk.LEFT, padx=5)
editbutton.pack(side=tk.LEFT, padx=5)
show_summary_button.pack(side=tk.LEFT, padx=5)

# Expense list frame
expense_frame.pack(pady=10)

expense_list.pack(side=tk.LEFT)
expense_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Total expenses
total_label.pack(pady=10)

# Start the application 
get_expense()
root.mainloop()

