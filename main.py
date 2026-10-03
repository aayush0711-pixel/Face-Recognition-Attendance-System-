import cv2
import face_recognition
import os
import csv
import sqlite3
from datetime import datetime

# Folder containing student photos
path = "ImagesAttendance"

known_encodings = []
classNames = []

# Load all student images
for filename in os.listdir(path):

    if filename.lower().endswith((".jpg", ".jpeg", ".png")):

        image_path = os.path.join(path, filename)

        image = face_recognition.load_image_file(image_path)

        encodings = face_recognition.face_encodings(image)

        if len(encodings) == 0:
            print("No face found in:", filename)
            continue

        known_encodings.append(encodings[0])

        name = os.path.splitext(filename)[0]
        classNames.append(name)

print("Students loaded:", classNames)


# Mark attendance in SQLite database
def mark_database_attendance(name):

    today = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")

    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO attendance (name, date, time)
            VALUES (?, ?, ?)
            """,
            (name, today, current_time)
        )

        conn.commit()
        print("Database attendance marked:", name)

    except sqlite3.IntegrityError:
        # Attendance already marked today
        pass

    conn.close()


# Mark attendance in CSV and database
def mark_attendance(name):

    today = datetime.now().strftime("%Y-%m-%d")

    file_exists = os.path.exists("Attendance.csv")

    already_marked = False

    if file_exists:

        with open("Attendance.csv", "r", newline="") as file:

            reader = csv.reader(file)

            for row in reader:

                if len(row) >= 2:

                    if row[0] == name and row[1] == today:
                        already_marked = True
                        break

    if not already_marked:

        now = datetime.now()
        time = now.strftime("%H:%M:%S")

        with open("Attendance.csv", "a", newline="") as file:

            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(["Name", "Date", "Time"])

            writer.writerow([name, today, time])

        print("CSV attendance marked:", name)

    # Save attendance to database
    mark_database_attendance(name)


# Start webcam
video = cv2.VideoCapture(0)

if not video.isOpened():

    print("Cannot open webcam!")
    exit()


while True:

    ret, frame = video.read()

    if not ret:

        print("Cannot read webcam!")
        break

    # Convert webcam frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces
    face_locations = face_recognition.face_locations(rgb_frame)

    face_encodings = face_recognition.face_encodings(
        rgb_frame, face_locations
    )

    # Recognize each face
    for face_encoding, location in zip(
        face_encodings, face_locations
    ):

        matches = face_recognition.compare_faces(
            known_encodings,
            face_encoding,
            tolerance=0.5
        )

        name = "Unknown"

        if True in matches:

            match_index = matches.index(True)

            name = classNames[match_index]

            mark_attendance(name)

        top, right, bottom, left = location

        # Green rectangle for recognized faces
        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)

        cv2.rectangle(
            frame,
            (left, top),
            (right, bottom),
            color,
            2
        )

        cv2.putText(
            frame,
            name,
            (left, top - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

    cv2.imshow("Face Recognition Attendance", frame)

    # Press Q to close webcam
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


video.release()
cv2.destroyAllWindows()