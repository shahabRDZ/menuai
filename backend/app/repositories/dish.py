from uuid import UUID

from sqlalchemy import select

from app.models import Dish, MenuScan
from app.repositories.base import BaseRepository


class DishRepository(BaseRepository[Dish]):
    model = Dish

    async def get_owned_by_user(self, dish_id: UUID, user_id: UUID) -> Dish | None:
        stmt = (
            select(Dish)
            .join(MenuScan, Dish.scan_id == MenuScan.id)
            .where(Dish.id == dish_id, MenuScan.user_id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
