
import os
import requests
import json
import time
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")
RUNPOD_ENDPOINT_ID = os.getenv("RUNPOD_ENDPOINT_ID")

if not RUNPOD_API_KEY:
    print("❌ Error: RUNPOD_API_KEY is not set.")
    exit(1)

if not RUNPOD_ENDPOINT_ID:
    print("❌ Error: RUNPOD_ENDPOINT_ID is not set.")
    exit(1)

print(f"🔍 Verifying RunPod Endpoint: {RUNPOD_ENDPOINT_ID}")

HEADERS = {
    "Authorization": f"Bearer {RUNPOD_API_KEY}",
    "Content-Type": "application/json"
}

def check_health():
    url = f"https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/health"
    try:
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        data = r.json()
        print("\n✅ Health Check Passed")
        print(json.dumps(data, indent=2))
        return True
    except Exception as e:
        print(f"\n❌ Health Check Failed: {e}")
        try:
            print(r.text)
        except:
            pass
        return False

def run_test_job():
    url = f"https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/run"
    
    # Standard payload structure expected by the handler
    payload = {
        "input": {
            "prompt": "A cute robot cat",
            "width": 512,
            "height": 512,
            "num_inference_steps": 20
        }
    }

    try:
        print(f"\n🚀 Submitting test job...")
        r = requests.post(url, headers=HEADERS, json=payload)
        r.raise_for_status()
        data = r.json()
        job_id = data.get('id')
        print(f"✅ Job Submitted. ID: {job_id}")
        
        return job_id
    except Exception as e:
        print(f"\n❌ Job Submission Failed: {e}")
        try:
             print(r.text)
        except:
            pass
        return None

def poll_job(job_id):
    url = f"https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/status/{job_id}"
    
    print(f"\n⏳ Polling job status...")
    
    start_time = time.time()
    while time.time() - start_time < 300: # 5 minute timeout
        try:
            r = requests.get(url, headers=HEADERS)
            data = r.json()
            status = data.get('status')
            
            print(f"Status: {status}")
            
            if status == 'COMPLETED':
                print("\n✨ Job Completed!")
                output = data.get('output', {})
                if 'image_base64' in output:
                    print("✅ Image data received.")
                    # Save it just to prove it works
                    with open("test_output.png", "wb") as f:
                        f.write(base64.b64decode(output['image_base64']))
                    print("✅ Saved to test_output.png")
                else:
                    print("⚠️ No image_base64 in output.")
                    print(output)
                return
            
            if status in ['FAILED', 'CANCELLED', 'TIMED_OUT']:
                print(f"\n❌ Job Failed: {status}")
                print(data)
                return
                
            time.sleep(2)
        except Exception as e:
            print(f"Error polling: {e}")
            time.sleep(2)

if __name__ == "__main__":
    if check_health():
        jid = run_test_job()
        if jid:
            poll_job(jid)
