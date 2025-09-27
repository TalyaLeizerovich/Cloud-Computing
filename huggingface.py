import requests
import json

# 1️⃣ קובץ JSON של הכתבה (כמו שהכנת קודם)
with open("article_guardian_minimal.json", "r", encoding="utf-8") as f:
    article_data = json.load(f)

text_to_classify = article_data.get("content", "")
published_at = article_data.get("publishedAt", "")

# 2️⃣ רשימת קטגוריות לניסוי
candidate_labels = ["technology", "politics", "sports", "health", "business", "entertainment", "science"]

# 3️⃣ API Hugging Face Zero-Shot
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
HF_API_TOKEN = ""  # הכנסי את ה‑token שלך

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "inputs": text_to_classify,
    "parameters": {
        "candidate_labels": candidate_labels,
        "multi_label": False  # רק קטגוריה אחת
    }
}

response = requests.post(API_URL, headers=headers, json=payload)

if response.status_code == 200:
    classification = response.json()
    
    # בוחרים את הקטגוריה עם ההסתברות הכי גבוהה
    top_label = classification["labels"][0]

    # JSON מינימלי עם תוכן, תאריך ונושא מוביל
    minimal_json = {
        "publishedAt": published_at,
        "content": text_to_classify,
        "topic": top_label
    }

    # שמירה לקובץ
    with open("article_classified_full.json", "w", encoding="utf-8") as f:
        json.dump(minimal_json, f, ensure_ascii=False, indent=2)

    print("✅ נשמר JSON עם תוכן + תאריך + נושא מוביל:", top_label)
else:
    print("❌ שגיאה:", response.status_code, response.text)
