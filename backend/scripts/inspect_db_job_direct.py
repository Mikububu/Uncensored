
import os
from pocketbase import PocketBase
import json

PB_URL = "https://uncensored-engine-db.fly.dev"

def inspect_job(job_id):
    print(f"Connecting to {PB_URL}...")
    client = PocketBase(PB_URL)
    
    try:
        job = client.collection("jobs").get_one(job_id)
        print(f"--- Job Details: {job_id} ---")
        print(f"Status: {job.status}")
        print(f"Type: {job.type}")
        print(f"Provider: {job.params.get('provider')}")
        print(f"Worker ID: {getattr(job, 'worker_id', 'N/A')}")
        
        # Check specific error field if it exists, or look in result
        if hasattr(job, 'result'):
            print(f"Result: {json.dumps(job.result, indent=2)}")
        else:
            print("Result: <empty>")
            
        # Some implementations might put error in a separate field or inside result
        # Check standard fields
        print(f"Created: {job.created}")
        print(f"Updated: {job.updated}")
        
    except Exception as e:
        print(f"Error fetching job: {e}")

if __name__ == "__main__":
    inspect_job("zkq4roezdrgzax4")
