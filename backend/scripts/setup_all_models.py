#!/usr/bin/env python3
"""
Script to automatically create RunPod endpoints for all uncensored models.
This will set up serverless endpoints for each model in the models.json config.
"""
import os
import json
import requests
import sys
from pathlib import Path

# Get RunPod API key from environment
RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")
if not RUNPOD_API_KEY:
    print("❌ ERROR: RUNPOD_API_KEY environment variable not set")
    sys.exit(1)

# Load model configuration
CONFIG_PATH = Path(__file__).parent.parent.parent / "config" / "models.json"
if not CONFIG_PATH.exists():
    print(f"❌ ERROR: Config file not found at {CONFIG_PATH}")
    sys.exit(1)

with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

models = config.get('models', [])

# GraphQL endpoint
GRAPHQL_URL = "https://api.runpod.io/graphql"
headers = {
    "Authorization": f"Bearer {RUNPOD_API_KEY}",
    "Content-Type": "application/json"
}

def run_query(query, variables=None):
    """Execute a GraphQL query"""
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    
    response = requests.post(GRAPHQL_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed: {response.status_code} {response.text}")

def create_template(model):
    """Create a RunPod template for a model"""
    template_name = f"uncensored-{model['id']}"
    
    # Use appropriate base image
    image_name = model.get('runpod_template', 'runpod/stable-diffusion:v1-5')
    
    mutation = """
    mutation($name: String!, $imageName: String!, $dockerArgs: String!) {
      saveTemplate(input: {
        name: $name,
        imageName: $imageName,
        dockerArgs: $dockerArgs,
        containerDiskInGb: 50,
        volumeInGb: 0,
        env: [
          { key: "MODEL_ID", value: "%s" }
        ],
        isServerless: true
      }) {
        id
        name
      }
    }
    """ % model['id']
    
    variables = {
        "name": template_name,
        "imageName": image_name,
        "dockerArgs": model.get('docker_args', '')
    }
    
    try:
        result = run_query(mutation, variables)
        if 'errors' in result:
            print(f"  ⚠️  Template creation error: {result['errors']}")
            return None
        template_id = result['data']['saveTemplate']['id']
        print(f"  ✅ Created template: {template_id}")
        return template_id
    except Exception as e:
        print(f"  ❌ Template creation failed: {e}")
        return None

def create_endpoint(model, template_id):
    """Create a RunPod endpoint for a model"""
    endpoint_name = f"uncensored-{model['id']}-endpoint"
    
    mutation = """
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
    
    # Select GPU based on model requirements
    # SD 1.5 models can use smaller GPUs, SDXL/Flux need more VRAM
    if model.get('base_model') in ['SDXL', 'Flux']:
        gpu_ids = "AMPERE_24"  # RTX 3090 or A40
    else:
        gpu_ids = "AMPERE_16"  # RTX 3080 or similar
    
    variables = {
        "name": endpoint_name,
        "templateId": template_id,
        "gpuIds": gpu_ids
    }
    
    try:
        result = run_query(mutation, variables)
        if 'errors' in result:
            print(f"  ⚠️  Endpoint creation error: {result['errors']}")
            return None
        endpoint_id = result['data']['saveEndpoint']['id']
        print(f"  ✅ Created endpoint: {endpoint_id}")
        return endpoint_id
    except Exception as e:
        print(f"  ❌ Endpoint creation failed: {e}")
        return None

def main():
    print("🚀 Setting up RunPod endpoints for all uncensored models...\n")
    
    results = {}
    
    for model in models:
        model_id = model['id']
        model_name = model['name']
        print(f"\n📦 Processing: {model_name} ({model_id})")
        
        # Create template
        template_id = create_template(model)
        if not template_id:
            print(f"  ⏭️  Skipping {model_id} due to template creation failure")
            continue
        
        # Create endpoint
        endpoint_id = create_endpoint(model, template_id)
        if endpoint_id:
            results[model_id] = {
                'name': model_name,
                'template_id': template_id,
                'endpoint_id': endpoint_id
            }
    
    # Save results to file
    output_file = Path(__file__).parent.parent / "endpoints.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Setup complete! Created {len(results)} endpoints")
    print(f"📄 Endpoint IDs saved to: {output_file}")
    print("\n📋 Summary:")
    for model_id, info in results.items():
        print(f"  {info['name']}: {info['endpoint_id']}")

if __name__ == "__main__":
    main()
