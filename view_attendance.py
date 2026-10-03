import sqlite3

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

cursor.execute("SELECT name, date, time FROM attendance")

records = cursor.fetchall()

print("\n===== ATTENDANCE RECORDS =====\n")

if len(records) == 0:
    print("No attendance records found.")
else:
    for record in records:
        print("Name:", record[0])
        print("Date:", record[1])
        print("Time:", record[2])
        print("----------------------")

conn.close()