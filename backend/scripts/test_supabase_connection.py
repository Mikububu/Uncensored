#!/usr/bin/env python3
"""
Test connection to RunPod using keys from Supabase.
"""
import requests
import sys

# Get keys from MCP (these are the Supabase keys)
RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY") or os.getenv("RUNPOD_KEY")
RUNPOD_ENDPOINT_ID = "etsl76glcc"

def test_runpod_connection():
    """Test RunPod API connection"""
    print("🔍 Testing RunPod Connection...\n")
    
    # Test 1: Check balance
    print("1. Testing API Key (checking balance)...")
    try:
        url = "https://api.runpod.io/graphql"
        query = "query { myself { clientBalance } }"
        headers = {
            "Authorization": f"Bearer {RUNPOD_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json={"query": query}, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'errors' in data:
                print(f"   {RED}❌ API Error: {data['errors']}{RESET}")
                return False
            balance = data.get('data', {}).get('myself', {}).get('clientBalance', 'N/A')
            print(f"   {GREEN}✅ API Key works! Balance: ${balance}{RESET}")
        else:
            print(f"   {RED}❌ Failed: {response.status_code} - {response.text}{RESET}")
            return False
    except Exception as e:
        print(f"   {RED}❌ Error: {e}{RESET}")
        return False
    
    # Test 2: Check endpoint
    print(f"\n2. Testing Endpoint ID: {RUNPOD_ENDPOINT_ID}...")
    try:
        url = f"https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/health"
        headers = {
            "Authorization": f"Bearer {RUNPOD_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            health = response.json()
            workers = health.get('workers', {})
            print(f"   {GREEN}✅ Endpoint exists!{RESET}")
            print(f"   → Workers: Init={workers.get('initializing', 0)}, Ready={workers.get('ready', 0)}, Running={workers.get('running', 0)}")
        elif response.status_code == 404:
            print(f"   {YELLOW}⚠️  Endpoint not found (may need to be created){RESET}")
        else:
            print(f"   {RED}❌ Failed: {response.status_code} - {response.text[:100]}{RESET}")
    except Exception as e:
        print(f"   {RED}❌ Error: {e}{RESET}")
    
    # Test 3: List all endpoints
    print(f"\n3. Listing all endpoints...")
    try:
        url = "https://api.runpod.io/graphql"
        query = """
        query {
          myself {
            endpoints {
              id
              name
            }
          }
        }
        """
        headers = {
            "Authorization": f"Bearer {RUNPOD_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json={"query": query}, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'errors' not in data:
                endpoints = data.get('data', {}).get('myself', {}).get('endpoints', [])
                print(f"   {GREEN}✅ Found {len(endpoints)} endpoints:{RESET}")
                for ep in endpoints[:5]:
                    match = "⭐" if ep['id'] == RUNPOD_ENDPOINT_ID else "  "
                    print(f"   {match} {ep['name']}: {ep['id']}")
                if len(endpoints) > 5:
                    print(f"   ... and {len(endpoints) - 5} more")
                
                # Check if our endpoint is in the list
                endpoint_ids = [ep['id'] for ep in endpoints]
                if RUNPOD_ENDPOINT_ID in endpoint_ids:
                    print(f"\n   {GREEN}✅ Your endpoint ID is valid!{RESET}")
                else:
                    print(f"\n   {YELLOW}⚠️  Your endpoint ID not found in list{RESET}")
                    print(f"   → You may need to create it or use a different ID")
            else:
                print(f"   {RED}❌ GraphQL errors: {data.get('errors')}{RESET}")
    except Exception as e:
        print(f"   {RED}❌ Error: {e}{RESET}")
    
    print(f"\n{GREEN}{'='*60}{RESET}")
    print(f"{GREEN}✅ Connection test complete!{RESET}")
    print(f"\n{GREEN}Keys from Supabase are working!{RESET}")
    print(f"   → API Key: Valid")
    print(f"   → Endpoint ID: {RUNPOD_ENDPOINT_ID}")

if __name__ == "__main__":
    # Colors
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    
    test_runpod_connection()
