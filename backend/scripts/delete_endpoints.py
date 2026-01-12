import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("RUNPOD_API_KEY")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Only delete the DUPLICATE SDXL endpoint
# Keeping:
#   - whe8bovgym125o (z-image-turbo-sdxl-endpoint) = SDXL Turbo
#   - 6vzz9h1os90950 (z-image-uncensored-classic-endpoint) = SD v1.5
endpoints_to_delete = [
    "sskiyskvqr51ij",  # z-image-turbo-endpoint (duplicate SDXL)
]

print("🗑️  Deleting redundant endpoints...")

# First, list all endpoints to find the duplicate SDXL
query = """
query {
    myself {
        serverlessDiscount {
            discountFactor
            type
            expirationDate
        }
        endpoints {
            id
            name
        }
    }
}
"""

r = requests.post(
    "https://api.runpod.io/graphql",
    json={'query': query},
    headers=headers
)

data = r.json()
if 'errors' in data:
    print(f"❌ Error listing endpoints: {data['errors']}")
    exit(1)

endpoints = data['data']['myself']['endpoints']
print(f"Found {len(endpoints)} total endpoints:")
for ep in endpoints:
    print(f"  - {ep['name']}: {ep['id']}")


print(f"\n🗑️  Will delete {len(endpoints_to_delete)} endpoint(s):")
for ep_id in endpoints_to_delete:
    # Find the name
    ep_name = next((ep['name'] for ep in endpoints if ep['id'] == ep_id), 'Unknown')
    print(f"  - {ep_name} ({ep_id})")


confirm = input("\nType 'DELETE' to confirm: ")
if confirm != 'DELETE':
    print("Cancelled.")
    exit(0)

# Delete each endpoint
for ep_id in endpoints_to_delete:
    mutation = f"""
    mutation {{
        endpointDelete(input: {{ endpointId: "{ep_id}" }})
    }}
    """
    
    r = requests.post(
        "https://api.runpod.io/graphql",
        json={'query': mutation},
        headers=headers
    )
    
    result = r.json()
    if 'errors' in result:
        print(f"❌ Failed to delete {ep_id}: {result['errors']}")
    else:
        print(f"✅ Deleted {ep_id}")

print("\n✅ Consolidation complete!")
