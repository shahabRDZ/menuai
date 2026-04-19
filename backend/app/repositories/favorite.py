from uuid import UUID

from sqlalchemy import select

from app.models import Dish, Favorite
from app.repositories.base import BaseRepository


class FavoriteRepository(BaseRepository[Favorite]):
    model = Favorite

    async def get_by_user_dish(self, user_id: UUID, dish_id: UUID) -> Favorite | None:
        stmt = select(Favorite).where(Favorite.user_id == user_id, Favorite.dish_id == dish_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def favorite_ids_for_user(self, user_id: UUID, dish_ids: list[UUID]) -> set[UUID]:
        if not dish_ids:
            return set()
        stmt = select(Favorite.dish_id).where(
            Favorite.user_id == user_id, Favorite.dish_id.in_(dish_ids)
        )
        rows = await self.session.execute(stmt)
        return {row[0] for row in rows.all()}

    async def list_dishes_for_user(self, user_id: UUID) -> list[Dish]:
        stmt = (
            select(Dish)
            .join(Favorite, Favorite.dish_id == Dish.id)
            .where(Favorite.user_id == user_id)
            .order_by(Favorite.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
