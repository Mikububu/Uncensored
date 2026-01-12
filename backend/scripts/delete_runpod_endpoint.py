
import os
import requests
import json

api_key = "os.getenv("RUNPOD_API_KEY") or os.getenv("RUNPOD_KEY")"

def delete_endpoint(eid):
    url = "https://api.runpod.io/graphql"
    
    mutation = """
    mutation($id: String!) {
      deleteEndpoint(id: $id)
    }
    """
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(url, json={"query": mutation, "variables": {"id": eid}}, headers=headers)
        r.raise_for_status()
        print(f"Delete Result for {eid}: {r.json()}")
    except Exception as e:
        print(f"Error deleting {eid}: {e}")

if __name__ == "__main__":
    delete_endpoint("tyj2436ozcz419")
    delete_endpoint("ne2b1gv0itfl8s")
