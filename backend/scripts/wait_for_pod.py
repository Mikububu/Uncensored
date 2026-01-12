import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv('backend/.env')
api_key = os.getenv('RUNPOD_API_KEY')
pod_id = "24hz46kbtb2si8"  # Hardcoded based on successful creation

def wait_for_pod():
    print(f"⏳ Waiting for Pod {pod_id} to be READY...")
    
    while True:
        # Simplified query without the problematic 'containerStatus'
        query = """
        query GetPod($id: String!) {
            pod(input: {podId: $id}) {
                id
                desiredStatus
                lastStatusChange
                runtime {
                    ports {
                        ip
                        privatePort
                        publicPort
                        type
                    }
                    gpus {
                        id
                        gpuUtilPercent
                        memoryUtilPercent
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
                print(f"   Error fetching status: {data['errors'][0]['message']}")
                time.sleep(5)
                continue
                
            pod = data.get('data', {}).get('pod')
            if not pod:
                print("   Pod not found in response?")
                time.sleep(5)
                continue

            status = pod.get('desiredStatus', 'UNKNOWN')
            
            runtime = pod.get('runtime')
            if runtime:
                 # Check if we have public IP/Port
                 ports = runtime.get('ports', [])
                 if ports:
                     print(f"   ✅ Pod is RUNNING! Connection info found.")
                     for p in ports:
                         print(f"      - {p['ip']}:{p['publicPort']} -> {p['privatePort']}")
                     return pod
            
            print(f"   Status: {status} (Waiting for IP/Ports...)")
            time.sleep(5)
            
        except Exception as e:
            print(f"   Check failed: {e}")
            time.sleep(5)

if __name__ == "__main__":
    wait_for_pod()
