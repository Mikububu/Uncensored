
import os
import time
from pocketbase import PocketBase

PB_URL = "https://uncensored-engine-db.fly.dev"

def generate_batch():
    print(f"Connecting to {PB_URL}...")
    client = PocketBase(PB_URL)
    
    prompts = [
        "A red apple",
        "A blue ocean", 
        "A green forest",
        "A yellow sun",
        "A purple flower"
    ]
    
    job_ids = []
    
    print(f"🚀 Submitting 5 jobs...")
    
    for i, prompt in enumerate(prompts):
        job_data = {
            "type": "image_generation",
            "params": {
                "prompt": prompt,
                "provider": "runpod",
                "num_inference_steps": 20,
                "guidance_scale": 7.0
            },
            "user_id": "test-batch-runner",
            "status": "queued"
        }
        
        try:
            job = client.collection("jobs").create(job_data)
            print(f"[{i+1}/5] Job created: {job.id}")
            job_ids.append(job.id)
        except Exception as e:
            print(f"❌ Failed to create job {i+1}: {e}")

    print("⏳ Waiting for results...")
    
    completed_count = 0
    failed_count = 0
    
    # Poll for 10 minutes max
    for _ in range(300):
        time.sleep(2)
        
        active_ids = [jid for jid in job_ids] # Copy
        
        for jid in active_ids:
            try:
                ud_job = client.collection("jobs").get_one(jid)
                status = ud_job.status
                
                if status == "completed":
                    print(f"✨ Job {jid} Completed!")
                    job_ids.remove(jid)
                    completed_count += 1
                elif status in ["failed", "error"]:
                    print(f"❌ Job {jid} Failed!")
                    job_ids.remove(jid)
                    failed_count += 1
            except:
                pass
                
        if len(job_ids) == 0:
            break
            
    print(f"Done. Completed: {completed_count}, Failed: {failed_count}")

if __name__ == "__main__":
    generate_batch()
