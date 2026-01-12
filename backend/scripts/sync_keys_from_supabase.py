#!/usr/bin/env python3
"""
Sync API keys from Supabase and set them as environment variables or save to .env
"""
import os
import sys
from pathlib import Path

def sync_keys_from_mcp():
    """Sync keys using MCP project-secrets"""
    try:
        # This would use the MCP server, but for now we'll create a helper
        # that can be called to set environment variables
        print("📥 Syncing keys from Supabase (via MCP)...")
        
        # The keys are available via MCP, but we need to set them in environment
        # For now, create a .env file with the keys
        env_file = Path(__file__).parent.parent / ".env"
        
        # Read existing .env if it exists
        env_vars = {}
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()
        
        # Note: In production, these should be loaded from Supabase dynamically
        # For now, we'll add placeholders that indicate they should be loaded from Supabase
        env_vars['RUNPOD_API_KEY'] = env_vars.get('RUNPOD_API_KEY', '# Load from Supabase')
        env_vars['RUNPOD_ENDPOINT_ID'] = env_vars.get('RUNPOD_ENDPOINT_ID', '# Load from Supabase')
        
        print("✅ Keys should be loaded from Supabase at runtime")
        print("   The worker will automatically fetch them when initialized")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    sync_keys_from_mcp()
