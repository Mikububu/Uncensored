import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("RUNPOD_API_KEY")
endpoints = {
    "Classic (SD v1.5)": os.getenv("RUNPOD_ENDPOINT_ID_SDV2"),
    "Turbo (SDXL)": os.getenv("RUNPOD_ENDPOINT_ID_SDXL")
}

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

print("🔍 Diagnosing RunPod Endpoints...")

for name, endpoint_id in endpoints.items():
    if not endpoint_id:
        print(f"❌ {name}: No ID found in env")
        continue

    print(f"\n--- Checking {name} ({endpoint_id}) ---")
    
    # 1. Get Endpoint Health/Status
    # RunPod v2 API: GET /v2/{endpoint_id}/health (or similar, falling back to GraphQL if needed)
    # Using GraphQL to get accurate worker/queue info as specific REST endpoints vary.
    
    # 1. Get Endpoint Health/Status via REST
    # Doc: https://docs.runpod.io/reference/endpoint-health
    url = f"https://api.runpod.ai/v2/{endpoint_id}/health"
    
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        
        # Check standard fields
        workers = data.get('workers', {})
        jobs = data.get('jobs', {})
        
        print(f"✅ Status Code: {r.status_code}")
        print(f"   Workers: Idle={workers.get('idle')}, Running={workers.get('running')}, Initializing={workers.get('initializing')}")
        print(f"   Queue: InProgress={jobs.get('inProgress')}, InQueue={jobs.get('inQueue')}")
        
    except Exception as e:
        print(f"❌ REST Request Failed: {e}")
