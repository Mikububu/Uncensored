import os
import requests
import sys
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RUNPOD_API_KEY")
DEFAULT_ENDPOINT_ID = os.getenv("RUNPOD_ENDPOINT_ID", "fxk8l9aqh27zx2")

def check_health(endpoint_id=None):
    eid = endpoint_id or DEFAULT_ENDPOINT_ID
    print(f"Checking health for endpoint: {eid}")
    url = f"https://api.runpod.ai/v2/{eid}/health"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        r = requests.get(url, headers=headers)
        print(f"Status Code: {r.status_code}")
        if r.status_code == 200:
            print("Response:", r.json())
        else:
            print("Error:", r.text)
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    target_id = sys.argv[1] if len(sys.argv) > 1 else None
    check_health(target_id)
