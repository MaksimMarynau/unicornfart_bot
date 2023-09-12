import requests
from bs4 import BeautifulSoup
import random
from urllib.parse import urljoin

BASE_URL = "https://aniagotuje.pl/"


def get_dinner_from_url(start_url, page_limit: int = 10) -> str:
    page = 0
    ideas = []
    while page != page_limit:
        url = urljoin(start_url, str(page))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for article in soup.find_all("article"):
            h3_element = article.find('h3')
            h3_name = h3_element.text
            link = urljoin(BASE_URL, article.find('a')['href'])
            ideas.append((h3_name, link))
        page = page + 1
    text = "Wyniki wyszukiwania:\n"
    for _ in range(5):
        title, link = random.choice(ideas)
        text += f"\n{title}: {link}"

    return text

if __name__ == "__main__":
    start_url = urljoin(BASE_URL, "/przepisy/dania-miesne/")
    text = get_dinner_from_url(start_url)
    print(text)