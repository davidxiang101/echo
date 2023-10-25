import requests
from bs4 import BeautifulSoup
import json
import sys

sys.path.append("/Users/cactuscolada/Projects/echo")
from storage.storage_manager import save_to_db

# Load scraping config from a JSON file
with open("config.json", "r") as file:
    config = json.load(file)


def fetch_article(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    else:
        print(f"Failed to retrieve {url}")
        return None


def extract_content(soup, tag):
    elements = soup.find_all(tag)
    if elements:
        return " ".join([element.get_text() for element in elements])
    return None


def main():
    urls = config[
        "urls"
    ]  # Assume the JSON config has a key "urls" with a list of URLs to scrape

    for url in urls:
        soup = fetch_article(url)
        if soup:
            # Assume articles have text inside <p> tags with class "content"
            content = extract_content(soup, "p")
            if content:
                print(f"Article content: {content}")
                if content:
                    save_to_db(url, content)


if __name__ == "__main__":
    main()
