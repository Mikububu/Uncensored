
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv(dotenv_path='backend/.env')
api_key = os.getenv("RUNPOD_API_KEY")

def delete_endpoint(endpoint_id):
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
        r = requests.post(url, json={"query": mutation, "variables": {"id": endpoint_id}}, headers=headers)
        print(f"Delete Result for {endpoint_id}: {json.dumps(r.json(), indent=2)}")
    except Exception as e:
        print(f"Error deleting {endpoint_id}: {e}")

if __name__ == "__main__":
    unused = ["cv5aetbohalzc8"]
    for eid in unused:
        delete_endpoint(eid)
