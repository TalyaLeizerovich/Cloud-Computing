# config.py

# Kafka settings
KAFKA_BROKER = "localhost:9092"  # Make sure this matches your container's port
TOPICS = {
    "בידור": "entertainment",  # Hebrew key mapped to English topic
    "פוליטיקה": "politics",
    "ספורט": "sports",
    "טכנולוגיה": "technology",
    "אחר": "others"
}

# Database settings (SOMEE)
DB_HOST = "CloudComputer.mssql.somee.com"  # Database host – changed from 'localhost' to SOMEE host
DB_PORT = 1433  # Database port (default for SQL Server)
DB_NAME = "CloudComputer"  # Database name
DB_USER = "Sarit_SQLLogin_1"  # Database username
DB_PASSWORD = "bndigkyn1p"  # Database password
