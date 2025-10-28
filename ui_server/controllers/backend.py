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

# --- Consume article IDs from Kafka ---
def consume_article_ids(topic_name, timeout=5000):
    # Create a Kafka consumer for the given topic
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset='earliest',  # Start reading from the beginning if no offset
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),  # Decode JSON messages
        consumer_timeout_ms=timeout  # Stop consuming after a timeout
    )
    article_ids = []
    # Iterate over messages received from Kafka
    for message in consumer:
        try:
            data = message.value
            article_id = data.get("article_id")
            if article_id is not None:
                article_ids.append(article_id)
        except Exception as e:
            print(f"Error decoding message: {e}")
    return article_ids

# --- Fetch articles by IDs from DB ---
def fetch_articles_by_ids(ids):
    # If no IDs provided, return an empty list
    if not ids:
        return []
    try:
        # Establish a connection to the SQL Server database
        with pyodbc.connect(conn_str, timeout=5) as conn:
            cursor = conn.cursor()
            # Prepare placeholders for the SQL query based on number of IDs
            placeholders = ','.join('?' for _ in ids)
            query = f"""
                SELECT newId, comments, content, date, topic
                FROM Posts
                WHERE newId IN ({placeholders})
            """
            cursor.execute(query, ids)
            rows = cursor.fetchall()

            # Convert rows into a list of article dictionaries
            articles = []
            for row in rows:
                articles.append({
                    "id": row.newId,
                    "title": row.comments,
                    "content": row.content,
                    "date": row.date,
                    "topic": row.topic
                })
            return articles
    except pyodbc.OperationalError as e:
        # Handle connection errors gracefully
        print("Error connecting to DB:", e)
        return []

# --- Format articles for display (HTML version with layout and styling) ---
def format_articles(articles):
    # If there are no articles, return a message in HTML
    if not articles:
        return "<p>No articles available for this topic.</p>"

    html = ""
    # Build HTML structure for each article
    for article in articles:
        title = article.get("title", "No Title")
        date = article.get("date", "No Date")
        content = article.get("content", "")

        # Retrieve an appropriate image using the NER + Guardian API
        text, image_url = article_with_images(content)

        # Create a formatted news card with image and text
        html += f"""
        <div class='news-card'>
            <div class='news-image'>
                {'<img src="' + image_url + '" alt="Image" />' if image_url else ''}
            </div>
            <div class='news-content'>
                <h3 class='news-title'>{title}</h3>
                <p class='news-date'>{date}</p>
                <p class='news-text'>{text}</p>
            </div>
        </div>
        """

    # Return the complete HTML string
    return html
