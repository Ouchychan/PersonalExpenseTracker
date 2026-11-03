import tkinter as tk
from tkinter import messagebox
import database

database.create_table()

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
            f"{expense[0]}. {expense[1]} - RM {expense[2]:.2f}"
        )

        total_expenses += expense[2]

    total_label.config(text=f"Total: RM {total_expenses:.2f}")
        
def add_expense():
    global total_expenses
    expense_name = expenseentry.get().strip() #strip whitespace from the input
    expense_amount = amountentry.get()

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
    
    expense = {
        "name": expense_name,
        "amount": expense_amount
    }

    database.add_expense(expense_name, expense_amount)
    
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
    
    total_label.config(
        text=f"Total Expenses: RM {total_expenses:.2f}"
    )
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
    edit_window.geometry("400x200")
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

    save_button = tk.Button(
        edit_window,
        text="Save Changes",
        font=("Arial", 12),
        command=lambda: save_changes(
            edit_expense_entry,
            edit_amount_entry,
            index,
            edit_window
        ) #lambda delays the execution of save_changes until the button is clicked
    )
    
    edit_expense_label.pack(pady=5)
    edit_expense_entry.pack(pady=5) 
    edit_amount_label.pack(pady=5)
    edit_amount_entry.pack(pady=5)
    save_button.pack(pady=10)
    
    
    
def save_changes(edit_expense_entry, edit_amount_entry, index, edit_window):
    edited_expense_name = edit_expense_entry.get().strip()
    edited_amount = edit_amount_entry.get().strip()

    if not edited_expense_name or not edited_amount:
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
        edited_amount
    )

    # Refresh the Listbox and total
    get_expense()

    edit_window.destroy()

    messagebox.showinfo(
        "Expense Updated",
        f"Expense '{edited_expense_name}' has been updated successfully."
    )

# Create the main application window

root = tk.Tk()
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

control_frame = tk.Frame(root)
control_frame.pack(pady=10)

# Configure the window
root.title("My Expense Manager")
root.geometry("900x600")
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

# Create an expense list
expense_list = tk.Listbox(
    root,
    font=("Arial", 14),
    width=50,
    height=10,
    selectmode=tk.EXTENDED
)
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

heading.pack(pady=20)
subheading.pack(pady=10)
#input_frame
expenselabel.pack(side=tk.LEFT, padx=5)
expenseentry.pack(side=tk.LEFT, padx=5)
amountlabel.pack(side=tk.LEFT, padx=5)
amountentry.pack(side=tk.LEFT, padx=5)

expense_list.pack(pady=15)
total_label.pack(pady=10)

#control_frame
addbutton.pack(side=tk.LEFT, padx=5)
selectbutton.pack(side=tk.LEFT, padx=5)
deletebutton.pack(side=tk.LEFT, padx=5)
editbutton.pack(side=tk.LEFT, padx=5)

# Start the application 
get_expense()
root.mainloop()

