#!/usr/bin/env python3
"""
Deploy ComfyUI worker to RunPod
Creates/updates templates and endpoints with the new ComfyUI image
"""

import os
import sys
import requests
import json

# Get RunPod API key from MCP/Supabase
def get_runpod_key():
    """Get RunPod API key from MCP project-secrets"""
    try:
        # Try MCP first
        import subprocess
        result = subprocess.run(
            ['python3', '-c', 
             'from mcp_project_secrets import get_api_key; '
             'print(get_api_key("runpod"))'],
            capture_output=True, text=True, timeout=2
        )
        if result.returncode == 0 and result.stdout.strip():
            key = result.stdout.strip()
            if key and not key.startswith('Error'):
                return key
    except:
        pass
    
    # Fallback to environment
    return os.getenv("RUNPOD_API_KEY")

def run_query(query, variables=None):
    """Run GraphQL query against RunPod API"""
    api_key = get_runpod_key()
    if not api_key:
        print("❌ RUNPOD_API_KEY not found")
        return None
    
    url = "https://api.runpod.io/graphql"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Query failed: {response.status_code} {response.text}")
            return None
    except Exception as e:
        print(f"❌ Request error: {e}")
        return None

def create_comfyui_template():
    """Create a RunPod template for ComfyUI worker"""
    # Get GitHub repo owner from environment or use default
    github_owner = os.getenv("GITHUB_REPOSITORY_OWNER", "your-username")
    image_name = f"ghcr.io/{github_owner}/uncensored-comfyui-worker:latest"
    
    print(f"📦 Creating template with image: {image_name}")
    
    mutation = """
    mutation($name: String!, $imageName: String!, $dockerArgs: String!) {
      saveTemplate(input: {
        name: $name,
        imageName: $imageName,
        dockerArgs: $dockerArgs,
        containerDiskInGb: 50,
        volumeInGb: 0,
        env: [],
        isServerless: true
      }) {
        id
        name
      }
    }
    """
    
    variables = {
        "name": "uncensored-comfyui-worker",
        "imageName": image_name,
        "dockerArgs": ""
    }
    
    result = run_query(mutation, variables)
    if result and 'data' in result:
        template_id = result['data']['saveTemplate']['id']
        print(f"✅ Created template: {template_id}")
        return template_id
    else:
        print(f"❌ Template creation failed: {result}")
        return None

def update_existing_endpoints(template_id):
    """Update existing endpoints to use new ComfyUI template"""
    # Get list of endpoints
    query = """
    query {
      myself {
        endpoints {
          id
          name
          templateId
        }
      }
    }
    """
    
    result = run_query(query)
    if not result or 'data' not in result:
        print("❌ Could not fetch endpoints")
        return
    
    endpoints = result['data']['myself'].get('endpoints', [])
    print(f"📋 Found {len(endpoints)} endpoints")
    
    updated = 0
    for endpoint in endpoints:
        endpoint_id = endpoint['id']
        endpoint_name = endpoint['name']
        
        print(f"🔄 Updating endpoint: {endpoint_name} ({endpoint_id})")
        
        update_mutation = """
        mutation($id: String!, $templateId: String!) {
          saveEndpoint(input: {
            id: $id,
            templateId: $templateId
          }) {
            id
            name
          }
        }
        """
        
        variables = {
            "id": endpoint_id,
            "templateId": template_id
        }
        
        update_result = run_query(update_mutation, variables)
        if update_result and 'data' in update_result:
            print(f"  ✅ Updated {endpoint_name}")
            updated += 1
        else:
            print(f"  ❌ Failed to update {endpoint_name}")
    
    print(f"\n✅ Updated {updated}/{len(endpoints)} endpoints")

def main():
    print("🚀 Deploying ComfyUI Worker to RunPod...\n")
    
    # Step 1: Create template
    template_id = create_comfyui_template()
    if not template_id:
        print("\n❌ Could not create template. Make sure:")
        print("   1. GitHub Actions has built the image")
        print("   2. Image is available at ghcr.io/YOUR_USERNAME/uncensored-comfyui-worker:latest")
        print("   3. RunPod API key is set")
        return
    
    # Step 2: Update existing endpoints
    print("\n🔄 Updating existing endpoints...")
    update_existing_endpoints(template_id)
    
    print("\n✅ Deployment complete!")
    print(f"   Template ID: {template_id}")
    print("   All endpoints updated to use ComfyUI worker")

if __name__ == "__main__":
    main()
