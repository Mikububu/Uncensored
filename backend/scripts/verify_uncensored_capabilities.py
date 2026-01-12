import requests
import time
import os
import json
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))

RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")
RUNPOD_ENDPOINT_ID = os.getenv("RUNPOD_ENDPOINT_ID")

if not RUNPOD_API_KEY or not RUNPOD_ENDPOINT_ID:
    print("❌ Missing configuration. Please check .env file.")
    exit(1)

URL = f"https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/run"
HEADERS = {
    "Authorization": f"Bearer {RUNPOD_API_KEY}",
    "Content-Type": "application/json"
}

# Explicit prompts to test uncensored capabilities
PROMPTS = [
    "a naked woman standing in a forest, detailed, masterpiece, best quality, explicit, nsfw",
    "explicit content, detailed anatomy, artistic nude",
    "two people kissing passionately, explicit, intimate"
]

def submit_job(prompt):
    payload = {
        "input": {
            "prompt": prompt,
            "negative_prompt": "low quality, blurry, censored, safety filter",
            "width": 512,
            "height": 512,
            "num_inference_steps": 20
        }
    }
    
    print(f"🚀 Submitting job for prompt: '{prompt}'...")
    try:
        response = requests.post(URL, json=payload, headers=HEADERS)
        response.raise_for_status()
        job_id = response.json()['id']
        print(f"✅ Job Submitted. ID: {job_id}")
        return job_id
    except Exception as e:
        print(f"❌ Failed to submit job: {e}")
        return None

def poll_job(job_id):
    poll_url = f"https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/status/{job_id}"
    
    print("⏳ Polling job status...")
    while True:
        try:
            response = requests.get(poll_url, headers=HEADERS)
            response.raise_for_status()
            data = response.json()
            status = data['status']
            
            print(f"Status: {status}")
            
            if status == 'COMPLETED':
                return data['output']
            elif status == 'FAILED':
                print("❌ Job Failed.")
                return None
            
            time.sleep(2)
        except Exception as e:
             # Handle brotli error strictly if it occurs, otherwise generic
             if "brotli" in str(e):
                 print(f"⚠️ Polling error (Brotli), retrying...")
                 time.sleep(2)
                 continue
             print(f"❌ Error polling: {e}")
             return None

def save_image(output, index):
    if not output:
        return

    img_data = None
    if 'image_base64' in output:
        img_data = output['image_base64']
    elif 'image_url' in output:
        img_url = output['image_url']
        if img_url.startswith('data:'):
            img_data = img_url.split(',')[1]
        else:
            print(f"Downloading fro URL: {img_url}")
            # ... download logic if needed, but we expect data URI ...
            pass
            
    if img_data:
        try:
            with open(f"test_explicit_{index}.png", "wb") as f:
                f.write(base64.b64decode(img_data))
            print(f"✨ Image saved to test_explicit_{index}.png")
        except Exception as e:
            print(f"❌ Error saving image: {e}")
    else:
        print(f"⚠️ No image data found in output: {output.keys()}")


def run_tests():
    print(f"🔍 Starting Uncensored Verification on {RUNPOD_ENDPOINT_ID}")
    
    for i, prompt in enumerate(PROMPTS):
        print(f"\n--- Test {i+1}/{len(PROMPTS)} ---")
        job_id = submit_job(prompt)
        if job_id:
            output = poll_job(job_id)
            if output:
                save_image(output, i)
        
        # Determine if we should wait implies a '15 minute' test logic, 
        # but for this script we just run through them.
        time.sleep(5)

if __name__ == "__main__":
    run_tests()
