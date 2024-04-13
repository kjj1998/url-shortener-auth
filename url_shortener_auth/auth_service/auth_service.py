"""Authentication service for the URL shortener"""

import os

from datetime import timedelta, datetime, timezone
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
from url_shortener_auth.auth_service.auth import User
from url_shortener_auth.repository.auth_repository import AuthRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
parent_directory_path = os.path.dirname(os.getcwd())
dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path)


class AuthService:
    """Service to authenticate users"""

    def __init__(self, user_service):
        self.user_service = user_service

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify the plain password against the hashed password"""

        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Get the hashed password"""

        return pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        """Create the access token"""

        to_encode: dict = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), os.getenv("HS256"))
        return encoded_jwt

    def authenticate_user(self, repo: AuthRepository, username:str, password: str) -> User | bool:
        """Authenticate the user"""

        user: User = repo.get_user_by_username(username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False

        return user
