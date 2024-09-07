import sqlite3

from databaseI import DbInterface

from models.user import UserBase


class Sql(DbInterface):
    """SQL Connector"""

    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    async def user_exists(self, user: UserBase) -> bool:
        try:
            self.cursor.execute(
                "SELECT 1 FROM users WHERE username = ?", (user.username,)
            )
        except Exception as err:
            return None, err
        return bool(self.cursor.fetchone()), None

    async def register_user(self, user: UserBase) -> Exception:
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (user.username, user.password),
            )
            self.conn.commit()
        except Exception as err:
            return err
        return None
