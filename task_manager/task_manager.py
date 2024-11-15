import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

# Database setup
def initialize_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            deadline TEXT,
            priority TEXT,
            category TEXT,
            completed BOOLEAN DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

# Function to add a task to the database
def add_task_to_db(title, description, deadline, priority, category):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (title, description, deadline, priority, category)
        VALUES (?, ?, ?, ?, ?)
    """, (title, description, deadline, priority, category))
    conn.commit()
    conn.close()

# Function to delete a task from the database
def delete_task(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No task selected!")
        return

    task_id = tree.item(selected_item, "values")[0]
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Task deleted successfully!")
    display_tasks(tree)

# Function to display all tasks
def display_tasks(tree):
    for row in tree.get_children():
        tree.delete(row)  # Clear the treeview

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, deadline, priority, category, completed FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        task_id, title, deadline, priority, category, completed = row
        status = "Task not completed" if not completed and datetime.strptime(deadline, "%Y-%m-%d") < datetime.now() else ""
        tree.insert("", tk.END, values=(task_id, title, deadline, priority, category, status))

# Function to handle adding a task
def add_task_gui(tree):
    def submit_task():
        title = title_entry.get()
        description = description_entry.get()
        deadline = deadline_entry.get()
        priority = priority_var.get()
        category = category_entry.get()

        if not title or not deadline or not priority or not category:
            messagebox.showerror("Input Error", "All fields are required!")
            return

        try:
            datetime.strptime(deadline, "%Y-%m-%d")  # Validate date format
        except ValueError:
            messagebox.showerror("Input Error", "Deadline must be in YYYY-MM-DD format!")
            return

        add_task_to_db(title, description, deadline, priority, category)
        messagebox.showinfo("Success", "Task added successfully!")
        add_task_window.destroy()
        display_tasks(tree)

    # New window for adding a task
    add_task_window = tk.Toplevel(root)
    add_task_window.title("Add Task")

    tk.Label(add_task_window, text="Title:").grid(row=0, column=0, padx=5, pady=5)
    title_entry = tk.Entry(add_task_window)
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(add_task_window, text="Description:").grid(row=1, column=0, padx=5, pady=5)
    description_entry = tk.Entry(add_task_window)
    description_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(add_task_window, text="Deadline (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
    deadline_entry = tk.Entry(add_task_window)
    deadline_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(add_task_window, text="Priority:").grid(row=3, column=0, padx=5, pady=5)
    priority_var = tk.StringVar(value="Low")
    priority_menu = ttk.Combobox(add_task_window, textvariable=priority_var, values=["Low", "Medium", "High"])
    priority_menu.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(add_task_window, text="Category:").grid(row=4, column=0, padx=5, pady=5)
    category_entry = tk.Entry(add_task_window)
    category_entry.grid(row=4, column=1, padx=5, pady=5)

    submit_button = tk.Button(add_task_window, text="Add Task", command=submit_task)
    submit_button.grid(row=5, column=0, columnspan=2, pady=10)

# Main application window
root = tk.Tk()
root.title("Task Manager")

# Task list display
columns = ("ID", "Title", "Deadline", "Priority", "Category", "Status")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.pack(padx=10, pady=10)

# Buttons
add_button = tk.Button(root, text="Add Task", command=lambda: add_task_gui(tree))
add_button.pack(pady=5)

delete_button = tk.Button(root, text="Delete Task", command=lambda: delete_task(tree))
delete_button.pack(pady=5)

refresh_button = tk.Button(root, text="Refresh", command=lambda: display_tasks(tree))
refresh_button.pack(pady=5)

# Initialize database and display tasks
initialize_db()
display_tasks(tree)

# Run the application
root.mainloop()
