#!/usr/bin/env python3
"""
Script to verify workers and endpoints are correctly configured.
"""
import os
import json
import sys
import requests
from pathlib import Path

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def check_mark(ok):
    return f"{GREEN}✅{RESET}" if ok else f"{RED}❌{RESET}"

def print_section(title):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{title}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def check_model_config():
    """Check if models.json exists and is valid"""
    print_section("1. MODEL CONFIGURATION")
    
    config_path = Path(__file__).parent.parent.parent / "config" / "models.json"
    if not config_path.exists():
        print(f"{RED}❌ models.json not found at {config_path}{RESET}")
        return False, None
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        models = config.get('models', [])
        print(f"{GREEN}✅ models.json found{RESET}")
        print(f"   → {len(models)} models configured")
        return True, models
    except Exception as e:
        print(f"{RED}❌ Error reading models.json: {e}{RESET}")
        return False, None

def check_endpoints_file():
    """Check if endpoints.json exists"""
    print_section("2. ENDPOINT MAPPING FILE")
    
    endpoints_path = Path(__file__).parent.parent / "endpoints.json"
    if not endpoints_path.exists():
        print(f"{YELLOW}⚠️  endpoints.json not found{RESET}")
        print(f"   → Run 'setup_all_models.py' to create endpoints")
        print(f"   → Or using default endpoint from RUNPOD_ENDPOINT_ID")
        return False, None
    
    try:
        with open(endpoints_path, 'r') as f:
            endpoints = json.load(f)
        print(f"{GREEN}✅ endpoints.json found{RESET}")
        print(f"   → {len(endpoints)} endpoints configured")
        for model_id, info in list(endpoints.items())[:3]:
            print(f"   → {model_id}: {info.get('endpoint_id', 'N/A')}")
        if len(endpoints) > 3:
            print(f"   → ... and {len(endpoints) - 3} more")
        return True, endpoints
    except Exception as e:
        print(f"{RED}❌ Error reading endpoints.json: {e}{RESET}")
        return False, None

def check_environment():
    """Check environment variables"""
    print_section("3. ENVIRONMENT VARIABLES")
    
    runpod_key = os.getenv("RUNPOD_API_KEY")
    endpoint_id = os.getenv("RUNPOD_ENDPOINT_ID")
    
    key_ok = bool(runpod_key)
    endpoint_ok = bool(endpoint_id)
    
    print(f"{check_mark(key_ok)} RUNPOD_API_KEY: {'Set' if key_ok else 'Not set'}")
    print(f"{check_mark(endpoint_ok)} RUNPOD_ENDPOINT_ID: {endpoint_id or 'Not set'}")
    
    return key_ok, endpoint_ok, endpoint_id

def check_runpod_endpoints(runpod_key, endpoints):
    """Check if RunPod endpoints actually exist"""
    print_section("4. RUNPOD ENDPOINT VERIFICATION")
    
    if not runpod_key:
        print(f"{YELLOW}⚠️  Skipping - RUNPOD_API_KEY not set{RESET}")
        return
    
    if not endpoints:
        print(f"{YELLOW}⚠️  Skipping - No endpoints to check{RESET}")
        return
    
    headers = {
        "Authorization": f"Bearer {runpod_key}",
        "Content-Type": "application/json"
    }
    
    # Query to get all endpoints
    query = """
    query {
      myself {
        endpoints {
          id
          name
          template {
            id
            name
          }
        }
      }
    }
    """
    
    try:
        response = requests.post(
            "https://api.runpod.io/graphql",
            json={"query": query},
            headers=headers,
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"{RED}❌ Failed to query RunPod API: {response.status_code}{RESET}")
            return
        
        data = response.json()
        if 'errors' in data:
            print(f"{RED}❌ GraphQL errors: {data['errors']}{RESET}")
            return
        
        runpod_endpoints = data.get('data', {}).get('myself', {}).get('endpoints', [])
        runpod_endpoint_ids = {ep['id']: ep for ep in runpod_endpoints}
        
        print(f"{GREEN}✅ Found {len(runpod_endpoints)} endpoints in RunPod{RESET}\n")
        
        # Check each configured endpoint
        for model_id, info in endpoints.items():
            endpoint_id = info.get('endpoint_id')
            if endpoint_id in runpod_endpoint_ids:
                ep_info = runpod_endpoint_ids[endpoint_id]
                print(f"{GREEN}✅{RESET} {model_id}: {endpoint_id}")
                print(f"      Name: {ep_info.get('name', 'N/A')}")
            else:
                print(f"{RED}❌{RESET} {model_id}: {endpoint_id} (NOT FOUND in RunPod)")
        
    except Exception as e:
        print(f"{RED}❌ Error checking RunPod endpoints: {e}{RESET}")

def check_worker_handler():
    """Check if worker handler files exist"""
    print_section("5. WORKER HANDLER FILES")
    
    worker_dir = Path(__file__).parent.parent / "worker"
    handler_multi = worker_dir / "handler_multi.py"
    handler_original = worker_dir / "handler.py"
    
    multi_exists = handler_multi.exists()
    original_exists = handler_original.exists()
    
    print(f"{check_mark(multi_exists)} handler_multi.py: {'Exists' if multi_exists else 'Missing'}")
    print(f"{check_mark(original_exists)} handler.py: {'Exists' if original_exists else 'Missing'}")
    
    if multi_exists:
        print(f"   → Multi-model handler available")
    if original_exists:
        print(f"   → Original handler available")
    
    return multi_exists or original_exists

def check_backend_worker():
    """Check backend worker configuration"""
    print_section("6. BACKEND WORKER CONFIGURATION")
    
    worker_file = Path(__file__).parent.parent / "z_image_worker.py"
    if not worker_file.exists():
        print(f"{RED}❌ z_image_worker.py not found{RESET}")
        return False
    
    print(f"{GREEN}✅ z_image_worker.py exists{RESET}")
    
    # Check if it has the model loading logic
    with open(worker_file, 'r') as f:
        content = f.read()
        has_model_config = '_load_model_config' in content
        has_endpoint_mapping = '_load_endpoint_mapping' in content
        has_get_endpoint = 'get_endpoint_for_model' in content
    
    print(f"{check_mark(has_model_config)} Model config loading")
    print(f"{check_mark(has_endpoint_mapping)} Endpoint mapping loading")
    print(f"{check_mark(has_get_endpoint)} Endpoint selection logic")
    
    return True

def main():
    print(f"\n{BLUE}🔍 VERIFYING WORKERS AND ENDPOINTS{RESET}\n")
    
    # 1. Check model config
    config_ok, models = check_model_config()
    
    # 2. Check endpoints file
    endpoints_ok, endpoints = check_endpoints_file()
    
    # 3. Check environment
    key_ok, endpoint_ok, default_endpoint = check_environment()
    
    # 4. Check RunPod endpoints (if we have API key and endpoints)
    if key_ok and endpoints:
        check_runpod_endpoints(os.getenv("RUNPOD_API_KEY"), endpoints)
    
    # 5. Check worker handlers
    handlers_ok = check_worker_handler()
    
    # 6. Check backend worker
    backend_ok = check_backend_worker()
    
    # Summary
    print_section("SUMMARY")
    
    all_ok = config_ok and (endpoints_ok or endpoint_ok) and key_ok and handlers_ok and backend_ok
    
    if all_ok:
        print(f"{GREEN}✅ All checks passed!{RESET}")
        print(f"\n{BLUE}Next steps:{RESET}")
        if not endpoints_ok:
            print(f"  1. Run: python scripts/setup_all_models.py")
        print(f"  2. Deploy worker handler to RunPod")
        print(f"  3. Test with: python scripts/test_model_uncensored.py")
    else:
        print(f"{YELLOW}⚠️  Some issues found:{RESET}")
        if not config_ok:
            print(f"  - Fix models.json configuration")
        if not endpoints_ok and not endpoint_ok:
            print(f"  - Set RUNPOD_ENDPOINT_ID or run setup_all_models.py")
        if not key_ok:
            print(f"  - Set RUNPOD_API_KEY environment variable")
        if not handlers_ok:
            print(f"  - Check worker handler files")
        if not backend_ok:
            print(f"  - Check backend worker configuration")
    
    print()

if __name__ == "__main__":
    main()
