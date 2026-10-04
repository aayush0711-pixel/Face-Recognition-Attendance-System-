import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


def load_students():
    for row in table.get_children():
        table.delete(row)

    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, image_path FROM students")
    students = cursor.fetchall()

    for student in students:
        table.insert("", tk.END, values=student)

    conn.close()


def delete_student():
    selected = table.selection()

    if not selected:
        messagebox.showwarning("Warning", "Please select a student.")
        return

    student = table.item(selected[0])["values"]
    student_id = student[0]
    student_name = student[1]

    confirm = messagebox.askyesno(
        "Delete Student",
        f"Delete {student_name}?"
    )

    if confirm:
        conn = sqlite3.connect("attendance.db")
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

        conn.commit()
        conn.close()

        load_students()
        messagebox.showinfo("Success", "Student deleted.")


root = tk.Tk()
root.title("Student Management")
root.geometry("700x450")

title = tk.Label(
    root,
    text="Student Management",
    font=("Arial", 20, "bold")
)
title.pack(pady=20)

columns = ("ID", "Name", "Image Path")

table = ttk.Treeview(
    root,
    columns=columns,
    show="headings"
)

table.heading("ID", text="ID")
table.heading("Name", text="Name")
table.heading("Image Path", text="Image Path")

table.column("ID", width=80)
table.column("Name", width=200)
table.column("Image Path", width=350)

table.pack(
    pady=10,
    fill="both",
    expand=True
)

delete_button = tk.Button(
    root,
    text="Delete Student",
    command=delete_student,
    width=20
)
delete_button.pack(pady=10)

refresh_button = tk.Button(
    root,
    text="Refresh",
    command=load_students,
    width=20
)
refresh_button.pack(pady=10)

load_students()

root.mainloop()