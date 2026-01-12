
import os
import time
from pocketbase import PocketBase

PB_URL = "https://uncensored-engine-db.fly.dev"

def test_simple_gen():
    print(f"Connecting to {PB_URL}...")
    client = PocketBase(PB_URL)
    
    # Minimal Payload - No model_id
    prompt = "A red apple"
    print(f"🚀 Submitting SIMPLE job with prompt: '{prompt}'...")
    
    job_data = {
        "type": "image_generation",
        "params": {
            "prompt": prompt,
            "provider": "runpod",
            "num_inference_steps": 20,
            "guidance_scale": 7.0,
            # "model_id": "pony-v6"  <-- REMOVED
        },
        "user_id": "test-script-runner",
        "status": "queued"
    }
    
    try:
        job = client.collection("jobs").create(job_data)
        print(f"✅ Job created: {job.id}")
    except Exception as e:
        print(f"❌ Failed to create job: {e}")
        return

    # Poll
    for i in range(120): # 4 mins
        time.sleep(2)
        try:
            ud_job = client.collection("jobs").get_one(job.id)
            status = ud_job.status
            if i % 5 == 0:
                print(f"⏳ Status: {status}")
            
            if status == "completed":
                print("✨ Job Completed!")
                print(f"Result: {ud_job.result}")
                return
            elif status in ["failed", "error"]:
                 print(f"❌ Job Failed! Result: {ud_job.result if hasattr(ud_job, 'result') else 'No result'}")
                 return
        except Exception as e:
             pass

if __name__ == "__main__":
    test_simple_gen()
