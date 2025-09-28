
import requests
import time

while True:
    resp = requests.get("http://127.0.0.1:8000/process/sports")  # או topic אחר
    print(resp.json())
    time.sleep(40)  # מחכה 40 שניות לפני הקריאה הבאה
