

import sqlite3
import os
from datetime import datetime

# Path to the SQLite database file
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "leads.db")


def get_connection():
    """Open a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # access columns by name
    return conn


def init_db():
    """Create the 'user' table if it doesn't exist yet."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            service TEXT,
            message TEXT,
            status TEXT NOT NULL DEFAULT 'Yeni',
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_user(name, email, phone, service, message):
    """Save a new contact form submission."""
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO user (name, email, phone, service, message, status, created_at)
        VALUES (?, ?, ?, ?, ?, 'Yeni', ?)
        """,
        (name, email, phone, service, message, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_all_users():
    """Return every user, newest first."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM user ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_users_by_status(status):
    """Return users filtered by status."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM user WHERE status = ? ORDER BY created_at DESC", (status,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def update_user_status(user_id, new_status):
    """Change the status of one user."""
    conn = get_connection()
    conn.execute("UPDATE user SET status = ? WHERE id = ?", (new_status, user_id))
    conn.commit()
    conn.close()


def count_today_users():
    """Count users received today."""
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_connection()
    row = conn.execute(
        "SELECT COUNT(*) as c FROM user WHERE created_at LIKE ?", (f"{today}%",)
    ).fetchone()
    conn.close()
    return row["c"]


def count_total_users():
    """Count all users."""
    conn = get_connection()
    row = conn.execute("SELECT COUNT(*) as c FROM user").fetchone()
    conn.close()
    return row["c"]
