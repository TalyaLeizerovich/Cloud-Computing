import requests
import json

GUARDIAN_KEY = "0b15e60e-4044-4006-b169-17230da9666f"

# מבקשים את הכתבה ה- newest עם full text (bodyText)
endpoint = "https://content.guardianapis.com/search"
params = {
    "order-by": "newest",
    "page-size": 1,
    "show-fields": "bodyText",
    "api-key": GUARDIAN_KEY
}

resp = requests.get(endpoint, params=params)
resp.raise_for_status()
data = resp.json()

results = data.get("response", {}).get("results", [])
if not results:
    print("לא נמצאו כתבות")
else:
    item = results[0]
    published = item.get("webPublicationDate")    # תאריך פרסום
    body_text = item.get("fields", {}).get("bodyText", "")  # הטקסט המלא (plain text)
    
    minimal = {
        "publishedAt": published,
        "content": body_text
    }

    with open("article_guardian_minimal.json", "w", encoding="utf-8") as f:
        json.dump(minimal, f, ensure_ascii=False, indent=2)

    print("נשמר article_guardian_minimal.json — תוכן + תאריך")
