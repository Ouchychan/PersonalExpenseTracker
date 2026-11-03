# Personal Expense Tracker

A simple desktop application built with Python, Tkinter and SQLite that helps users record, manage and track their daily expenses.

This project was developed as a hands-on learning project to practise Python programming, GUI development, database management and software development fundamentals.

## Features

- **Add Expenses** – Record expenses with a name and amount.
- **View Expenses** – Display all saved expenses in a list.
- **Edit Expenses** – Update the name and amount of existing expenses.
- **Delete Expenses** – Remove individual or multiple expenses.
- **Automatic Total Calculation** – Calculate total expenses automatically.
- **Data Persistence** – Store expense records using SQLite, allowing data to remain available after restarting the application.
- **Input Validation** – Handle empty fields, invalid amounts and non-positive values.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Tkinter | Graphical User Interface (GUI) |
| SQLite | Database and persistent storage |
| SQL | Database operations (CRUD) |
| VS Code | Development environment |
| Git & GitHub | Version control and project hosting |

## Project Structure

```text
PersonalExpenseTracker/
│
├── main.py          # Main application and Tkinter interface
├── database.py      # SQLite connection and database operations
├── expenses.db      # SQLite database (generated automatically)
└── README.md        # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.x
- Git (optional, for cloning the repository)

### Installation

1. Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

2. Navigate to the project directory:

```bash
cd PersonalExpenseTracker
```

3. Run the application:

```bash
python main.py
```

No additional Python packages are required because Tkinter and SQLite are included with standard Python installations.

## How It Works

The application uses Tkinter to provide a graphical interface and SQLite to store expense records.

The database module handles the four fundamental database operations:

| Operation | Description |
|---|---|
| Create | Insert a new expense |
| Read | Retrieve saved expenses |
| Update | Modify an existing expense |
| Delete | Remove an expense |

The application retrieves records from SQLite and displays them in the Tkinter interface. Whenever an expense is added, edited or deleted, the interface refreshes to reflect the latest database records.

## What I Learned

Through this project, I practised:

- Building desktop applications using Python and Tkinter.
- Working with Python functions, lists, dictionaries and tuples.
- Handling user input and exceptions using `try` and `except`.
- Connecting Python applications to SQLite databases.
- Writing SQL queries using `INSERT`, `SELECT`, `UPDATE` and `DELETE`.
- Separating application logic and database operations into different modules.
- Using Git and GitHub to manage and showcase a software project.

## Future Improvements

Planned features and enhancements:

- [ ] Add expense categories.
- [ ] Record transaction dates.
- [ ] Search and filter expenses.
- [ ] Generate monthly expense reports.
- [ ] Improve the graphical interface and user experience.
- [ ] Add automated tests.
- [ ] Package the application as a Windows executable.

## Project Status

**Current status:** Functional prototype with SQLite integration.

This project is actively being developed as part of my journey in learning Python and software development.

## License

This project is available for educational and learning purposes.
