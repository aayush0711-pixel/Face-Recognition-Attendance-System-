import sqlite3
import csv
from tkinter import Tk, filedialog, messagebox


def export_report():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, date, time
        FROM attendance
        ORDER BY date DESC, time DESC
    """)

    records = cursor.fetchall()
    conn.close()

    if not records:
        messagebox.showwarning(
            "No Data",
            "No attendance records found."
        )
        return

    root = Tk()
    root.withdraw()

    file_path = filedialog.asksaveasfilename(
        title="Save Attendance Report",
        defaultextension=".csv",
        filetypes=[
            ("CSV files", "*.csv")
        ]
    )

    root.destroy()

    if file_path:
        with open(
            file_path,
            "w",
            newline=""
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Student Name",
                "Date",
                "Time"
            ])

            writer.writerows(records)

        messagebox.showinfo(
            "Success",
            "Attendance report exported successfully!"
        )


export_report()