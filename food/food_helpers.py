import requests
from bs4 import BeautifulSoup
import random
from urllib.parse import urljoin
from unicornfart_utils import configs
from unidecode import unidecode


def build_url(base_url, path):
    return urljoin(base_url, path)


def get_all_ideas(base_url, page_limit: int = 30) -> list:
    page = 0
    ideas = []
    while page != page_limit:
        modified_url = build_url(base_url, str(page))
        response = requests.get(modified_url)
        if response.status_code == 404: # FIXME include other error codes(make better validation)
            break
        soup = BeautifulSoup(response.text, "html.parser")
        for article in soup.find_all("article"):
            h3_element = article.find('h3')
            h3_name = h3_element.text
            article_path = article.find('a')['href']
            link = build_url(configs.FOOD_PURE_URL, article_path)
            ideas.append((h3_name, link))
        page = page + 1
    return ideas


def build_text(text, ideas) -> str:
    for _ in range(2):
        title, link = random.choice(ideas)
        text += f"\n{title}: {link}"
    return text


def get_all_tags(base_url) -> str:
    all_tags = []
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    for div in soup.find("div", class_="tags"):
        tag = div.span.string.strip()
        tag = normalize_tag(tag)
        all_tags.append(tag)

    return all_tags


def normalize_tag(tag: str) -> str:
    return unidecode(tag.replace(" ", "-"))