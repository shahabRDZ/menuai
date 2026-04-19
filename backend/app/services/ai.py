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

_MENU_SCAN_SYSTEM = """You are an expert multilingual menu translator and food critic.

You receive photos of restaurant menus (often in Turkish, but any language is possible)
and return a structured JSON list of every dish you can identify on the menu.

For each dish:
- name_original: the dish as printed on the menu (preserve original spelling)
- name_translated: a natural, appetizing translation into the target language
- description: 1-2 sentences describing what it is, in the target language. If the
  menu has a description, translate it faithfully. Otherwise infer from dish knowledge.
- category: appetizer | soup | salad | main | side | dessert | drink | unknown
- price: numeric price if visible, else null
- currency: "TRY" | "USD" | "EUR" | ... (ISO-4217) if visible, else null
- ingredients: array of likely main ingredients (3-6 items) in the target language
- allergens: array from ["gluten", "dairy", "egg", "nuts", "peanuts", "seafood",
  "fish", "soy", "sesame"] - only include ones that are likely present
- is_vegetarian: true/false/null (null if unsure)
- is_vegan: true/false/null
- spice_level: integer 0-3 where 0 is not spicy and 3 is very spicy, or null

Respond ONLY with valid JSON matching this shape:
{ "restaurant_name": string | null, "dishes": [ ... ] }

No prose, no markdown fences."""


_MENU_TEXT_SYSTEM = """You are an expert multilingual menu translator.

You receive the raw text or HTML of a digital restaurant menu (fetched from a URL
that the user typically scanned as a QR code). Extract every dish you can find and
return a structured JSON list.

For each dish, fill the same fields as a photographed menu:
- name_original, name_translated, description, category, price, currency,
  ingredients (3-6 items, in the target language), allergens (subset of
  gluten/dairy/egg/nuts/peanuts/seafood/fish/soy/sesame), is_vegetarian,
  is_vegan, spice_level (0-3 or null)

Ignore navigation, footers, cookie banners, delivery disclaimers, and marketing copy.

Respond ONLY with valid JSON:
{ "restaurant_name": string | null, "dishes": [ ... ] }

No prose, no markdown fences."""


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
    is_vegetarian: bool | None
    is_vegan: bool | None
    spice_level: int | None


@dataclass(slots=True)
class ParsedMenu:
    restaurant_name: str | None
    dishes: list[ParsedDish]


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
        return not self._api_key

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
        dishes = [cls._to_parsed_dish(d) for d in raw.get("dishes", [])]
        return ParsedMenu(
            restaurant_name=raw.get("restaurant_name"),
            dishes=[d for d in dishes if d is not None],
        )

    @staticmethod
    def _to_parsed_dish(raw: Any) -> ParsedDish | None:
        if not isinstance(raw, dict) or not raw.get("name_original"):
            return None
        return ParsedDish(
            name_original=str(raw["name_original"])[:300],
            name_translated=_as_str(raw.get("name_translated")),
            description=_as_str(raw.get("description")),
            category=_as_str(raw.get("category")),
            price=_as_float(raw.get("price")),
            currency=_as_str(raw.get("currency")),
            ingredients=_as_str_list(raw.get("ingredients")),
            allergens=_as_str_list(raw.get("allergens")),
            is_vegetarian=_as_bool(raw.get("is_vegetarian")),
            is_vegan=_as_bool(raw.get("is_vegan")),
            spice_level=_as_int(raw.get("spice_level")),
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
