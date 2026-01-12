import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv('backend/.env')
api_key = os.getenv('RUNPOD_API_KEY')
# Official SDXL Template (8so3fiji3e)
template_id = "8so3fiji3e"

def create_pod_request(gpu_id, cloud_type):
    print(f"   Trying {gpu_id} ({cloud_type})...")
    url = "https://api.runpod.io/graphql"
    
    query = """
    mutation CreatePod($input: PodFindAndDeployOnDemandInput!) {
      podFindAndDeployOnDemand(input: $input) {
        id
        name
        imageName
        desiredStatus
        machineId
        machine {
            podHostId
        }
      }
    }
    """
    
    variables = {
        "input": {
            "cloudType": cloud_type, 
            "gpuCount": 1,
            "volumeInGb": 60,
            "containerDiskInGb": 60,
            "minVcpuCount": 2,
            "minMemoryInGb": 15,
            "gpuTypeId": gpu_id,
            "name": f"Ded-Official-SDXL-{gpu_id.replace(' ', '-')}",
            # "imageName": "runpod/stable-diffusion:v1-5", # REMOVED: Let template decide
            # "dockerArgs": "", # REMOVED: Let template decide
            "ports": "3000/http",
            "volumeMountPath": "/workspace",
            "templateId": template_id
        }
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
        data = r.json()
        
        if 'errors' in data:
            # print(f"      Response: {data['errors'][0]['message']}")
            return None
            
        pod = data['data']['podFindAndDeployOnDemand']
        return pod

    except Exception as e:
        print(f"      Exception: {e}")
        return None

def create_dedicated_pod():
    print("🚀 Provisioning Dedicated GPU Pod (With Fallbacks)...")
    
    # Priority List: GPU ID, Cloud Type
    configs = [
        ("NVIDIA GeForce RTX 4090", "COMMUNITY"),
        ("NVIDIA GeForce RTX 3090", "COMMUNITY"),
        ("NVIDIA RTX 6000 Ada Generation", "COMMUNITY"),
        ("NVIDIA RTX A6000", "COMMUNITY"),
        ("NVIDIA RTX A5000", "COMMUNITY"),
        ("NVIDIA RTX A4500", "COMMUNITY"),
        ("NVIDIA RTX A4000", "COMMUNITY"),
        ("NVIDIA GeForce RTX 4090", "SECURE"), # Retry secure if community failed
    ]
    
    for gpu_id, cloud_type in configs:
        pod = create_pod_request(gpu_id, cloud_type)
        if pod:
             print(f"✅ Pod Created Successfully!")
             print(f"   ID: {pod['id']}")
             print(f"   GPU: {gpu_id} ({cloud_type})")
             return pod['id']
        else:
             print(f"   ❌ Failed/Unavailable. Trying next...")
             
    print("❌ All fallback options failed.")
    return None

def wait_for_pod(pod_id):
    print(f"⏳ Waiting for Pod {pod_id} to be READY...")
    
    while True:
        # Check status
        # (This uses a separate health/status check call logic or runpod lib, 
        #  but for simplicity in this script we'll just poll the API)
        
        # We need a query to get pod status by ID
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
                    containerStatus {
                        reason
                        message
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
                print(f"   Error fetching status: {data['errors']}")
                time.sleep(5)
                continue
                
            pod = data['data']['pod']
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
    pod_id = create_dedicated_pod()
    if pod_id:
        wait_for_pod(pod_id)
