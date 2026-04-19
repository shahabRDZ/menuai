from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.deps import AuthServiceDep, CurrentUser
from app.models import User
from app.schemas.auth import RegisterRequest, TokenResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, auth: AuthServiceDep) -> TokenResponse:
    _, token = await auth.register(payload)
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth: AuthServiceDep,
) -> TokenResponse:
    _, token = await auth.login(email=form.username, password=form.password)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
async def me(user: CurrentUser) -> User:
    return user
