# Handles database connections and lead storage and retrieval.

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
    conn = None
    try:
        conn = get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                service TEXT,
                message TEXT,
                status TEXT NOT NULL DEFAULT 'New',
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"[database] Failed to create table: {e}")
    finally:
        if conn:
            conn.close()


def add_user(name, email, phone, service, message):
    """Save a new contact form submission. Returns True on success, False on failure."""
    conn = None
    try:
        conn = get_connection()
        conn.execute(
            """
            INSERT INTO user (name, email, phone, service, message, status, created_at)
            VALUES (?, ?, ?, ?, ?, 'New', ?)
            """,
            (name, email, phone, service, message, datetime.now().isoformat())
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"[database] Failed to add user: {e}")
        return False
    finally:
        if conn:
            conn.close()


def get_all_users():
    """Return every user, newest first. Returns an empty list on failure."""
    conn = None
    try:
        conn = get_connection()
        rows = conn.execute("SELECT * FROM user ORDER BY created_at DESC").fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        print(f"[database] Failed to fetch users: {e}")
        return []
    finally:
        if conn:
            conn.close()


def get_users_by_status(status):
    """Return users filtered by status."""
    conn = None
    try:
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM user WHERE status = ? ORDER BY created_at DESC", (status,)
        ).fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        print(f"[database] Failed to fetch users by status: {e}")
        return []
    finally:
        if conn:
            conn.close()


def update_user_status(user_id, new_status):
    """Change the status of one user. Returns True on success, False on failure."""
    conn = None
    try:
        conn = get_connection()
        conn.execute("UPDATE user SET status = ? WHERE id = ?", (new_status, user_id))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"[database] Failed to update status: {e}")
        return False
    finally:
        if conn:
            conn.close()


def count_today_users():
    """Count users received today."""
    conn = None
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        conn = get_connection()
        row = conn.execute(
            "SELECT COUNT(*) as c FROM user WHERE created_at LIKE ?", (f"{today}%",)
        ).fetchone()
        return row["c"]
    except sqlite3.Error as e:
        print(f"[database] Failed to count today's users: {e}")
        return 0
    finally:
        if conn:
            conn.close()


def count_total_users():
    """Count all users."""
    conn = None
    try:
        conn = get_connection()
        row = conn.execute("SELECT COUNT(*) as c FROM user").fetchone()
        return row["c"]
    except sqlite3.Error as e:
        print(f"[database] Failed to count total users: {e}")
        return 0
    finally:
        if conn:
            conn.close()
