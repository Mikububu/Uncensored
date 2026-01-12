import os
import requests
import json
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

API_KEY = os.getenv("RUNPOD_API_KEY")
ENDPOINT_ID = os.getenv("RUNPOD_ENDPOINT_ID")

def inspect_endpoints():
    print(f"🕵️ INSPECTING RUNPOD ACCOUNT...")
    
    # Try getting 'myself' or 'endpoints' list
    query = """
    query {
      myself {
        id
        endpoints {
          id
          name
          gpuIds
          templateId
          env {
             key 
             value
          }
          dockerArgs
          containerDiskSizeGb
          volumeInGb
          minDiskSizeGb
        }
      }
    }
    """
    
    res = requests.post(
        f"https://api.runpod.io/graphql?api_key={API_KEY}",
        json={"query": query},
        headers={"Content-Type": "application/json"}
    )
    
    if res.status_code != 200:
        print(f"❌ HTTP Error: {res.text}")
        return

    data = res.json()
    if "errors" in data:
        print(f"❌ GraphQL Error: {data['errors']}")
        # Fallback to older schema if needed?
        return

    endpoints = data.get("data", {}).get("myself", {}).get("endpoints", [])
    
    target = None
    for ep in endpoints:
        print(f"Found Endpoint: {ep['id']} ({ep.get('name')})")
        if ep['id'] == ENDPOINT_ID:
            target = ep
            
    if target:
        print(f"\n✅ TARGET FOUND: {target['id']}")
        print(json.dumps(target, indent=2))
        
        # Save to file for next script
        with open("target_endpoint_config.json", "w") as f:
            json.dump(target, f)
    else:
        print(f"⚠️ Target {ENDPOINT_ID} not found in account list.")

if __name__ == "__main__":
    inspect_endpoints()
