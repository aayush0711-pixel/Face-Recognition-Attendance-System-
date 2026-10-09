
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3
import sys
import os
from PIL import Image, ImageTk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "attendance.db")

student_id = int(sys.argv[1])
student_name = sys.argv[2]


# =========================
# DATABASE
# =========================

def get_student():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name, username FROM students WHERE id = ?",
        (student_id,)
    )
    result = cursor.fetchone()
    conn.close()
    return result


# =========================
# LOGOUT
# =========================

def logout():
    root.destroy()


# =========================
# CHANGE PASSWORD
# =========================

def change_password():
    window = tk.Toplevel(root)
    window.title("Change Password")
    window.geometry("350x280")
    window.resizable(False, False)
    window.configure(bg="#F1F5F9")

    tk.Label(
        window,
        text="Change Password",
        font=("Arial", 16, "bold"),
        bg="#F1F5F9"
    ).pack(pady=15)

    tk.Label(window, text="New Password:", bg="#F1F5F9").pack()
    new_password = tk.Entry(window, show="*", width=25)
    new_password.pack(pady=5)

    tk.Label(window, text="Confirm Password:", bg="#F1F5F9").pack()
    confirm_password = tk.Entry(window, show="*", width=25)
    confirm_password.pack(pady=5)

    def save_password():
        password = new_password.get()
        confirm = confirm_password.get()

        if not password or not confirm:
            messagebox.showwarning(
                "Warning", "Please fill in both fields.", parent=window
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

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE students SET password = ? WHERE id = ?",
            (password, student_id)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success", "Password changed successfully!", parent=window
        )
        window.destroy()

    tk.Button(
        window,
        text="Save Password",
        command=save_password,
        bg="#2563EB",
        fg="white",
        font=("Arial", 10, "bold")
    ).pack(pady=15)


# =========================
# EDIT PROFILE
# =========================

def edit_profile():
    window = tk.Toplevel(root)
    window.title("Edit Profile")
    window.geometry("350x250")
    window.resizable(False, False)
    window.configure(bg="white")

    current = get_student()

    if not current:
        messagebox.showerror(
            "Error", "Student record not found.", parent=window
        )
        window.destroy()
        return

    current_name, current_username = current

    tk.Label(
        window,
        text="Edit Student Profile",
        font=("Arial", 16, "bold"),
        bg="white"
    ).pack(pady=15)

    tk.Label(window, text="Full Name", bg="white").pack()
    name_entry = tk.Entry(window, width=30)
    name_entry.insert(0, current_name or "")
    name_entry.pack(pady=5)

    tk.Label(window, text="Username", bg="white").pack()
    username_entry = tk.Entry(window, width=30)
    username_entry.insert(0, current_username or "")
    username_entry.pack(pady=5)

    def save_profile():
        new_name = name_entry.get().strip()
        new_username = username_entry.get().strip()

        if not new_name or not new_username:
            messagebox.showwarning(
                "Warning", "Please fill in all fields.", parent=window
            )
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT name FROM students WHERE id = ?",
                (student_id,)
            )
            row = cursor.fetchone()

            if not row:
                messagebox.showerror(
                    "Error", "Student record not found.", parent=window
                )
                return

            old_name = row[0]

            # Update student profile.
            cursor.execute(
                """
                UPDATE students
                SET name = ?, username = ?
                WHERE id = ?
                """,
                (new_name, new_username, student_id)
            )

            # Keep existing attendance history connected.
            if old_name != new_name:
                cursor.execute(
                    "UPDATE attendance SET name = ? WHERE name = ?",
                    (new_name, old_name)
                )

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Profile updated successfully. Please log in again.",
                parent=window
            )
            window.destroy()
            root.destroy()

        except sqlite3.IntegrityError:
            conn.rollback()
            messagebox.showerror(
                "Error",
                "This username or name may already be in use.",
                parent=window
            )

        finally:
            conn.close()

    tk.Button(
        window,
        text="Save Profile",
        command=save_profile,
        bg="#2563EB",
        fg="white",
        font=("Arial", 10, "bold")
    ).pack(pady=15)


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()
root.title("Student Attendance Dashboard")
root.geometry("1200x800")
root.resizable(False, False)


# =========================
# BACKGROUND
# =========================

background_path = os.path.join(
    BASE_DIR, "cu_background_dark.jpg"
)

try:
    background_image = Image.open(background_path)
    background_image = background_image.resize(
        (1200, 800), Image.Resampling.LANCZOS
    )
    background_photo = ImageTk.PhotoImage(background_image)

    background_label = tk.Label(
        root, image=background_photo
    )
    background_label.place(
        x=0, y=0, relwidth=1, relheight=1
    )
except Exception as e:
    print("Background image error:", e)
    root.configure(bg="#172033")


# =========================
# HEADER
# =========================

header = tk.Frame(root, bg="#172033", height=90)
header.place(x=0, y=0, width=1200, height=90)

# University logo
logo_path = os.path.join(
    BASE_DIR, "Chandigarh_University_logo.png"
)

try:
    logo_image = Image.open(logo_path)
    logo_image.thumbnail((65, 65))
    logo_photo = ImageTk.PhotoImage(logo_image)

    logo_label = tk.Label(
        header,
        image=logo_photo,
        bg="#172033"
    )
    logo_label.pack(side="left", padx=25)
except Exception as e:
    print("Logo error:", e)

header_text = tk.Frame(header, bg="#172033")
header_text.pack(side="left")

tk.Label(
    header_text,
    text="CHANDIGARH UNIVERSITY",
    bg="#172033",
    fg="white",
    font=("Arial", 18, "bold")
).pack(anchor="w")

tk.Label(
    header_text,
    text="Student Attendance Portal",
    bg="#172033",
    fg="#CBD5E1",
    font=("Arial", 10)
).pack(anchor="w")

tk.Button(
    header,
    text="Logout",
    command=logout,
    bg="#DC2626",
    fg="white",
    activebackground="#B91C1C",
    activeforeground="white",
    relief="flat",
    font=("Arial", 10, "bold"),
    cursor="hand2"
).pack(side="right", padx=25)

tk.Button(
    header,
    text="Edit Profile",
    command=edit_profile,
    bg="#0F766E",
    fg="white",
    activebackground="#115E59",
    activeforeground="white",
    relief="flat",
    font=("Arial", 10, "bold"),
    cursor="hand2"
).pack(side="right", padx=10)

tk.Button(
    header,
    text="Change Password",
    command=change_password,
    bg="#2563EB",
    fg="white",
    activebackground="#1D4ED8",
    activeforeground="white",
    relief="flat",
    font=("Arial", 10, "bold"),
    cursor="hand2"
).pack(side="right", padx=10)


# =========================
# MAIN CONTENT
# =========================

main_frame = tk.Frame(root, bg="#F1F5F9")
main_frame.place(
    x=30, y=105, width=1140, height=665
)

tk.Label(
    main_frame,
    text=f"Welcome, {student_name}",
    bg="#F1F5F9",
    fg="#172033",
    font=("Arial", 24, "bold")
).pack(pady=(12, 2))

tk.Label(
    main_frame,
    text="Student Attendance Portal",
    bg="#F1F5F9",
    fg="#64748B",
    font=("Arial", 10)
).pack(pady=(0, 8))


# =========================
# STUDENT PROFILE
# =========================

profile = tk.Frame(
    main_frame,
    bg="white",
    relief="solid",
    bd=1
)
profile.pack(padx=35, fill="x", pady=(0, 10))

current_student = get_student()
student_username = (
    current_student[1] or "N/A"
    if current_student else "N/A"
)

tk.Label(
    profile,
    text="Student Profile",
    bg="white",
    fg="#172033",
    font=("Arial", 13, "bold")
).grid(row=0, column=0, padx=20, pady=10, sticky="w")

tk.Label(
    profile,
    text=f"Student ID: {student_id}",
    bg="white",
    fg="#475569",
    font=("Arial", 10)
).grid(row=0, column=1, padx=25)

tk.Label(
    profile,
    text=f"Name: {student_name}",
    bg="white",
    fg="#475569",
    font=("Arial", 10)
).grid(row=0, column=2, padx=25)

tk.Label(
    profile,
    text=f"Username: {student_username}",
    bg="white",
    fg="#475569",
    font=("Arial", 10)
).grid(row=0, column=3, padx=25)


# =========================
# ATTENDANCE SUMMARY CARDS
# =========================

cards = tk.Frame(main_frame, bg="#F1F5F9")
cards.pack(pady=5)


def create_card(parent, title, color):
    frame = tk.Frame(
        parent,
        bg="white",
        width=230,
        height=90,
        relief="solid",
        bd=1
    )
    frame.pack_propagate(False)

    tk.Label(
        frame,
        text=title,
        bg="white",
        fg="#64748B",
        font=("Arial", 10, "bold")
    ).pack(pady=(10, 2))

    value = tk.Label(
        frame,
        text="0",
        bg="white",
        fg=color,
        font=("Arial", 21, "bold")
    )
    value.pack()

    return frame, value


present_card, present_label = create_card(
    cards, "PRESENT DAYS", "#16A34A"
)
present_card.grid(row=0, column=0, padx=12)

total_card, total_label = create_card(
    cards, "TOTAL DAYS", "#2563EB"
)
total_card.grid(row=0, column=1, padx=12)

percentage_card, percentage_label = create_card(
    cards, "ATTENDANCE", "#9333EA"
)
percentage_card.grid(row=0, column=2, padx=12)


# =========================
# ATTENDANCE STATUS
# =========================

status_label = tk.Label(
    main_frame,
    text="Attendance",
    bg="#F1F5F9",
    fg="#16A34A",
    font=("Arial", 11, "bold")
)
status_label.pack(pady=5)

tk.Label(
    main_frame,
    text="Attendance History",
    bg="#F1F5F9",
    fg="#172033",
    font=("Arial", 16, "bold")
).pack(pady=(3, 7))


# =========================
# MONTHLY REPORT FILTER
# =========================

month_frame = tk.Frame(main_frame, bg="#F1F5F9")
month_frame.pack(pady=(0, 8))

tk.Label(
    month_frame,
    text="Month:",
    bg="#F1F5F9",
    fg="#172033",
    font=("Arial", 10, "bold")
).pack(side="left", padx=(0, 5))

month_options = [
    "All Months", "01", "02", "03", "04",
    "05", "06", "07", "08", "09", "10", "11", "12"
]

month_var = tk.StringVar(
    value=datetime.now().strftime("%m")
)

ttk.Combobox(
    month_frame,
    textvariable=month_var,
    values=month_options,
    state="readonly",
    width=12
).pack(side="left", padx=(0, 15))

tk.Label(
    month_frame,
    text="Year:",
    bg="#F1F5F9",
    fg="#172033",
    font=("Arial", 10, "bold")
).pack(side="left", padx=(0, 5))

years_conn = sqlite3.connect(DB_PATH)
years_cursor = years_conn.cursor()
years_cursor.execute(
    """
    SELECT DISTINCT strftime('%Y', date)
    FROM attendance
    WHERE date IS NOT NULL
    ORDER BY 1 DESC
    """
)
available_years = [
    row[0] for row in years_cursor.fetchall() if row[0]
]
years_conn.close()

current_year = datetime.now().strftime("%Y")

if current_year not in available_years:
    available_years.insert(0, current_year)

year_options = ["All Years"] + available_years
year_var = tk.StringVar(value=current_year)

ttk.Combobox(
    month_frame,
    textvariable=year_var,
    values=year_options,
    state="readonly",
    width=10
).pack(side="left", padx=(0, 10))


# =========================
# LOAD ATTENDANCE
# =========================

def load_attendance():
    for item in table.get_children():
        table.delete(item)

    selected_month = month_var.get()
    selected_year = year_var.get()

    date_filter = ""
    params = [student_name]

    if selected_month != "All Months":
        date_filter += " AND strftime('%m', date) = ?"
        params.append(selected_month)

    if selected_year != "All Years":
        date_filter += " AND strftime('%Y', date) = ?"
        params.append(selected_year)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        f"""
        SELECT date, time
        FROM attendance
        WHERE name = ? {date_filter}
        ORDER BY date DESC, time DESC
        """,
        tuple(params)
    )
    records = cursor.fetchall()

    cursor.execute(
        f"""
        SELECT COUNT(*)
        FROM attendance
        WHERE name = ? {date_filter}
        """,
        tuple(params)
    )
    present_days = cursor.fetchone()[0]

    total_filter = ""
    total_params = []

    if selected_month != "All Months":
        total_filter += " AND strftime('%m', date) = ?"
        total_params.append(selected_month)

    if selected_year != "All Years":
        total_filter += " AND strftime('%Y', date) = ?"
        total_params.append(selected_year)

    cursor.execute(
        f"""
        SELECT COUNT(DISTINCT date)
        FROM attendance
        WHERE 1=1 {total_filter}
        """,
        tuple(total_params)
    )
    total_days = cursor.fetchone()[0]

    conn.close()

    percentage = (
        present_days / total_days * 100
        if total_days else 0
    )

    present_label.config(text=str(present_days))
    total_label.config(text=str(total_days))
    percentage_label.config(text=f"{percentage:.2f}%")

    if percentage >= 75:
        status_label.config(
            text="Good Attendance",
            fg="#16A34A"
        )
    else:
        status_label.config(
            text="Low Attendance",
            fg="#DC2626"
        )

    for date, time in records:
        table.insert(
            "", tk.END,
            values=(date, time, "Present")
        )


def show_all_records():
    month_var.set("All Months")
    year_var.set("All Years")
    load_attendance()


tk.Button(
    month_frame,
    text="Show Report",
    command=load_attendance,
    bg="#2563EB",
    fg="white",
    relief="flat",
    font=("Arial", 9, "bold"),
    cursor="hand2"
).pack(side="left", padx=5)

tk.Button(
    month_frame,
    text="All Records",
    command=show_all_records,
    bg="#64748B",
    fg="white",
    relief="flat",
    font=("Arial", 9, "bold"),
    cursor="hand2"
).pack(side="left", padx=5)


# =========================
# ATTENDANCE TABLE
# =========================

table_frame = tk.Frame(main_frame, bg="white")
table_frame.pack(
    padx=35,
    fill="both",
    expand=True
)

columns = ("Date", "Time", "Status")

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

table.heading("Date", text="DATE")
table.heading("Time", text="TIME")
table.heading("Status", text="STATUS")

table.column("Date", width=300, anchor="center")
table.column("Time", width=300, anchor="center")
table.column("Status", width=300, anchor="center")

table.pack(fill="both", expand=True)


# =========================
# START
# =========================

load_attendance()
root.mainloop()
