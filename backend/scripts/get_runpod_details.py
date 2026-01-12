
import os
import requests
import json

api_key = "os.getenv("RUNPOD_API_KEY") or os.getenv("RUNPOD_KEY")"
endpoint_id = "fxk8l9aqh27zx2"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def get_endpoint_details():
    # RunPod GraphQL API is better for this
    url = "https://api.runpod.io/graphql"
    
    query = """
    query {
      myself {
        endpoints {
          id
          name
          templateId
          gpuIds
          idleTimeout
          locations
          scalerType
          scalerValue
          workersMin
          workersMax
        }
      }
    }
    """
    
    try:
        r = requests.post(url, headers=headers, json={"query": query})
        r.raise_for_status()
        data = r.json()
        endpoints = data.get('data', {}).get('myself', {}).get('endpoints', [])
        
        for ep in endpoints:
            if ep['id'] == endpoint_id:
                print(f"Endpoint: {ep['name']} ({ep['id']})")
                print(f"Template ID: {ep['templateId']}")
                print(f"GPU IDs: {ep['gpuIds']}")
                print(f"Workers: Min={ep['workersMin']}, Max={ep['workersMax']}")
                print(f"Scaler: {ep['scalerType']}={ep['scalerValue']}")
                print(f"Idle Timeout: {ep['idleTimeout']}")
                return ep
        
        print("Endpoint not found in list.")
        # Print all endpoints just in case
        print("\nAll Endpoints:")
        for ep in endpoints:
             print(f"- {ep['name']} ({ep['id']})")
             
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_endpoint_details()
