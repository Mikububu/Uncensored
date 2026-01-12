
import os
import requests
import json

api_key = "os.getenv("RUNPOD_API_KEY") or os.getenv("RUNPOD_KEY")"

def list_all_endpoints():
    url = "https://api.runpod.io/graphql"
    query = """
    query {
      myself {
        endpoints {
          id
          name
          templateId
        }
      }
    }
    """
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(url, json={"query": query}, headers=headers)
        r.raise_for_status()
        data = r.json()
        print(f"Endpoints: {json.dumps(data, indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_all_endpoints()
