import requests
from bs4 import BeautifulSoup
import random
from urllib.parse import urljoin
from unicornfart_utils import configs
from unidecode import unidecode
from collections import defaultdict

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


def get_all_tags(base_url) -> list:
    all_tags = []
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    for div in soup.find("div", class_="tags"):
        tag = div.span.string.strip()
        tag = normalize_tag(tag)
        all_tags.append(tag)

    return all_tags


def get_all_categories(base_url) -> dict:
    categories_dict = defaultdict(lambda: None)
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    left_nav = soup.find('nav', class_='leftNav')
    if left_nav:
        categories = left_nav.find_all('div', class_="cat-group")
        for category in categories:
            category_name = category.string     
            categories_dict[category_name] = []
            ul_elements = category.find_next('ul', id=True)
            for ul_element in ul_elements:
                li_link = ul_element.a['href']
                link = build_url(base_url, li_link)
                categories_dict[category_name].append(link)
    return categories_dict


def normalize_tag(tag: str) -> str:
    return unidecode(tag.replace(" ", "-"))