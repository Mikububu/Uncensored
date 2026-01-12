
import os
import requests
from pocketbase import PocketBase
from dotenv import load_dotenv

load_dotenv('/Users/michaelperinwogenburg/Desktop/big challenge/Uncensored/backend/.env')

pb_url = os.getenv("PB_URL", "https://uncensored-engine-db.fly.dev")
admin_email = os.getenv("PB_ADMIN_EMAIL", "admin@example.com")
admin_pass = os.getenv("PB_ADMIN_PASSWORD", "password123456")

def cleanup_stuck_jobs():
    try:
        # Auth
        auth_url = f"{pb_url}/api/admins/auth-with-password"
        response = requests.post(auth_url, json={
            "identity": admin_email,
            "password": admin_pass
        })
        response.raise_for_status()
        token = response.json().get('token')
        
        headers = {"Authorization": token}
        
        # Get processing jobs
        jobs_url = f"{pb_url}/api/collections/jobs/records"
        params = {"filter": "status='processing'"}
        
        r = requests.get(jobs_url, headers=headers, params=params)
        r.raise_for_status()
        jobs = r.json().get('items', [])
        
        print(f"Found {len(jobs)} stuck jobs.")
        for job in jobs:
            print(f"Resetting job {job['id']}...")
            update_url = f"{jobs_url}/{job['id']}"
            r_upd = requests.patch(update_url, headers=headers, json={"status": "failed", "error": "Cleanup stuck job"})
            print(f"Result: {r_upd.status_code}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    cleanup_stuck_jobs()
