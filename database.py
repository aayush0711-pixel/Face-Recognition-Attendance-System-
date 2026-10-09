import sqlite3

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

# Create students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    image_path TEXT
)
""")

# Add username column if it does not exist
try:
    cursor.execute("ALTER TABLE students ADD COLUMN username TEXT")
except sqlite3.OperationalError:
    pass

# Add password column if it does not exist
try:
    cursor.execute("ALTER TABLE students ADD COLUMN password TEXT")
except sqlite3.OperationalError:
    pass

# Create attendance table
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    date TEXT,
    time TEXT,
    UNIQUE(name, date)
)
""")

# Make username unique
cursor.execute("""
CREATE UNIQUE INDEX IF NOT EXISTS idx_students_username
ON students(username)
""")

conn.commit()
conn.close()

print("Database updated successfully!")