#!/usr/bin/env python3
"""
Quick verification script to check if the uncensored models setup is complete.
"""
import os
import json
import sys
from pathlib import Path

def check_file(path, description):
    """Check if a file exists"""
    if path.exists():
        print(f"✅ {description}: {path}")
        return True
    else:
        print(f"❌ {description}: {path} (NOT FOUND)")
        return False

def check_env_var(name, description):
    """Check if environment variable is set"""
    value = os.getenv(name)
    if value:
        print(f"✅ {description}: Set")
        return True
    else:
        print(f"❌ {description}: Not set")
        return False

def main():
    print("🔍 Verifying Uncensored Models Setup\n")
    print("=" * 60)
    
    base_path = Path(__file__).parent.parent.parent
    all_good = True
    
    # Check configuration files
    print("\n📁 Configuration Files:")
    config_path = base_path / "config" / "models.json"
    if check_file(config_path, "Model configuration"):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                models = config.get('models', [])
                print(f"   → {len(models)} models configured")
        except Exception as e:
            print(f"   ⚠️  Error reading config: {e}")
            all_good = False
    else:
        all_good = False
    
    # Check endpoints file
    endpoints_path = Path(__file__).parent.parent / "endpoints.json"
    print(f"\n📡 RunPod Endpoints:")
    if check_file(endpoints_path, "Endpoint mapping"):
        try:
            with open(endpoints_path, 'r') as f:
                endpoints = json.load(f)
                print(f"   → {len(endpoints)} endpoints configured")
                for model_id, info in list(endpoints.items())[:3]:
                    print(f"   → {model_id}: {info.get('endpoint_id', 'N/A')}")
        except Exception as e:
            print(f"   ⚠️  Error reading endpoints: {e}")
    else:
        print("   ⚠️  Run 'setup_all_models.py' to create endpoints")
    
    # Check environment variables
    print(f"\n🔑 Environment Variables:")
    runpod_key = check_env_var("RUNPOD_API_KEY", "RUNPOD_API_KEY")
    if not runpod_key:
        all_good = False
    
    endpoint_id = check_env_var("RUNPOD_ENDPOINT_ID", "RUNPOD_ENDPOINT_ID (optional)")
    
    # Check worker files
    print(f"\n🤖 Worker Files:")
    worker_path = Path(__file__).parent.parent / "worker" / "handler_multi.py"
    check_file(worker_path, "Multi-model worker handler")
    
    # Check scripts
    print(f"\n📜 Setup Scripts:")
    setup_script = Path(__file__).parent / "setup_all_models.py"
    test_script = Path(__file__).parent / "test_model_uncensored.py"
    check_file(setup_script, "Setup script")
    check_file(test_script, "Test script")
    
    # Summary
    print("\n" + "=" * 60)
    if all_good:
        print("✅ Setup looks good! You can proceed with:")
        print("   1. Run 'setup_all_models.py' to create endpoints")
        print("   2. Run 'test_model_uncensored.py' to test models")
        print("   3. Start the frontend and begin testing")
    else:
        print("⚠️  Some issues found. Please fix them before proceeding.")
        print("   See SETUP_GUIDE.md for help.")
    
    print()

if __name__ == "__main__":
    main()
