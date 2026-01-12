import os
import time
from pocketbase import PocketBase

PB_URL = "https://uncensored-engine-db.fly.dev"

def test_runpod_generation():
    print(f"Connecting to {PB_URL}...")
    client = PocketBase(PB_URL)
    
    # Create the job
    prompt = "A detailed sensual oil painting of a woman in lingerie, dramatic lighting, masterpiece"
    print(f"🚀 Submitting job with prompt: '{prompt}' (Provider: RunPod)...")
    
    job_data = {
        "type": "image_generation",
        "params": {
            "prompt": prompt,
            "provider": "runpod",
            "num_inference_steps": 25,
            "guidance_scale": 7.5,
            "enable_safety_checker": False
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
    for i in range(60): # 2 mins max (approx)
        time.sleep(2)
        try:
            ud_job = client.collection("jobs").get_one(job.id)
            status = ud_job.status
            print(f"⏳ Job Status: {status}")
            
            if status == "completed":
                print("✨ Job Completed!")
                # Check for images
                if hasattr(ud_job, 'result') and ud_job.result and 'images' in ud_job.result:
                    images = ud_job.result['images']
                    if images and len(images) > 0:
                        print(f"🖼️ Generated Image URL: {images[0].get('url', 'No URL found')}")
                    else:
                        print("⚠️ Result present but no images found.")
                else:
                    print("⚠️ Completed but no result/images data found.")
                    
                return
            elif status in ["failed", "error"]:
                print(f"❌ Job Failed with status: {ud_job.status}")
                return
        except Exception as e:
             print(f"⚠️ Error polling: {e}")
    
    print("❌ Timed out.")

if __name__ == "__main__":
    test_runpod_generation()
