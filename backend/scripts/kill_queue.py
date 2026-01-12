
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv('/Users/michaelperinwogenburg/Desktop/big challenge/Uncensored/backend/.env')

# Config
# Config
api_key = os.getenv("RUNPOD_API_KEY")
endpoint_id = os.getenv("RUNPOD_ENDPOINT_ID")
pb_url = os.getenv("PB_URL", "https://uncensored-engine-db.fly.dev")
admin_email = os.getenv("PB_ADMIN_EMAIL", "admin@example.com")
admin_pass = os.getenv("PB_ADMIN_PASSWORD", "password123456")

def kill_the_queue():
    # 1. Purge RunPod Queue
    print(f"🧨 Purging RunPod Queue for {endpoint_id}...")
    runpod_url = f"https://api.runpod.ai/v2/{endpoint_id}/purge-queue"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    try:
        r = requests.post(runpod_url, headers=headers)
        print(f"RunPod Purge Result: {r.status_code} {r.text}")
    except Exception as e:
        print(f"RunPod Purge Error: {e}")

    # 2. Clear PocketBase Jobs
    print(f"🧨 Clearing PocketBase Jobs...")
    try:
        # Auth
        auth_url = f"{pb_url}/api/admins/auth-with-password"
        response = requests.post(auth_url, json={
            "identity": admin_email,
            "password": admin_pass
        })
        response.raise_for_status()
        token = response.json().get('token')
        pb_headers = {"Authorization": token}
        
        # Get all jobs
        jobs_url = f"{pb_url}/api/collections/jobs/records"
        r_all = requests.get(jobs_url, headers=pb_headers, params={"perPage": 100})
        jobs = r_all.json().get('items', [])
        
        print(f"Found {len(jobs)} jobs in PocketBase. Deleting...")
        for job in jobs:
            requests.delete(f"{jobs_url}/{job['id']}", headers=pb_headers)
            print(f"Deleted {job['id']}")
            
    except Exception as e:
        print(f"PocketBase Clear Error: {e}")

if __name__ == "__main__":
    kill_the_queue()
