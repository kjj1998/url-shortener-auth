"""APIs for the URL shortener authentication service."""

import os

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from url_shortener_auth.repository.auth_repository import AuthRepository
from url_shortener_auth.auth_service.auth_service import AuthService
from url_shortener_auth.web.api.schemas import Token, UserReceive, UserReturn, TokenData
from url_shortener_auth.repository.unit_of_work import UnitOfWork
from url_shortener_auth.auth_service.auth import User


ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserReturn
)
def register_user(user: UserReceive) -> UserReturn:
    """Register a new user"""

    with UnitOfWork() as unit_of_work:
        repo: AuthRepository = AuthRepository(unit_of_work.session)
        auth_service: AuthService = AuthService(repo)

        if auth_service.get_user(repo, user.username) is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already registered",
            )

        user = auth_service.create_user(repo, user.username, user.password)

        return UserReturn(
            username=user.username,
            created_at=user.created_at,
            last_login_at=user.last_login_at,
        )

@router.get("/users/me/", response_model=UserReturn)
async def get_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """Get the user details based on information stored in the token"""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), os.getenv("ALGORITHM"))
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as exc:
        raise credentials_exception from exc

    with UnitOfWork() as unit_of_work:
        repo: AuthRepository = AuthRepository(unit_of_work.session)
        auth_service: AuthService = AuthService(repo)

        user = auth_service.get_user(repo, token_data.username)

    if user is None:
        raise credentials_exception
    return UserReturn(
        username=user.username,
        created_at=user.created_at,
        last_login_at=user.last_login_at,
    )


@router.get("/health/storage_health", status_code=status.HTTP_200_OK)
def storage_health_check():
    """Health check for in-memory and persistence storage"""
    with UnitOfWork() as unit_of_work:
        repo: AuthRepository = AuthRepository(unit_of_work.session)
        health_check = {
            "Database Status": "Online" if repo.check_health() else "Offline",
        }
        unit_of_work.commit()

    return health_check
