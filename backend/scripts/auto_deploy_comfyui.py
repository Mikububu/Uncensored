#!/usr/bin/env python3
"""
Fully automated ComfyUI deployment
Uses Supabase keys to deploy to RunPod automatically
"""

import os
import sys
import requests
import json
import subprocess
from pathlib import Path

def get_runpod_key():
    """Get RunPod API key from MCP/Supabase"""
    try:
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
    return os.getenv("RUNPOD_API_KEY")

def get_github_owner():
    """Get GitHub repository owner"""
    # Try to get from git remote
    try:
        result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            capture_output=True, text=True, timeout=2
        )
        if result.returncode == 0:
            url = result.stdout.strip()
            # Extract owner from URL
            if 'github.com' in url:
                parts = url.replace('.git', '').split('/')
                if len(parts) >= 2:
                    return parts[-2]
    except:
        pass
    return os.getenv("GITHUB_REPOSITORY_OWNER", "your-username")

def check_image_exists(image_name):
    """Check if Docker image exists in GitHub Container Registry"""
    # For now, we'll assume it exists if GitHub Actions has run
    # In production, you'd check the registry API
    print(f"📦 Checking if image exists: {image_name}")
    print("   (Assuming image exists if GitHub Actions completed)")
    return True

def create_or_update_template(image_name, api_key):
    """Create or update RunPod template"""
    url = "https://api.runpod.io/graphql"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # First, check if template exists
    check_query = """
    query {
      myself {
        templates {
          id
          name
          imageName
        }
      }
    }
    """
    
    result = requests.post(url, json={"query": check_query}, headers=headers)
    if result.status_code == 200:
        data = result.json()
        templates = data.get('data', {}).get('myself', {}).get('templates', [])
        
        # Look for existing template
        for template in templates:
            if template.get('name') == 'uncensored-comfyui-worker':
                template_id = template['id']
                print(f"✅ Found existing template: {template_id}")
                
                # Update it
                update_mutation = """
                mutation($id: String!, $imageName: String!) {
                  saveTemplate(input: {
                    id: $id,
                    imageName: $imageName,
                    containerDiskInGb: 50
                  }) {
                    id
                    name
                  }
                }
                """
                
                variables = {
                    "id": template_id,
                    "imageName": image_name
                }
                
                update_result = requests.post(
                    url, 
                    json={"query": update_mutation, "variables": variables},
                    headers=headers
                )
                
                if update_result.status_code == 200:
                    print(f"✅ Updated template with new image")
                    return template_id
    
    # Create new template
    print("📦 Creating new template...")
    create_mutation = """
    mutation($name: String!, $imageName: String!) {
      saveTemplate(input: {
        name: $name,
        imageName: $imageName,
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
        "imageName": image_name
    }
    
    result = requests.post(
        url,
        json={"query": create_mutation, "variables": variables},
        headers=headers
    )
    
    if result.status_code == 200:
        data = result.json()
        if 'data' in data and 'saveTemplate' in data['data']:
            template_id = data['data']['saveTemplate']['id']
            print(f"✅ Created template: {template_id}")
            return template_id
    
    print(f"❌ Failed to create template: {result.text}")
    return None

def update_endpoints(template_id, api_key):
    """Update all endpoints to use new template"""
    url = "https://api.runpod.io/graphql"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Get endpoints
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
    
    result = requests.post(url, json={"query": query}, headers=headers)
    if result.status_code != 200:
        print(f"❌ Failed to fetch endpoints: {result.text}")
        return
    
    data = result.json()
    endpoints = data.get('data', {}).get('myself', {}).get('endpoints', [])
    
    print(f"\n🔄 Updating {len(endpoints)} endpoints...")
    
    updated = 0
    for endpoint in endpoints:
        endpoint_id = endpoint['id']
        endpoint_name = endpoint['name']
        
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
        
        update_result = requests.post(
            url,
            json={"query": update_mutation, "variables": variables},
            headers=headers
        )
        
        if update_result.status_code == 200:
            print(f"  ✅ {endpoint_name}")
            updated += 1
        else:
            print(f"  ❌ {endpoint_name}: {update_result.text}")
    
    print(f"\n✅ Updated {updated}/{len(endpoints)} endpoints")

def main():
    print("🚀 Automated ComfyUI Deployment\n")
    
    # Get credentials
    api_key = get_runpod_key()
    if not api_key:
        print("❌ Could not get RunPod API key from Supabase/MCP")
        return
    
    github_owner = get_github_owner()
    image_name = f"ghcr.io/{github_owner}/uncensored-comfyui-worker:latest"
    
    print(f"📦 Image: {image_name}")
    print(f"🔑 API Key: {'*' * 20}...{api_key[-4:]}\n")
    
    # Check if image exists (assume yes for now)
    if not check_image_exists(image_name):
        print("\n⚠️  Image not found. Make sure GitHub Actions has built it first.")
        print("   Push code to GitHub and wait for Actions to complete.")
        return
    
    # Create/update template
    template_id = create_or_update_template(image_name, api_key)
    if not template_id:
        print("\n❌ Failed to create/update template")
        return
    
    # Update endpoints
    update_endpoints(template_id, api_key)
    
    print("\n✅ Deployment complete!")
    print(f"   All endpoints now use ComfyUI worker")

if __name__ == "__main__":
    main()
