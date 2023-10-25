from bs4 import BeautifulSoup
import requests
import re
import json

url = "https://medium.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

links = set()
article_pattern = re.compile(r"https://medium.com/@[^/]+/[^/]+")

for a_tag in soup.find_all("a", {"rel": "noopener follow"}):
    href = a_tag.get("href")
    if href.startswith("/@"):
        full_url = f"https://medium.com{href}"
        if article_pattern.match(full_url):
            links.add(full_url)

print(links)
with open("config.json", "r") as f:
    config = json.load(f)

# Update urls in the config dictionary
config["urls"] = list(links)

# Write updated config back to config.json
with open("config.json", "w") as f:
    json.dump(config, f, indent=4)
