# # app/article_images.py
# from transformers import pipeline
# import requests

# # --- NER pipeline של Hugging Face ---
# ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")

# # --- API של מאגר תמונות (Pexels או Unsplash) ---
# PEXELS_API_KEY = "0b15e60e-4044-4006-b169-17230da9666f"

# def get_image_for_entity(entity):
#     """ מקבלת ישות ומחזירה URL של תמונה """
#     headers = {"Authorization": PEXELS_API_KEY}
#     params = {"query": entity, "per_page": 1}
#     response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params).json()
#     if response.get("photos"):
#         return response["photos"][0]["src"]["medium"]
#     # תמונה ברירת מחדל אם אין תוצאה
#     return "https://example.com/default.jpg"

# def article_with_images(article_text):
#     """ מחזירה טקסט + URL של תמונה רלוונטית """
#     # מזהה ישויות מרכזיות
#     entities = [e["word"] for e in ner_pipeline(article_text) if e["score"] > 0.85]
#     # מחפש תמונות לכל ישות
#     images = [get_image_for_entity(ent) for ent in entities]
#     # מחזיר תמונה אחת (או ברירת מחדל)
#     image_to_show = images[0] if images else "https://example.com/default.jpg"
#     return article_text, image_to_show

# app/article_images.py
import requests
import json
# קריאת קובץ הקונפיג
with open("keys.json", "r") as f:
    keys = json.load(f)

# שימוש במפתחות מתוך הקובץ
HF_API_TOKEN = keys["HF_API_TOKEN"]
GUARDIAN_KEY = keys["GUARDIAN_API_KEY"]

# --- API של Hugging Face Inference ---

HF_NER_MODEL = "dbmdz/bert-large-cased-finetuned-conll03-english"



def ner_via_hf_api(text):
    """
    שולח את הטקסט ל-Hugging Face API ומקבל ישויות (NER).
    """
    if not isinstance(text, str):
        text = str(text)

    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {"inputs": text}

    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{HF_NER_MODEL}",
            headers=headers,
            json=payload,
            timeout=30
        )
        data = response.json()
    except Exception as e:
        print("Error calling HF API:", e)
        return []

    # אם HF מחזיר שגיאה (מחרוזת) במקום רשימה, מחזירים רשימה ריקה
    if isinstance(data, dict) and data.get("error"):
        print("HF API error:", data["error"])
        return []
    if not isinstance(data, list):
        print("HF API returned unexpected data:", data)
        return []

    # מסנן ישויות עם סבירות גבוהה
    entities = [item["word"] for item in data if item.get("score", 0) > 0.85]
    return entities

def get_guardian_image_for_entity(entity):
    """
    מקבל ישות ומחזיר URL של תמונה מתוך The Guardian.
    """
    if not isinstance(entity, str):
        entity = str(entity)

    url = "https://content.guardianapis.com/search"
    params = {
        "q": entity,
        "show-fields": "thumbnail,main",
        "page-size": 1,
        "api-key": GUARDIAN_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=15).json()
        results = response.get("response", {}).get("results", [])
        if results:
            fields = results[0].get("fields", {})
            return fields.get("thumbnail") or fields.get("main") or "https://m.media-amazon.com/images/I/71OEDHkyS-L._UF894,1000_QL80_.jpg"
    except Exception as e:
        print("Error fetching image from The Guardian:", e)

    return "https://m.media-amazon.com/images/I/71OEDHkyS-L._UF894,1000_QL80_.jpg"

def article_with_images(article_text):
    """
    מחזירה טקסט + URL של תמונה רלוונטית לפי ישויות ב-Hugging Face API.
    """
    entities = ner_via_hf_api(article_text)
    images = [get_guardian_image_for_entity(ent) for ent in entities]
    image_to_show = images[0] if images else "https://m.media-amazon.com/images/I/71OEDHkyS-L._UF894,1000_QL80_.jpg"
    return str(article_text), image_to_show
