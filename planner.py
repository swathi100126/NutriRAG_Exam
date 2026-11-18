"""Build one day of meals from the IFCT table for a saved profile."""

from __future__ import annotations

from dataclasses import dataclass

from foods import (
    CALORIE_TARGETS,
    DAIRY_CATEGORIES,
    EGG_CATEGORIES,
    Food,
    allowed_foods,
    load_foods,
)

MEAL_SLOTS = (
    ("Breakfast", 0.25, (("staple", 0.55), ("breakfast_side", 0.45))),
    ("Morning snack", 0.10, (("fruit", 1.0),)),
    ("Lunch", 0.30, (("staple", 0.45), ("protein", 0.35), ("vegetable", 0.20))),
    ("Evening snack", 0.10, (("snack", 1.0),)),
    ("Dinner", 0.25, (("staple", 0.40), ("protein", 0.40), ("vegetable", 0.20))),
)

PLAN_NOTE = (
    "Portions are estimated from per-100 g values in Indian Food Composition Tables 2017. "
    "This is a general eating pattern, not a clinical diet."
)


class PlannerError(RuntimeError):
    """Raised when the food table cannot fill a meal."""


@dataclass(frozen=True)
class PlanItem:
    meal: str
    food_name: str
    grams: int
    calories: float
    protein_g: float
    source: str


@dataclass(frozen=True)
class MealPlan:
    items: tuple[PlanItem, ...]
    calorie_target: int
    note: str

    @property
    def total_calories(self) -> float:
        return sum(item.calories for item in self.items)

    @property
    def total_protein(self) -> float:
        return sum(item.protein_g for item in self.items)


def _dairy_ok(profile: dict) -> bool:
    return profile["diet"] != "Vegan" and "Dairy" not in profile.get("allergies", [])


def _egg_ok(profile: dict) -> bool:
    return profile["diet"] in {"Eggetarian", "Non-vegetarian"} and "Egg" not in profile.get(
        "allergies", []
    )


def _categories_for(role: str, profile: dict) -> set[str]:
    if role == "staple":
        return {"Cereals and Millets"}
    if role == "fruit":
        return {"Fruits"}
    if role == "vegetable":
        return {"Green Leafy Vegetables", "Other Vegetables", "Roots and Tubers"}
    if role == "breakfast_side":
        if _dairy_ok(profile):
            return set(DAIRY_CATEGORIES)
        return {"Fruits"}
    if role == "snack":
        categories = {"Fruits"}
        if "Nuts" not in profile.get("allergies", []) or "Peanut" not in profile.get("allergies", []):
            categories.add("Nuts and Oil Seeds")
        return categories
    if role == "protein":
        categories = {"Grain Legumes"}
        if _dairy_ok(profile):
            categories |= set(DAIRY_CATEGORIES)
        if _egg_ok(profile):
            categories |= set(EGG_CATEGORIES)
        if profile["diet"] == "Non-vegetarian":
            categories |= {"Poultry", "Animal Meat"}
        return categories
    return set()


def _preferences(role: str, profile: dict, meal: str) -> list[str]:
    allergies = set(profile.get("allergies") or [])
    gluten = "Gluten" in allergies
    if role == "staple":
        if meal == "Dinner":
            prefs = [] if gluten else ["Wheat flour, atta", "Jowar"]
            prefs += ["Ragi", "Rice, raw, brown", "Bajra"]
            return prefs
        if meal == "Breakfast":
            return ["Rice flakes", "Ragi", "Jowar", "Rice, raw, milled"]
        return ["Rice, raw, milled", "Rice, parboiled, milled", "Jowar", "Ragi"]
    if role == "breakfast_side":
        if _dairy_ok(profile):
            return ["Milk, whole, Cow", "Curd (Dahi)"]
        return ["Banana, ripe, robusta", "Apple, big"]
    if role == "fruit":
        return ["Banana, ripe, robusta", "Apple, big", "Papaya"]
    if role == "vegetable":
        if meal == "Dinner":
            return ["Amaranth leaves, green", "Potato, brown skin, small", "Beet root"]
        return ["Carrot, orange", "Bottle gourd, elongate, pale green", "Potato, brown skin, big"]
    if role == "snack":
        prefs = []
        if "Nuts" not in allergies:
            prefs.append("Almond")
        if "Peanut" not in allergies:
            prefs.append("Ground nut")
        prefs += ["Banana, ripe, robusta", "Apple, big"]
        if _dairy_ok(profile):
            prefs.append("Curd (Dahi)")
        return prefs
    prefs = []
    if profile["diet"] == "Non-vegetarian":
        prefs.append("Chicken, poultry, breast, skinless")
    if _egg_ok(profile):
        prefs.append("Egg, poultry, whole, boiled")
    if _dairy_ok(profile):
        prefs.append("Paneer")
    if meal == "Dinner":
        prefs += ["Green gram, dal", "Black gram, dal", "Bengal gram, dal"]
    else:
        prefs += ["Bengal gram, dal", "Green gram, dal", "Black gram, dal"]
    return prefs


def _pick(pool: list[Food], preferences: list[str], used: set[str]) -> Food | None:
    available = [food for food in pool if food.name not in used] or list(pool)
    for preference in preferences:
        needle = preference.lower()
        for food in available:
            if food.name.lower() == needle or food.name.lower().startswith(needle):
                return food
    if not available:
        return None
    return sorted(available, key=lambda food: food.name)[0]


def _grams_for(food: Food, kcal_target: float) -> int:
    grams = int(round(kcal_target / food.energy_kcal * 100))
    return max(40, min(grams, 400))


def build_meal_plan(profile: dict, foods: list[Food] | None = None) -> MealPlan:
    table = foods if foods is not None else load_foods()
    choices = allowed_foods(table, profile)
    if not choices:
        raise PlannerError("No foods match this diet and allergy list.")

    target = CALORIE_TARGETS[profile["goal"]]
    used: set[str] = set()
    items: list[PlanItem] = []

    for meal, meal_share, roles in MEAL_SLOTS:
        meal_kcal = target * meal_share
        for role, role_share in roles:
            categories = _categories_for(role, profile)
            pool = [food for food in choices if food.category in categories]
            food = _pick(pool, _preferences(role, profile, meal), used)
            if food is None:
                raise PlannerError(f"No {role} food is available for {meal}.")
            grams = _grams_for(food, meal_kcal * role_share)
            items.append(
                PlanItem(
                    meal=meal,
                    food_name=food.name,
                    grams=grams,
                    calories=food.energy_kcal * grams / 100,
                    protein_g=food.protein_g * grams / 100,
                    source=food.source,
                )
            )
            used.add(food.name)

    return MealPlan(items=tuple(items), calorie_target=target, note=PLAN_NOTE)
