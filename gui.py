import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import matplotlib.pyplot as plt

FILE_NAME = "expenses.csv"
selected_index = None


# ---------- FILE FUNCTIONS ----------

def create_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Category", "Amount", "Note"])


def load_expenses():
    data = []
    with open(FILE_NAME, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) == 4:
                data.append(row)
    return data


def save_all(data):
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Category", "Amount", "Note"])
        writer.writerows(data)


# ---------- FUNCTIONS ----------

def add_expense():
    date = date_entry.get()
    category = category_box.get()
    amount = amount_entry.get()
    note = note_entry.get()

    if date == "" or amount == "":
        messagebox.showwarning("Error", "Date & Amount required")
        return

    try:
        amount = float(amount)
    except:
        messagebox.showerror("Error", "Amount must be number")
        return

    data = load_expenses()
    data.append([date, category, amount, note])
    save_all(data)

    clear_fields()
    show_data()


def show_data():
    for i in table.get_children():
        table.delete(i)

    data = load_expenses()
    filter_cat = filter_box.get()

    total = 0

    for i, row in enumerate(data):
        if filter_cat == "All" or row[1] == filter_cat:
            table.insert("", "end", values=row, tags=(str(i),))
            total += float(row[2])

    total_label.config(text=f"Total: ₹{total:.2f}")


def delete_expense():
    selected = table.selection()

    if not selected:
        messagebox.showwarning("Error", "Select one")
        return

    index = int(table.item(selected[0], "tags")[0])

    data = load_expenses()
    data.pop(index)
    save_all(data)

    show_data()


def select_item():
    global selected_index

    selected = table.selection()

    if not selected:
        return

    selected_index = int(table.item(selected[0], "tags")[0])
    data = load_expenses()[selected_index]

    date_entry.delete(0, tk.END)
    date_entry.insert(0, data[0])

    category_box.set(data[1])

    amount_entry.delete(0, tk.END)
    amount_entry.insert(0, data[2])

    note_entry.delete(0, tk.END)
    note_entry.insert(0, data[3])


def update_expense():
    global selected_index

    if selected_index is None:
        messagebox.showwarning("Error", "Select first")
        return

    data = load_expenses()

    data[selected_index] = [
        date_entry.get(),
        category_box.get(),
        float(amount_entry.get()),
        note_entry.get()
    ]

    save_all(data)
    clear_fields()
    show_data()


def clear_fields():
    global selected_index

    date_entry.delete(0, tk.END)
    category_box.set("Food")
    amount_entry.delete(0, tk.END)
    note_entry.delete(0, tk.END)

    selected_index = None


def show_chart():
    data = load_expenses()

    if not data:
        return

    cat_total = {}

    for row in data:
        cat = row[1]
        amt = float(row[2])
        cat_total[cat] = cat_total.get(cat, 0) + amt

    plt.pie(cat_total.values(), labels=cat_total.keys(), autopct="%1.1f%%")
    plt.title("Expenses")
    plt.show()


# ---------- GUI ----------

create_file()

root = tk.Tk()
root.title("Expense Tracker")
root.geometry("750x500")

tk.Label(root, text="Expense Tracker", font=("Arial", 18, "bold")).pack(pady=10)

frame = tk.Frame(root)
frame.pack()

tk.Label(frame, text="Date").grid(row=0, column=0)
date_entry = tk.Entry(frame)
date_entry.grid(row=0, column=1)

tk.Label(frame, text="Category").grid(row=0, column=2)
category_box = ttk.Combobox(frame, values=["Food", "Travel", "Shopping", "Other"])
category_box.grid(row=0, column=3)
category_box.set("Food")

tk.Label(frame, text="Amount").grid(row=1, column=0)
amount_entry = tk.Entry(frame)
amount_entry.grid(row=1, column=1)

tk.Label(frame, text="Note").grid(row=1, column=2)
note_entry = tk.Entry(frame)
note_entry.grid(row=1, column=3)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add", command=add_expense).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Update", command=update_expense).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete", command=delete_expense).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Chart", command=show_chart).grid(row=0, column=3, padx=5)

# Filter
tk.Label(root, text="Filter").pack()
filter_box = ttk.Combobox(root, values=["All", "Food", "Travel", "Shopping", "Other"])
filter_box.set("All")
filter_box.pack()

tk.Button(root, text="Apply Filter", command=show_data).pack(pady=5)

# Table
columns = ("Date", "Category", "Amount", "Note")
table = ttk.Treeview(root, columns=columns, show="headings", height=8)

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=150)

table.pack()

table.bind("<<TreeviewSelect>>", lambda e: select_item())

total_label = tk.Label(root, text="Total: ₹0.00", font=("Arial", 12, "bold"))
total_label.pack(pady=10)

show_data()

root.mainloop()