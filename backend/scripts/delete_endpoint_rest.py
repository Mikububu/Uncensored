import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("RUNPOD_API_KEY")

headers = {
    "Authorization": f"Bearer {api_key}",
}

# Endpoint to delete
endpoint_id = "sskiyskvqr51ij"  # z-image-turbo-endpoint (duplicate)

print(f"🗑️  Deleting endpoint {endpoint_id}...")

# Use REST API instead of GraphQL
url = f"https://api.runpod.io/v2/{endpoint_id}"

try:
    r = requests.delete(url, headers=headers)
    
    if r.status_code == 204 or r.status_code == 200:
        print(f"✅ Successfully deleted {endpoint_id}")
    else:
        print(f"❌ Failed to delete: {r.status_code}")
        print(f"   Response: {r.text}")
except Exception as e:
    print(f"❌ Error: {e}")
