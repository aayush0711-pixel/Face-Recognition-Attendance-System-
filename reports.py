import tkinter as tk
from tkinter import ttk
import sqlite3


def load_report():
    for row in table.get_children():
        table.delete(row)

    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    # Total students
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    # Total attendance records
    cursor.execute("SELECT COUNT(*) FROM attendance")
    total_attendance = cursor.fetchone()[0]

    # Students with attendance
    cursor.execute("SELECT COUNT(DISTINCT name) FROM attendance")
    present_students = cursor.fetchone()[0]

    total_label.config(text=f"Total Students: {total_students}")
    attendance_label.config(
        text=f"Total Attendance Records: {total_attendance}"
    )
    present_label.config(
        text=f"Students Present: {present_students}"
    )

    # Attendance records
    cursor.execute("""
        SELECT name, date, time
        FROM attendance
        ORDER BY date DESC, time DESC
    """)

    records = cursor.fetchall()

    for record in records:
        table.insert("", tk.END, values=record)

    conn.close()


root = tk.Tk()
root.title("Attendance Reports")
root.geometry("800x550")

title = tk.Label(
    root,
    text="Attendance Reports",
    font=("Arial", 20, "bold")
)
title.pack(pady=20)

# Summary
summary_frame = tk.Frame(root)
summary_frame.pack(pady=10)

total_label = tk.Label(
    summary_frame,
    text="Total Students: 0",
    font=("Arial", 12, "bold")
)
total_label.grid(row=0, column=0, padx=20)

attendance_label = tk.Label(
    summary_frame,
    text="Total Attendance Records: 0",
    font=("Arial", 12, "bold")
)
attendance_label.grid(row=0, column=1, padx=20)

present_label = tk.Label(
    summary_frame,
    text="Students Present: 0",
    font=("Arial", 12, "bold")
)
present_label.grid(row=0, column=2, padx=20)

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

table.column("Name", width=250)
table.column("Date", width=200)
table.column("Time", width=200)

table.pack(
    pady=20,
    fill="both",
    expand=True
)

# Refresh button
refresh_button = tk.Button(
    root,
    text="Refresh Report",
    command=load_report,
    width=20
)
refresh_button.pack(pady=15)

load_report()

root.mainloop()