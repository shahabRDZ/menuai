"""Canned menu fixture used when no vision API key is configured.

Lets the full stack work end-to-end for local demos without any external calls.
Translations are stored as dicts keyed by target language; if the target
language isn't present, we fall back to English.
"""
from typing import Any

DEMO_RESTAURANT = "Çiya Sofrası (demo)"

_DEMO_DISHES: list[dict[str, Any]] = [
    {
        "name_original": "Mercimek Çorbası",
        "name_translated": {
            "en": "Red Lentil Soup",
            "fa": "سوپ عدس قرمز",
            "ar": "حساء العدس الأحمر",
            "tr": "Mercimek Çorbası",
            "de": "Rote-Linsen-Suppe",
            "fr": "Soupe aux lentilles corail",
            "es": "Sopa de lentejas rojas",
            "ru": "Суп из красной чечевицы",
        },
        "description": {
            "en": "A velvety Turkish staple: red lentils simmered with onion, carrot, and paprika, finished with lemon.",
            "fa": "سوپ سنتی ترکیه: عدس قرمز با پیاز، هویج و پاپریکا، با لیمو تازه سرو می‌شود.",
        },
        "category": "soup",
        "price": 85,
        "currency": "TRY",
        "ingredients": ["red lentils", "onion", "carrot", "paprika", "lemon"],
        "allergens": [],
        "is_vegetarian": True,
        "is_vegan": True,
        "spice_level": 1,
    },
    {
        "name_original": "İçli Köfte",
        "name_translated": {
            "en": "Stuffed Bulgur Dumplings",
            "fa": "کوفته برنجی پر شده",
            "ar": "كبة محشوة",
            "tr": "İçli Köfte",
        },
        "description": {
            "en": "Bulgur shells hand-shaped around spiced minced beef with onions and walnuts, then fried.",
            "fa": "پوسته بلغور دست‌ساز که با گوشت چرخ‌کرده، پیاز و گردو پر شده و سرخ می‌شود.",
        },
        "category": "appetizer",
        "price": 180,
        "currency": "TRY",
        "ingredients": ["bulgur", "minced beef", "onion", "walnuts", "spices"],
        "allergens": ["gluten", "nuts"],
        "is_vegetarian": False,
        "is_vegan": False,
        "spice_level": 1,
    },
    {
        "name_original": "Hünkar Beğendi",
        "name_translated": {
            "en": "Sultan's Delight",
            "fa": "خورش هونکار بگندی",
            "ar": "متعة السلطان",
            "tr": "Hünkar Beğendi",
        },
        "description": {
            "en": "Slow-braised lamb cubes served over a smoky eggplant and kaşar purée. An Ottoman palace classic.",
            "fa": "تکه‌های بره خورشت‌شده روی پوره بادمجان دودی و پنیر کاشار. غذای کلاسیک دربار عثمانی.",
        },
        "category": "main",
        "price": 420,
        "currency": "TRY",
        "ingredients": ["lamb", "eggplant", "kaşar cheese", "butter", "flour"],
        "allergens": ["dairy", "gluten"],
        "is_vegetarian": False,
        "is_vegan": False,
        "spice_level": 0,
    },
    {
        "name_original": "Adana Kebap",
        "name_translated": {
            "en": "Adana Kebab",
            "fa": "کباب آدانا",
            "ar": "كباب أضنة",
            "tr": "Adana Kebap",
        },
        "description": {
            "en": "Hand-minced lamb with red pepper flakes, pressed onto wide skewers and grilled over charcoal.",
            "fa": "گوشت بره دست‌چرخ‌شده با فلفل قرمز، روی سیخ پهن و کباب زغالی.",
        },
        "category": "main",
        "price": 380,
        "currency": "TRY",
        "ingredients": ["lamb", "red pepper", "garlic", "sumac", "parsley"],
        "allergens": [],
        "is_vegetarian": False,
        "is_vegan": False,
        "spice_level": 2,
    },
    {
        "name_original": "Mantı",
        "name_translated": {
            "en": "Turkish Beef Dumplings",
            "fa": "منتی (راویولی ترکی با گوشت)",
            "ar": "مانتي (معكرونة تركية محشوة)",
            "tr": "Mantı",
        },
        "description": {
            "en": "Tiny beef-filled dumplings served under garlic yogurt and drizzled with chili butter.",
            "fa": "راویولی‌های ریز پر شده با گوشت، سرو شده با ماست سیردار و کره فلفل.",
        },
        "category": "main",
        "price": 320,
        "currency": "TRY",
        "ingredients": ["flour", "egg", "minced beef", "yogurt", "garlic", "chili butter"],
        "allergens": ["gluten", "egg", "dairy"],
        "is_vegetarian": False,
        "is_vegan": False,
        "spice_level": 1,
    },
    {
        "name_original": "Çoban Salatası",
        "name_translated": {
            "en": "Shepherd's Salad",
            "fa": "سالاد چوپانی",
            "ar": "سلطة الراعي",
            "tr": "Çoban Salatası",
        },
        "description": {
            "en": "Crisp tomato, cucumber, green pepper, and onion tossed with parsley, olive oil, and lemon.",
            "fa": "گوجه، خیار، فلفل سبز و پیاز خرد شده با جعفری، روغن زیتون و لیمو.",
        },
        "category": "salad",
        "price": 120,
        "currency": "TRY",
        "ingredients": ["tomato", "cucumber", "green pepper", "onion", "parsley", "olive oil"],
        "allergens": [],
        "is_vegetarian": True,
        "is_vegan": True,
        "spice_level": 0,
    },
    {
        "name_original": "Künefe",
        "name_translated": {
            "en": "Künefe",
            "fa": "کنافه",
            "ar": "كنافة",
            "tr": "Künefe",
        },
        "description": {
            "en": "Shredded filo baked around a salty cheese core, soaked in syrup and served piping hot with pistachio.",
            "fa": "خمیر رشته‌ای برشته شده دور پنیر نمکی، در شربت خیس خورده و با پسته سرو می‌شود.",
        },
        "category": "dessert",
        "price": 220,
        "currency": "TRY",
        "ingredients": ["kadayıf", "cheese", "butter", "syrup", "pistachio"],
        "allergens": ["dairy", "gluten", "nuts"],
        "is_vegetarian": True,
        "is_vegan": False,
        "spice_level": 0,
    },
    {
        "name_original": "Ayran",
        "name_translated": {
            "en": "Ayran",
            "fa": "دوغ",
            "ar": "عيران",
            "tr": "Ayran",
        },
        "description": {
            "en": "Classic salted yogurt drink — the standard pairing with any Turkish grill.",
            "fa": "نوشیدنی کلاسیک ماست و نمک؛ همراه همیشگی کباب‌های ترکی.",
        },
        "category": "drink",
        "price": 40,
        "currency": "TRY",
        "ingredients": ["yogurt", "water", "salt"],
        "allergens": ["dairy"],
        "is_vegetarian": True,
        "is_vegan": False,
        "spice_level": 0,
    },
]


def demo_menu(target_language: str) -> dict[str, Any]:
    dishes: list[dict[str, Any]] = []
    for raw in _DEMO_DISHES:
        dishes.append(
            {
                "name_original": raw["name_original"],
                "name_translated": _pick(raw["name_translated"], target_language),
                "description": _pick(raw["description"], target_language),
                "category": raw["category"],
                "price": raw["price"],
                "currency": raw["currency"],
                "ingredients": raw["ingredients"],
                "allergens": raw["allergens"],
                "is_vegetarian": raw["is_vegetarian"],
                "is_vegan": raw["is_vegan"],
                "spice_level": raw["spice_level"],
            }
        )
    return {"restaurant_name": DEMO_RESTAURANT, "dishes": dishes}


def demo_dish_explanation(dish_name: str, target_language: str) -> dict[str, Any]:
    for raw in _DEMO_DISHES:
        if raw["name_original"].lower() == dish_name.lower():
            return {
                "name_translated": _pick(raw["name_translated"], target_language),
                "description": _pick(raw["description"], target_language),
                "ingredients": raw["ingredients"],
                "allergens": raw["allergens"],
                "cultural_context": None,
            }
    return {
        "name_translated": dish_name,
        "description": "Demo mode: connect an API key for real dish explanations.",
        "ingredients": [],
        "allergens": [],
        "cultural_context": None,
    }


def _pick(translations: dict[str, str] | str, target_language: str) -> str:
    if isinstance(translations, str):
        return translations
    return translations.get(target_language) or translations.get("en") or next(iter(translations.values()))
