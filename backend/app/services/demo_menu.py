"""Canned menu fixture used when no vision API key is configured.

Shape matches the enriched MenuAI spec: restaurant_context, rich allergen
block with risk + hidden_risks, dietary_flags, smart_insights, cultural
context, recommendation score, and scan-level ai_recommendations +
order_suggestions.
"""
from typing import Any

_RESTAURANT_CONTEXT: dict[str, Any] = {
    "name": "Çiya Sofrası (demo)",
    "location": "Kadıköy, Istanbul",
    "cuisine_type": "Turkish / Ottoman",
}


def _tr(values: dict[str, str] | str, target_language: str) -> str:
    if isinstance(values, str):
        return values
    return values.get(target_language) or values.get("en") or next(iter(values.values()))


_TRY_TO_USD = 0.031  # demo-fixture exchange rate; real one comes from AI at runtime


def _dish(
    *,
    original: str,
    translated: dict[str, str],
    description: dict[str, str],
    category: str,
    price: float,
    typical_min: float,
    typical_max: float,
    ingredients: list[str],
    allergens_contain: list[str],
    allergen_risk: str,
    hidden_risks: list[str],
    vegetarian: bool,
    vegan: bool,
    halal_possible: bool,
    spice: int,
    popularity: str,
    trap_risk: str,
    value: str,
    score: int,
    origin: str,
    tradition: str,
    when_eaten: str,
) -> dict[str, Any]:
    midpoint = (typical_min + typical_max) / 2
    delta = round((price - midpoint) / midpoint * 100) if midpoint else None
    if delta is None:
        fairness = None
    elif delta < -10:
        fairness = "below_typical"
    elif delta > 15:
        fairness = "above_typical"
    else:
        fairness = "typical"
    return {
        "original": original,
        "translated": translated,
        "description": description,
        "category": category,
        "price": price,
        "price_usd": round(price * _TRY_TO_USD, 1),
        "typical_min": typical_min,
        "typical_max": typical_max,
        "price_fairness": fairness,
        "price_delta_percent": delta,
        "price_estimate_confidence": "medium",
        "ingredients": ingredients,
        "allergens_contain": allergens_contain,
        "allergen_risk": allergen_risk,
        "hidden_risks": hidden_risks,
        "vegetarian": vegetarian,
        "vegan": vegan,
        "halal_possible": halal_possible,
        "spice": spice,
        "popularity": popularity,
        "trap_risk": trap_risk,
        "value": value,
        "score": score,
        "origin": origin,
        "tradition": tradition,
        "when_eaten": when_eaten,
    }


_DEMO_DISHES: list[dict[str, Any]] = [
    _dish(
        original="Mercimek Çorbası",
        translated={
            "en": "Red Lentil Soup",
            "fa": "سوپ عدس قرمز",
            "ar": "حساء العدس الأحمر",
            "tr": "Mercimek Çorbası",
        },
        description={
            "en": "Velvety Turkish red-lentil soup simmered with onion, carrot, and paprika, finished with lemon.",
            "fa": "سوپ سنتی ترکیه: عدس قرمز با پیاز، هویج و پاپریکا، با لیمو سرو می‌شود.",
        },
        category="soup",
        price=85,
        typical_min=70,
        typical_max=110,
        ingredients=["red lentils", "onion", "carrot", "paprika", "lemon"],
        allergens_contain=[],
        allergen_risk="low",
        hidden_risks=["may be finished with butter in some kitchens"],
        vegetarian=True,
        vegan=True,
        halal_possible=True,
        spice=1,
        popularity="high",
        trap_risk="low",
        value="cheap",
        score=88,
        origin="Anatolia",
        tradition="A default starter at almost every Turkish meal",
        when_eaten="Served year-round, especially before a heavy main",
    ),
    _dish(
        original="İçli Köfte",
        translated={
            "en": "Stuffed Bulgur Dumplings",
            "fa": "کوفته بلغور پرشده",
            "ar": "كبة محشوة",
        },
        description={
            "en": "Bulgur shells shaped by hand around spiced minced beef with onions and walnuts, then fried.",
            "fa": "پوسته بلغور دست‌ساز که با گوشت چرخ‌کرده، پیاز و گردو پر شده و سرخ می‌شود.",
        },
        category="appetizer",
        price=180,
        typical_min=150,
        typical_max=220,
        ingredients=["bulgur", "minced beef", "onion", "walnuts", "spices"],
        allergens_contain=["gluten", "nuts"],
        allergen_risk="high",
        hidden_risks=["shells are bulgur wheat — not gluten free", "nut filling is traditional"],
        vegetarian=False,
        vegan=False,
        halal_possible=True,
        spice=1,
        popularity="high",
        trap_risk="low",
        value="fair",
        score=82,
        origin="Southeast Turkey (Gaziantep / Şanlıurfa)",
        tradition="A mezze staple with Arab-Turkish roots",
        when_eaten="Appetizer at any time of day",
    ),
    _dish(
        original="Hünkar Beğendi",
        translated={
            "en": "Sultan's Delight",
            "fa": "خورش هونکار بگندی",
            "ar": "متعة السلطان",
        },
        description={
            "en": "Slow-braised lamb cubes served over a smoky eggplant and kaşar purée. An Ottoman palace classic.",
            "fa": "تکه‌های بره خورشت‌شده روی پوره بادمجان دودی و پنیر کاشار — غذای کلاسیک دربار عثمانی.",
        },
        category="main",
        price=420,
        typical_min=280,
        typical_max=380,
        ingredients=["lamb", "eggplant", "kaşar cheese", "butter", "flour"],
        allergens_contain=["dairy", "gluten"],
        allergen_risk="high",
        hidden_risks=["roux uses flour", "purée contains butter and melted cheese"],
        vegetarian=False,
        vegan=False,
        halal_possible=True,
        spice=0,
        popularity="high",
        trap_risk="medium",
        value="expensive",
        score=90,
        origin="Ottoman palace kitchens",
        tradition="Said to have been a favorite of Sultan Murad IV",
        when_eaten="Dinner, special occasions",
    ),
    _dish(
        original="Adana Kebap",
        translated={
            "en": "Adana Kebab",
            "fa": "کباب آدانا",
            "ar": "كباب أضنة",
        },
        description={
            "en": "Hand-minced lamb with red pepper flakes, pressed onto wide skewers and grilled over charcoal.",
            "fa": "گوشت بره دست‌چرخ‌شده با فلفل قرمز، روی سیخ پهن و کباب زغالی.",
        },
        category="main",
        price=380,
        typical_min=320,
        typical_max=440,
        ingredients=["lamb", "red pepper", "garlic", "sumac", "parsley"],
        allergens_contain=[],
        allergen_risk="medium",
        hidden_risks=["served with lavash bread (gluten) and yogurt (dairy)"],
        vegetarian=False,
        vegan=False,
        halal_possible=True,
        spice=2,
        popularity="high",
        trap_risk="low",
        value="fair",
        score=92,
        origin="Adana, Turkey",
        tradition="Protected designation — real Adana kebap must be coarsely minced, not ground",
        when_eaten="Lunch or dinner",
    ),
    _dish(
        original="Mantı",
        translated={
            "en": "Turkish Beef Dumplings",
            "fa": "منتی (راویولی ترکی با گوشت)",
            "ar": "مانتي",
        },
        description={
            "en": "Tiny beef-filled dumplings served under garlic yogurt and drizzled with chili butter.",
            "fa": "راویولی‌های ریز پر شده با گوشت، با ماست سیردار و کره فلفل.",
        },
        category="main",
        price=320,
        typical_min=260,
        typical_max=360,
        ingredients=["flour", "egg", "minced beef", "yogurt", "garlic", "chili butter"],
        allergens_contain=["gluten", "egg", "dairy"],
        allergen_risk="high",
        hidden_risks=["pasta dough includes egg and wheat", "yogurt is dairy"],
        vegetarian=False,
        vegan=False,
        halal_possible=True,
        spice=1,
        popularity="medium",
        trap_risk="low",
        value="fair",
        score=86,
        origin="Kayseri, central Anatolia",
        tradition="Traditionally prepared by the bride's family for her trousseau",
        when_eaten="Lunch, dinner, family gatherings",
    ),
    _dish(
        original="Çoban Salatası",
        translated={
            "en": "Shepherd's Salad",
            "fa": "سالاد چوپانی",
            "ar": "سلطة الراعي",
        },
        description={
            "en": "Crisp tomato, cucumber, green pepper, and onion tossed with parsley, olive oil, and lemon.",
            "fa": "گوجه، خیار، فلفل سبز و پیاز خرد شده با جعفری، روغن زیتون و لیمو.",
        },
        category="salad",
        price=120,
        typical_min=90,
        typical_max=150,
        ingredients=["tomato", "cucumber", "green pepper", "onion", "parsley", "olive oil"],
        allergens_contain=[],
        allergen_risk="low",
        hidden_risks=[],
        vegetarian=True,
        vegan=True,
        halal_possible=True,
        spice=0,
        popularity="high",
        trap_risk="low",
        value="cheap",
        score=75,
        origin="Rural Anatolia",
        tradition="Named after shepherds who made it with whatever was fresh",
        when_eaten="Accompanies any Turkish meal",
    ),
    _dish(
        original="Künefe",
        translated={
            "en": "Künefe",
            "fa": "کنافه",
            "ar": "كنافة",
        },
        description={
            "en": "Shredded filo baked around a salty cheese core, soaked in syrup, served hot with pistachio.",
            "fa": "خمیر رشته‌ای برشته شده دور پنیر نمکی، در شربت خیس و با پسته سرو می‌شود.",
        },
        category="dessert",
        price=220,
        typical_min=180,
        typical_max=260,
        ingredients=["kadayıf", "cheese", "butter", "syrup", "pistachio"],
        allergens_contain=["dairy", "gluten", "nuts"],
        allergen_risk="high",
        hidden_risks=["kadayıf is wheat", "pistachio garnish is not optional in Hatay style"],
        vegetarian=True,
        vegan=False,
        halal_possible=True,
        spice=0,
        popularity="high",
        trap_risk="medium",
        value="fair",
        score=88,
        origin="Hatay, southern Turkey / Levant",
        tradition="Eaten piping hot straight from the tray",
        when_eaten="After dinner, celebrations",
    ),
    _dish(
        original="Ayran",
        translated={
            "en": "Ayran",
            "fa": "دوغ",
            "ar": "عيران",
        },
        description={
            "en": "Classic salted yogurt drink — the standard pairing with any Turkish grill.",
            "fa": "نوشیدنی کلاسیک ماست و نمک؛ همراه همیشگی کباب‌های ترکی.",
        },
        category="drink",
        price=40,
        typical_min=30,
        typical_max=60,
        ingredients=["yogurt", "water", "salt"],
        allergens_contain=["dairy"],
        allergen_risk="medium",
        hidden_risks=[],
        vegetarian=True,
        vegan=False,
        halal_possible=True,
        spice=0,
        popularity="high",
        trap_risk="low",
        value="cheap",
        score=80,
        origin="Central Asia / Turkic peoples",
        tradition="Turkey's unofficial national drink",
        when_eaten="Alongside kebap and pilav",
    ),
]


def _ai_recommendations(target_language: str) -> dict[str, Any]:
    return {
        "best_for_user": [
            {
                "dish_name": _tr({"en": "Adana Kebab", "fa": "کباب آدانا"}, target_language),
                "reason": _tr(
                    {
                        "en": "Iconic local, fair price, no hidden dairy or gluten.",
                        "fa": "انتخاب سنتی و پرطرفدار محلی، قیمت منصفانه، بدون لبنیات یا گلوتن مخفی.",
                    },
                    target_language,
                ),
            },
            {
                "dish_name": _tr({"en": "Red Lentil Soup", "fa": "سوپ عدس قرمز"}, target_language),
                "reason": _tr(
                    {
                        "en": "Safe vegan starter under 100 TRY.",
                        "fa": "پیش‌غذای امن و وگان زیر ۱۰۰ لیر.",
                    },
                    target_language,
                ),
            },
        ],
        "avoid_if": [
            {
                "condition": _tr({"en": "Gluten intolerance", "fa": "حساسیت به گلوتن"}, target_language),
                "reason": _tr(
                    {
                        "en": "Mantı, İçli Köfte, Künefe, and Hünkar Beğendi all contain wheat.",
                        "fa": "منتی، ایچلی کوفته، کنافه و هونکار بگندی همگی گندم دارند.",
                    },
                    target_language,
                ),
            },
            {
                "condition": _tr({"en": "Dairy allergy", "fa": "آلرژی به لبنیات"}, target_language),
                "reason": _tr(
                    {
                        "en": "Mantı, Hünkar Beğendi, Künefe, and Ayran are all dairy-heavy.",
                        "fa": "منتی، هونکار بگندی، کنافه و دوغ همگی لبنیات بالایی دارند.",
                    },
                    target_language,
                ),
            },
        ],
    }


def _order_suggestions(target_language: str) -> dict[str, Any]:
    return {
        "light_option": _tr(
            {"en": "Shepherd's Salad + Red Lentil Soup", "fa": "سالاد چوپانی + سوپ عدس"},
            target_language,
        ),
        "protein_rich_option": _tr(
            {"en": "Adana Kebab with Ayran", "fa": "کباب آدانا با دوغ"}, target_language
        ),
        "budget_option": _tr(
            {"en": "Red Lentil Soup + Shepherd's Salad", "fa": "سوپ عدس + سالاد چوپانی"},
            target_language,
        ),
        "local_experience_option": _tr(
            {"en": "Hünkar Beğendi followed by Künefe", "fa": "هونکار بگندی به همراه کنافه"},
            target_language,
        ),
    }


def demo_menu(target_language: str) -> dict[str, Any]:
    dishes: list[dict[str, Any]] = []
    for raw in _DEMO_DISHES:
        dishes.append(
            {
                "original_name": raw["original"],
                "translated_name": _tr(raw["translated"], target_language),
                "description": _tr(raw["description"], target_language),
                "category": raw["category"],
                "price": {
                    "value": raw["price"],
                    "currency": "TRY",
                    "usd_equivalent": raw["price_usd"],
                },
                "market_price_estimate": {
                    "typical_min": raw["typical_min"],
                    "typical_max": raw["typical_max"],
                    "currency": "TRY",
                    "fairness": raw["price_fairness"],
                    "delta_percent": raw["price_delta_percent"],
                    "confidence": raw["price_estimate_confidence"],
                },
                "ingredients": raw["ingredients"],
                "allergens": {
                    "contains": raw["allergens_contain"],
                    "risk_level": raw["allergen_risk"],
                    "hidden_risks": raw["hidden_risks"],
                },
                "dietary_flags": {
                    "vegetarian": raw["vegetarian"],
                    "vegan": raw["vegan"],
                    "halal_possible": raw["halal_possible"],
                },
                "spice_level": raw["spice"],
                "cultural_context": {
                    "origin": raw["origin"],
                    "tradition": raw["tradition"],
                    "when_eaten": raw["when_eaten"],
                },
                "smart_insights": {
                    "local_popularity": raw["popularity"],
                    "tourist_trap_risk": raw["trap_risk"],
                    "value_assessment": raw["value"],
                },
                "recommendation_score": raw["score"],
            }
        )
    return {
        "restaurant_context": _RESTAURANT_CONTEXT,
        "dishes": dishes,
        "ai_recommendations": _ai_recommendations(target_language),
        "order_suggestions": _order_suggestions(target_language),
    }


def demo_dish_explanation(dish_name: str, target_language: str) -> dict[str, Any]:
    for raw in _DEMO_DISHES:
        if raw["original"].lower() == dish_name.lower():
            return {
                "name_translated": _tr(raw["translated"], target_language),
                "description": _tr(raw["description"], target_language),
                "ingredients": raw["ingredients"],
                "allergens": raw["allergens_contain"],
                "cultural_context": raw["origin"],
            }
    return {
        "name_translated": dish_name,
        "description": "Demo mode: connect an API key for real dish explanations.",
        "ingredients": [],
        "allergens": [],
        "cultural_context": None,
    }
