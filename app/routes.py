# app/routes.py
from fastapi import APIRouter
from app.news import fetch_latest_article
from app.classifier import classify_article
from app.db import save_to_db

router = APIRouter()


@router.get("/process/{topic}")
def process_article(topic: str):
    """
    Fetches the latest article, classifies it, saves to DB, and returns the result.
    """
    # שלב 1: Fetch latest article
    news_result = fetch_latest_article()
    if news_result.get("status") != "success":
        return news_result  # יכול להיות "empty" או "error"

    article = news_result["article"]

    # אם רוצים, אפשר לבדוק שהכתבה מתאימה לנושא שהמשתמש ביקש
    # כרגע מתעלמים מהפרמטר topic, או ניתן להוסיף פילטר

    # שלב 2: Classify with HuggingFace
    classified_result = classify_article(article)
    if classified_result.get("status") != "success":
        return classified_result

    classified_article = classified_result["article"]

    # שלב 3: Save to DB
    db_result = save_to_db(classified_article)

    # החזרת המידע למשתמש
    return {
        "news": article,
        "classified": classified_article,
        "db": db_result
    }
