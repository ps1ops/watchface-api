from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# CORS, чтобы iOS-приложение могло обращаться
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/watchfaces")
def get_watchfaces(page: int = Query(1, ge=1)):
    url = f"https://amazfitwatchfaces.com/mi-band-7?page={page}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    items = soup.select(".watchface-item")
    results = []

    for item in items:
        name_tag = item.select_one(".title")
        img_tag = item.select_one("img")
        link_tag = item.select_one("a")

        if name_tag and img_tag and link_tag:
            name = name_tag.text.strip()
            preview = img_tag.get("data-src")
            relative = link_tag.get("href")
            full_link = f"https://amazfitwatchfaces.com{relative}"

            results.append({
                "name": name,
                "previewImageURL": preview,
                "pageURL": full_link
            })

    return results
