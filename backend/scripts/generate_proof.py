import sys
import os
import time
import requests
import base64
import random

# Add backend to sys path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# We need to hit the running backend API or RunPod directly.
# Let's hit the deployed backend API to test the full stack.
API_URL = "https://uncensored-explicit-worker.fly.dev" 
# Fallback to direct RunPod if backend is down? No, user uses the app.

def generate_proof_images():
    print("🕵️ STARTING PROOF OF LIFE: 5 IMAGES 🕵️")
    
    # Models to test
    models = ['sdxl-turbo', 'pony-v6', 'sd-15-uncensored']
    
    success_count = 0
    
    for i in range(1, 6):
        model_id = random.choice(models)
        prompt = f"Proof of life image {i}, masterpiece, best quality, {model_id}, cat wearing a hat"
        print(f"\n[JOB {i}/5] Submitting to {model_id}...")
        
        try:
            # We need to mock the job creation like the frontend does.
            # But we don't have PocketBase auth here easily.
            # So we will invoke the ZImageWorker class DIRECTLY locally if possible,
            # OR we check if there's a direct generation endpoint.
            
            # The backend `server.py` doesn't expose a direct "generate" endpoint, it listens to PocketBase.
            # So testing "full stack" is hard without PB auth.
            # BETTER OPTION: Use ZImageWorker directly from this script, 
            # effectively acting as the backend worker.
            
            from z_image_worker import ZImageWorker
            worker = ZImageWorker() # This reads env vars
            
            # Verify ENV vars are loaded
            if not worker.runpod_api_key or not worker.endpoint_id:
                print("❌ ERROR: Missing ENV vars. Loading from .env...")
                from dotenv import load_dotenv
                load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
                worker = ZImageWorker()

            # Construct Payload
            task = {'id': f'proof_{i}'}
            input_data = {
                'prompt': prompt,
                'width': 512, # Safe Res
                'height': 512,
                'num_inference_steps': 20,
                'guidance_scale': 7,
                'model_id': model_id
            }
            
            print("   -> Sending to RunPod...")
            start_t = time.time()
            result = asyncio.run(worker.generate_with_runpod(task, input_data))
            dur = time.time() - start_t
            
            if result['success']:
                print(f"   ✅ SUCCESS ({dur:.2f}s)")
                
                # Save Image
                img_data = result.get('image_base64')
                if not img_data and result.get('image_url'):
                    # Download URL
                    import requests
                    img_data = base64.b64encode(requests.get(result['image_url']).content).decode('utf-8')
                    
                if img_data:
                    filename = f"proof_image_{i}_{model_id}.png"
                    with open(filename, "wb") as f:
                        f.write(base64.b64decode(img_data))
                    print(f"   💾 Saved to {filename}")
                    success_count += 1
                else:
                    print("   ❌ FAILURE: No image data in success response.")
            else:
                print(f"   ❌ FAILURE: {result.get('error')}")

        except Exception as e:
            print(f"   ❌ EXCEPTION: {e}")

    print(f"\n📊 SUMMARY: {success_count}/5 Successful.")
    
    if success_count == 5:
        print("🎉 MISSION ACCOMPLISHED.")
    else:
        print("💀 MISSION FAILED.")

import asyncio
if __name__ == "__main__":
    generate_proof_images()
