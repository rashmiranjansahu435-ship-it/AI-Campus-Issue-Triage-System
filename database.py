import sqlite3
import os

# Database file name
DB_NAME = "triage.db"

def get_connection():
    """
    Connect to SQLite database.
    SQLite is a simple file-based database built into Python.
    """
    conn = sqlite3.connect(DB_NAME)
    # Enable row dictionary access so columns can be accessed by name
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Initialize the database table if it doesn't already exist.
    Creates an 'issues' table to store student reports.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create table SQL statement
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            location TEXT NOT NULL,
            issue_text TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            department TEXT NOT NULL,
            suggested_action TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'OPEN',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def add_issue(student_name, location, issue_text, category, priority, department, suggested_action):
    """
    Save a new issue report into the database.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO issues (student_name, location, issue_text, category, priority, department, suggested_action, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'OPEN')
    ''', (student_name, location, issue_text, category, priority, department, suggested_action))
    
    conn.commit()
    inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id

def get_all_issues():
    """
    Fetch all issues from the database ordered by newest first.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM issues ORDER BY id DESC")
    rows = cursor.fetchall()
    
    # Convert sqlite3.Row objects to python dictionaries
    issues = [dict(row) for row in rows]
    conn.close()
    return issues

def update_issue_status(issue_id, new_status):
    """
    Update the status of an issue (e.g. OPEN -> IN PROGRESS -> RESOLVED).
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE issues SET status = ? WHERE id = ?", (new_status, issue_id))
    
    conn.commit()
    conn.close()

def get_issue_stats():
    """
    Calculate simple summary statistics for the dashboard.
    Returns total count, and counts for HIGH, MEDIUM, LOW priorities.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM issues")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM issues WHERE priority = 'HIGH'")
    high = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM issues WHERE priority = 'MEDIUM'")
    medium = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM issues WHERE priority = 'LOW'")
    low = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM issues WHERE status = 'OPEN'")
    open_count = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "total": total,
        "high": high,
        "medium": medium,
        "low": low,
        "open": open_count
    }

def seed_sample_data():
    """
    Add sample initial data if the database is empty.
    This helps demonstrate the app immediately without manual data entry.
    """
    issues = get_all_issues()
    if len(issues) == 0:
        add_issue(
            student_name="Rashmi Ranjan Sharma",
            location="Block C - Room 302",
            issue_text="The Wi-Fi in Block C has stopped working for everyone since morning.",
            category="Network",
            priority="HIGH",
            department="IT Support",
            suggested_action="Check Block C router and main switch configuration."
        )
        add_issue(
            student_name="Priya Patel",
            location="Lab 2",
            issue_text="The classroom projector isn't working and display is flickering.",
            category="Equipment",
            priority="MEDIUM",
            department="Maintenance",
            suggested_action="Inspect projector HDMI cable and lamp power supply."
        )
        add_issue(
            student_name="Amit Kumar",
            location="Library Floor 1",
            issue_text="Air conditioner is making a loud noise and blowing warm air.",
            category="Infrastructure",
            priority="MEDIUM",
            department="Facilities",
            suggested_action="Schedule AC servicing and filter cleaning."
        )
        add_issue(
            student_name="Neha Gupta",
            location="Hostel Building A",
            issue_text="Water leakage near the ground floor washroom sink.",
            category="Infrastructure",
            priority="HIGH",
            department="Facilities",
            suggested_action="Send plumbing team urgently to fix pipe leak."
        )

# Initialize DB when module is imported
init_db()
