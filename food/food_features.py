from food import food_helpers
import json
from pathlib import Path


def search_idea(base_url, query: str) -> str:
    text = "Wyniki wyszukiwania:\n"
    try:
        ideas = food_helpers.get_search_ideas(base_url, query)
        text = food_helpers.build_text(text, ideas)
    except ValueError as err:
        text += str(err)
    return text


def get_available_categories() -> str:
    text = "Wszystkie dostępne kategorie:\n"
    categories_file = Path(__file__).parent / "categories_data.json"
    categories_data = json.loads(categories_file.read_text())
    for key, value in categories_data.items():
        text += f"\n{food_helpers.normalize_pl_chars(key)}\n" + "\n".join(value)
    return text


if __name__ == "__main__":
    pass
