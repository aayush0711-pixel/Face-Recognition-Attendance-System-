import tkinter as tk
from tkinter import ttk
import sqlite3


def load_attendance():

    # Clear old records
    for row in table.get_children():
        table.delete(row)

    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, date, time FROM attendance ORDER BY date DESC, time DESC")

    records = cursor.fetchall()

    for record in records:
        table.insert("", tk.END, values=record)

    conn.close()


# Create window
root = tk.Tk()
root.title("Face Recognition Attendance Dashboard")
root.geometry("700x450")

# Heading
title = tk.Label(
    root,
    text="Face Recognition Attendance Dashboard",
    font=("Arial", 18, "bold")
)
title.pack(pady=20)

# Table
columns = ("Name", "Date", "Time")

table = ttk.Treeview(
    root,
    columns=columns,
    show="headings"
)

table.heading("Name", text="Name")
table.heading("Date", text="Date")
table.heading("Time", text="Time")

table.column("Name", width=220)
table.column("Date", width=180)
table.column("Time", width=180)

table.pack(pady=10, fill="both", expand=True)

# Refresh button
refresh_button = tk.Button(
    root,
    text="Refresh",
    command=load_attendance,
    width=15
)
refresh_button.pack(pady=15)

# Load records when dashboard starts
load_attendance()

# Start application
root.mainloop()