#!/usr/bin/env python3
"""Test RunPod endpoints to find working ones"""

import os
import requests
import json

RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY", "")

ENDPOINTS = {
    "4e7784vway3niq": "ComfyUI Multi-Model",
    "4znje87s0eaktv": "Flux Dev Uncensored",
    "fehw5gl26qnnu4": "AbyssOrangeMix V3",
    "obmmh7nyfl7i4m": "Realistic Vision V5",
}

print("Testing RunPod endpoints...\n")
print(f"API Key: {RUNPOD_API_KEY[:10]}...{RUNPOD_API_KEY[-4:] if RUNPOD_API_KEY else 'NOT SET'}")
print()

for eid, name in ENDPOINTS.items():
    print(f"Testing {name} ({eid})...")
    try:
        # Test health endpoint
        url = f"https://api.runpod.ai/v2/{eid}/health"
        headers = {"Authorization": f"Bearer {RUNPOD_API_KEY}"}
        
        r = requests.get(url, headers=headers, timeout=5)
        
        if r.status_code == 200:
            data = r.json()
            workers = data.get('workers', {})
            status = "✅ HEALTHY" if workers.get('ready', 0) > 0 else "⚠️ NO WORKERS"
            print(f"   {status}")
            print(f"   Workers: Init={workers.get('initializing', 0)}, Ready={workers.get('ready', 0)}, Running={workers.get('running', 0)}")
        elif r.status_code == 404:
            print(f"   ❌ 404 NOT FOUND - Endpoint may have been deleted")
        elif r.status_code == 401:
            print(f"   ❌ 401 UNAUTHORIZED - Check API key")
        else:
            print(f"   ❌ Status {r.status_code}: {r.text[:100]}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()
