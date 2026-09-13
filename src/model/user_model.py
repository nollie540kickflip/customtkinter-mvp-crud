import sqlite3
from contextlib import closing


class UserModel:
    """
    ユーザー情報のデータベース操作（CRUD）を担当するモデルクラス。
    """

    def __init__(self, db_path: str = "app.db") -> None:
        """
        UserModelを初期化します。

        Args:
            db_path (str): SQLiteデータベースファイルのパス
        """
        self.db_path = db_path

    def create(self, name: str, email: str, age: int | None) -> None:
        """
        新しいユーザーをデータベースに追加します。

        Args:
            name (str): ユーザー名
            email (str): メールアドレス
            age (int | None): 年齢（任意の整数またはNone）
        """
        with closing(sqlite3.connect(self.db_path)) as conn, conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                (name, email, age),
            )

    def get_all(self) -> list[tuple]:
        """
        すべてのユーザー情報を取得します。

        Returns:
            list[tuple]: ユーザー情報のタプルのリスト。IDの降順でソートされます。
        """
        with closing(sqlite3.connect(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email, age FROM users ORDER BY id DESC")
            return cursor.fetchall()

    def update(self, user_id: int, name: str, email: str, age: int | None) -> None:
        """
        指定されたIDのユーザー情報を更新します。

        Args:
            user_id (int): 更新対象のユーザーID
            name (str): 新しいユーザー名
            email (str): 新しいメールアドレス
            age (int | None): 新しい年齢
        """
        with closing(sqlite3.connect(self.db_path)) as conn, conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET name = ?, email = ?, age = ? WHERE id = ?",
                (name, email, age, user_id),
            )

    def delete(self, user_id: int) -> None:
        """
        指定されたIDのユーザーをデータベースから削除します。

        Args:
            user_id (int): 削除対象のユーザーID
        """
        with closing(sqlite3.connect(self.db_path)) as conn, conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
