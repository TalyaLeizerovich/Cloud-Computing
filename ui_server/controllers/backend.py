# Article title with date and image alongside the article
from kafka import KafkaConsumer
import pyodbc
import json
from ui_server.models.config import KAFKA_BROKER, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from ui_server.controllers.image import article_with_images

# --- Database connection string ---
conn_str = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={DB_HOST},{DB_PORT};"
    f"DATABASE={DB_NAME};"
    f"UID={DB_USER};PWD={DB_PASSWORD};"
    f"Encrypt=yes;TrustServerCertificate=yes;"
)

# --- Consumer matched to your Producer ---
def consume_article_ids(topic_name, timeout=5000):
    """
    Receives article IDs from Kafka by topic.
    Matches the format that the Producer sends: {"article_id": ...}
    """
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset='earliest',  # Start from the earliest messages if no offset is committed
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),  # Deserialize JSON messages
        consumer_timeout_ms=timeout  # Stop consuming after timeout
    )
    article_ids = []
    for message in consumer:
        try:
            data = message.value
            article_id = data.get("article_id")
            if article_id is not None:
                article_ids.append(article_id)  # Collect valid article IDs
        except Exception as e:
            print(f"Error decoding message: {e}")
    return article_ids

# --- Fetch articles from DB by IDs ---
def fetch_articles_by_ids(ids):
    """
    Fetch articles from the DB using a list of IDs.
    Returns a list of dictionaries: {id, title, content, date, topic}
    """
    if not ids:
        return []  # Return empty list if no IDs provided
    try:
        with pyodbc.connect(conn_str, timeout=5) as conn:
            cursor = conn.cursor()
            placeholders = ','.join('?' for _ in ids)  # Prepare placeholders for SQL query
            query = f"""
                SELECT newId, comments, content, date, topic
                FROM Posts
                WHERE newId IN ({placeholders})
            """
            cursor.execute(query, ids)
            rows = cursor.fetchall()

            # Convert each row to a dictionary
            articles = []
            for row in rows:
                articles.append({
                    "id": row.newId,
                    "title": row.comments,   # Article title
                    "content": row.content,
                    "date": row.date,
                    "topic": row.topic
                })
            return articles
    except pyodbc.OperationalError as e:
        print("Error connecting to DB:", e)
        return []

# --- Format articles for Gradio ---
def format_articles(articles):
    """
    Returns Markdown text for Gradio display.
    """
    if not articles:
        return "אין כתבות זמינות לנושא זה."  # No articles available message
    md=""
    for article in articles:
        title = article.get("title", "ללא כותרת")  # Default title if missing
        date = article.get("date", "ללא תאריך")     # Default date if missing
        content = article.get("content", "")
        
        # Get content and image URL
        text, image_url = article_with_images(content)
       
        md += f"### {title}\n"
        md += f"**Date:** {date} \n\n"
        md += f"{text}\n\n"
        if image_url:
            md += f"![image]({image_url})\n\n"  # Include image if available
        md += "---\n"
    return md
