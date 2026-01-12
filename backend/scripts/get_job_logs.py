
import os
import requests
import json

api_key = "os.getenv("RUNPOD_API_KEY") or os.getenv("RUNPOD_KEY")"
job_id = "ddc73f53-4d37-4c7a-92b9-5dc70177e56f-e2"

def get_job_logs():
    # REST API for logs
    url = f"https://api.runpod.ai/v2/fxk8l9aqh27zx2/logging/{job_id}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        print(f"Logs: {json.dumps(data, indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_job_logs()
