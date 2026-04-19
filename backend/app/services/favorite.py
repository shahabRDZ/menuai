from uuid import UUID

from sqlalchemy.exc import IntegrityError

from app.exceptions import NotFound
from app.models import Favorite, User
from app.repositories import DishRepository, FavoriteRepository
from app.schemas.dish import DishResponse
from app.services.menu import MenuService


class FavoriteService:
    def __init__(self, dishes: DishRepository, favorites: FavoriteRepository) -> None:
        self.dishes = dishes
        self.favorites = favorites

    async def add(self, user: User, dish_id: UUID) -> None:
        dish = await self.dishes.get_owned_by_user(dish_id, user.id)
        if dish is None:
            raise NotFound("Dish not found")

        favorite = Favorite(user_id=user.id, dish_id=dish.id)
        try:
            await self.favorites.add(favorite)
            await self.favorites.session.commit()
        except IntegrityError:
            await self.favorites.session.rollback()

    async def remove(self, user: User, dish_id: UUID) -> None:
        favorite = await self.favorites.get_by_user_dish(user.id, dish_id)
        if favorite is None:
            return
        await self.favorites.delete(favorite)
        await self.favorites.session.commit()

    async def list_for_user(self, user: User) -> list[DishResponse]:
        dishes = await self.favorites.list_dishes_for_user(user.id)
        return [MenuService._dish_to_response(d, is_favorite=True) for d in dishes]
