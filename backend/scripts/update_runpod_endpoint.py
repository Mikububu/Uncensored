
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='backend/.env')
api_key = os.getenv("RUNPOD_API_KEY")
endpoint_id = os.getenv("RUNPOD_ENDPOINT_ID") # Updated to use env var

def update_endpoint():
    url = "https://api.runpod.io/graphql"
    
    query = """
    mutation UpdateEndpoint($endpoint: EndpointInput!) {
      saveEndpoint(input: $endpoint) {
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
    
    # Check if we should use the 'fast' template settings or standard
    # Using hardcoded values for safety based on current plan
    variables = {
        "endpoint": {
            "id": endpoint_id,
            "name": "z-official-sdxl-16",
            "templateId": "8so3fiji3e", 
            "gpuIds": "ADA_16",
            "workersMin": 1, 
            "workersMax": 1,
            "idleTimeout": 300
        }
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    print(f"Updating endpoint {endpoint_id} to Min 1...")
    try:
        r = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
        print(f"Update Result: {json.dumps(r.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_endpoint()
