# # backend.py
# from kafka import KafkaProducer, KafkaConsumer
# import pyodbc
# import json
# from config import KAFKA_BROKER, TOPICS, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

# # --- Kafka ---
# producer = KafkaProducer(
#     bootstrap_servers=KAFKA_BROKER,
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

# def send_topic_request(topic_name):
#     """שליחת נושא ל-Kafka כדי לקבל מזהי כתבות"""
#     producer.send(topic_name, {"request": "get_ids"})
#     producer.flush()

# def consume_article_ids(topic_name, timeout=5000):
#     """קבלת מזהי כתבות מ-Kafka"""
#     consumer = KafkaConsumer(
#         topic_name,
#         bootstrap_servers=KAFKA_BROKER,
#         auto_offset_reset='latest',
#         value_deserializer=lambda m: json.loads(m.decode('utf-8')),
#         consumer_timeout_ms=timeout
#     )
#     ids = []
#     for msg in consumer:
#         ids.extend(msg.value.get("article_id", []))
#     return ids

# # --- Database ---
# conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};" \
#            f"SERVER={DB_HOST},{DB_PORT};" \
#            f"DATABASE={DB_NAME};UID={DB_USER};PWD={DB_PASSWORD}"

# def fetch_articles_by_ids(ids):
#     """שליפת כתבות מהDB לפי רשימת מזהים"""
#     if not ids:
#         return []
#     with pyodbc.connect(conn_str) as conn:
#         cursor = conn.cursor()
#         placeholders = ','.join('?' for _ in ids)
#         query = f"SELECT title, content, date FROM News WHERE id IN ({placeholders})"
#         cursor.execute(query, ids)
#         return cursor.fetchall()

# # --- Utils ---
# def format_articles(articles):
#     """פורמט הכתבות להצגה ב-Markdown"""
#     if not articles:
#         return "אין כתבות זמינות לנושא זה."
#     md = ""
#     for title, content, date in articles:
#         md += f"### {title} ({date})\n{content}\n\n---\n"
#     return md






















#עובד- כתבה עם תמונה ישר אחרי הכתבה אבל בלי כותרת ושעת פרסום
# from kafka import KafkaConsumer
# import pyodbc
# import json
# from config import KAFKA_BROKER, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

# # --- Database connection string ---
# conn_str = (
#     f"DRIVER={{ODBC Driver 18 for SQL Server}};"
#     f"SERVER={DB_HOST},{DB_PORT};"
#     f"DATABASE={DB_NAME};"
#     f"UID={DB_USER};PWD={DB_PASSWORD};"
#     f"Encrypt=yes;TrustServerCertificate=yes;"
# )

# # --- Consumer matched to your Producer ---
# def consume_article_ids(topic_name, timeout=5000):
#     """
#     Receives article IDs from Kafka by topic.
#     Matches the format that the Producer sends: {"article_id": ...}
#     """
#     consumer = KafkaConsumer(
#         topic_name,
#         bootstrap_servers=KAFKA_BROKER,
#         auto_offset_reset='earliest',
#         value_deserializer=lambda m: json.loads(m.decode('utf-8')),
#         consumer_timeout_ms=timeout
#     )
#     article_ids = []
#     for message in consumer:
#         try:
#             data = message.value
#             article_id = data.get("article_id")
#             if article_id is not None:
#                 article_ids.append(article_id)
#         except Exception as e:
#             print(f"Error decoding message: {e}")
#     return article_ids

# # --- Fetch articles from DB by IDs ---
# def fetch_articles_by_ids(ids):
#     if not ids:
#         return []
#     try:
#         with pyodbc.connect(conn_str, timeout=5) as conn:
#             cursor = conn.cursor()
#             placeholders = ','.join('?' for _ in ids)
#             # שולף את העמודות הקיימות בטבלה: content, date, topic
#             query = f"SELECT content, date, topic FROM Posts WHERE newId IN ({placeholders})"
#             cursor.execute(query, ids)
#             return cursor.fetchall()
#     except pyodbc.OperationalError as e:
#         print("Error connecting to DB:", e)
#         return []

# # --- Format articles for Gradio ---
# def format_articles(articles):
#     if not articles:
#         return "אין כתבות זמינות לנושא זה."
#     md = ""
#     for content, date, topic in articles:
#         md += f"### {topic} ({date})\n{content}\n\n---\n"
#     return md



#כותרת עם תאריך ותמונה לצד הכתבה
from kafka import KafkaConsumer
import pyodbc
import json
from config import KAFKA_BROKER, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

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
        auto_offset_reset='earliest',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        consumer_timeout_ms=timeout
    )
    article_ids = []
    for message in consumer:
        try:
            data = message.value
            article_id = data.get("article_id")
            if article_id is not None:
                article_ids.append(article_id)
        except Exception as e:
            print(f"Error decoding message: {e}")
    return article_ids

# --- Fetch articles from DB by IDs ---
def fetch_articles_by_ids(ids):
    """
    שולף כתבות מה־DB לפי IDs.
    מחזיר רשימת מילונים: {id, title, content, date, topic}
    """
    if not ids:
        return []
    try:
        with pyodbc.connect(conn_str, timeout=5) as conn:
            cursor = conn.cursor()
            placeholders = ','.join('?' for _ in ids)
            query = f"""
                SELECT newId, comments, content, date, topic
                FROM Posts
                WHERE newId IN ({placeholders})
            """
            cursor.execute(query, ids)
            rows = cursor.fetchall()

            # הופך כל שורה למילון
            articles = []
            for row in rows:
                articles.append({
                    "id": row.newId,
                    "title": row.comments,   # הכותרת
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
    מחזיר טקסט Markdown ל־Gradio.
    """
    if not articles:
        return "אין כתבות זמינות לנושא זה."

    md = ""
    for article in articles:
        title = article.get("title", "ללא כותרת")
        date = article.get("date", "ללא תאריך")
        content = article.get("content", "")
      
        md += f"### {title}\n"
        md += f"**Date:** {date} \n\n"
        md += f"{content}\n\n---\n"
    return md

