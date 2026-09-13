import sqlite3
from contextlib import closing


def init_db(db_path: str = "app.db") -> None:
    """Initialize the database and create tables if they do not exist."""
    with closing(sqlite3.connect(db_path)) as conn:
        with conn:  # Automatically commits on success, rollbacks on exception
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    age INTEGER
                )
                """
            )
