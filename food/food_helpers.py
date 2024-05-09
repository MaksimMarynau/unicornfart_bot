import requests
from bs4 import BeautifulSoup
import random
from urllib.parse import urljoin
from unicornfart_utils import configs
from unidecode import unidecode
from functools import lru_cache


def build_url(base_url, path):
    return urljoin(base_url, path)


@lru_cache(maxsize=128)
def get_search_ideas(base_url, query, page_limit: int = 10) -> list:
    page = 0
    ideas = {}
    try:
        while page != page_limit:
            modified_url = build_url(base_url, f"szukaj/{str(page)}?s={query}/")
            response = requests.get(modified_url)
            if (
                response.status_code == 404
            ):  # FIXME include other error codes(make better validation)
                break
            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all("article")
            no_results = soup.find("h2", class_="error-title")
            if not articles and no_results:
                raise ValueError(no_results.text)  # TODO: Create own type of error
            for article in articles:
                h3_element = article.find("h3")
                h3_name = h3_element.text
                article_path = article.find("a")["href"]
                link = build_url(configs.FOOD_PURE_URL, article_path)
                ideas[h3_name] = link
            page = page + 1
    except ValueError as err:
        if ideas:
            return ideas
        raise err
    return ideas


def build_text(text: str, ideas: dict) -> str:
    random_idea = random.choice(list(ideas.items()))
    text += f"\n{random_idea[0]}: {random_idea[1]}"
    return text


def normalize_pl_chars(char: str) -> str:
    return unidecode(char)
