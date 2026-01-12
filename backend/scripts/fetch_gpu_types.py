import runpod
import os
import json
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

runpod.api_key = os.getenv("RUNPOD_API_KEY")

def list_gpus():
    print("🕵️ FETCHING GPU TYPES...")
    try:
        gpus = runpod.api.get_gpus()
        # gpus might be a list of objects or dicts
        
        valid_gpus = []
        for gpu in gpus:
             # runpod.api.get_gpus returns list of dicts: {'id': 'NVIDIA GeForce RTX 4090', 'displayName': ...}
             # Wait, usually the ID is something like "NVIDIA GeForce RTX 4090" or a slug.
             # Let's inspect.
             
             print(f"Found: {gpu.get('id')} / {gpu.get('displayName')} - Stock: {gpu.get('lowestPrice', {}).get('stockStatus', '?')}")
             valid_gpus.append(gpu)
             
        with open("gpu_types.json", "w") as f:
            json.dump(valid_gpus, f, indent=2)
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    list_gpus()
