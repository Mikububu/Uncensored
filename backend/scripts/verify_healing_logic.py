import sys
import os
import json
import shutil

# Add backend to sys path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from self_healing_agent import SelfHealingAgent, CONFIG_PATH

def test_healer():
    print("🏥 STARTING HEALER LOGIC VERIFICATION 🏥")
    
    # Setup: Clean existing config
    if os.path.exists(CONFIG_PATH):
        shutil.move(CONFIG_PATH, CONFIG_PATH + ".bak")
    
    agent = SelfHealingAgent()
    
    # Test 1: Simulate OOM
    print("\n[TEST 1] Simulating CUDA OOM on 'sdxl-turbo'...")
    agent.report_failure('sdxl-turbo', 'RuntimeError: CUDA out of memory. Tried to allocate 20GB...')
    
    # Check Result
    config = agent.load_config()
    sdxl_cfg = config.get('sdxl-turbo', {})
    if sdxl_cfg.get('width') == 768:
        print("✅ PASS: Healer downgraded resolution to 768px.")
    else:
        print(f"❌ FAIL: Config not updated correctly: {sdxl_cfg}")
        
    # Test 2: Simulate Repeated OOM (Should downgrade further)
    print("\n[TEST 2] Simulating SECOND OOM (Persistent Failure)...")
    agent.report_failure('sdxl-turbo', 'RuntimeError: CUDA out of memory again...')
    
    config = agent.load_config()
    sdxl_cfg = config.get('sdxl-turbo', {})
    if sdxl_cfg.get('width') == 512:
        print("✅ PASS: Healer downgraded resolution to 512px (Safe Mode).")
    else:
        print(f"❌ FAIL: Config not updated correctly: {sdxl_cfg}")

    # Test 3: Simulate Timeout on Pony
    print("\n[TEST 3] Simulating Timeout on 'pony-v6'...")
    agent.report_failure('pony-v6', 'TimeoutError: Job timed out.')
    
    config = agent.load_config()
    pony_cfg = config.get('pony-v6', {})
    if pony_cfg.get('max_steps') == 20:
        print("✅ PASS: Healer capped steps to 20.")
    else:
        print(f"❌ FAIL: Config not updated correctly: {pony_cfg}")

    # Cleanup
    if os.path.exists(CONFIG_PATH + ".bak"):
        shutil.move(CONFIG_PATH + ".bak", CONFIG_PATH)
    else:
        os.remove(CONFIG_PATH)
    
    print("\n🏥 HEALER VERIFICATION COMPLETED.")

if __name__ == "__main__":
    test_healer()
