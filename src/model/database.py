import sqlite3
from contextlib import closing


def init_db(db_path: str = "app.db") -> None:
    """
    指定されたパスにSQLiteデータベースを初期化し、
    usersテーブルが存在しない場合は作成します。
    """
    with (
        closing(sqlite3.connect(db_path)) as conn,
        conn,
    ):  # 成功時には自動コミット、例外発生時にはロールバックされます
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
