# app/classifier.py

import requests  # For making HTTP requests to external APIs
import json  # For handling JSON serialization and deserialization


with open("keys.json", "r") as f:
    keys = json.load(f)

HF_API_TOKEN = keys["HF_API_TOKEN"]

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"  # HuggingFace zero-shot model endpoint
CANDIDATE_LABELS = ["technology", "politics", "sports", "health", "business", "entertainment", "science"]  # Possible topics


def classify_article(article: dict):
    """
    Receives a minimal article dict with 'content' and 'publishedAt',
    classifies it with HuggingFace zero-shot, returns the article with topic.
    """
    text_to_classify = article.get("content", "")  # Extract content or empty string if missing
    published_at = article.get("publishedAt", "")  # Extract published date or empty string if missing

    if not text_to_classify:
        return {"status": "error", "message": "No content to classify."}  # Return error if content is empty

    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",  # Set Bearer token for authorization
        "Content-Type": "application/json"  # Specify JSON content type
    }

    payload = {
        "inputs": text_to_classify,  # Text to classify
        "parameters": {
            "candidate_labels": CANDIDATE_LABELS,  # The set of labels to classify against
            "multi_label": False  # Single-label classification
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)  # Make POST request to HuggingFace API
        response.raise_for_status()  # Raise exception for HTTP errors
        classification = response.json()  # Parse JSON response
        top_label = classification["labels"][0]  # Get the top predicted label

        minimal_json = {
            "publishedAt": published_at,
            "content": text_to_classify,
            "topic": top_label  # Add predicted topic to article
        }

        # Optionally save the classified article to a JSON file
        with open("article_classified_full.json", "w", encoding="utf-8") as f:
            json.dump(minimal_json, f, ensure_ascii=False, indent=2)

        return {"status": "success", "article": minimal_json}  # Return success with classified article

    except Exception as e:
        return {"status": "error", "message": str(e)}  # Return error if request or processing fails
