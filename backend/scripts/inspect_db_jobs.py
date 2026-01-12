
import os
import requests
from pocketbase import PocketBase
from dotenv import load_dotenv

# Load from backend/.env
load_dotenv('/Users/michaelperinwogenburg/Desktop/big challenge/Uncensored/backend/.env')

pb_url = os.getenv("PB_URL", "https://uncensored-engine-db.fly.dev")
admin_email = os.getenv("PB_ADMIN_EMAIL", "admin@example.com")
admin_pass = os.getenv("PB_ADMIN_PASSWORD", "password123456")

print(f"Connecting to {pb_url} as {admin_email}...")

def check_jobs():
    try:
        # Auth
        auth_url = f"{pb_url}/api/admins/auth-with-password"
        response = requests.post(auth_url, json={
            "identity": admin_email,
            "password": admin_pass
        })
        response.raise_for_status()
        auth_data = response.json()
        token = auth_data.get('token')
        
        headers = {"Authorization": token}
        
        # Get failed jobs
        jobs_url = f"{pb_url}/api/collections/jobs/records"
        params = {
            "filter": "status='failed'",
            "sort": "-created",
            "perPage": 10
        }
        
        r = requests.get(jobs_url, headers=headers, params=params)
        r.raise_for_status()
        jobs = r.json().get('items', [])
        
        print(f"\nFound {len(jobs)} failed jobs.")
            
        # Get pending jobs
        params["filter"] = "status='pending'"
        r = requests.get(jobs_url, headers=headers, params=params)
        r.raise_for_status()
        pending_jobs = r.json().get('items', [])
        
        print(f"\nFound {len(pending_jobs)} pending jobs:")
        for job in pending_jobs:
            print(f"- Job {job['id']} (Created: {job.get('created')})")

        # Get queued jobs
        params["filter"] = "status='queued'"
        r = requests.get(jobs_url, headers=headers, params=params)
        r.raise_for_status()
        queued_jobs = r.json().get('items', [])
        
        print(f"\nFound {len(queued_jobs)} queued jobs:")
        for job in queued_jobs:
            print(f"- Job {job['id']} (Created: {job.get('created')})")

        # Get processing jobs (stuck?)
        params["filter"] = "status='processing'"
        r = requests.get(jobs_url, headers=headers, params=params)
        r.raise_for_status()
        processing_jobs = r.json().get('items', [])
        
        print(f"\nFound {len(processing_jobs)} processing jobs stuck in state.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_jobs()
