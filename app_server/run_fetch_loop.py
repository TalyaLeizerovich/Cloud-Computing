# This script continuously sends a GET request to a local FastAPI server every 40 seconds and prints the JSON response.
import requests
import time

while True:
    # Send a GET request to the local server endpoint
    resp = requests.get("http://127.0.0.1:8000/process/sports")  # or use another topic
    
    # Print the response in JSON format
    print(resp.json())
    
    # Wait 40 seconds before sending the next request
    time.sleep(40)
