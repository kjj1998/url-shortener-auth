"""This module contains the database models for the authentication service."""

from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserModel(Base): # pylint: disable=too-few-public-methods
    """User SQL model"""

    __tablename__ = "user"

    username = Column(String, primary_key=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(
        DateTime, nullable=False, default=datetime.now(timezone.utc)
    )
    last_login_at = Column(DateTime, nullable=True)

    def dict(self):
        """Render as dictionary"""
        return {
            "username": self.username,
            "created_at": self.created_at,
            "last_login_at": self.last_login_at,
        }
