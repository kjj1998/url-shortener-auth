"""APIs for the URL shortener authentication service."""


from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from url_shortener_auth.repository.auth_repository import AuthRepository
from url_shortener_auth.auth_service.auth_service import AuthService
from url_shortener_auth.web.api.schemas import Token, UserReceive, UserReturn
from url_shortener_auth.repository.unit_of_work import UnitOfWork
from url_shortener_auth.auth_service.auth import User


ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"

router = APIRouter()


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """Get the access token for the user"""

    with UnitOfWork() as unit_of_work:
        repo: AuthRepository = AuthRepository(unit_of_work.session)
        auth_service: AuthService = AuthService(repo)

        user: User = auth_service.authenticate_user(
            repo, form_data.username, form_data.password
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_service.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        return Token(access_token=access_token, token_type="bearer")


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserReturn)
def register_user(user: UserReceive) -> UserReturn:
    """Register a new user"""

    with UnitOfWork() as unit_of_work:
        repo: AuthRepository = AuthRepository(unit_of_work.session)
        auth_service: AuthService = AuthService(repo)

        if auth_service.get_user(repo, user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already registered",
            )

        user = auth_service.create_user(repo, user.username, user.password)

        return user.dict()

