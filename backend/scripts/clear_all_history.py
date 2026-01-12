#!/usr/bin/env python3
"""
Script to clear all history (jobs) from PocketBase database.
"""
import os
import requests
import sys
from dotenv import load_dotenv

# Load environment
load_dotenv()

PB_URL = os.getenv("PB_URL", "https://uncensored-engine-db.fly.dev")
ADMIN_EMAIL = os.getenv("PB_ADMIN_EMAIL", "admin@example.com")
ADMIN_PASS = os.getenv("PB_ADMIN_PASS") or os.getenv("PB_ADMIN_PASSWORD", "password123456")

def clear_all_history():
    """Delete all jobs from PocketBase"""
    print("🗑️  Clearing all history from PocketBase...\n")
    
    try:
        # Authenticate
        print("1. Authenticating...")
        auth_url = f"{PB_URL}/api/admins/auth-with-password"
        response = requests.post(auth_url, json={
            "identity": ADMIN_EMAIL,
            "password": ADMIN_PASS
        })
        response.raise_for_status()
        token = response.json().get('token')
        print("   ✅ Authenticated")
        
        headers = {"Authorization": token}
        
        # Get all jobs
        print("\n2. Fetching all jobs...")
        jobs_url = f"{PB_URL}/api/collections/jobs/records"
        
        all_jobs = []
        page = 1
        per_page = 500
        
        while True:
            params = {"page": page, "perPage": per_page, "sort": "-created"}
            r = requests.get(jobs_url, headers=headers, params=params)
            r.raise_for_status()
            data = r.json()
            jobs = data.get('items', [])
            
            if not jobs:
                break
            
            all_jobs.extend(jobs)
            print(f"   → Fetched page {page}: {len(jobs)} jobs")
            
            # Check if there are more pages
            total_pages = data.get('totalPages', 1)
            if page >= total_pages:
                break
            page += 1
        
        total = len(all_jobs)
        print(f"\n   ✅ Found {total} jobs total")
        
        if total == 0:
            print("\n✅ No jobs to delete. History is already empty!")
            return
        
        # Confirm deletion
        print(f"\n⚠️  About to delete {total} jobs")
        confirm = input("   Type 'DELETE' to confirm: ")
        
        if confirm != "DELETE":
            print("   ❌ Cancelled")
            return
        
        # Delete all jobs
        print(f"\n3. Deleting {total} jobs...")
        deleted = 0
        errors = 0
        
        for i, job in enumerate(all_jobs, 1):
            try:
                job_id = job['id']
                delete_url = f"{jobs_url}/{job_id}"
                r = requests.delete(delete_url, headers=headers)
                
                if r.status_code in [200, 204]:
                    deleted += 1
                    if i % 50 == 0:
                        print(f"   → Deleted {i}/{total}...")
                else:
                    errors += 1
                    print(f"   ⚠️  Failed to delete {job_id}: {r.status_code}")
            except Exception as e:
                errors += 1
                print(f"   ⚠️  Error deleting job: {e}")
        
        print(f"\n✅ Deletion complete!")
        print(f"   → Deleted: {deleted}")
        print(f"   → Errors: {errors}")
        print(f"   → Remaining: {total - deleted - errors}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    clear_all_history()
