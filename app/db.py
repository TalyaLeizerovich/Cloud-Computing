# app/db_handler.py
import pyodbc

def save_to_db(article: dict):
    """
    Receives an article dict with 'content', 'topic', and 'publishedAt'
    and inserts it into the SOMEE SQL Server DB.
    """
    content = article.get("content", "")
    topic = article.get("topic", "")
    published_at = article.get("publishedAt", None)

    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=CloudComputer.mssql.somee.com,1433;"
        "DATABASE=CloudComputer;"
        "UID=Sarit_SQLLogin_1;"
        "PWD=bndigkyn1p;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
        "Connection Timeout=30;"
    )

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO dbo.Posts (date, content, topic, comments)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(insert_query, published_at, content, topic, None)
        conn.commit()

        cursor.close()
        conn.close()
        return {"status": "success", "message": "Article added to DB."}

    except Exception as e:
        return {"status": "error", "message": str(e)}

