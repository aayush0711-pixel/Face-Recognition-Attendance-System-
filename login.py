import tkinter as tk
from tkinter import messagebox
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

WHITE = "#FFFFFF"
PRIMARY = "#2563EB"
PRIMARY_DARK = "#1D4ED8"
DARK = "#172033"
TEXT = "#475569"
RED = "#DC2626"


# =========================================================
# LOGIN FUNCTION
# =========================================================

def login():

    username = username_entry.get().strip()
    password = password_entry.get()

    if username == "admin" and password == "admin123":

        messagebox.showinfo(
            "Login",
            "Login successful!"
        )

        dashboard_path = os.path.join(
            BASE_DIR,
            "dashboard.py"
        )

        subprocess.Popen(
            [sys.executable, dashboard_path],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )

        root.destroy()

    else:

        messagebox.showerror(
            "Login Failed",
            "Invalid username or password!"
        )


# =========================================================
# SHOW / HIDE PASSWORD
# =========================================================

def toggle_password():

    if password_entry.cget("show") == "*":

        password_entry.config(
            show=""
        )

        show_button.config(
            text="Hide"
        )

    else:

        password_entry.config(
            show="*"
        )

        show_button.config(
            text="Show"
        )


# =========================================================
# WINDOW
# =========================================================

root = tk.Tk()

root.title(
    "Face Recognition Attendance - Login"
)

root.geometry(
    "1100x700"
)

root.resizable(
    False,
    False
)


# =========================================================
# BACKGROUND IMAGE
# =========================================================

background_path = os.path.join(
    BASE_DIR,
    "cu_background_dark.jpg"
)

try:

    background_image = Image.open(
        background_path
    ).convert("RGB")

    background_image = background_image.resize(
        (1100, 700),
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

    print(
        "Background image error:",
        e
    )

    root.configure(
        bg=DARK
    )


# =========================================================
# DARK OVERLAY
# =========================================================

overlay = tk.Frame(
    root,
    bg="#172033"
)

overlay.place(
    x=0,
    y=0,
    relwidth=1,
    relheight=1
)

# Make overlay slightly transparent
try:

    overlay.configure(
        bg="#172033"
    )

except:
    pass


# =========================================================
# LOGIN CARD
# =========================================================

login_card = tk.Frame(
    root,
    bg=WHITE,
    width=420,
    height=560
)

login_card.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)

login_card.pack_propagate(
    False
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
        (90, 90)
    )

    logo_photo = ImageTk.PhotoImage(
        logo_image
    )

    logo_label = tk.Label(
        login_card,
        image=logo_photo,
        bg=WHITE
    )

    logo_label.pack(
        pady=(25, 8)
    )

except Exception as e:

    print(
        "Logo error:",
        e
    )


# =========================================================
# TITLE
# =========================================================

tk.Label(
    login_card,
    text="Welcome Back",
    bg=WHITE,
    fg=DARK,
    font=("Arial", 24, "bold")
).pack(
    pady=(5, 3)
)


tk.Label(
    login_card,
    text="Face Recognition Attendance System",
    bg=WHITE,
    fg="#64748B",
    font=("Arial", 10)
).pack(
    pady=(0, 25)
)


# =========================================================
# USERNAME
# =========================================================

tk.Label(
    login_card,
    text="Username",
    bg=WHITE,
    fg=TEXT,
    font=("Arial", 10, "bold")
).pack(
    anchor="w",
    padx=45
)


username_entry = tk.Entry(
    login_card,
    font=("Arial", 11),
    relief="solid",
    bd=1
)

username_entry.pack(
    fill="x",
    padx=45,
    ipady=8,
    pady=(6, 18)
)


# =========================================================
# PASSWORD
# =========================================================

tk.Label(
    login_card,
    text="Password",
    bg=WHITE,
    fg=TEXT,
    font=("Arial", 10, "bold")
).pack(
    anchor="w",
    padx=45
)


password_frame = tk.Frame(
    login_card,
    bg=WHITE
)

password_frame.pack(
    fill="x",
    padx=45,
    pady=(6, 22)
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
    command=toggle_password,
    bg="#E2E8F0",
    fg=DARK,
    relief="flat",
    bd=0,
    width=6,
    cursor="hand2"
)

show_button.pack(
    side="right",
    padx=(5, 0),
    ipady=5
)


# =========================================================
# LOGIN BUTTON
# =========================================================

login_button = tk.Button(
    login_card,
    text="LOGIN",
    command=login,
    bg=PRIMARY,
    fg=WHITE,
    activebackground=PRIMARY_DARK,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    font=("Arial", 11, "bold"),
    cursor="hand2"
)

login_button.pack(
    fill="x",
    padx=45,
    ipady=10
)


# =========================================================
# DEFAULT LOGIN INFORMATION
# =========================================================

tk.Label(
    login_card,
    text="Admin Login",
    bg=WHITE,
    fg=PRIMARY,
    font=("Arial", 10, "bold")
).pack(
    pady=(22, 2)
)


tk.Label(
    login_card,
    text="Username: admin    Password: admin123",
    bg=WHITE,
    fg="#94A3B8",
    font=("Arial", 8)
).pack()


# =========================================================
# FOOTER
# =========================================================

tk.Label(
    login_card,
    text="Chandigarh University",
    bg=WHITE,
    fg="#CBD5E1",
    font=("Arial", 8)
).pack(
    side="bottom",
    pady=15
)


# =========================================================
# ENTER KEY
# =========================================================

root.bind(
    "<Return>",
    lambda event: login()
)


# =========================================================
# START
# =========================================================

root.mainloop()