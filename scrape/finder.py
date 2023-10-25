from bs4 import BeautifulSoup
import requests
import re

url = "https://medium.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

links = []
article_pattern = re.compile(r"https://medium.com/@[^/]+/[^/]+")

for a_tag in soup.find_all("a", {"rel": "noopener follow"}):
    href = a_tag.get("href")
    if href.startswith("/@"):
        full_url = f"https://medium.com{href}"
        if article_pattern.match(full_url):
            links.append(full_url)

print(links)
