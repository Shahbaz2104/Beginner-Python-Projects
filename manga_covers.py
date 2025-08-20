import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://chainsaw-man.fandom.com"
PAGE_URL = "https://chainsaw-man.fandom.com/wiki/Chainsaw_Man_(Manga)"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Step 1: Get the main manga page
resp = requests.get(PAGE_URL, headers=HEADERS)
soup = BeautifulSoup(resp.text, "html.parser")

# Step 2: Find links to volume file pages
volume_links = []
for a in soup.find_all("a", href=True):
    if "File:Volume_" in a["href"] and a["href"].endswith(".png"):
        full_link = urljoin(BASE_URL, a["href"])
        if full_link not in volume_links:
            volume_links.append(full_link)

print(f"Found {len(volume_links)} volume file pages.")

# Step 3: Make folder
os.makedirs("covers", exist_ok=True)

# Step 4: Visit each file page & download image
for link in volume_links:
    print(f"Visiting: {link}")
    file_page = requests.get(link, headers=HEADERS)
    file_soup = BeautifulSoup(file_page.text, "html.parser")

    # High-res image is inside .fullMedia a
    full_image_tag = file_soup.select_one(".fullMedia a")
    if full_image_tag:
        img_url = urljoin(BASE_URL, full_image_tag["href"])
        filename = os.path.basename(img_url)
        print(f"Downloading {filename}...")
        img_data = requests.get(img_url, headers=HEADERS).content
        with open(os.path.join("covers", filename), "wb") as f:
            f.write(img_data)

print("✅ Done! All covers saved in 'covers' folder.")
