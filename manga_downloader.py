#!/usr/bin/env python3
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://ww5.readchainsawman.com/chapter/chainsaw-man-chapter-"
START = 210
END = 211

HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64)'}

for chap in range(START, END+1):
    chap_url = f"{BASE}{chap}/"
    folder = os.path.expanduser(f"~/Manga/C/Chapter_{chap}/")	
    os.makedirs(folder, exist_ok=True)
    print(f"Fetching chapter {chap}: {chap_url}")

    resp = requests.get(chap_url, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, "html.parser")
    imgs = soup.find_all("img")
    print(f"  Found {len(imgs)} <img> tags")

    count = 1
    for img in imgs:
        src = img.get("data-src") or img.get("src")
        if not src or src.lower().startswith("data:") or "ads" in src:
            continue
        img_url = urljoin(chap_url, src)
        ext = os.path.splitext(img_url)[1].split('?')[0] or '.jpg'
        filename = os.path.join(folder, f"{count:03d}{ext}")
        try:
            print(f"   ► Downloading {img_url} to {filename}")
            img_data = requests.get(img_url, headers=HEADERS).content
            with open(filename, "wb") as f:
                f.write(img_data)
            count += 1
        except Exception as e:
            print("     ⚠️ Failed:", e)

    print(f" Chapter {chap} done: downloaded {count-1} images.\n")
