
import os
import requests
import json
import argparse

def get_job_logs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--job_id", help="Job ID to fetch logs for")
    args = parser.parse_args()

    api_key = os.getenv("RUNPOD_API_KEY", "os.getenv("RUNPOD_API_KEY") or os.getenv("RUNPOD_KEY")")
    endpoint_id = os.getenv("RUNPOD_ENDPOINT_ID", "rpdeckmxkatov6")
    job_id = args.job_id or "sicqaysau476lmx" # Default to the stuck one

    # REST API for logs
    # Note: Logs might not be available if the job is stuck in QUEUE
    url = f"https://api.runpod.ai/v2/{endpoint_id}/job/{job_id}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    print(f"Checking status for job {job_id} on endpoint {endpoint_id}...")

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        print(f"Status: {json.dumps(data, indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_job_logs()
