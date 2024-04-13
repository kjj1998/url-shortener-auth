"""User repository"""

from datetime import datetime, timezone

from sqlalchemy.exc import DatabaseError
from sqlalchemy.sql import text
from sqlalchemy import select

from url_shortener_auth.repository.models import UserModel
from url_shortener_auth.auth_service.auth import User


class AuthRepository:
    """Authentication repository"""

    def __init__(self, session):
        self.session = session

    def get_user_by_username(self, username) -> User:
        """Get the user by username"""

        user_model: UserModel = (
            self.session.query(UserModel).filter(UserModel.username == username).first()
        )

        if user_model:
            return User(**user_model.dict())

        return None

    def create_user(self, username, password) -> User:
        """Create a new user"""

        record = UserModel(username=username, password=password)
        self.session.add(record)

        try:
            self.session.commit()
        except DatabaseError as error:
            self.session.rollback()
            print("Database:", error)

        return User(**record.dict())

    def update_user_last_login(self, username):
        """Update the last login time of the user"""

        user_model: UserModel = self.session.execute(
            select(UserModel).filter_by(username=username)
        ).scalar_one()

        user_model.last_login_at = datetime.now(timezone.utc)

        try:
            self.session.commit()
        except DatabaseError as error:
            self.session.rollback()
            print("Database:", error)

    def check_health(self):
        """Check the health of the database."""
        try:
            self.session.execute(text("SELECT 1"))
            return True
        except DatabaseError as e:
            print("Database:", e)
            return False
