
import os
import requests
import json
import argparse
from dotenv import load_dotenv

load_dotenv(dotenv_path='backend/.env')

def get_job_logs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--job_id", required=True)
    args = parser.parse_args()

    api_key = os.getenv("RUNPOD_API_KEY", "os.getenv("RUNPOD_API_KEY") or os.getenv("RUNPOD_KEY")")
    endpoint_id = os.getenv("RUNPOD_ENDPOINT_ID", "fxk8l9aqh27zx2") # Default to current target
    job_id = args.job_id

    # REST API for logs
    # Using 'status' which might include logs or at least status detail
    url = f"https://api.runpod.ai/v2/{endpoint_id}/status/{job_id}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        print(f"Job Status Data: {json.dumps(data, indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_job_logs()
