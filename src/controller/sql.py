import sqlite3

from controller.databaseI import DbInterface
from models.user import UserBase
import bcrypt


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

    async def create_user(self, user: UserBase) -> Exception:
        # Create a password hash to store in DB
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), salt)
        user.password = hashed_password
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (user.username, user.password),
            )
            self.conn.commit()
        except Exception as err:
            return err
        return None

    async def user_login(self, user: UserBase):
        try:
            # Get the stored password hash for the user
            self.cursor.execute(
                "SELECT password FROM users WHERE username = ?",
                (user.username,)
            )
            result = self.cursor.fetchone()
            
            if not result:
                return False, "User not found"
            
            stored_password = result[0]
            
            # Verify the password
            if bcrypt.checkpw(user.password.encode('utf-8'), stored_password):
                return True, None
            return False, "Invalid password"
            
        except Exception as err:
            return False, str(err)

        
