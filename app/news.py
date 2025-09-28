# app/news_fetcher.py
import requests
import json
import os
from datetime import datetime, date

GUARDIAN_KEY = "0b15e60e-4044-4006-b169-17230da9666f"
ENDPOINT = "https://content.guardianapis.com/search"
OUTPUT_FILE = "articles_guardian.json"

# טוענים את הקובץ אם כבר קיים
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        all_articles = json.load(f)
else:
    all_articles = []

# שמירה של ids שכבר הורדנו
seen_ids = {a["id"] for a in all_articles}


def fetch_latest_article():
    """Fetch the latest article from The Guardian and save it if new."""
    today = date.today().isoformat()

    params = {
        "order-by": "newest",
        "from-date": today,
        "page-size": 50,
        "show-fields": "bodyText",
        "api-key": GUARDIAN_KEY
    }

    try:
        resp = requests.get(ENDPOINT, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        results = data.get("response", {}).get("results", [])
        if not results:
            return {"status": "empty", "message": "No articles found today."}

        for item in results:
            article_id = item.get("id")
            if article_id not in seen_ids:
                published = item.get("webPublicationDate")
                body_text = item.get("fields", {}).get("bodyText", "")

                minimal = {
                    "id": article_id,
                    "fetchedAt": datetime.now().isoformat(),
                    "publishedAt": published,
                    "content": body_text
                }

                # מוסיפים לראש הרשימה כדי שהחדשה ביותר תהיה בראש
                all_articles.insert(0, minimal)
                seen_ids.add(article_id)

                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                    json.dump(all_articles, f, ensure_ascii=False, indent=2)

                return {"status": "success", "article": minimal}

        return {"status": "empty", "message": "All recent articles already saved."}

    except Exception as e:
        return {"status": "error", "message": str(e)}
