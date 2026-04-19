from app.repositories.dish import DishRepository
from app.repositories.favorite import FavoriteRepository
from app.repositories.menu_scan import MenuScanRepository
from app.repositories.user import UserRepository

__all__ = [
    "UserRepository",
    "MenuScanRepository",
    "DishRepository",
    "FavoriteRepository",
]
