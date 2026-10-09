import tkinter as tk
from tkinter import ttk
import sqlite3


def load_report():
    # Clear table
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

    # Students present
    cursor.execute("SELECT COUNT(DISTINCT name) FROM attendance")
    present_students = cursor.fetchone()[0]

    # Total attendance days
    cursor.execute("SELECT COUNT(DISTINCT date) FROM attendance")
    total_days = cursor.fetchone()[0]

    # Update summary
    total_label.config(
        text=f"Total Students: {total_students}"
    )

    attendance_label.config(
        text=f"Total Attendance Records: {total_attendance}"
    )

    present_label.config(
        text=f"Students Present: {present_students}"
    )

    # Get students
    cursor.execute("SELECT name FROM students")
    students = cursor.fetchall()

    for student in students:
        student_name = student[0]

        # Count present days
        cursor.execute(
            "SELECT COUNT(*) FROM attendance WHERE name = ?",
            (student_name,)
        )

        present_days = cursor.fetchone()[0]

        # Calculate percentage
        if total_days > 0:
            percentage = (present_days / total_days) * 100
        else:
            percentage = 0

        # Calculate status
        if percentage >= 75:
            status = "Good"
        else:
            status = "Low"

        # Add to table
        table.insert(
            "",
            tk.END,
            values=(
                student_name,
                present_days,
                total_days,
                f"{percentage:.2f}%",
                status
            )
        )

    conn.close()


# Main window
root = tk.Tk()
root.title("Attendance Reports")
root.geometry("950x550")


# Title
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


# Table columns
columns = (
    "Name",
    "Present Days",
    "Total Days",
    "Percentage",
    "Status"
)


table = ttk.Treeview(
    root,
    columns=columns,
    show="headings"
)


# Headings
table.heading(
    "Name",
    text="Student Name"
)

table.heading(
    "Present Days",
    text="Present Days"
)

table.heading(
    "Total Days",
    text="Total Days"
)

table.heading(
    "Percentage",
    text="Attendance %"
)

table.heading(
    "Status",
    text="Status"
)


# Column width
table.column(
    "Name",
    width=250
)

table.column(
    "Present Days",
    width=150
)

table.column(
    "Total Days",
    width=150
)

table.column(
    "Percentage",
    width=150
)

table.column(
    "Status",
    width=120
)


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


# Load report
load_report()


# Start application
root.mainloop()