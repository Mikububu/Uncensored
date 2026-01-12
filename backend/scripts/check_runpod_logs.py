
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv(dotenv_path='backend/.env')
api_key = os.getenv("RUNPOD_API_KEY")
endpoint_id = os.getenv("RUNPOD_ENDPOINT_ID")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def check_endpoint_logs():
    url = f"https://api.runpod.ai/v2/{endpoint_id}/health"
    try:
        print(f"Checking health for {endpoint_id}...")
        r = requests.get(url, headers=headers)
        print(f"Status Code: {r.status_code}")
        print(f"Health Response: {r.json()}")
        
        # Try to find a job ID that is in the queue to check its status specifically
        # (Though we can't easily list specific job IDs from the health endpoint)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_endpoint_logs()
