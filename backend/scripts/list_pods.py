import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("RUNPOD_API_KEY")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

print("🔍 Listing Active Pods to find Serverless Worker...")

# Query to list pods (myself)
query = """
query Pods {
    myself {
        pods {
            id
            name
            desiredStatus
            imageName
        }
    }
}
"""

try:
    r = requests.post(
        "https://api.runpod.io/graphql", 
        json={'query': query}, 
        headers=headers
    )
    data = r.json()
    
    if 'errors' in data:
        print(f"❌ Error: {data['errors']}")
    else:
        pods = data['data']['myself']['pods']
        print(f"found {len(pods)} pods")
        for pod in pods:
            print(f"📦 Pod: {pod['id']} | Name: {pod['name']} | Status: {pod['desiredStatus']}")
            print(f"   Image: {pod['imageName']}")
            print(f"   Uptime: {pod.get('runtime', {}).get('uptimeInSeconds')}s")
            print("-" * 20)

except Exception as e:
    print(f"❌ Request Failed: {e}")
