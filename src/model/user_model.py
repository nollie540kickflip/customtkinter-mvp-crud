import sqlite3
from contextlib import closing


class UserModel:
    def __init__(self, db_path: str = "app.db") -> None:
        self.db_path = db_path

    def create(self, name: str, email: str, age: int | None) -> None:
        with closing(sqlite3.connect(self.db_path)) as conn, conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                (name, email, age),
            )

    def get_all(self) -> list[tuple]:
        with closing(sqlite3.connect(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email, age FROM users ORDER BY id DESC")
            return cursor.fetchall()

    def update(self, user_id: int, name: str, email: str, age: int | None) -> None:
        with closing(sqlite3.connect(self.db_path)) as conn, conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET name = ?, email = ?, age = ? WHERE id = ?",
                (name, email, age, user_id),
            )

    def delete(self, user_id: int) -> None:
        with closing(sqlite3.connect(self.db_path)) as conn, conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
