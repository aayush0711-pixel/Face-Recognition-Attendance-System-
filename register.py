import cv2
import os
import re
import sqlite3
from tkinter import Tk, filedialog

folder = "ImagesAttendance"
os.makedirs(folder, exist_ok=True)


def save_student(name, username, password, path):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO students (name, image_path, username, password)
            VALUES (?, ?, ?, ?)
            """,
            (name, path, username, password)
        )

        conn.commit()
        print("Student saved in database!")

    except sqlite3.IntegrityError:
        print("Username already exists!")

    conn.close()


# Student name
name = input("Enter student name: ").strip()

if not name:
    print("Name cannot be empty.")
    exit()

name = re.sub(r'[<>:"/\\|?*]', "_", name)


# Username
username = input("Create username: ").strip()

if not username:
    print("Username cannot be empty.")
    exit()


# Password
password = input("Create password: ").strip()

if not password:
    print("Password cannot be empty.")
    exit()


print("\n1. Register using Webcam")
print("2. Register using Photo Upload")

choice = input("Choose option: ")


# =========================
# WEBCAM REGISTRATION
# =========================

if choice == "1":

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera not found.")
        exit()

    print("Press S to capture photo, Q to quit.")

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        cv2.imshow("Student Registration", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):

            path = os.path.join(folder, name + ".jpg")

            cv2.imwrite(path, frame)

            save_student(
                name,
                username,
                password,
                path
            )

            print("Photo saved:", path)

            break

        elif key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


# =========================
# PHOTO UPLOAD
# =========================

elif choice == "2":

    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select Student Photo",
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png")
        ]
    )

    root.destroy()

    if file_path:

        image = cv2.imread(file_path)

        if image is not None:

            path = os.path.join(
                folder,
                name + ".jpg"
            )

            cv2.imwrite(path, image)

            save_student(
                name,
                username,
                password,
                path
            )

            print("Photo saved:", path)

        else:
            print("Invalid image.")

    else:
        print("No photo selected.")


else:
    print("Invalid choice.")