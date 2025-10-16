# app/news_fetcher.py
import requests
import json
import os
from datetime import datetime, date

# קריאת קובץ הקונפיג
with open("keys.json", "r") as f:
    keys = json.load(f)
GUARDIAN_KEY = keys["GUARDIAN_API_KEY"]

# Endpoint for The Guardian API
ENDPOINT = "https://content.guardianapis.com/search"
# File to store fetched articles
OUTPUT_FILE = "articles_guardian.json"

# Load the existing file if it already exists
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        all_articles = json.load(f)
else:
    all_articles = []

# Keep track of article IDs that were already saved
seen_ids = {a["id"] for a in all_articles}


def fetch_latest_article():
    """Fetch the latest article from The Guardian and save it if it's new."""
    today = date.today().isoformat()

    params = {
        "order-by": "newest",
        "from-date": today,
        "page-size": 50,
        "show-fields": "bodyText",
        "api-key": GUARDIAN_KEY
    }

    try:
        # Make a request to The Guardian API
        resp = requests.get(ENDPOINT, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # Extract results list
        results = data.get("response", {}).get("results", [])
        if not results:
            return {"status": "empty", "message": "No articles found today."}

        for item in results:
            article_id = item.get("id")
            # Check if the article is new
            if article_id not in seen_ids:
                published = item.get("webPublicationDate")
                body_text = item.get("fields", {}).get("bodyText", "")
                title = item.get("webTitle", "")  # ✅ כותרת הכתבה

                # Minimal structure for saving the article
                minimal = {
                    "id": article_id,
                    "fetchedAt": datetime.now().isoformat(),
                    "publishedAt": published,
                    "content": body_text,
                    "comments": title  # ✅ הכותרת נשמרת כאן

                }

                # Insert at the beginning so the newest article is first
                all_articles.insert(0, minimal)
                seen_ids.add(article_id)

                # Save updated list to file
                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                    json.dump(all_articles, f, ensure_ascii=False, indent=2)

                return {"status": "success", "article": minimal}

        # If all fetched articles are already stored
        return {"status": "empty", "message": "All recent articles already saved."}

    except Exception as e:
        # Handle any error during request or processing
        return {"status": "error", "message": str(e)}
