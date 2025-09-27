from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

request = {"topic": "sports", "db_id": 975}
producer.send("sports_requests", request)
producer.flush()
