# Face Recognition Attendance System

A Python-based attendance management system that uses face recognition
and a webcam to identify registered students and record attendance
automatically.

## Table of Contents

-   [Project Overview](#project-overview)
-   [Purpose](#purpose)
-   [Objectives](#objectives)
-   [Features](#features)
-   [Technologies](#technologies)
-   [Project Structure](#project-structure)
-   [Requirements](#requirements)
-   [Installation](#installation)
-   [How to Run](#how-to-run)
-   [How It Works](#how-it-works)
-   [Attendance Output](#attendance-output)
-   [Current Status](#current-status)
-   [Troubleshooting](#troubleshooting)
-   [Future Improvements](#future-improvements)
-   [Author](#author)

## Project Overview

This project uses computer vision and facial recognition to automate
attendance. The webcam captures live video, detects faces, compares them
with registered student images, and stores attendance in a CSV file.

## Purpose

To reduce manual attendance work by recognizing registered students and
recording their attendance with date and time.

## Objectives

-   Capture live video through a webcam.
-   Detect and recognize registered faces.
-   Display the student's name.
-   Record attendance with date and time.
-   Prevent duplicate attendance for the same student on the same day.

## Features

-   Real-time face detection.
-   Recognition from stored student images.
-   Student name displayed for recognized faces.
-   Green rectangle for recognized faces and red for unknown faces.
-   Automatic CSV attendance recording.
-   Date and time logging.
-   Daily duplicate prevention.
-   Support for multiple registered images.

## Technologies

  Technology           Purpose
  -------------------- -----------------------------
  Python               Main programming language
  OpenCV               Webcam and video processing
  face_recognition     Face encoding and matching
  NumPy                Numerical processing
  CSV                  Attendance storage
  Visual Studio Code   Development environment

## Project Structure

``` text
FaceRecognitionAttendance/
├── main.py
├── Attendance.csv
├── ImagesAttendance/
│   ├── Aayush.jpg
│   └── Student2.jpg
├── requirements.txt
├── .gitignore
└── venv/  (local environment; do not upload)
```

## Requirements

-   Windows 10/11
-   Python 3.10 or compatible version
-   Webcam
-   Git
-   Internet connection for installation

## Installation

### 1. Install Python and Git

Install Python from https://www.python.org/downloads/ and Git from
https://git-scm.com/downloads. Verify:

``` cmd
python --version
git --version
```

### 2. Clone the repository

``` cmd
git clone https://github.com/aayush0711-pixel/Face-Recognition-Attendance-System-.git
cd Face-Recognition-Attendance-System-
```

### 3. Create and activate a virtual environment

``` cmd
python -m venv venv
venv\Scripts\activate
```

### 4. Install dependencies

``` cmd
python -m pip install --upgrade pip
python -m pip install opencv-python numpy face-recognition
```

**Note:** `face_recognition` depends on `dlib`. On Windows, installation
may require compatible build tools or a compatible prebuilt package.

### 5. Add student photographs

Place clear, front-facing JPG images with one face each inside
`ImagesAttendance/`. The image filename (without extension) is used as
the displayed name.

Example:

``` text
ImagesAttendance/
├── Aayush.jpg
└── Student2.jpg
```

## How to Run

1.  Open CMD in the project directory.

2.  Activate the environment:

    ``` cmd
    venv\Scripts\activate
    ```

3.  Run the application:

    ``` cmd
    python main.py
    ```

4.  Look at the webcam. A recognized student's name should appear, and
    attendance is saved according to the program's logic.

5.  Press **Q** in the webcam window to exit, if supported by the
    program.

## How It Works

1.  Images are loaded from `ImagesAttendance/`.
2.  The program creates face encodings from the images.
3.  The webcam captures live frames.
4.  Faces are detected and compared with registered encodings.
5.  The matching name is displayed.
6.  Attendance is written to `Attendance.csv` with date and time.
7.  Existing records are checked to avoid duplicate entries for the same
    student and date.

## Attendance Output

Attendance is stored in `Attendance.csv`. Example format:

  Name       Date         Time
  ---------- ------------ ----------
  Aayush     YYYY-MM-DD   HH:MM:SS
  Student2   YYYY-MM-DD   HH:MM:SS

These are sample values. Open the CSV file in Excel or another
spreadsheet application.

## Current Status

-   Python environment and libraries configured.
-   Webcam-based face detection and recognition tested.
-   Registered face recognition working.
-   CSV attendance recording implemented.
-   Daily duplicate prevention implemented.
-   Two student JPG images added for multi-student testing.

## Troubleshooting

### Python command not found

Install Python and ensure it is added to PATH. Reopen CMD and run
`python --version`.

### ModuleNotFoundError

Activate the virtual environment and install the missing dependency
using pip.

### Webcam does not open

Check camera connection and Windows camera permissions. Close other apps
using the camera.

### Face is not recognized

Use a clear, front-facing image and confirm it is saved in
`ImagesAttendance/` with a supported extension.

### dlib installation fails

Check Python compatibility and install the required Windows build tools
or use a compatible installation method.

### Attendance is not saved

Check write permissions, the CSV path, and whether the student already
has an entry for that date.

## Future Improvements

-   Test with more registered students.
-   Add a graphical user interface.
-   Generate date-wise attendance reports.
-   Add student registration and management.
-   Integrate a database such as MySQL or MongoDB.
-   Export reports to Excel or PDF.

## Author

**Aayush Ranjan**\
Project: Face Recognition Attendance System\
GitHub: [aayush0711-pixel](https://github.com/aayush0711-pixel)

## License

Created for educational and learning purposes. Add a license file if you
plan to distribute or reuse the project under specific terms.
