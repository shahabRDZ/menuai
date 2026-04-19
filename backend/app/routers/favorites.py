from uuid import UUID

from fastapi import APIRouter, status

from app.deps import CurrentUser, FavoriteServiceDep
from app.schemas.dish import DishResponse

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.post("/{dish_id}", status_code=status.HTTP_201_CREATED)
async def add_favorite(
    dish_id: UUID, user: CurrentUser, favorites: FavoriteServiceDep
) -> dict[str, str]:
    await favorites.add(user, dish_id)
    return {"status": "ok", "dish_id": str(dish_id)}


@router.delete("/{dish_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_favorite(dish_id: UUID, user: CurrentUser, favorites: FavoriteServiceDep) -> None:
    await favorites.remove(user, dish_id)


@router.get("", response_model=list[DishResponse])
async def list_favorites(user: CurrentUser, favorites: FavoriteServiceDep) -> list[DishResponse]:
    return await favorites.list_for_user(user)
