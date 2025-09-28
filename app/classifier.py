# app/classifier.py
import os
import requests
import json

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
CANDIDATE_LABELS = ["technology", "politics", "sports", "health", "business", "entertainment", "science"]


def classify_article(article: dict):
    """
    Receives a minimal article dict with 'content' and 'publishedAt',
    classifies it with HuggingFace zero-shot, returns the article with topic.
    """
    text_to_classify = article.get("content", "")
    published_at = article.get("publishedAt", "")

    if not text_to_classify:
        return {"status": "error", "message": "No content to classify."}

    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": text_to_classify,
        "parameters": {
            "candidate_labels": CANDIDATE_LABELS,
            "multi_label": False
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        classification = response.json()
        top_label = classification["labels"][0]

        minimal_json = {
            "publishedAt": published_at,
            "content": text_to_classify,
            "topic": top_label
        }

        # אפשר גם לשמור לקובץ אם רוצים
        with open("article_classified_full.json", "w", encoding="utf-8") as f:
            json.dump(minimal_json, f, ensure_ascii=False, indent=2)

        return {"status": "success", "article": minimal_json}

    except Exception as e:
        return {"status": "error", "message": str(e)}
