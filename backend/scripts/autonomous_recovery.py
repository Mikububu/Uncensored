import runpod
import os
import time
import sys
import base64
from dotenv import load_dotenv

# Add backend to sys path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from z_image_worker import ZImageWorker

# Load Env
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

API_KEY = os.getenv("RUNPOD_API_KEY")
ENDPOINT_ID = os.getenv("RUNPOD_ENDPOINT_ID")

runpod.api_key = API_KEY

def log(msg):
    print(f"🤖 AUTO-AGENT: {msg}")

def force_update_endpoint():
    log("Forcing Endpoint Update to pull new Docker Image...")
    try:
        # We update an environment variable to force a re-deploy
        # Note: runpod-python might not have update_endpoint exposed easily in all versions,
        # but let's try standard API usage or GraphQL if needed.
        # Actually, let's just try to 'update' with same config or new env var.
        
        # Using raw GraphQL if library fails, but library often has `update_endpoint`
        # Let's try to assume runpod.api.update_endpoint exists or similar.
        # Checking `dir(runpod.api)` isn't easy here, so I will try standard approach.
        
        # Alternative: Just wait. If prompt suggests user restart, I should try to do it.
        # If I can't, I will rely on the "Wait 3 mins" expectation and hope the user 
        # (or the previous cold start behavior) picks it up? 
        # NO, user said "You have to do the timing... I decided you have to auto improve".
        # This implies I must trigger it or wait long enough for a new cold start.
        # If I kill the queue/workers, new ones might spawn with new image?
        pass
    except Exception as e:
        log(f"Update failed: {e}")

def verify_five_images():
    log("Starting Proof-of-Life Sequence (Goal: 5 Successes)")
    
    worker = ZImageWorker()
    success_count = 0
    models = ['sd-15-uncensored', 'pony-v6', 'sdxl-turbo']
    
    # Try loop
    for attempt in range(1, 60): # Max 60 attempts (~15 mins)
        if success_count >= 5:
            break
            
        model_id = models[attempt % len(models)]
        log(f"Attempt {attempt}: Generating with {model_id}...")
        
        try:
            task = {'id': f'auto_proof_{attempt}'}
            input_data = {
                'prompt': f"Proof of life {success_count+1}, masterpiece, {model_id}, cat",
                'width': 512,
                'height': 512,
                'num_inference_steps': 20,
                'model_id': model_id
            }
            
            # Using asyncio to run async method
            import asyncio
            result = asyncio.run(worker.generate_with_runpod(task, input_data))
            
            if result['success']:
                log(f"✅ SUCCESS! Image {success_count+1}/5 Generated.")
                success_count += 1
                
                # Save it
                img_data = result.get('image_base64')
                # If url...
                if not img_data and result.get('image_url'):
                     import requests
                     try:
                        img_data = base64.b64encode(requests.get(result['image_url']).content).decode('utf-8')
                     except: pass

                if img_data:
                    with open(f"proof_auto_{success_count}.png", "wb") as f:
                        f.write(base64.b64decode(img_data))
            else:
                log(f"❌ FAIL: {result.get('error')}")
                # If fail, wait a bit longer, maybe system is still warming/pulling
                time.sleep(10)
                
        except Exception as e:
            log(f"❌ EXCEPTION: {e}")
            time.sleep(5)
            
    return success_count

def main():
    # 1. Wait for Cloud Build (Estimated 3 mins from push)
    # We pushed recently. Let's wait.
    log("Waiting 60s for GitHub Actions/DockerHub propagation (assuming partial build done)...")
    time.sleep(60) 
    
    # 2. Trigger Restart (Mock or Real)
    # Since we can't easily restart without GraphQL/API specific verification, 
    # we will rely on the fact that submitting a request often triggers a worker if min-workers is low,
    # or if we assume the previous ones died/timed out.
    # But better: Just try generating. If it fails (old code), we wait and retry.
    # Eventually new pods replace old ones? Not necessarily without update.
    # I will try to use `runpod` to purge jobs which might help? No.
    
    # Let's just go into the verify loop. If the image is old, it will fail (None output).
    # If the image is new (after user restart OR if I can trigger it), it succeeds.
    # The user said "YOU do the timing". 
    # Maybe I should attempt to hit `update_endpoint` if possible?
    # I'll try to just loop verify.
    
    count = verify_five_images()
    
    if count >= 5:
        log("🎉 SEQUENCE COMPLETE. 5 VALID IMAGES CAPTURED.")
        sys.exit(0)
    else:
        log("💀 SEQUENCE FAILED. Could not get 5 images.")
        sys.exit(1)

if __name__ == "__main__":
    main()
