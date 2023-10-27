from food import food_helpers
from unicornfart_utils import configs


def get_ideas_from_url(base_url) -> str:
    ideas = food_helpers.get_all_ideas(base_url)
    text = "Wyniki wyszukiwania:\n"
    text = food_helpers.build_text(text, ideas)
    return text


def get_tag_dishes(base_url, tag_name: str) -> str:
    text = "Wyniki wyszukiwania:\n"
    available_tags = food_helpers.get_all_tags(base_url)
    if tag_name in available_tags:
        url = food_helpers.build_url(base_url, f"tag/{tag_name}/")
        ideas = food_helpers.get_all_ideas(url)
        text = food_helpers.build_text(text, ideas)
    else:
        text += f"Nie ma takiego tagu: <<< {tag_name} >>>"

    return text


def get_available_tags(base_url, elements_per_line: int = 3) -> str:
    text = "Wszystkie dostępne tagi:\n"
    tags = food_helpers.get_all_tags(base_url)
    for i, tag in enumerate(tags, start=1):
        text += f"{i}.{tag}"
        if i % elements_per_line == 0:
            text += "\n"
        else:
            text += ", "
    return text


if __name__ == "__main__":
    text = food_helpers.get_all_tags(configs.FOOD_PURE_URL)
    print(text)
