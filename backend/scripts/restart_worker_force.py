import os
import time
import requests
import json
from dotenv import load_dotenv

# Load Env
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

API_KEY = os.getenv("RUNPOD_API_KEY")
ENDPOINT_ID = os.getenv("RUNPOD_ENDPOINT_ID")

RUNPOD_API_URL = f"https://api.runpod.io/graphql?api_key={API_KEY}"

def run_query(query, variables=None):
    headers = {"Content-Type": "application/json"}
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
        
    response = requests.post(RUNPOD_API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"GraphQL Query Failed: {response.text}")
    return response.json()

def force_restart():
    print(f"🔄 INITIATING FORCED RESTART FOR: {ENDPOINT_ID}")
    
    # 1. Fetch Current Config
    query_info = """
    query Endpoint($id: String!) {
      endpoint(id: $id) {
        id
        env {
          key
          value
        }
        gpuIds
        networkVolumeId
        locations
        idleTimeout
        scalerType
        scalerValue
        workersMin
        workersMax
        templateId
      }
    }
    """
    
    data = run_query(query_info, {"id": ENDPOINT_ID})
    endpoint = data.get("data", {}).get("endpoint")
    
    if not endpoint:
        print("❌ ERROR: Could not fetch endpoint details.")
        return

    current_env = endpoint.get("env", [])
    print(f"   Current Env Vars: {len(current_env)}")
    
    # 2. Modify Env (Add/Update RESTART_TRIGGER)
    new_env = [item for item in current_env if item['key'] != 'RESTART_TRIGGER']
    new_env.append({'key': 'RESTART_TRIGGER', 'value': str(int(time.time()))})
    
    # 3. Update Endpoint
    query_update = """
    mutation UpdateEndpoint($id: String!, $input: EndpointInput!) {
      updateEndpoint(id: $id, input: $input) {
        id
        adapterId
        gpuIds
        idleTimeout
        locations
        networkVolumeId
        scalerType
        scalerValue
        templateId
        workersMax
        workersMin
        env {
          key
          value
        }
      }
    }
    """
    
    # Construct Input (Only include fields we want to keep/update)
    # Note: RunPod API requires passing back most fields or they might reset? 
    # Usually 'input' handles updates. 
    # We must match the EndpointInput structure.
    
    update_input = {
        "env": new_env,
        # We might need to preserve other fields if the API is replace-based.
        # RunPod updateEndpoint usually does a merge or partial update? 
        # Safest is to pass known scaler vals.
        "idleTimeout": endpoint['idleTimeout'],
        "scalerType": endpoint['scalerType'],
        "scalerValue": endpoint['scalerValue'],
        "workersMin": endpoint['workersMin'],
        "workersMax": endpoint['workersMax']
    }
    
    print("   Sending Update Mutation...")
    res = run_query(query_update, {"id": ENDPOINT_ID, "input": update_input})
    
    if "errors" in res:
        print(f"❌ ERROR: {res['errors']}")
    else:
        print("✅ SUCCESS: Endpoint updated. Restart triggering...")
        print("   Worker should recycle within 60 seconds.")

if __name__ == "__main__":
    force_restart()
