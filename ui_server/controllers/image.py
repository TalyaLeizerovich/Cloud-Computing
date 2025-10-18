# app/article_images.py
import requests
import json

# Read configuration file
with open("keys.json", "r") as f:
    keys = json.load(f)

# Use API keys from the config file
HF_API_TOKEN = keys["HF_API_TOKEN"]
GUARDIAN_KEY = keys["GUARDIAN_API_KEY"]

# --- Hugging Face Inference API ---
HF_NER_MODEL = "dbmdz/bert-large-cased-finetuned-conll03-english"

def ner_via_hf_api(text):
    """
    Sends text to Hugging Face API and receives named entities (NER).
    """
    if not isinstance(text, str):
        text = str(text)  # Ensure input is a string

    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {"inputs": text}

    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{HF_NER_MODEL}",
            headers=headers,
            json=payload,
            timeout=30  # Wait up to 30 seconds
        )
        data = response.json()
    except Exception as e:
        print("Error calling HF API:", e)
        return []

    # If HF returns an error instead of a list, return empty list
    if isinstance(data, dict) and data.get("error"):
        print("HF API error:", data["error"])
        return []
    if not isinstance(data, list):
        print("HF API returned unexpected data:", data)
        return []

    # Filter entities with high confidence (> 0.85)
    entities = [item["word"] for item in data if item.get("score", 0) > 0.85]
    print("Extracted entities:", entities)
    return entities

def get_guardian_image_for_entity(entity):
    """
    Receives an entity and returns an image URL from The Guardian.
    """
    if not isinstance(entity, str):
        entity = str(entity)  # Ensure entity is a string

    url = "https://content.guardianapis.com/search"
    print("url", url)
    params = {
        "q": entity,  # Search query
        "show-fields": "thumbnail,main",  # Request image fields
        "page-size": 1,  # Only need the first result
        "api-key": GUARDIAN_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=15).json()
        results = response.get("response", {}).get("results", [])
        if results:
            fields = results[0].get("fields", {})
            return fields.get("thumbnail") or fields.get("main") or None
    except Exception as e:
        print("Error fetching image from The Guardian:", e)

    return None

def article_with_images(article_text):
    """
    Returns a tuple of (text, image URL).
    Returns (text, None) if no valid image is found.
    """
    entities = ner_via_hf_api(article_text)  # Extract entities from text
    
    for ent in entities:
        url = get_guardian_image_for_entity(ent)
        # Return the first valid image URL
        if url:  
            return (article_text, url)
    
    # If no image found, return text with None
    return (article_text, None)
