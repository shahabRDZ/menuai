"""Vision-backed menu parsing and dish lookup.

Wraps the Anthropic SDK in a small service with two public methods:
- ``scan_menu`` — photo in, structured dish list out
- ``explain_dish`` — name in, translation + ingredients + allergens out

The two system prompts are large and stable, so they are marked with
``cache_control`` ephemeral caching. Successive requests only pay for the
user turn (image + short instruction).
"""

import base64
import json
from dataclasses import dataclass
from io import BytesIO
from typing import Any

from anthropic import AsyncAnthropic
from PIL import Image

from app.config import settings
from app.exceptions import UpstreamError
from app.services.demo_menu import demo_dish_explanation, demo_menu

_MENU_SYSTEM_CORE = """You are MenuAI — a food intelligence system for global travelers.

Your job is to turn menu content into structured, safety-aware JSON. You never
produce prose outside the JSON. Priorities, in order:

  1. Accuracy  2. Food safety (allergens)  3. Cultural insight  4. User intent

Core rules:

- Infer *hidden* ingredients even when the menu doesn't list them
  (e.g. meatballs → breadcrumbs, egg; cream sauces → dairy, flour).
  Record these in `allergens.hidden_risks`.
- Allergy safety: never understate risk. Prefer a false positive over a false
  negative. `allergens.risk_level` is "high" whenever cross-contamination or
  hidden ingredients are plausible.
- Cultural context: for every dish, give origin (region or tradition if known),
  when it's eaten, and any relevant cultural meaning.
- `smart_insights` are grounded estimates, not guesses:
  - local_popularity: how common this dish is with locals
  - tourist_trap_risk: is this menu item over-priced for tourists
  - value_assessment: "cheap" | "fair" | "expensive" for its category
- `recommendation_score` (0-100) balances safety, popularity, price fairness,
  and how authentic the dish is.

Schema — return exactly this shape (use null or [] for missing values):

{
  "restaurant_context": {
    "name": string | null,
    "location": string | null,
    "cuisine_type": string | null
  },
  "dishes": [
    {
      "original_name": string,
      "translated_name": string,
      "description": string,
      "category": "appetizer" | "soup" | "salad" | "main" | "side"
                   | "dessert" | "drink" | "snack" | "unknown",
      "price": { "value": number | null, "currency": string | null },
      "ingredients": [string, ...],
      "allergens": {
        "contains": [string, ...],
        "risk_level": "low" | "medium" | "high",
        "hidden_risks": [string, ...]
      },
      "dietary_flags": {
        "vegetarian": boolean | null,
        "vegan": boolean | null,
        "halal_possible": boolean | null
      },
      "spice_level": 0 | 1 | 2 | 3 | null,
      "cultural_context": {
        "origin": string | null,
        "tradition": string | null,
        "when_eaten": string | null
      },
      "smart_insights": {
        "local_popularity": "low" | "medium" | "high",
        "tourist_trap_risk": "low" | "medium" | "high",
        "value_assessment": "cheap" | "fair" | "expensive"
      },
      "recommendation_score": number
    }
  ],
  "ai_recommendations": {
    "best_for_user": [ { "dish_name": string, "reason": string } ],
    "avoid_if": [ { "condition": string, "reason": string } ]
  },
  "order_suggestions": {
    "light_option": string | null,
    "protein_rich_option": string | null,
    "budget_option": string | null,
    "local_experience_option": string | null
  }
}

Allergen names must come from this set:
  gluten, dairy, egg, nuts, peanuts, seafood, fish, soy, sesame.

Translate `translated_name`, `description`, `ingredients`, the cultural context,
and the recommendation reasons into the user's target language. Keep
`original_name` as printed. No prose, no markdown fences."""


_MENU_SCAN_SYSTEM = (
    _MENU_SYSTEM_CORE
    + "\n\nInput channel: photograph of a paper or printed menu. Use vision to "
    "read every dish, including handwritten additions. Ignore decorative text."
)


_MENU_TEXT_SYSTEM = (
    _MENU_SYSTEM_CORE
    + "\n\nInput channel: text or HTML of a digital menu page (usually fetched "
    "from a QR code URL). Ignore navigation, footers, cookie banners, delivery "
    "disclaimers, and marketing copy."
)


_DISH_EXPLAIN_SYSTEM = """You are a multilingual food expert.

Given a single dish name (in any language) and a target language, return a concise
structured explanation so a foreign diner can decide whether to order it.

Respond ONLY as valid JSON:
{
  "name_translated": string,
  "description": string (2-3 sentences in target language),
  "ingredients": [string, ...],
  "allergens": [string, ...],
  "cultural_context": string | null
}

Allergens must be drawn from: gluten, dairy, egg, nuts, peanuts, seafood, fish, soy, sesame.
No prose, no markdown fences."""


_ALLERGEN_CANON = {
    "gluten",
    "dairy",
    "egg",
    "nuts",
    "peanuts",
    "seafood",
    "fish",
    "soy",
    "sesame",
}
_RISK_LEVELS = {"low", "medium", "high"}
_VALUE_LEVELS = {"cheap", "fair", "expensive"}


@dataclass(slots=True)
class ParsedDish:
    name_original: str
    name_translated: str | None
    description: str | None
    category: str | None
    price: float | None
    currency: str | None
    ingredients: list[str] | None
    allergens: list[str] | None
    allergen_risk: str | None
    hidden_risks: list[str] | None
    is_vegetarian: bool | None
    is_vegan: bool | None
    is_halal_possible: bool | None
    spice_level: int | None
    local_popularity: str | None
    tourist_trap_risk: str | None
    value_assessment: str | None
    recommendation_score: int | None
    cultural_context: dict[str, Any] | None
    metadata: dict[str, Any] | None


@dataclass(slots=True)
class ParsedMenu:
    restaurant_name: str | None
    location: str | None
    cuisine_type: str | None
    dishes: list[ParsedDish]
    ai_recommendations: dict[str, Any] | None
    order_suggestions: dict[str, Any] | None


@dataclass(slots=True)
class DishExplanation:
    name_translated: str
    description: str
    ingredients: list[str]
    allergens: list[str]
    cultural_context: str | None


class MenuVisionService:
    """Menu vision and translation service.

    One instance per process; construction is cheap but we only need one
    client. All I/O is async.
    """

    def __init__(self, api_key: str, model: str) -> None:
        self._api_key = api_key
        self._model = model
        self._client: AsyncAnthropic | None = None

    @property
    def demo_mode(self) -> bool:
        # Empty, unset, or clearly-not-a-real-key values all trigger demo mode.
        # Real Anthropic keys start with "sk-ant-".
        return not self._api_key or not self._api_key.startswith("sk-")

    @property
    def client(self) -> AsyncAnthropic:
        if self._client is None:
            self._client = AsyncAnthropic(api_key=self._api_key)
        return self._client

    async def scan_menu(
        self,
        image_bytes: bytes,
        target_language: str,
        source_language: str = "auto",
    ) -> ParsedMenu:
        if self.demo_mode:
            return self._to_parsed_menu(demo_menu(target_language))

        compressed, media_type = self._compress_image(image_bytes)
        b64 = base64.b64encode(compressed).decode()

        instruction = (
            f"Target language for translations/descriptions: {target_language}. "
            f"Source language hint: {source_language}. "
            "Extract every dish you can see. Return the JSON object only."
        )

        response = await self.client.messages.create(
            model=self._model,
            max_tokens=4096,
            system=[
                {"type": "text", "text": _MENU_SCAN_SYSTEM, "cache_control": {"type": "ephemeral"}}
            ],
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {"type": "base64", "media_type": media_type, "data": b64},
                        },
                        {"type": "text", "text": instruction},
                    ],
                }
            ],
        )
        data = self._parse_json_response(response)
        if not isinstance(data, dict) or "dishes" not in data:
            raise UpstreamError("Model response missing 'dishes' field")

        dishes = [self._to_parsed_dish(raw) for raw in data.get("dishes", [])]
        return ParsedMenu(
            restaurant_name=data.get("restaurant_name"),
            dishes=[d for d in dishes if d is not None],
        )

    async def parse_menu_text(
        self,
        text: str,
        target_language: str,
        source_language: str = "auto",
    ) -> ParsedMenu:
        if self.demo_mode:
            return self._to_parsed_menu(demo_menu(target_language))

        instruction = (
            f"Target language: {target_language}\n"
            f"Source language hint: {source_language}\n"
            "Menu content follows, delimited by ===.\n"
            f"===\n{text}\n===\n"
            "Return the JSON object only."
        )

        response = await self.client.messages.create(
            model=self._model,
            max_tokens=4096,
            system=[
                {"type": "text", "text": _MENU_TEXT_SYSTEM, "cache_control": {"type": "ephemeral"}}
            ],
            messages=[{"role": "user", "content": instruction}],
        )
        data = self._parse_json_response(response)
        if not isinstance(data, dict) or "dishes" not in data:
            raise UpstreamError("Model response missing 'dishes' field")
        return self._to_parsed_menu(data)

    async def explain_dish(
        self,
        dish_name: str,
        target_language: str,
        source_language: str = "auto",
    ) -> DishExplanation:
        if self.demo_mode:
            data = demo_dish_explanation(dish_name, target_language)
            return DishExplanation(
                name_translated=str(data.get("name_translated") or dish_name),
                description=str(data.get("description") or ""),
                ingredients=list(data.get("ingredients") or []),
                allergens=list(data.get("allergens") or []),
                cultural_context=data.get("cultural_context"),
            )

        instruction = (
            f'Dish name: "{dish_name}"\n'
            f"Source language: {source_language}\n"
            f"Target language: {target_language}\n"
            "Return the JSON object only."
        )

        response = await self.client.messages.create(
            model=self._model,
            max_tokens=1024,
            system=[
                {
                    "type": "text",
                    "text": _DISH_EXPLAIN_SYSTEM,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[{"role": "user", "content": instruction}],
        )
        data = self._parse_json_response(response)
        return DishExplanation(
            name_translated=str(data.get("name_translated") or dish_name),
            description=str(data.get("description") or ""),
            ingredients=_as_str_list(data.get("ingredients")) or [],
            allergens=_as_str_list(data.get("allergens")) or [],
            cultural_context=data.get("cultural_context"),
        )

    @staticmethod
    def _compress_image(
        image_bytes: bytes, max_dim: int = 1600, quality: int = 85
    ) -> tuple[bytes, str]:
        img = Image.open(BytesIO(image_bytes)).convert("RGB")
        img.thumbnail((max_dim, max_dim))
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True)
        return buf.getvalue(), "image/jpeg"

    @staticmethod
    def _parse_json_response(response: Any) -> Any:
        text = "".join(block.text for block in response.content if block.type == "text").strip()
        if text.startswith("```"):
            text = text.split("```", 2)[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip().rstrip("`").strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise UpstreamError(f"Model returned invalid JSON: {e}") from e

    @classmethod
    def _to_parsed_menu(cls, raw: dict[str, Any]) -> ParsedMenu:
        ctx = raw.get("restaurant_context") or {}
        dishes = [cls._to_parsed_dish(d) for d in raw.get("dishes", [])]
        return ParsedMenu(
            restaurant_name=_as_str(ctx.get("name")) or _as_str(raw.get("restaurant_name")),
            location=_as_str(ctx.get("location")),
            cuisine_type=_as_str(ctx.get("cuisine_type")),
            dishes=[d for d in dishes if d is not None],
            ai_recommendations=raw.get("ai_recommendations") or None,
            order_suggestions=raw.get("order_suggestions") or None,
        )

    @classmethod
    def _to_parsed_dish(cls, raw: Any) -> ParsedDish | None:
        if not isinstance(raw, dict):
            return None

        original = raw.get("original_name") or raw.get("name_original")
        if not original:
            return None

        price_block = raw.get("price") if isinstance(raw.get("price"), dict) else None
        price_value = _as_float(price_block.get("value")) if price_block else _as_float(raw.get("price"))
        currency = (
            _as_str(price_block.get("currency")) if price_block else _as_str(raw.get("currency"))
        )

        allergens_block = raw.get("allergens")
        if isinstance(allergens_block, dict):
            contains = _as_str_list(allergens_block.get("contains"))
            risk_level = _pick_enum(allergens_block.get("risk_level"), _RISK_LEVELS)
            hidden_risks = _as_str_list(allergens_block.get("hidden_risks"))
        else:
            contains = _as_str_list(allergens_block)
            risk_level = None
            hidden_risks = None
        contains = [a for a in (contains or []) if a in _ALLERGEN_CANON] or None

        flags = raw.get("dietary_flags") or {}
        is_veg = _as_bool(flags.get("vegetarian") if flags else raw.get("is_vegetarian"))
        is_vegan = _as_bool(flags.get("vegan") if flags else raw.get("is_vegan"))
        halal = _as_bool(flags.get("halal_possible"))

        insights = raw.get("smart_insights") or {}

        return ParsedDish(
            name_original=str(original)[:300],
            name_translated=_as_str(raw.get("translated_name") or raw.get("name_translated")),
            description=_as_str(raw.get("description")),
            category=_as_str(raw.get("category")),
            price=price_value,
            currency=currency,
            ingredients=_as_str_list(raw.get("ingredients")),
            allergens=contains,
            allergen_risk=risk_level,
            hidden_risks=hidden_risks,
            is_vegetarian=is_veg,
            is_vegan=is_vegan,
            is_halal_possible=halal,
            spice_level=_as_int(raw.get("spice_level")),
            local_popularity=_pick_enum(insights.get("local_popularity"), _RISK_LEVELS),
            tourist_trap_risk=_pick_enum(insights.get("tourist_trap_risk"), _RISK_LEVELS),
            value_assessment=_pick_enum(insights.get("value_assessment"), _VALUE_LEVELS),
            recommendation_score=_as_int(raw.get("recommendation_score")),
            cultural_context=raw.get("cultural_context") if isinstance(raw.get("cultural_context"), dict) else None,
            metadata=raw,
        )


def _as_str(v: Any) -> str | None:
    if v is None or v == "":
        return None
    return str(v)


def _as_float(v: Any) -> float | None:
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _as_int(v: Any) -> int | None:
    if v is None:
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _as_bool(v: Any) -> bool | None:
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        s = v.lower()
        if s in {"true", "yes", "1"}:
            return True
        if s in {"false", "no", "0"}:
            return False
    return None


def _pick_enum(v: Any, allowed: set[str]) -> str | None:
    if v is None:
        return None
    normalized = str(v).strip().lower()
    return normalized if normalized in allowed else None


def _as_str_list(v: Any) -> list[str] | None:
    if v is None:
        return None
    if isinstance(v, list):
        return [str(x) for x in v if x]
    return None


menu_vision_service = MenuVisionService(
    api_key=settings.anthropic_api_key,
    model=settings.claude_model,
)
