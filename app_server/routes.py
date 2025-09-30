# app/routes.py
from fastapi import APIRouter
from app_server.news import fetch_latest_article
from app_server.classifier import classify_article
from app_server.db import save_to_db

router = APIRouter()

# This endpoint processes an article workflow (fetch, classify, save, return results)
@router.get("/process/{topic}")
def process_article(topic: str):
    """
    Fetches the latest article, classifies it, saves to DB, and returns the result.
    """

    # Step 1: Fetch the latest article
    news_result = fetch_latest_article()
    if news_result.get("status") != "success":
        return news_result  # could be "empty" or "error"

    article = news_result["article"]

    # Optional: check if the article matches the requested topic
    # Currently ignoring the topic parameter, but filtering can be added

    # Step 2: Classify the article using HuggingFace
    classified_result = classify_article(article)
    if classified_result.get("status") != "success":
        return classified_result

    classified_article = classified_result["article"]

    # Step 3: Save the classified article to the database
    db_result = save_to_db(classified_article)

    # Step 4: Return all information to the user (original, classified, DB result)
    return {
        "news": article,
        "classified": classified_article,
        "db": db_result
    }
