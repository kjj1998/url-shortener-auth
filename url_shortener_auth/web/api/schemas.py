"""Schemas for the API"""

from datetime import datetime
from pydantic import BaseModel


class Token(BaseModel):
    """Schema for the JWT token response"""

    access_token: str
    token_type: str


class User(BaseModel):
    """Schema for the user"""

    username: str


class UserReceive(User):
    """Schema for the user object received from the client"""

    password: str


class UserReturn(UserReceive):
    """Schema for the user object to return to the client"""

    created_at: datetime
    last_login_at: datetime
