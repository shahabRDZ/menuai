from uuid import UUID

from app.exceptions import NotFound
from app.models import Dish, MenuScan, User
from app.repositories import FavoriteRepository, MenuScanRepository
from app.schemas.dish import (
    DishResponse,
    ExplainDishResponse,
    MenuScanResponse,
    MenuScanSummary,
)
from app.services.ai import MenuVisionService, ParsedDish, ParsedMenu
from app.services.url_fetcher import UrlFetcher


class MenuService:
    def __init__(
        self,
        scans: MenuScanRepository,
        favorites: FavoriteRepository,
        vision: MenuVisionService,
        url_fetcher: UrlFetcher,
    ) -> None:
        self.scans = scans
        self.favorites = favorites
        self.vision = vision
        self.url_fetcher = url_fetcher

    async def scan(
        self,
        user: User,
        image_bytes: bytes,
        target_language: str | None,
        source_language: str,
        restaurant_name: str | None,
    ) -> MenuScanResponse:
        target = target_language or user.target_language
        parsed: ParsedMenu = await self.vision.scan_menu(
            image_bytes=image_bytes,
            target_language=target,
            source_language=source_language,
        )

        scan = await self._persist_scan(
            user=user,
            parsed=parsed,
            restaurant_name=restaurant_name,
            source_language=source_language,
            target_language=target,
        )
        await self.scans.session.commit()
        fresh = await self.scans.reload_with_dishes(scan.id)
        return self._to_scan_response(fresh, favorite_ids=set())

    async def import_from_url(
        self,
        user: User,
        url: str,
        target_language: str | None,
        restaurant_name: str | None,
    ) -> MenuScanResponse:
        target = target_language or user.target_language
        text = await self.url_fetcher.fetch_text(url)
        parsed = await self.vision.parse_menu_text(text=text, target_language=target)

        scan = await self._persist_scan(
            user=user,
            parsed=parsed,
            restaurant_name=restaurant_name,
            source_language="auto",
            target_language=target,
            image_url=url,
        )
        await self.scans.session.commit()
        fresh = await self.scans.reload_with_dishes(scan.id)
        return self._to_scan_response(fresh, favorite_ids=set())

    async def get_scan(self, user: User, scan_id: UUID) -> MenuScanResponse:
        scan = await self.scans.get_for_user(scan_id, user.id)
        if scan is None:
            raise NotFound("Scan not found")
        favorite_ids = await self.favorites.favorite_ids_for_user(
            user_id=user.id,
            dish_ids=[d.id for d in scan.dishes],
        )
        return self._to_scan_response(scan, favorite_ids)

    async def list_scans(self, user: User) -> list[MenuScanSummary]:
        rows = await self.scans.list_summaries(user.id)
        return [
            MenuScanSummary(
                id=scan.id,
                restaurant_name=scan.restaurant_name,
                target_language=scan.target_language,
                created_at=scan.created_at,
                dish_count=dish_count,
            )
            for scan, dish_count in rows
        ]

    async def delete_scan(self, user: User, scan_id: UUID) -> None:
        scan = await self.scans.get_for_user(scan_id, user.id)
        if scan is None:
            raise NotFound("Scan not found")
        await self.scans.delete(scan)
        await self.scans.session.commit()

    async def explain_dish(
        self,
        user: User,
        dish_name: str,
        source_language: str,
        target_language: str | None,
    ) -> ExplainDishResponse:
        target = target_language or user.target_language
        explanation = await self.vision.explain_dish(
            dish_name=dish_name,
            target_language=target,
            source_language=source_language,
        )
        return ExplainDishResponse(
            name_translated=explanation.name_translated,
            description=explanation.description,
            ingredients=explanation.ingredients,
            allergens=explanation.allergens,
            cultural_context=explanation.cultural_context,
        )

    async def _persist_scan(
        self,
        user: User,
        parsed: ParsedMenu,
        restaurant_name: str | None,
        source_language: str,
        target_language: str,
        image_url: str | None = None,
    ) -> MenuScan:
        scan = MenuScan(
            user_id=user.id,
            restaurant_name=restaurant_name or parsed.restaurant_name,
            location=parsed.location,
            cuisine_type=parsed.cuisine_type,
            image_url=image_url,
            source_language=source_language,
            target_language=target_language,
            ai_recommendations=parsed.ai_recommendations,
            order_suggestions=parsed.order_suggestions,
        )
        await self.scans.add(scan)
        for position, parsed_dish in enumerate(parsed.dishes):
            self.scans.session.add(self._to_dish(scan.id, position, parsed_dish))
        return scan

    @staticmethod
    def _to_dish(scan_id: UUID, position: int, parsed: ParsedDish) -> Dish:
        return Dish(
            scan_id=scan_id,
            position=position,
            name_original=parsed.name_original,
            name_translated=parsed.name_translated,
            description=parsed.description,
            category=parsed.category,
            price=parsed.price,
            currency=parsed.currency,
            price_usd=parsed.price_usd,
            typical_price_min=parsed.typical_price_min,
            typical_price_max=parsed.typical_price_max,
            price_fairness=parsed.price_fairness,
            price_delta_percent=parsed.price_delta_percent,
            price_estimate_confidence=parsed.price_estimate_confidence,
            ingredients=parsed.ingredients,
            allergens=parsed.allergens,
            allergen_risk=parsed.allergen_risk,
            hidden_risks=parsed.hidden_risks,
            is_vegetarian=parsed.is_vegetarian,
            is_vegan=parsed.is_vegan,
            is_halal_possible=parsed.is_halal_possible,
            spice_level=parsed.spice_level,
            local_popularity=parsed.local_popularity,
            tourist_trap_risk=parsed.tourist_trap_risk,
            value_assessment=parsed.value_assessment,
            recommendation_score=parsed.recommendation_score,
            cultural_context=parsed.cultural_context,
            ai_metadata=parsed.metadata,
        )

    @staticmethod
    def _to_scan_response(scan: MenuScan, favorite_ids: set[UUID]) -> MenuScanResponse:
        return MenuScanResponse(
            id=scan.id,
            restaurant_name=scan.restaurant_name,
            location=scan.location,
            cuisine_type=scan.cuisine_type,
            source_language=scan.source_language,
            target_language=scan.target_language,
            created_at=scan.created_at,
            ai_recommendations=scan.ai_recommendations,
            order_suggestions=scan.order_suggestions,
            dishes=[MenuService._dish_to_response(d, d.id in favorite_ids) for d in scan.dishes],
        )

    @staticmethod
    def _dish_to_response(dish: Dish, is_favorite: bool) -> DishResponse:
        return DishResponse(
            id=dish.id,
            scan_id=dish.scan_id,
            position=dish.position,
            name_original=dish.name_original,
            name_translated=dish.name_translated,
            description=dish.description,
            category=dish.category,
            price=float(dish.price) if dish.price is not None else None,
            currency=dish.currency,
            price_usd=float(dish.price_usd) if dish.price_usd is not None else None,
            typical_price_min=(
                float(dish.typical_price_min) if dish.typical_price_min is not None else None
            ),
            typical_price_max=(
                float(dish.typical_price_max) if dish.typical_price_max is not None else None
            ),
            price_fairness=dish.price_fairness,
            price_delta_percent=dish.price_delta_percent,
            price_estimate_confidence=dish.price_estimate_confidence,
            ingredients=dish.ingredients,
            allergens=dish.allergens,
            allergen_risk=dish.allergen_risk,
            hidden_risks=dish.hidden_risks,
            is_vegetarian=dish.is_vegetarian,
            is_vegan=dish.is_vegan,
            is_halal_possible=dish.is_halal_possible,
            spice_level=dish.spice_level,
            local_popularity=dish.local_popularity,
            tourist_trap_risk=dish.tourist_trap_risk,
            value_assessment=dish.value_assessment,
            recommendation_score=dish.recommendation_score,
            cultural_context=dish.cultural_context,
            created_at=dish.created_at,
            is_favorite=is_favorite,
        )
