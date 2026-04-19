from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DishBase(BaseModel):
    name_original: str
    name_translated: str | None = None
    description: str | None = None
    category: str | None = None
    price: float | None = None
    currency: str | None = None
    ingredients: list[str] | None = None
    allergens: list[str] | None = None
    is_vegetarian: bool | None = None
    is_vegan: bool | None = None
    spice_level: int | None = None


class DishResponse(DishBase):
    id: UUID
    position: int
    scan_id: UUID
    created_at: datetime
    is_favorite: bool = False

    class Config:
        from_attributes = True


class MenuScanResponse(BaseModel):
    id: UUID
    restaurant_name: str | None
    source_language: str
    target_language: str
    created_at: datetime
    dishes: list[DishResponse]

    class Config:
        from_attributes = True


class MenuScanSummary(BaseModel):
    id: UUID
    restaurant_name: str | None
    target_language: str
    created_at: datetime
    dish_count: int

    class Config:
        from_attributes = True


class ExplainDishRequest(BaseModel):
    dish_name: str
    source_language: str = "auto"
    target_language: str = "en"


class ExplainDishResponse(BaseModel):
    name_translated: str
    description: str
    ingredients: list[str]
    allergens: list[str]
    cultural_context: str | None = None
