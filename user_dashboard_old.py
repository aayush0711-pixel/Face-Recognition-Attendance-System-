import tkinter as tk
from tkinter import ttk
import sqlite3
import sys
import os
from PIL import Image, ImageTk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

student_id = sys.argv[1]
student_name = sys.argv[2]


# =========================
# GET STUDENT USERNAME
# =========================

def get_username():
    conn = sqlite3.connect(
        os.path.join(BASE_DIR, "attendance.db")
    )
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username FROM students WHERE id = ?",
        (student_id,)
    )

    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]

    return "N/A"


student_username = get_username()


# =========================
# LOAD ATTENDANCE
# =========================

def load_attendance():

    for row in table.get_children():
        table.delete(row)

    conn = sqlite3.connect(
        os.path.join(BASE_DIR, "attendance.db")
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT date, time
        FROM attendance
        WHERE name = ?
        ORDER BY date DESC, time DESC
        """,
        (student_name,)
    )

    records = cursor.fetchall()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM attendance
        WHERE name = ?
        """,
        (student_name,)
    )

    present_days = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(DISTINCT date)
        FROM attendance
        """
    )

    total_days = cursor.fetchone()[0]

    conn.close()

    if total_days > 0:
        percentage = (present_days / total_days) * 100
    else:
        percentage = 0

    present_label.config(
        text=str(present_days)
    )

    total_label.config(
        text=str(total_days)
    )

    percentage_label.config(
        text=f"{percentage:.2f}%"
    )

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
            "",
            tk.END,
            values=(
                date,
                time,
                "Present"
            )
        )


# =========================
# LOGOUT
# =========================

def logout():
    root.destroy()


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()

root.title(
    "Student Attendance Dashboard"
)

root.geometry(
    "1200x800"
)

root.resizable(False, False)


# =========================
# BACKGROUND
# =========================

background_path = os.path.join(
    BASE_DIR,
    "cu_background_dark.jpg"
)

try:

    background_image = Image.open(
        background_path
    )

    background_image = background_image.resize(
        (1200, 800),
        Image.Resampling.LANCZOS
    )

    background_photo = ImageTk.PhotoImage(
        background_image
    )

    background_label = tk.Label(
        root,
        image=background_photo
    )

    background_label.place(
        x=0,
        y=0,
        relwidth=1,
        relheight=1
    )

except Exception as e:

    print("Background image error:", e)

    root.configure(
        bg="#172033"
    )


# =========================
# HEADER
# =========================

header = tk.Frame(
    root,
    bg="#172033",
    height=90
)

header.place(
    x=0,
    y=0,
    width=1200,
    height=90
)


# =========================
# CU LOGO
# =========================

logo_path = os.path.join(
    BASE_DIR,
    "Chandigarh_University_logo.png"
)

try:

    logo_image = Image.open(
        logo_path
    )

    logo_image.thumbnail(
        (65, 65)
    )

    logo_photo = ImageTk.PhotoImage(
        logo_image
    )

    logo_label = tk.Label(
        header,
        image=logo_photo,
        bg="#172033"
    )

    logo_label.pack(
        side="left",
        padx=25
    )

except Exception as e:

    print("Logo error:", e)


# =========================
# HEADER TEXT
# =========================

header_text = tk.Frame(
    header,
    bg="#172033"
)

header_text.pack(
    side="left"
)

tk.Label(
    header_text,
    text="CHANDIGARH UNIVERSITY",
    bg="#172033",
    fg="white",
    font=("Arial", 18, "bold")
).pack(
    anchor="w"
)

tk.Label(
    header_text,
    text="Student Attendance Portal",
    bg="#172033",
    fg="#CBD5E1",
    font=("Arial", 10)
).pack(
    anchor="w"
)


# =========================
# LOGOUT
# =========================

logout_button = tk.Button(
    header,
    text="Logout",
    command=logout,
    bg="#DC2626",
    fg="white",
    activebackground="#B91C1C",
    activeforeground="white",
    relief="flat",
    font=("Arial", 10, "bold"),
    width=12,
    cursor="hand2"
)

logout_button.pack(
    side="right",
    padx=30
)


# =========================
# MAIN CONTENT
# =========================

main_frame = tk.Frame(
    root,
    bg="#F1F5F9"
)

main_frame.place(
    x=30,
    y=105,
    width=1140,
    height=665
)


# =========================
# WELCOME
# =========================

tk.Label(
    main_frame,
    text=f"Welcome, {student_name}",
    bg="#F1F5F9",
    fg="#172033",
    font=("Arial", 24, "bold")
).pack(
    pady=(12, 2)
)


tk.Label(
    main_frame,
    text="Student Attendance Portal",
    bg="#F1F5F9",
    fg="#64748B",
    font=("Arial", 10)
).pack(
    pady=(0, 8)
)


# =========================
# PROFILE
# =========================

profile = tk.Frame(
    main_frame,
    bg="white",
    relief="solid",
    bd=1
)

profile.pack(
    padx=35,
    fill="x",
    pady=(0, 10)
)


tk.Label(
    profile,
    text="Student Profile",
    bg="white",
    fg="#172033",
    font=("Arial", 13, "bold")
).grid(
    row=0,
    column=0,
    padx=20,
    pady=10,
    sticky="w"
)


tk.Label(
    profile,
    text=f"Student ID: {student_id}",
    bg="white",
    fg="#475569",
    font=("Arial", 10)
).grid(
    row=0,
    column=1,
    padx=25
)


tk.Label(
    profile,
    text=f"Name: {student_name}",
    bg="white",
    fg="#475569",
    font=("Arial", 10)
).grid(
    row=0,
    column=2,
    padx=25
)


tk.Label(
    profile,
    text=f"Username: {student_username}",
    bg="white",
    fg="#475569",
    font=("Arial", 10)
).grid(
    row=0,
    column=3,
    padx=25
)


# =========================
# STAT CARDS
# =========================

cards = tk.Frame(
    main_frame,
    bg="#F1F5F9"
)

cards.pack(
    pady=5
)


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
    ).pack(
        pady=(10, 2)
    )

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
    cards,
    "PRESENT DAYS",
    "#16A34A"
)

present_card.grid(
    row=0,
    column=0,
    padx=12
)


total_card, total_label = create_card(
    cards,
    "TOTAL DAYS",
    "#2563EB"
)

total_card.grid(
    row=0,
    column=1,
    padx=12
)


percentage_card, percentage_label = create_card(
    cards,
    "ATTENDANCE",
    "#9333EA"
)

percentage_card.grid(
    row=0,
    column=2,
    padx=12
)


# =========================
# STATUS
# =========================

status_label = tk.Label(
    main_frame,
    text="Attendance",
    bg="#F1F5F9",
    fg="#16A34A",
    font=("Arial", 11, "bold")
)

status_label.pack(
    pady=5
)


# =========================
# ATTENDANCE TITLE
# =========================

tk.Label(
    main_frame,
    text="Attendance History",
    bg="#F1F5F9",
    fg="#172033",
    font=("Arial", 16, "bold")
).pack(
    pady=(3, 7)
)


# =========================
# TABLE
# =========================

table_frame = tk.Frame(
    main_frame,
    bg="white"
)

table_frame.pack(
    padx=35,
    fill="both",
    expand=True
)


columns = (
    "Date",
    "Time",
    "Status"
)

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

table.heading(
    "Date",
    text="DATE"
)

table.heading(
    "Time",
    text="TIME"
)

table.heading(
    "Status",
    text="STATUS"
)

table.column(
    "Date",
    width=300,
    anchor="center"
)

table.column(
    "Time",
    width=300,
    anchor="center"
)

table.column(
    "Status",
    width=300,
    anchor="center"
)

table.pack(
    fill="both",
    expand=True
)


# =========================
# LOAD DATA
# =========================

load_attendance()


# =========================
# START
# =========================

root.mainloop()