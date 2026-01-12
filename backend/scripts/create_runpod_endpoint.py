
import os
import requests
import json

api_key = "os.getenv("RUNPOD_API_KEY") or os.getenv("RUNPOD_KEY")"

def create_endpoint():
    url = "https://api.runpod.io/graphql"
    
    mutation = """
    mutation($input: EndpointInput!) {
      saveEndpoint(input: $input) {
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
    
    variables = {
        "input": {
            "name": "z-uncensored-ada-16",
            "templateId": "5ugs7iop50", 
            "gpuIds": "ADA_16",
            "workersMin": 0, 
            "workersMax": 1,
            "idleTimeout": 300
        }
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(url, json={"query": mutation, "variables": variables}, headers=headers)
        r.raise_for_status()
        data = r.json()
        print(f"Create Result: {json.dumps(data, indent=2)}")
        return data
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_endpoint()
