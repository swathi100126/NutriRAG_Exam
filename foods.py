"""Load the IFCT food table and keep foods that match a diet and allergy list."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from config import DOCUMENTS_PATH

FOODS_CSV = Path(DOCUMENTS_PATH) / "indianfood.csv"

GOALS = ("Lose weight", "Maintain weight", "Gain muscle")
DIETS = ("Vegetarian", "Vegan", "Eggetarian", "Non-vegetarian")
ALLERGY_OPTIONS = (
    "Dairy",
    "Egg",
    "Nuts",
    "Peanut",
    "Gluten",
    "Soy",
    "Fish",
    "Shellfish",
)
CALORIE_TARGETS = {
    "Lose weight": 1600,
    "Maintain weight": 2000,
    "Gain muscle": 2400,
}

ANIMAL_CATEGORIES = {
    "Animal Meat",
    "Poultry",
    "Marine Fish",
    "Fresh Water Fish and Shellfish",
    "Marine Shellfish",
    "Marine Mollusks",
}
EGG_CATEGORIES = {"Egg and Egg Products"}
DAIRY_CATEGORIES = {"Milk and Milk Products"}
FISH_CATEGORIES = {"Marine Fish", "Fresh Water Fish and Shellfish"}
SHELLFISH_CATEGORIES = {"Marine Shellfish", "Marine Mollusks"}
SKIP_CATEGORIES = {
    "Condiments and Spices",
    "Sugars",
    "Edible Oils and Fats",
    "Miscellaneous Foods",
}

_DAIRY_WORDS = (
    "milk",
    "paneer",
    "curd",
    "cheese",
    "ghee",
    "khoa",
    "buttermilk",
    "butter",
    "channa",
    "dahi",
)
_NUT_WORDS = ("almond", "cashew", "walnut", "pistachio", "hazelnut", "pecan", "pine nut")
_PEANUT_WORDS = ("peanut", "ground nut", "groundnut")
_GLUTEN_WORDS = ("wheat", "barley", "rye", "semolina", "maida", "gluten", "bread")
_SOY_WORDS = ("soy", "soya")
_SHELLFISH_WORDS = (
    "prawn",
    "shrimp",
    "crab",
    "lobster",
    "oyster",
    "mussel",
    "squid",
    "shellfish",
)


@dataclass(frozen=True)
class Food:
    name: str
    category: str
    energy_kcal: float
    protein_g: float
    source: str


def load_foods(path: Path | None = None) -> list[Food]:
    csv_path = path or FOODS_CSV
    foods: list[Food] = []
    with csv_path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            try:
                energy = float(row["energy_kcal"])
                protein = float(row["protein_g"])
            except (TypeError, ValueError):
                continue
            name = (row.get("name") or "").strip()
            if not name or energy <= 0:
                continue
            foods.append(
                Food(
                    name=name,
                    category=(row.get("category") or "").strip(),
                    energy_kcal=energy,
                    protein_g=protein,
                    source=(row.get("source") or "IFCT2017").strip() or "IFCT2017",
                )
            )
    return foods


def validate_profile(age: int, goal: str, diet: str, allergies: list[str] | tuple[str, ...]) -> dict:
    age_value = int(age)
    if age_value < 16 or age_value > 80:
        raise ValueError("Age must be between 16 and 80.")
    if goal not in GOALS:
        raise ValueError("Choose a health goal.")
    if diet not in DIETS:
        raise ValueError("Choose a diet.")
    chosen = []
    for allergy in allergies or []:
        if allergy not in ALLERGY_OPTIONS:
            raise ValueError(f"Unknown allergy: {allergy}")
        if allergy not in chosen:
            chosen.append(allergy)
    return {
        "age": age_value,
        "goal": goal,
        "diet": diet,
        "allergies": chosen,
    }


def _contains_any(name: str, words: tuple[str, ...]) -> bool:
    lowered = name.lower()
    return any(word in lowered for word in words)


def food_allowed(food: Food, diet: str, allergies: list[str] | tuple[str, ...]) -> bool:
    if food.category in SKIP_CATEGORIES:
        return False

    blocked = set()
    if diet == "Vegan":
        blocked |= ANIMAL_CATEGORIES | EGG_CATEGORIES | DAIRY_CATEGORIES
    elif diet == "Vegetarian":
        blocked |= ANIMAL_CATEGORIES | EGG_CATEGORIES
    elif diet == "Eggetarian":
        blocked |= ANIMAL_CATEGORIES
    if food.category in blocked:
        return False

    allergy_set = set(allergies or [])
    if "Dairy" in allergy_set and (
        food.category in DAIRY_CATEGORIES or _contains_any(food.name, _DAIRY_WORDS)
    ):
        return False
    if "Egg" in allergy_set and (
        food.category in EGG_CATEGORIES or "egg" in food.name.lower()
    ):
        return False
    if "Nuts" in allergy_set and _contains_any(food.name, _NUT_WORDS):
        return False
    if "Peanut" in allergy_set and _contains_any(food.name, _PEANUT_WORDS):
        return False
    if "Gluten" in allergy_set and _contains_any(food.name, _GLUTEN_WORDS):
        return False
    if "Soy" in allergy_set and _contains_any(food.name, _SOY_WORDS):
        return False
    if "Fish" in allergy_set and (
        food.category in FISH_CATEGORIES or "fish" in food.name.lower()
    ):
        return False
    if "Shellfish" in allergy_set and (
        food.category in SHELLFISH_CATEGORIES or _contains_any(food.name, _SHELLFISH_WORDS)
    ):
        return False
    return True


def allowed_foods(foods: list[Food], profile: dict) -> list[Food]:
    return [
        food
        for food in foods
        if food_allowed(food, profile["diet"], profile.get("allergies") or [])
    ]
