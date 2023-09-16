
from unidecode import unidecode
from features import food_helpers
from features import PURE_URL


def get_dinner_from_url(base_url) -> str:
    ideas = food_helpers.get_ideas(base_url)
    text = "Wyniki wyszukiwania:\n"
    text = food_helpers.build_text(text, ideas)
    return text


def get_tag_dishes(base_url, tag_name: str) -> str:
    text = "Wyniki wyszukiwania:\n"
    available_tags = food_helpers.get_all_tags(base_url)
    if tag_name in available_tags:
        tag_name = unidecode(tag_name)
        url = food_helpers.build_url(base_url, f"tag/{tag_name}/")
        ideas = food_helpers.get_ideas(url, page_limit=5)
        text = food_helpers.build_text(text, ideas)
    else:
        text += f"Nie ma takiego tagu: <<< {tag_name} >>>"

    return text


if __name__ == "__main__":
    text = food_helpers.get_all_tags(PURE_URL)
    print(text)
