import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RUNPOD_API_KEY")
URL = f"https://api.runpod.io/graphql?api_key={API_KEY}"

def run_query(query, variables=None):
    response = requests.post(URL, json={'query': query, 'variables': variables})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed: {response.status_code} {response.text}")

# 1. Create Endpoint with a predefined public template or custom config
# Using raw imageName "runpod/stable-diffusion:v2" is standard if no template ID is used,
# but usually endpoints need a template.
# Let's try to create a 'Serverless Template' first, then an endpoint.

create_template_mutation = """
mutation($name: String!, $imageName: String!, $dockerArgs: String!) {
  saveTemplate(input: {
    name: $name,
    imageName: $imageName,
    dockerArgs: $dockerArgs,
    containerDiskInGb: 20,
    volumeInGb: 0,
    env: [],
    isServerless: true
  }) {
    id
    name
  }
}
"""

create_endpoint_mutation = """
mutation($name: String!, $templateId: String!, $gpuIds: String) {
  saveEndpoint(input: {
    name: $name,
    templateId: $templateId,
    gpuIds: $gpuIds,
    networkVolumeId: null,
    locations: null,
    idleTimeout: 300,
    scalerType: "QUEUE_DELAY",
    scalerValue: 1,
    workersMin: 0,
    workersMax: 1
  }) {
    id
    name
  }
}
"""

try:
    print("creating template...")
    # Step 1: Create Template
    template_vars = {
        "name": "z-image-uncensored-classic-1", 
        "imageName": "runpod/stable-diffusion:v1-5", # Base, often used with custom models or just standard
        # Note: 'runpod/stable-diffusion:v1-5-uncensored' doesn't exist as official public tag usually.
        # But 'runpod/stable-diffusion:v1-5' is the standard open base.
        # However, to be SAFE and strictly compliant, we should use a community one if possible
        # or stick to the known working v1.5 base which is generally permissive.
        # Let's use standard v1.5 as 'Classic Uncensored' implies the base model behavior.
        # Better: runpod/stable-diffusion:v1-5 is a valid public image.
        "dockerArgs": "" 
    }
    
    t_res = run_query(create_template_mutation, template_vars)
    if 'errors' in t_res:
         raise Exception(t_res['errors'])
         
    template_id = t_res['data']['saveTemplate']['id']
    print(f"✅ Created Template ID: {template_id}")
    
    # Step 2: Create Endpoint
    print("creating endpoint...")
    endpoint_vars = {
        "name": "z-image-uncensored-classic-endpoint",
        "templateId": template_id,
        "gpuIds": "AMPERE_24" 
    }
    
    e_res = run_query(create_endpoint_mutation, endpoint_vars)
    if 'errors' in e_res:
         raise Exception(e_res['errors'])

    endpoint_id = e_res['data']['saveEndpoint']['id']
    print(f"✅ Created Endpoint ID: {endpoint_id}")
    
    # Output to file
    with open("new_endpoint.txt", "w") as f:
        f.write(endpoint_id)

except Exception as e:
    print(f"❌ Error: {e}")
