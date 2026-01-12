#!/usr/bin/env python3
"""
Script to load API keys from Supabase and set them as environment variables.
This can be used to sync keys before running other scripts.
"""
import os
import sys

# Try to import supabase client
try:
    from supabase import create_client, Client
except ImportError:
    print("Installing supabase client...")
    os.system("pip install supabase")
    from supabase import create_client, Client

def load_keys_from_supabase():
    """Load API keys from Supabase api_keys table"""
    
    # Supabase connection (you may need to set these as env vars)
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_ANON_KEY")
    
    if not supabase_url or not supabase_key:
        print("❌ SUPABASE_URL and SUPABASE_SERVICE_KEY not set")
        print("   Set these environment variables to connect to Supabase")
        return None
    
    try:
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # Fetch keys from api_keys table
        response = supabase.table("api_keys").select("*").execute()
        
        keys = {}
        for row in response.data:
            service = row.get('service')
            key = row.get('key')
            if service and key:
                keys[service] = key
        
        print(f"✅ Loaded {len(keys)} keys from Supabase:")
        for service in keys.keys():
            print(f"   → {service}")
        
        return keys
        
    except Exception as e:
        print(f"❌ Error loading from Supabase: {e}")
        return None

if __name__ == "__main__":
    keys = load_keys_from_supabase()
    if keys:
        # Print keys (for debugging - be careful!)
        for service, key in keys.items():
            print(f"\n{service.upper()}={key[:10]}...")
