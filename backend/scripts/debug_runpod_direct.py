import runpod
import os
import time
from dotenv import load_dotenv

# Load Env
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

API_KEY = os.getenv("RUNPOD_API_KEY")
ENDPOINT_ID = os.getenv("RUNPOD_ENDPOINT_ID")

runpod.api_key = API_KEY

def debug_runpod():
    print(f"🕵️ DEBUGGING RUNPOD DIRECTLY: {ENDPOINT_ID}")
    
    # Test only Pony V6 first (Base model)
    payload = {
        "input": {
            "prompt": "DEBUG PROOF OF LIFE, cat",
            "width": 512,
            "height": 512,
            "num_inference_steps": 20,
            "model_id": "pony-v6" 
        }
    }
    
    try:
        endpoint = runpod.Endpoint(ENDPOINT_ID)
        run_request = endpoint.run(payload)
        
        job_id = run_request.job_id
        print(f"👉 Job Submitted: {job_id}")
        
        # Poll Manually to see status
        while True:
            # Refresh job status
            status = run_request.status() # This makes API call
            print(f"   Status: {status}")
            
            if status == 'COMPLETED':
                output = run_request.output()
                print(f"✅ COMPLETED. Output: {output}")
                break
            elif status == 'FAILED':
                # Can we get the error detail?
                 # Often need to call specific API or just look at output
                 # runpod-python usually raises error on output() if failed
                 try:
                     run_request.output()
                 except Exception as e:
                     print(f"❌ FAILED. Error: {e}")
                 break
                
            time.sleep(2)
            
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")

if __name__ == "__main__":
    debug_runpod()
