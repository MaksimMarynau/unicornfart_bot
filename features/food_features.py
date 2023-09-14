import requests
from bs4 import BeautifulSoup
import random
from urllib.parse import urljoin
from unidecode import unidecode


BASE_URL = "https://aniagotuje.pl/"


def build_url(base_url, path):
    return urljoin(base_url, path)


def get_dinner_from_url(start_url, page_limit: int = 10) -> str:
    page = 0
    ideas = []
    while page != page_limit:
        url = build_url(start_url, str(page))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for article in soup.find_all("article"):
            h3_element = article.find('h3')
            h3_name = h3_element.text
            article_path = article.find('a')['href']
            link = build_url(start_url, article_path)
            ideas.append((h3_name, link))
        page = page + 1
    text = "Wyniki wyszukiwania:\n"
    for _ in range(5):
        title, link = random.choice(ideas)
        text += f"\n{title}: {link}"

    return text


def get_all_tags(start_url) -> str:
    all_tags = []
    response = requests.get(start_url)
    soup = BeautifulSoup(response.text, "html.parser")
    for div in soup.find("div", class_="tags"):
        tag = div.span.string.strip()
        all_tags.append(tag)

    return all_tags


def get_tag_dishes(start_url, tag_name: str, page_limit: int = 5) -> str:
    text = "Wyniki wyszukiwania:\n"
    page = 0
    ideas = []
    available_tags = get_all_tags(start_url)
    if tag_name in available_tags:
        while page != page_limit:
            tag_name = unidecode(tag_name)
            url = build_url(start_url, f"tag/{tag_name}/{page}")
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            for article in soup.find_all("article"):
                h3_element = article.find('h3')
                h3_name = h3_element.text
                article_path = article.find('a')['href']
                link = build_url(BASE_URL, article_path)
                ideas.append((h3_name, link))
            page = page + 1
    
        for _ in range(5):
            title, link = random.choice(ideas)
            text += f"\n{title}: {link}"
    else:
        text += f"Nie ma takiego tagu: <<< {tag_name} >>>"

    return text


if __name__ == "__main__":
    text = get_all_tags(BASE_URL)
    print(text)
