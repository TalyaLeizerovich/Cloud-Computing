from kafka import KafkaConsumer, KafkaProducer
import json
import pyodbc

consumer = KafkaConsumer("sports_requests",
                         bootstrap_servers='localhost:9092',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# התחברות ל-SQL Server
conn = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=...;DATABASE=...;UID=...;PWD=...;Encrypt=yes;TrustServerCertificate=yes;")
cursor = conn.cursor()

for msg in consumer:
    db_id = msg.value["db_id"]
    cursor.execute("SELECT content FROM Posts WHERE newId=?", db_id)
    content = cursor.fetchone()[0]
    response = {"db_id": db_id, "content": content}
    producer.send("sports_responses", response)
    producer.flush()
