import tkinter as tk
from tkinter import ttk
import sqlite3
import subprocess
import sys
import os
from PIL import Image, ImageTk


# =========================================================
# PATH
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# =========================================================
# COLORS
# =========================================================

BG = "#F3F6FB"
WHITE = "#FFFFFF"
PRIMARY = "#2563EB"
PRIMARY_DARK = "#1D4ED8"
DARK = "#172033"
TEXT = "#475569"
BORDER = "#DCE4EF"
GREEN = "#16A34A"
RED = "#DC2626"
LIGHT_BLUE = "#EFF6FF"


# =========================================================
# FUNCTIONS
# =========================================================

def load_attendance():

    for row in table.get_children():
        table.delete(row)

    search_name = name_entry.get().strip()
    search_date = date_entry.get().strip()

    db_path = os.path.join(
        BASE_DIR,
        "attendance.db"
    )

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
        SELECT name, date, time
        FROM attendance
        WHERE 1=1
    """

    values = []

    if search_name:
        query += " AND name LIKE ?"
        values.append("%" + search_name + "%")

    if search_date:
        query += " AND date = ?"
        values.append(search_date)

    query += " ORDER BY date DESC, time DESC"

    cursor.execute(
        query,
        values
    )

    records = cursor.fetchall()

    for record in records:
        table.insert(
            "",
            tk.END,
            values=record
        )

    conn.close()

    update_statistics()


def update_statistics():

    db_path = os.path.join(
        BASE_DIR,
        "attendance.db"
    )

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM students"
    )

    total_students = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM attendance"
    )

    total_records = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(DISTINCT date) FROM attendance"
    )

    total_days = cursor.fetchone()[0]

    students_count.config(
        text=str(total_students)
    )

    records_count.config(
        text=str(total_records)
    )

    days_count.config(
        text=str(total_days)
    )

    conn.close()


def clear_search():

    name_entry.delete(
        0,
        tk.END
    )

    date_entry.delete(
        0,
        tk.END
    )

    load_attendance()


def open_register():

    path = os.path.join(
        BASE_DIR,
        "register.py"
    )

    subprocess.Popen(
        [sys.executable, path],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )


def open_students():

    path = os.path.join(
        BASE_DIR,
        "students.py"
    )

    subprocess.Popen(
        [sys.executable, path],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )


def start_recognition():

    path = os.path.join(
        BASE_DIR,
        "main.py"
    )

    subprocess.Popen(
        [sys.executable, path],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )


def open_reports():

    path = os.path.join(
        BASE_DIR,
        "reports.py"
    )

    subprocess.Popen(
        [sys.executable, path],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )


def export_report():

    path = os.path.join(
        BASE_DIR,
        "export_report.py"
    )

    subprocess.Popen(
        [sys.executable, path],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )


def logout():

    login_path = os.path.join(
        BASE_DIR,
        "login.py"
    )

    subprocess.Popen(
        [sys.executable, login_path],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    root.destroy()


# =========================================================
# WINDOW
# =========================================================

root = tk.Tk()

root.title(
    "Face Recognition Attendance System"
)

root.geometry(
    "1200x850"
)

root.minsize(
    1100,
    800
)

root.configure(
    bg=BG
)


# =========================================================
# STYLE
# =========================================================

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Treeview",
    background=WHITE,
    foreground=TEXT,
    rowheight=28,
    fieldbackground=WHITE,
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    background="#EAF0F8",
    foreground=DARK,
    font=("Arial", 10, "bold"),
    padding=7
)

style.map(
    "Treeview",
    background=[
        ("selected", "#DBEAFE")
    ],
    foreground=[
        ("selected", DARK)
    ]
)


# =========================================================
# HEADER
# =========================================================

header = tk.Frame(
    root,
    bg=WHITE,
    height=75
)

header.pack(
    fill="x"
)

header.pack_propagate(
    False
)


header_left = tk.Frame(
    header,
    bg=WHITE
)

header_left.pack(
    side="left",
    padx=30,
    pady=8
)


# =========================================================
# CU LOGO
# =========================================================

logo_path = os.path.join(
    BASE_DIR,
    "Chandigarh_University_logo.png"
)

try:

    logo_image = Image.open(
        logo_path
    )

    logo_image.thumbnail(
        (50, 50)
    )

    logo_photo = ImageTk.PhotoImage(
        logo_image
    )

    logo_label = tk.Label(
        header_left,
        image=logo_photo,
        bg=WHITE
    )

    logo_label.pack(
        side="left",
        padx=(0, 12)
    )

except Exception as e:

    logo_photo = None

    print(
        "Logo image error:",
        e
    )


# =========================================================
# HEADER TEXT
# =========================================================

header_text = tk.Frame(
    header_left,
    bg=WHITE
)

header_text.pack(
    side="left"
)


tk.Label(
    header_text,
    text="Face Recognition",
    bg=WHITE,
    fg=PRIMARY,
    font=("Arial", 20, "bold")
).pack(
    anchor="w"
)


tk.Label(
    header_text,
    text="Attendance Management System",
    bg=WHITE,
    fg="#64748B",
    font=("Arial", 10)
).pack(
    anchor="w"
)


# =========================================================
# ADMIN + LOGOUT
# =========================================================

admin_frame = tk.Frame(
    header,
    bg=WHITE
)

admin_frame.pack(
    side="right",
    padx=30
)


tk.Label(
    admin_frame,
    text="● Admin",
    bg=WHITE,
    fg=GREEN,
    font=("Arial", 10, "bold")
).pack(
    side="left",
    padx=15
)


tk.Button(
    admin_frame,
    text="Logout",
    command=logout,
    bg=WHITE,
    fg=RED,
    activebackground="#FEE2E2",
    relief="solid",
    bd=1,
    width=10,
    cursor="hand2"
).pack(
    side="left"
)


# =========================================================
# MAIN CONTENT
# =========================================================

main = tk.Frame(
    root,
    bg=BG
)

main.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=15
)


# =========================================================
# CU CAMPUS BANNER
# =========================================================

banner_frame = tk.Frame(
    main,
    bg=WHITE,
    height=110,
    highlightbackground=BORDER,
    highlightthickness=1
)

banner_frame.pack(
    fill="x",
    pady=(0, 12)
)

banner_frame.pack_propagate(
    False
)


background_path = os.path.join(
    BASE_DIR,
    "cu_background_dark.jpg"
)


try:

    campus_image = Image.open(
        background_path
    ).convert("RGB")

    campus_image = campus_image.resize(
        (1150, 110),
        Image.Resampling.LANCZOS
    )

    campus_photo = ImageTk.PhotoImage(
        campus_image
    )

    campus_label = tk.Label(
        banner_frame,
        image=campus_photo,
        bd=0
    )

    campus_label.place(
        x=0,
        y=0,
        relwidth=1,
        relheight=1
    )

except Exception as e:

    campus_photo = None

    print(
        "Background image error:",
        e
    )


# =========================================================
# BANNER TEXT
# =========================================================

banner_text = tk.Frame(
    banner_frame,
    bg=WHITE,
    highlightbackground=BORDER,
    highlightthickness=1
)

banner_text.place(
    x=20,
    y=18
)


tk.Label(
    banner_text,
    text="CHANDIGARH UNIVERSITY",
    bg=WHITE,
    fg=PRIMARY,
    font=("Arial", 15, "bold")
).pack(
    padx=15,
    pady=(7, 0)
)


tk.Label(
    banner_text,
    text="Face Recognition Attendance System",
    bg=WHITE,
    fg=DARK,
    font=("Arial", 9)
).pack(
    padx=15,
    pady=(0, 7)
)


# =========================================================
# TITLE
# =========================================================

title_frame = tk.Frame(
    main,
    bg=BG
)

title_frame.pack(
    fill="x",
    pady=(0, 8)
)


tk.Label(
    title_frame,
    text="Dashboard",
    bg=BG,
    fg=DARK,
    font=("Arial", 22, "bold")
).pack(
    side="left"
)


tk.Label(
    title_frame,
    text="  •  Attendance Overview",
    bg=BG,
    fg=PRIMARY,
    font=("Arial", 10, "bold")
).pack(
    side="left",
    pady=(6, 0)
)


# =========================================================
# STATISTICS
# =========================================================

stats_frame = tk.Frame(
    main,
    bg=BG
)

stats_frame.pack(
    fill="x",
    pady=(0, 10)
)


def create_card(
    parent,
    title,
    icon
):

    card = tk.Frame(
        parent,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1,
        height=75
    )

    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=5
    )

    card.pack_propagate(
        False
    )

    tk.Label(
        card,
        text=icon,
        bg=WHITE,
        fg=PRIMARY,
        font=("Arial", 15, "bold")
    ).pack(
        side="left",
        padx=(18, 8)
    )

    text_frame = tk.Frame(
        card,
        bg=WHITE
    )

    text_frame.pack(
        side="left",
        pady=8
    )

    tk.Label(
        text_frame,
        text=title,
        bg=WHITE,
        fg="#64748B",
        font=("Arial", 8, "bold")
    ).pack(
        anchor="w"
    )

    label = tk.Label(
        text_frame,
        text="0",
        bg=WHITE,
        fg=DARK,
        font=("Arial", 19, "bold")
    )

    label.pack(
        anchor="w"
    )

    return label


students_count = create_card(
    stats_frame,
    "TOTAL STUDENTS",
    "ST"
)


records_count = create_card(
    stats_frame,
    "ATTENDANCE RECORDS",
    "AT"
)


days_count = create_card(
    stats_frame,
    "ATTENDANCE DAYS",
    "DY"
)


# =========================================================
# SEARCH
# =========================================================

search_box = tk.Frame(
    main,
    bg=WHITE,
    highlightbackground=BORDER,
    highlightthickness=1,
    height=55
)

search_box.pack(
    fill="x",
    pady=(0, 10)
)

search_box.pack_propagate(
    False
)


tk.Label(
    search_box,
    text="Search Attendance",
    bg=WHITE,
    fg=DARK,
    font=("Arial", 11, "bold")
).pack(
    side="left",
    padx=18
)


tk.Label(
    search_box,
    text="Student:",
    bg=WHITE,
    fg=TEXT
).pack(
    side="left",
    padx=(10, 4)
)


name_entry = tk.Entry(
    search_box,
    width=18,
    relief="solid",
    bd=1
)

name_entry.pack(
    side="left",
    padx=4
)


tk.Label(
    search_box,
    text="Date:",
    bg=WHITE,
    fg=TEXT
).pack(
    side="left",
    padx=(15, 4)
)


date_entry = tk.Entry(
    search_box,
    width=14,
    relief="solid",
    bd=1
)

date_entry.pack(
    side="left",
    padx=4
)


tk.Button(
    search_box,
    text="Search",
    command=load_attendance,
    bg=PRIMARY,
    fg=WHITE,
    activebackground=PRIMARY_DARK,
    relief="flat",
    width=9,
    cursor="hand2"
).pack(
    side="left",
    padx=5
)


tk.Button(
    search_box,
    text="Clear",
    command=clear_search,
    bg="#E2E8F0",
    fg=DARK,
    activebackground="#CBD5E1",
    relief="flat",
    width=9,
    cursor="hand2"
).pack(
    side="left",
    padx=5
)


# =========================================================
# ATTENDANCE TABLE
# =========================================================

table_frame = tk.Frame(
    main,
    bg=WHITE,
    highlightbackground=BORDER,
    highlightthickness=1,
    height=150
)

table_frame.pack(
    fill="x",
    pady=(0, 10)
)

table_frame.pack_propagate(
    False
)


columns = (
    "Name",
    "Date",
    "Time"
)


table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)


table.heading(
    "Name",
    text="STUDENT NAME"
)

table.heading(
    "Date",
    text="DATE"
)

table.heading(
    "Time",
    text="TIME"
)


table.column(
    "Name",
    width=450
)

table.column(
    "Date",
    width=300
)

table.column(
    "Time",
    width=300
)


table.pack(
    fill="both",
    expand=True,
    padx=8,
    pady=8
)


# =========================================================
# BUTTON AREA
# =========================================================

button_area = tk.Frame(
    main,
    bg=BG
)

button_area.pack(
    fill="x",
    pady=(2, 0)
)


# Equal columns for centering

button_area.grid_columnconfigure(
    0,
    weight=1
)

button_area.grid_columnconfigure(
    1,
    weight=1
)

button_area.grid_columnconfigure(
    2,
    weight=1
)


def action_button(
    text,
    command
):

    return tk.Button(
        button_area,
        text=text,
        command=command,
        bg=WHITE,
        fg=DARK,
        activebackground=LIGHT_BLUE,
        activeforeground=PRIMARY,
        relief="solid",
        bd=1,
        width=20,
        height=2,
        cursor="hand2",
        font=("Arial", 9, "bold")
    )


# =========================================================
# BUTTON ROW 1
# =========================================================

action_button(
    "Register Student",
    open_register
).grid(
    row=0,
    column=0,
    padx=8,
    pady=4
)


action_button(
    "Student Management",
    open_students
).grid(
    row=0,
    column=1,
    padx=8,
    pady=4
)


action_button(
    "Face Recognition",
    start_recognition
).grid(
    row=0,
    column=2,
    padx=8,
    pady=4
)


# =========================================================
# BUTTON ROW 2
# =========================================================

action_button(
    "Attendance Reports",
    open_reports
).grid(
    row=1,
    column=0,
    padx=8,
    pady=4
)


action_button(
    "Export Report",
    export_report
).grid(
    row=1,
    column=1,
    padx=8,
    pady=4
)


action_button(
    "Refresh",
    load_attendance
).grid(
    row=1,
    column=2,
    padx=8,
    pady=4
)


# =========================================================
# FOOTER
# =========================================================

tk.Label(
    main,
    text="Chandigarh University • Face Recognition Attendance System",
    bg=BG,
    fg="#94A3B8",
    font=("Arial", 8)
).pack(
    pady=(5, 0)
)


# =========================================================
# START
# =========================================================

load_attendance()

root.mainloop()