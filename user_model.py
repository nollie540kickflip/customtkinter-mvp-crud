from database import get_connection


class UserModel:
    def create(self, name: str, email: str, age: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)", (name, email, age)
        )
        conn.commit()
        conn.close()

    def get_all(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, age FROM users ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def update(self, user_id: int, name: str, email: str, age: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET name = ?, email = ?, age = ? WHERE id = ?",
            (name, email, age, user_id),
        )
        conn.commit()
        conn.close()

    def delete(self, user_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
