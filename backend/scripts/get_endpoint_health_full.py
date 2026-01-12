
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv(dotenv_path='backend/.env')
api_key = os.getenv("RUNPOD_API_KEY")
endpoint_id = os.getenv("RUNPOD_ENDPOINT_ID")

def get_worker_logs():
    url = "https://api.runpod.io/graphql"
    
    # Query for endpoint workers
    query = """
    query Endpoint($id: String!) {
      endpoint(id: $id) {
        id
        name
        templateId
        gpuIds
        workersMin
        workersMax
        idleTimeout
      }
    }
    """
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(url, json={"query": query, "variables": {"id": endpoint_id}}, headers=headers)
        data = r.json()
        print(f"Endpoint Details: {json.dumps(data, indent=2)}")
        
        # There is no direct "worker logs" for serverless via GraphQL usually, 
        # it's usually via the status/health API or the UI.
        # But we can check health again more deeply.
        
        health_url = f"https://api.runpod.ai/v2/{endpoint_id}/health"
        r_health = requests.get(health_url, headers=headers)
        print(f"Health: {json.dumps(r_health.json(), indent=2)}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_worker_logs()
