import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv('backend/.env')
api_key = os.getenv('RUNPOD_API_KEY')
pod_id = "zfgep93pvydisz"

def get_pod_logs():
    print(f"📄 Fetching Logs for Pod {pod_id}...")
    
    query = """
    query PodLogs($id: String!) {
      pod(input: {podId: $id}) {
        id
        runtime {
            containerLogs {
                stdout
                stderr
            }
        }
      }
    }
    """
    
    try:
        r = requests.post(
            "https://api.runpod.io/graphql", 
            json={"query": query, "variables": {"id": pod_id}}, 
            headers={"Authorization": f"Bearer {api_key}"}
        )
        data = r.json()
        
        if 'errors' in data:
            print(f"❌ Error: {data['errors'][0]['message']}")
            return

        pod = data.get('data', {}).get('pod')
        logs = pod.get('runtime', {}).get('containerLogs', [])
        
        if not logs:
            print("No logs found yet.")
            return

        print("--- STDOUT ---")
        for log in logs:
            print(log.get('stdout', ''))
            
        print("\n--- STDERR ---")
        for log in logs:
            print(log.get('stderr', ''))

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    get_pod_logs()
