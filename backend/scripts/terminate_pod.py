import os
import requests
import json
from dotenv import load_dotenv

load_dotenv('backend/.env')
api_key = os.getenv('RUNPOD_API_KEY')
pod_id = "zfgep93pvydisz"

def terminate_pod():
    print(f"🧨 Terminating Pod {pod_id}...")
    url = "https://api.runpod.io/graphql"
    
    query = """
    mutation TerminatePod($id: String!) {
      podTerminate(input: {podId: $id})
    }
    """
    
    try:
        r = requests.post(
            url, 
            json={"query": query, "variables": {"id": pod_id}}, 
            headers={"Authorization": f"Bearer {api_key}"}
        )
        data = r.json()
        print(f"Result: {json.dumps(data, indent=2)}")
        
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    terminate_pod()
