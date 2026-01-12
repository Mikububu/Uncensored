import requests
import sys
import json
import time

def test_pod_connection(ip, port):
    base_url = f"http://{ip}:{port}"
    print(f"🔬 Testing Connection to {base_url}...")
    
    # 1. Test standard A1111/Forge API
    print("   Checking /sdapi/v1/txt2img...")
    try:
        r = requests.get(f"{base_url}/sdapi/v1/options", timeout=5)
        if r.status_code == 200:
            print("   ✅ A1111 API Detected!")
            return "A1111"
    except Exception as e:
        print(f"      Failed: {e}")

    # 2. Test RunPod Worker API
    print("   Checking /run...")
    try:
        # RunPod worker usually expects POST to /run
        r = requests.post(f"{base_url}/run", json={"input": {"test": True}}, timeout=5)
        # 400 or 200 means it's listening
        if r.status_code in [200, 400, 500]: 
            print("   ✅ RunPod Worker API Detected!")
            return "WORKER"
    except Exception as e:
        print(f"      Failed: {e}")

    # 3. Test Root
    print("   Checking / ...")
    try:
        r = requests.get(base_url, timeout=5)
        print(f"      Root Status: {r.status_code}")
    except Exception as e:
        print(f"      Failed: {e}")

    return None

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 test_new_pod_connection.py <IP> <PORT>")
        sys.exit(1)
        
    ip = sys.argv[1]
    port = sys.argv[2]
    
    test_pod_connection(ip, port)
