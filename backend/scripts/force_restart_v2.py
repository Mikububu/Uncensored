import os
import time
import requests
import json
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

API_KEY = os.getenv("RUNPOD_API_KEY")
ENDPOINT_ID = os.getenv("RUNPOD_ENDPOINT_ID")
RUNPOD_API_URL = f"https://api.runpod.io/graphql?api_key={API_KEY}"

def run_query(query, variables=None):
    headers = {"Content-Type": "application/json"}
    payload = {"query": query}
    if variables: payload["variables"] = variables
    res = requests.post(RUNPOD_API_URL, headers=headers, json=payload)
    if res.status_code != 200: raise Exception(res.text)
    return res.json()

def force_restart_v2():
    print(f"🔄 FORCE RESTART V2: {ENDPOINT_ID}")
    
    # 1. Fetch via 'myself' (Safer)
    q_fetch = """
    query {
      myself {
        endpoints {
          id
          env { key value }
          gpuIds
          workersMin
          workersMax
          idleTimeout
          scalerType
          scalerValue
          templateId
        }
      }
    }
    """
    
    data = run_query(q_fetch)
    endpoints = data.get("data", {}).get("myself", {}).get("endpoints", [])
    
    target = next((e for e in endpoints if e['id'] == ENDPOINT_ID), None)
    if not target:
        print("❌ Target endpoint not found.")
        return

    print("✅ Found Target Endpoint.")
    current_env = target.get('env') or []
    
    # 2. Prepare Update
    new_env = [x for x in current_env if x['key'] != 'RESTART_TRIGGER']
    new_env.append({'key': 'RESTART_TRIGGER', 'value': str(int(time.time()))})
    
    q_update = """
    mutation UpdateEndpoint($id: String!, $input: EndpointInput!) {
      updateEndpoint(id: $id, input: $input) {
        id
        env { key value }
      }
    }
    """
    
    # Minimal Input
    update_input = {
        "env": new_env,
        "workersMin": target['workersMin'],
        "workersMax": target['workersMax'],
        "idleTimeout": target['idleTimeout'],
        "scalerType": target['scalerType'],
        "scalerValue": target['scalerValue']
    }
    
    print("🚀 Sending Update Mutation...")
    res = run_query(q_update, {"id": ENDPOINT_ID, "input": update_input})
    
    if "errors" in res:
        print(f"❌ UPDATE FAILED: {res['errors']}")
    else:
        print("✅ UPDATE SUCCESS: RESTART_TRIGGER injected.")

if __name__ == "__main__":
    force_restart_v2()
