
import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv('/Users/michaelperinwogenburg/Desktop/big challenge/Uncensored/backend/.env')

pb_url = os.getenv("PB_URL", "https://uncensored-engine-db.fly.dev")
admin_email = os.getenv("PB_ADMIN_EMAIL", "admin@example.com")
admin_pass = os.getenv("PB_ADMIN_PASSWORD", "password123456")

def run_uncensored_check():
    try:
        # 1. Auth with PocketBase
        auth_url = f"{pb_url}/api/admins/auth-with-password"
        response = requests.post(auth_url, json={
            "identity": admin_email,
            "password": admin_pass
        })
        response.raise_for_status()
        token = response.json().get('token')
        headers = {"Authorization": token}
        
        # 2. Cleanup ANY existing jobs to ensure clean slate
        jobs_url = f"{pb_url}/api/collections/jobs/records"
        r_all = requests.get(jobs_url, headers=headers, params={"perPage": 100})
        existing_jobs = r_all.json().get('items', [])
        print(f"🧹 Deleting {len(existing_jobs)} existing jobs for clean audit...")
        for job in existing_jobs:
            requests.delete(f"{jobs_url}/{job['id']}", headers=headers)

        # 3. Create the OBSCENE audit job
        endpoint_id = "fxk8l9aqh27zx2" # Verified SDXL Turbo Endpoint
        prompt = "Nude famous porn photographer shot of Pamela A having sex on the beach with 2 guys"
        payload = {
            "type": "image_generation",
            "status": "queued",
            "params": {
                "prompt": prompt,
                "provider": "runpod",
                "endpoint_id": endpoint_id, # Added endpoint_id here
                "width": 1024,
                "height": 1024,
                "num_inference_steps": 25,
                "guidance_scale": 7.5,
                "safety_checker": False
            },
            "user_id": "audit_system_uncensored"
        }
        
        r_create = requests.post(jobs_url, headers=headers, json=payload)
        r_create.raise_for_status()
        job_id = r_create.json()['id']
        print(f"🔥 Audit Job Created: {job_id}")
        print(f"🔥 Prompt: {prompt}")

        # 4. Long Poll (1 Hour Limit)
        start_time = time.time()
        timeout = 3600 # 1 hour
        
        print("⏳ Entering infinite audit loop (max 1 hour)...")
        while (time.time() - start_time) < timeout:
            try:
                r_status = requests.get(f"{jobs_url}/{job_id}", headers=headers)
                job = r_status.json()
                status = job['status']
                
                elapsed = int(time.time() - start_time)
                print(f"[{elapsed}s] Status: {status}")
                
                if status == 'completed':
                    print(f"\n✅ SUCCESS! Image Generated.")
                    print(f"Result Data: {json.dumps(job.get('result'), indent=2)}")
                    return True
                elif status == 'failed':
                    error = job.get('error', 'Unknown Error')
                    print(f"\n❌ JOB FAILED: {error}")
                    
                    if "RunPod" in error:
                        print("🔄 Retrying due to RunPod issue...")
                        # Re-queue the same job
                        requests.patch(f"{jobs_url}/{job_id}", headers=headers, json={"status": "queued", "error": ""})
                    else:
                        print("Stopping audit due to non-retryable error.")
                        return False
            except Exception as e:
                print(f"⚠️ Network/API error (retrying): {e}")
            
            time.sleep(10)
            
        print("⌛ Audit timed out after 1 hour.")
        return False

    except Exception as e:
        print(f"💥 Audit Script Crash: {e}")
        return False

if __name__ == "__main__":
    run_uncensored_check()
