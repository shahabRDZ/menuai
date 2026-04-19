from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import Unauthorized
from app.models import User
from app.repositories import (
    DishRepository,
    FavoriteRepository,
    MenuScanRepository,
    UserRepository,
)
from app.services.ai import MenuVisionService, menu_vision_service
from app.services.auth import AuthService
from app.services.favorite import FavoriteService
from app.services.menu import MenuService
from app.services.security import (
    PasswordHasher,
    TokenService,
    password_hasher,
    token_service,
)
from app.services.url_fetcher import UrlFetcher, url_fetcher

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=True)

DbSession = Annotated[AsyncSession, Depends(get_db)]


def get_password_hasher() -> PasswordHasher:
    return password_hasher


def get_token_service() -> TokenService:
    return token_service


def get_vision_service() -> MenuVisionService:
    return menu_vision_service


def get_url_fetcher() -> UrlFetcher:
    return url_fetcher


def get_user_repository(db: DbSession) -> UserRepository:
    return UserRepository(db)


def get_menu_scan_repository(db: DbSession) -> MenuScanRepository:
    return MenuScanRepository(db)


def get_dish_repository(db: DbSession) -> DishRepository:
    return DishRepository(db)


def get_favorite_repository(db: DbSession) -> FavoriteRepository:
    return FavoriteRepository(db)


def get_auth_service(
    users: Annotated[UserRepository, Depends(get_user_repository)],
    hasher: Annotated[PasswordHasher, Depends(get_password_hasher)],
    tokens: Annotated[TokenService, Depends(get_token_service)],
) -> AuthService:
    return AuthService(users=users, password_hasher=hasher, token_service=tokens)


def get_menu_service(
    scans: Annotated[MenuScanRepository, Depends(get_menu_scan_repository)],
    favorites: Annotated[FavoriteRepository, Depends(get_favorite_repository)],
    vision: Annotated[MenuVisionService, Depends(get_vision_service)],
    fetcher: Annotated[UrlFetcher, Depends(get_url_fetcher)],
) -> MenuService:
    return MenuService(scans=scans, favorites=favorites, vision=vision, url_fetcher=fetcher)


def get_favorite_service(
    dishes: Annotated[DishRepository, Depends(get_dish_repository)],
    favorites: Annotated[FavoriteRepository, Depends(get_favorite_repository)],
) -> FavoriteService:
    return FavoriteService(dishes=dishes, favorites=favorites)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    users: Annotated[UserRepository, Depends(get_user_repository)],
    tokens: Annotated[TokenService, Depends(get_token_service)],
) -> User:
    user_id = tokens.verify(token)
    if user_id is None:
        raise Unauthorized("Invalid or expired token")
    user = await users.get(user_id)
    if user is None:
        raise Unauthorized("User not found")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
MenuServiceDep = Annotated[MenuService, Depends(get_menu_service)]
FavoriteServiceDep = Annotated[FavoriteService, Depends(get_favorite_service)]
