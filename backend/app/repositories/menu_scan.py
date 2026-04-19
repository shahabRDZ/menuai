from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.models import Dish, MenuScan
from app.repositories.base import BaseRepository


class MenuScanRepository(BaseRepository[MenuScan]):
    model = MenuScan

    async def get_for_user(self, scan_id: UUID, user_id: UUID) -> MenuScan | None:
        stmt = (
            select(MenuScan)
            .options(selectinload(MenuScan.dishes))
            .where(MenuScan.id == scan_id, MenuScan.user_id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_summaries(self, user_id: UUID) -> list[tuple[MenuScan, int]]:
        stmt = (
            select(MenuScan, func.count(Dish.id).label("dish_count"))
            .outerjoin(Dish, Dish.scan_id == MenuScan.id)
            .where(MenuScan.user_id == user_id)
            .group_by(MenuScan.id)
            .order_by(MenuScan.created_at.desc())
        )
        rows = await self.session.execute(stmt)
        return [(scan, dish_count) for scan, dish_count in rows.all()]

    async def reload_with_dishes(self, scan_id: UUID) -> MenuScan:
        stmt = (
            select(MenuScan)
            .options(selectinload(MenuScan.dishes))
            .where(MenuScan.id == scan_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()
