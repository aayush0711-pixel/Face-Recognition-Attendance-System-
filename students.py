
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "attendance.db")


def connect_db():
    return sqlite3.connect(DB_PATH)


def load_students():
    for row in table.get_children():
        table.delete(row)

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, image_path, username FROM students")
    
    for student in cursor.fetchall():
        table.insert("", tk.END, values=student)

    conn.close()


def set_credentials():
    selected = table.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select a student first.")
        return

    student = table.item(selected[0])["values"]
    student_id = student[0]
    student_name = student[1]

    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showwarning(
            "Missing Details",
            "Enter both username and password."
        )
        return

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE students SET username = ?, password = ? WHERE id = ?",
            (username, password, student_id)
        )
        conn.commit()
        messagebox.showinfo(
            "Success",
            f"Login details saved for {student_name}."
        )
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        load_students()

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Error",
            "That username is already being used."
        )

    finally:
        conn.close()


def select_student(event):
    selected = table.selection()

    if selected:
        student = table.item(selected[0])["values"]
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

        if student[3]:
            username_entry.insert(0, student[3])


def delete_student():
    selected = table.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select a student first.")
        return

    student = table.item(selected[0])["values"]

    if messagebox.askyesno(
        "Confirm Delete",
        f"Delete student {student[1]}?"
    ):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student[0],))
        conn.commit()
        conn.close()

        load_students()
        messagebox.showinfo("Success", "Student deleted.")


root = tk.Tk()
root.title("Admin - Student Management")
root.geometry("950x650")
root.configure(bg="#F1F5F9")

tk.Label(
    root,
    text="Student Management",
    font=("Arial", 22, "bold"),
    bg="#F1F5F9",
    fg="#172033"
).pack(pady=20)

columns = ("ID", "Name", "Image Path", "Username")
table = ttk.Treeview(root, columns=columns, show="headings", height=10)

for col in columns:
    table.heading(col, text=col)

table.column("ID", width=60, anchor="center")
table.column("Name", width=180)
table.column("Image Path", width=400)
table.column("Username", width=180)

table.pack(padx=20, fill="x")
table.bind("<<TreeviewSelect>>", select_student)

form = tk.Frame(root, bg="#F1F5F9")
form.pack(pady=20)

tk.Label(form, text="Username:", bg="#F1F5F9").grid(
    row=0, column=0, padx=10, pady=8, sticky="e"
)
username_entry = tk.Entry(form, width=30)
username_entry.grid(row=0, column=1, padx=10, pady=8)

tk.Label(form, text="New Password:", bg="#F1F5F9").grid(
    row=1, column=0, padx=10, pady=8, sticky="e"
)
password_entry = tk.Entry(form, width=30, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=8)

tk.Button(
    root,
    text="Save Login Details",
    command=set_credentials,
    bg="#2563EB",
    fg="white",
    width=25
).pack(pady=8)

tk.Button(
    root,
    text="Delete Selected Student",
    command=delete_student,
    bg="#DC2626",
    fg="white",
    width=25
).pack(pady=8)

tk.Button(
    root,
    text="Refresh",
    command=load_students,
    width=25
).pack(pady=8)

load_students()
root.mainloop()
