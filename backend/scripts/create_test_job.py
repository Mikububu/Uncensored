
import os
import requests
from dotenv import load_dotenv

load_dotenv('/Users/michaelperinwogenburg/Desktop/big challenge/Uncensored/backend/.env')

pb_url = os.getenv("PB_URL", "https://uncensored-engine-db.fly.dev")
admin_email = os.getenv("PB_ADMIN_EMAIL", "admin@example.com")
admin_pass = os.getenv("PB_ADMIN_PASSWORD", "password123456")

def create_test_job():
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
        
        # Create job
        jobs_url = f"{pb_url}/api/collections/jobs/records"
        payload = {
            "type": "image_generation",
            "status": "queued",
            "params": {
                "prompt": "Nude famous porn photographer shot of Pamela A having sex on the beach with 2 guys",
                "provider": "runpod",
                "width": 1024,
                "height": 1024,
                "num_inference_steps": 25,
                "guidance_scale": 7.5
            },
            "user_id": "system_test"
        }
        
        r = requests.post(jobs_url, headers=headers, json=payload)
        r.raise_for_status()
        job = r.json()
        print(f"✅ Created Test Job: {job['id']}")
        return job['id']

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_test_job()
