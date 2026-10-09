import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def login():
    username = username_entry.get().strip()
    password = password_entry.get()

    if not username or not password:
        messagebox.showwarning(
            "Login",
            "Please enter username and password."
        )
        return

    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name
        FROM students
        WHERE username = ? AND password = ?
        """,
        (username, password)
    )

    student = cursor.fetchone()
    conn.close()

    if student:
        student_id = student[0]
        student_name = student[1]

        messagebox.showinfo(
            "Login Successful",
            f"Welcome, {student_name}!"
        )

        dashboard_path = os.path.join(
            BASE_DIR,
            "user_dashboard.py"
        )

        subprocess.Popen(
            [
                sys.executable,
                dashboard_path,
                str(student_id),
                student_name
            ]
        )

        root.destroy()

    else:
        messagebox.showerror(
            "Login Failed",
            "Invalid username or password!"
        )

# =========================
# FORGOT PASSWORD
# =========================

def forgot_password():
    window = tk.Toplevel(root)
    window.title("Forgot Password")
    window.geometry("350x330")
    window.resizable(False, False)
    window.configure(bg="white")

    tk.Label(
        window,
        text="Reset Password",
        font=("Arial", 18, "bold"),
        bg="white",
        fg="#172033"
    ).pack(pady=15)

    tk.Label(window, text="Registered Username", bg="white").pack()
    user_entry = tk.Entry(window, font=("Arial", 11))
    user_entry.pack(pady=5)

    tk.Label(window, text="Registered Full Name", bg="white").pack()
    name_entry = tk.Entry(window, font=("Arial", 11))
    name_entry.pack(pady=5)

    tk.Label(window, text="New Password", bg="white").pack()
    new_entry = tk.Entry(window, show="*", font=("Arial", 11))
    new_entry.pack(pady=5)

    tk.Label(window, text="Confirm New Password", bg="white").pack()
    confirm_entry = tk.Entry(window, show="*", font=("Arial", 11))
    confirm_entry.pack(pady=5)

    def reset_password():
        username = user_entry.get().strip()
        name = name_entry.get().strip()
        password = new_entry.get()
        confirm = confirm_entry.get()

        if not username or not name or not password or not confirm:
            messagebox.showwarning(
                "Warning", "Please fill in all fields.", parent=window
            )
            return

        if password != confirm:
            messagebox.showerror(
                "Error", "Passwords do not match.", parent=window
            )
            return

        if len(password) < 5:
            messagebox.showwarning(
                "Warning",
                "Password must be at least 5 characters.",
                parent=window
            )
            return

        conn = sqlite3.connect(
            os.path.join(BASE_DIR, "attendance.db")
        )
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id FROM students
            WHERE username = ? AND name = ?
            """,
            (username, name)
        )

        student = cursor.fetchone()

        if student:
            cursor.execute(
                "UPDATE students SET password = ? WHERE id = ?",
                (password, student[0])
            )
            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Password reset successfully!",
                parent=window
            )
            window.destroy()
        else:
            conn.close()
            messagebox.showerror(
                "Error",
                "Username or registered name is incorrect.",
                parent=window
            )

    tk.Button(
        window,
        text="RESET PASSWORD",
        command=reset_password,
        bg="#2563EB",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat"
    ).pack(pady=15)

def show_password():
    if password_entry.cget("show") == "*":
        password_entry.config(show="")
        show_button.config(text="Hide")
    else:
        password_entry.config(show="*")
        show_button.config(text="Show")


# =========================
# WINDOW
# =========================

root = tk.Tk()

root.title("Student Login")
root.geometry("500x500")
root.resizable(False, False)
root.configure(bg="#172033")


# =========================
# LOGIN CARD
# =========================

card = tk.Frame(
    root,
    bg="white",
    width=400,
    height=400
)

card.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)

card.pack_propagate(False)


# Title

tk.Label(
    card,
    text="Student Login",
    bg="white",
    fg="#172033",
    font=("Arial", 24, "bold")
).pack(pady=(40, 10))


tk.Label(
    card,
    text="Face Recognition Attendance System",
    bg="white",
    fg="#64748B",
    font=("Arial", 10)
).pack(pady=(0, 30))


# Username

tk.Label(
    card,
    text="Username",
    bg="white",
    fg="#475569",
    font=("Arial", 10, "bold")
).pack(anchor="w", padx=50)

username_entry = tk.Entry(
    card,
    font=("Arial", 11),
    relief="solid",
    bd=1
)

username_entry.pack(
    fill="x",
    padx=50,
    ipady=8,
    pady=(6, 20)
)


# Password

tk.Label(
    card,
    text="Password",
    bg="white",
    fg="#475569",
    font=("Arial", 10, "bold")
).pack(anchor="w", padx=50)


password_frame = tk.Frame(
    card,
    bg="white"
)

password_frame.pack(
    fill="x",
    padx=50,
    pady=(6, 25)
)


password_entry = tk.Entry(
    password_frame,
    font=("Arial", 11),
    relief="solid",
    bd=1,
    show="*"
)

password_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=8
)


show_button = tk.Button(
    password_frame,
    text="Show",
    command=show_password,
    bg="#E2E8F0",
    fg="#172033",
    relief="flat",
    width=6
)

show_button.pack(
    side="right",
    padx=(5, 0),
    ipady=5
)


# Login button

login_button = tk.Button(
    card,
    text="LOGIN",
    command=login,
    bg="#2563EB",
    fg="white",
    activebackground="#1D4ED8",
    activeforeground="white",
    relief="flat",
    font=("Arial", 11, "bold"),
    cursor="hand2"
)

login_button.pack(
    fill="x",
    padx=50,
    ipady=10
)

# Forgot Password button

tk.Button(
    card,
    text="Forgot Password?",
    command=forgot_password,
    bg="white",
    fg="#2563EB",
    relief="flat",
    cursor="hand2",
    font=("Arial", 10, "underline")
).pack(pady=(10, 0))



tk.Label(
    card,
    text="Student Portal",
    bg="white",
    fg="#2563EB",
    font=("Arial", 10, "bold")
).pack(pady=20)


# Enter key

root.bind(
    "<Return>",
    lambda event: login()
)


root.mainloop()