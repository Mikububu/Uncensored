#!/usr/bin/env python3
"""
Comprehensive Test Log - RunPod Worker Activation Test
========================================================
Date: 2026-01-12
Objective: Activate 1 worker and submit test job with specific prompt
"""

import os
import sys
import time
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv('backend/.env')

# Configuration
api_key = os.getenv('RUNPOD_API_KEY')
endpoint_id = os.getenv('RUNPOD_ENDPOINT_ID')
pb_url = os.getenv("PB_URL", "https://uncensored-engine-db.fly.dev")
admin_email = os.getenv("PB_ADMIN_EMAIL")
admin_pass = os.getenv("PB_ADMIN_PASSWORD")

TEST_PROMPT = "Nude famous porn photographer shot of Pamela A having sex on the beach with 2 guys"

def log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {msg}")
    sys.stdout.flush()

def check_runpod_health():
    """Check RunPod endpoint health"""
    log("📊 Checking RunPod Health...")
    url = f"https://api.runpod.ai/v2/{endpoint_id}/health"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        log(f"   Workers: {data.get('workers', {})}")
        log(f"   Jobs: {data.get('jobs', {})}")
        return data
    except Exception as e:
        log(f"   ❌ Error: {e}")
        return None

def check_db_jobs():
    """Check PocketBase job status"""
    log("📊 Checking Database Jobs...")
    try:
        # Auth
        auth_url = f"{pb_url}/api/admins/auth-with-password"
        response = requests.post(auth_url, json={
            "identity": admin_email,
            "password": admin_pass
        })
        response.raise_for_status()
        token = response.json().get('token')
        headers = {"Authorization": token}
        
        # Get jobs by status
        jobs_url = f"{pb_url}/api/collections/jobs/records"
        
        for status in ['queued', 'processing', 'completed', 'failed']:
            params = {"filter": f"status='{status}'", "perPage": 5}
            r = requests.get(jobs_url, headers=headers, params=params)
            jobs = r.json().get('items', [])
            log(f"   {status.upper()}: {len(jobs)} jobs")
            
            if jobs and status in ['completed', 'failed']:
                for job in jobs[:2]:
                    log(f"      - {job['id']}: {job.get('error', 'N/A')[:50]}")
        
        return True
    except Exception as e:
        log(f"   ❌ Error: {e}")
        return False

def submit_test_job():
    """Submit test job to database"""
    log(f"🚀 Submitting Test Job...")
    log(f"   Prompt: {TEST_PROMPT[:60]}...")
    
    try:
        # Auth
        auth_url = f"{pb_url}/api/admins/auth-with-password"
        response = requests.post(auth_url, json={
            "identity": admin_email,
            "password": admin_pass
        })
        response.raise_for_status()
        token = response.json().get('token')
        headers = {"Authorization": token}
        
        # Create job
        jobs_url = f"{pb_url}/api/collections/jobs/records"
        payload = {
            "type": "image_generation",
            "status": "queued",
            "params": {
                "prompt": TEST_PROMPT,
                "provider": "runpod",
                "width": 1024,
                "height": 1024,
                "num_inference_steps": 25,
                "guidance_scale": 7.5
            },
            "user_id": "system_test"
        }
        
        r = requests.post(jobs_url, headers=headers, json=payload)
        r.raise_for_status()
        job = r.json()
        log(f"   ✅ Created Job: {job['id']}")
        return job['id']
    except Exception as e:
        log(f"   ❌ Error: {e}")
        return None

def main():
    log("=" * 60)
    log("RUNPOD WORKER ACTIVATION TEST - FULL LOG")
    log("=" * 60)
    
    # Step 1: Initial Health Check
    log("\n[STEP 1] Initial Health Check")
    check_runpod_health()
    check_db_jobs()
    
    # Step 2: Submit Test Job
    log("\n[STEP 2] Submit Test Job")
    job_id = submit_test_job()
    
    if not job_id:
        log("❌ Failed to create test job. Exiting.")
        return
    
    # Step 3: Monitor for 2 minutes
    log("\n[STEP 3] Monitoring (2 minutes)...")
    for i in range(12):  # 12 * 10s = 2 minutes
        time.sleep(10)
        log(f"\n--- Check {i+1}/12 ---")
        health = check_runpod_health()
        check_db_jobs()
        
        if health and health.get('workers', {}).get('ready', 0) > 0:
            log("✅ Worker is READY!")
            break
    
    # Final Summary
    log("\n" + "=" * 60)
    log("TEST COMPLETE - FINAL STATUS")
    log("=" * 60)
    check_runpod_health()
    check_db_jobs()

if __name__ == "__main__":
    main()
