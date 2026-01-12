
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv('/Users/michaelperinwogenburg/Desktop/big challenge/Uncensored/backend/.env')

pb_url = os.getenv("PB_URL", "https://uncensored-engine-db.fly.dev")
admin_email = os.getenv("PB_ADMIN_EMAIL", "admin@example.com")
admin_pass = os.getenv("PB_ADMIN_PASSWORD", "password123456")

def check_specific_job(id):
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
        
        # Get job
        job_url = f"{pb_url}/api/collections/jobs/records/{id}"
        r = requests.get(job_url, headers=headers)
        job = r.json()
        print(f"Job: {json.dumps(job, indent=2)}")
        
        # If processing, check RunPod status if we can find the RunPod ID
        # Our worker stores the RunPod ID in the result or params usually? No, it's usually transient.
        # But we can check the endpoint health to see if it's in progress.
        
        runpod_id = "os.getenv("RUNPOD_API_KEY") or os.getenv("RUNPOD_KEY")"
        endpoint_id = "fxk8l9aqh27zx2"
        
        print("\nChecking RunPod Health...")
        health_url = f"https://api.runpod.ai/v2/{endpoint_id}/health"
        r_health = requests.get(health_url, headers={"Authorization": f"Bearer {runpod_id}"})
        print(f"RunPod Health: {json.dumps(r_health.json(), indent=2)}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_specific_job("v16w0udczpp1hov")
