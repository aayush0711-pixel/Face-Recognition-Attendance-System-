import cv2
import os
import re
import sqlite3
from tkinter import Tk, filedialog

folder = "ImagesAttendance"
os.makedirs(folder, exist_ok=True)


# Save student information in database
def save_student(name, path):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR REPLACE INTO students (name, image_path) VALUES (?, ?)",
        (name, path)
    )

    conn.commit()
    conn.close()


# Get student name
name = input("Enter student name: ").strip()

if not name:
    print("Name cannot be empty.")
    exit()

name = re.sub(r'[<>:"/\\|?*]', "_", name)


print("1. Register using Webcam")
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

            save_student(name, path)

            print("Photo saved:", path)
            print("Student saved in database!")

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

            path = os.path.join(folder, name + ".jpg")

            cv2.imwrite(path, image)

            save_student(name, path)

            print("Photo saved:", path)
            print("Student saved in database!")

        else:
            print("Invalid image.")

    else:
        print("No photo selected.")


else:
    print("Invalid choice.")