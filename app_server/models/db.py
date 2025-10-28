import pyodbc  # Library for connecting to SQL Server databases via ODBC
import random  # For generating random article IDs
from datetime import datetime  # To handle datetime objects
from kafka import KafkaProducer  # Kafka producer for sending messages to topics
import json  # For serializing data to JSON format

# Connect to Kafka – create a single producer instance for reuse
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # Kafka server address
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize Python dicts to JSON bytes
)

def save_to_db(article: dict, max_attempts: int = 10):
    """
    Tries to insert an article into the database.
    If article_id already exists, generates a new one and retries.
    After successful insertion, sends article_id to Kafka topic based on article['topic'].
    """
    content = article.get("content", "")  
    topic = article.get("topic", "") 
    published_at = article.get("publishedAt", datetime.now()) 
    title = article.get("comments", "") 

    # Connection string to the SQL Server database hosted on SOMEE
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=CloudComputer.mssql.somee.com,1433;"
        "UID=Sarit_SQLLogin_1;"
        "PWD=bndigkyn1p;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
        "Connection Timeout=30;"
        "DATABASE=CloudComputer;"
    )

    # List of known topics
    KNOWN_TOPICS = ["sports", "entertainment", "politics", "technology"]

    attempt = 0
    while attempt < max_attempts:
        newId = random.randint(0, 2**10 - 1)  # Generate a random article ID
        try:
            conn = pyodbc.connect(conn_str)  # Connect to the database
            cursor = conn.cursor()  # Create a cursor for executing SQL queries

            # SQL query to insert a new post
            insert_query = """
            INSERT INTO dbo.Posts (newId, date, content, topic, comments)
            VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(insert_query, newId, published_at, content, topic, title)  
            conn.commit()  # Commit the transaction

            cursor.close()  # Close cursor
            conn.close()  # Close connection

            # Successfully inserted – now send the ID to Kafka based on topic
            topic_to_send = topic.lower() if topic else ""
            payload = {"article_id": newId}

            if topic_to_send in KNOWN_TOPICS:
                producer.send(topic_to_send, payload)
            else:
                producer.send("others", payload)

            producer.flush()  # Ensure message is sent immediately

            # Return JSON with article_id
            return {
                "status": "success",
                "message": "Article added to DB and sent to Kafka.",
                "article_id": newId
            }

        except pyodbc.IntegrityError:
            # ID already exists – generate a new one and retry
            print(f"article_id {newId} already exists. Generating new ID and retrying...")
            attempt += 1

        except Exception as e:
            # Handle any other exceptions
            return {"status": "error", "message": str(e)}

    # If all attempts fail
    return {
        "status": "error",
        "message": f"Failed to insert the post after {max_attempts} attempts – all generated article_ids already exist."
    }
