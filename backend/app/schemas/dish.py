from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel


class DishBase(BaseModel):
    name_original: str
    name_translated: str | None = None
    description: str | None = None
    category: str | None = None
    price: float | None = None
    currency: str | None = None
    price_usd: float | None = None
    typical_price_min: float | None = None
    typical_price_max: float | None = None
    price_fairness: str | None = None
    price_delta_percent: int | None = None
    price_estimate_confidence: str | None = None
    ingredients: list[str] | None = None
    allergens: list[str] | None = None
    allergen_risk: str | None = None
    hidden_risks: list[str] | None = None
    is_vegetarian: bool | None = None
    is_vegan: bool | None = None
    is_halal_possible: bool | None = None
    spice_level: int | None = None
    local_popularity: str | None = None
    tourist_trap_risk: str | None = None
    value_assessment: str | None = None
    recommendation_score: int | None = None
    cultural_context: dict[str, Any] | None = None


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
    location: str | None = None
    cuisine_type: str | None = None
    source_language: str
    target_language: str
    created_at: datetime
    ai_recommendations: dict[str, Any] | None = None
    order_suggestions: dict[str, Any] | None = None
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


class ImportMenuRequest(BaseModel):
    url: str
    target_language: str = ""
    restaurant_name: str | None = None


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
