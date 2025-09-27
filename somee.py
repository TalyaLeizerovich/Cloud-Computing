import json
import pyodbc

# 1️⃣ קראי את ה-JSON הסופי
with open("article_classified_full.json", "r", encoding="utf-8") as f:
    article_data = json.load(f)

content = article_data.get("content", "")
topic = article_data.get("topic", "")
published_at = article_data.get("publishedAt", None)

# 2️⃣ הגדרת חיבור ל-SQL Server
# החליפי USERNAME, PASSWORD, SERVER לפי ההגדרות שלך
conn_str = (
      "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=CloudComputer.mssql.somee.com,1433;"  # פורט חובה
    "DATABASE=CloudComputer;"
    "UID=Sarit_SQLLogin_1;"
    "PWD=bndigkyn1p;"
    "Encrypt=yes;"  # דרוש בדרך כלל ל‑Driver 18
    "TrustServerCertificate=yes;"  # מותאם ל‑ODBC
    "Connection Timeout=30;"
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# 3️⃣ הכנסה לטבלה
insert_query = """
INSERT INTO dbo.Posts (date, content, topic, comments)
VALUES (?, ?, ?, ?)
"""

# ניתן להשאיר comments ריק (NULL)
cursor.execute(insert_query, published_at, content, topic, None)
conn.commit()

print("✅ הכתבה נוספה בהצלחה לטבלה dbo.Posts")

# 4️⃣ סגירת החיבור
cursor.close()
conn.close()
