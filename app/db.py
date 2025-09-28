# # app/db_handler.py
# import pyodbc

# def save_to_db(article: dict):
#     """
#     Receives an article dict with 'content', 'topic', and 'publishedAt'
#     and inserts it into the SOMEE SQL Server DB.
#     """
#     content = article.get("content", "")
#     topic = article.get("topic", "")
#     published_at = article.get("publishedAt", None)

#     conn_str = (
#         "DRIVER={ODBC Driver 18 for SQL Server};"
#         "SERVER=CloudComputer.mssql.somee.com,1433;"
#         "DATABASE=CloudComputer;"
#         "UID=Sarit_SQLLogin_1;"
#         "PWD=bndigkyn1p;"
#         "Encrypt=yes;"
#         "TrustServerCertificate=yes;"
#         "Connection Timeout=30;"
#     )

#     try:
#         conn = pyodbc.connect(conn_str)
#         cursor = conn.cursor()

#         insert_query = """
#         INSERT INTO dbo.Posts (date, content, topic, comments)
#         VALUES (?, ?, ?, ?)
#         """
#         cursor.execute(insert_query, published_at, content, topic, None)
#         conn.commit()

#         cursor.close()
#         conn.close()
#         return {"status": "success", "message": "Article added to DB."}

#     except Exception as e:
#         return {"status": "error", "message": str(e)}

# app/db_handler.py
# import pyodbc
# import random

# from requests import post

# def save_to_db(article: dict):
#     """
#     Receives an article dict with 'content', 'topic', and 'publishedAt'
#     and inserts it into the SOMEE SQL Server DB.
#     Generates a random article_id between 0 and 2**10 - 1.
#     """
#     content = article.get("content", "")
#     topic = article.get("topic", "")
#     published_at = article.get("publishedAt", None)

#     # Generate a random article ID (0 - 1023)
#     article_id = random.randint(0, 2**10 - 1)

#     # conn_str = (
#     #     "DRIVER={ODBC Driver 18 for SQL Server};"
#     #     "SERVER=CloudComputer.mssql.somee.com,1433;"
#     #     "DATABASE=CloudComputer;"
#     #     "UID=Sarit_SQLLogin_1;"
#     #     "PWD=bndigkyn1p;"
#     #     "Encrypt=yes;"
#     #     "TrustServerCertificate=yes;"
#     #     "Connection Timeout=30;"

#     # )

#     conn_str = (
#     "DRIVER={ODBC Driver 18 for SQL Server};"
#     "SERVER=CloudComputer.mssql.somee.com,1433;"
#     "UID=Sarit_SQLLogin_1;"
#     "PWD=bndigkyn1p;"
#     "Encrypt=yes;"
#     "TrustServerCertificate=yes;"
#     "Connection Timeout=30;"
#     "Workstation ID=CloudComputer.mssql.somee.com;"
#     "Packet Size=4096;"
#     "Persist Security Info=False;"
#     "DATABASE=CloudComputer;"
#   )

#     try:
#         conn = pyodbc.connect(conn_str)
#         cursor = conn.cursor()

#         insert_query = """
#         INSERT INTO dbo.Posts (article_id, date, content, topic, comments)
#         VALUES (?, ?, ?, ?, ?)
#         """
#         cursor.execute(insert_query, article_id, published_at, content, topic, None)
#         conn.commit()

#         cursor.close()
#         conn.close()

#         # Return JSON including the generated article_id
#         return {
#             "status": "success",
#             "message": "Article added to DB.",
#             "article_id": article_id
#         }
#     except pyodbc.IntegrityError as e:
#         print("status": "error", "message": f"newId {article_id} כבר קיים.")
#         _id = random.randint(0, 2**10 - 1)

#     except Exception as e:
#         return {"status": "error", "message": str(e)}
# import pyodbc
# import random
# from datetime import datetime

# def save_to_db(article: dict, max_attempts: int = 10):
#     """
#     Tries to insert an article into the database.
#     If article_id already exists, generates a new one and retries.
#     """
#     content = article.get("content", "")
#     topic = article.get("topic", "")
#     published_at = article.get("publishedAt", datetime.now())

#     conn_str = (
#         "DRIVER={ODBC Driver 18 for SQL Server};"
#         "SERVER=CloudComputer.mssql.somee.com,1433;"
#         "UID=Sarit_SQLLogin_1;"
#         "PWD=bndigkyn1p;"
#         "Encrypt=yes;"
#         "TrustServerCertificate=yes;"
#         "Connection Timeout=30;"
#         "DATABASE=CloudComputer;"
#     )

#     attempt = 0
#     while attempt < max_attempts:
#         article_id = random.randint(0, 2**10 - 1)
#         try:
#             conn = pyodbc.connect(conn_str)
#             cursor = conn.cursor()

#             insert_query = """
#             INSERT INTO dbo.Posts (article_id, date, content, topic, comments)
#             VALUES (?, ?, ?, ?, ?)
#             """
#             cursor.execute(insert_query, article_id, published_at, content, topic, None)
#             conn.commit()

#             cursor.close()
#             conn.close()

#             # הצלחנו – מחזירים JSON
#             return {
#                 "status": "success",
#                 "message": "Article added to DB.",
#                 "article_id": article_id
#             }

#         except pyodbc.IntegrityError:
#             # ID כבר קיים – מגרילים חדש ומנסים שוב
#             print(f"newId {article_id} כבר קיים. מגרילים חדש ומנסים שוב...")
#             attempt += 1

#         except Exception as e:
#             return {"status": "error", "message": str(e)}

#     # אם אחרי כל הניסיונות לא הצלחנו
#     return {
#         "status": "error",
#         "message": f"לא הצלחנו להכניס את הפוסט אחרי {max_attempts} ניסיונות – כל ה־article_id שהוגרלו כבר קיימים."
#     }
# app/db_handler.py
import pyodbc
import random
from datetime import datetime
from kafka import KafkaProducer
import json

# חיבור ל-Kafka – ניצור Producer אחד לשימוש
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
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
    # רשימת Topics מוכרים
    KNOWN_TOPICS = ["sports", "economy", "politics", "technology"]

    attempt = 0
    while attempt < max_attempts:
        newId = random.randint(0, 2**10 - 1)
        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()

            insert_query = """
            INSERT INTO dbo.Posts (newId, date, content, topic, comments)
            VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(insert_query, newId, published_at, content, topic, None)
            conn.commit()

            cursor.close()
            conn.close()

            # הצלחנו – עכשיו שולחים את ה-ID ל-Kafka לפי topic
            # שולחים רק אם יש topic
            

            topic_to_send = topic.lower() if topic else ""
            if topic_to_send in KNOWN_TOPICS:
                producer.send(topic_to_send, {"article_id": newId})
            else:
                producer.send("others", {"article_id": newId})
            producer.flush()







            # מחזירים JSON עם article_id
            return {
                "status": "success",
                "message": "Article added to DB and sent to Kafka.",
                "article_id": newId
            }

        except pyodbc.IntegrityError:
            # ID כבר קיים – מגרילים חדש ומנסים שוב
            print(f"article_id {newId} כבר קיים. מגרילים חדש ומנסים שוב...")
            attempt += 1

        except Exception as e:
            return {"status": "error", "message": str(e)}

    # אם אחרי כל הניסיונות לא הצלחנו
    return {
        "status": "error",
        "message": f"לא הצלחנו להכניס את הפוסט אחרי {max_attempts} ניסיונות – כל ה־article_id שהוגרלו כבר קיימים."
    }
