#!/usr/bin/env python3
"""
Test website functionality internally - test each model with explicit prompts
and identify what works and what doesn't. Reports in human-readable format.
"""
import os
import sys
import asyncio
import json
import requests
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from z_image_worker import ZImageWorker

# Explicit test prompts
TEST_PROMPTS = [
    "nude woman, explicit, detailed anatomy",
    "explicit sexual content, detailed, high quality"
]

RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY") or os.getenv("RUNPOD_KEY")

async def test_model_functionality(model_id, endpoint_id, model_name):
    """Test if a model actually works"""
    print(f"\n🧪 Testing: {model_name}")
    print(f"   Model ID: {model_id}")
    print(f"   Endpoint: {endpoint_id}")
    
    worker = ZImageWorker()
    worker.runpod_api_key = RUNPOD_API_KEY
    
    results = {
        'model_id': model_id,
        'model_name': model_name,
        'endpoint_id': endpoint_id,
        'works': False,
        'blocks_explicit': False,
        'has_errors': False,
        'error_message': '',
        'human_readable_status': ''
    }
    
    # Test with explicit prompt
    test_prompt = TEST_PROMPTS[0]
    print(f"   Testing with: {test_prompt[:50]}...")
    
    task = {
        'id': f'test-{model_id}',
        'type': 'image_generation',
        'input': {
            'prompt': test_prompt,
            'model_id': model_id,
            'endpoint_id': endpoint_id,
            'num_inference_steps': 15,
            'guidance_scale': 7.5,
            'width': 512,
            'height': 512
        }
    }
    
    try:
        result = await worker.generate_with_runpod(task, task['input'], endpoint_id)
        
        if result.get('success'):
            results['works'] = True
            results['human_readable_status'] = f"✅ {model_name} WORKS - Successfully generated image with explicit prompt. This model allows explicit content."
            print(f"   ✅ SUCCESS - Model works!")
        else:
            error = result.get('error', 'Unknown error')
            error_lower = error.lower()
            
            # Check for censorship
            if any(k in error_lower for k in ['safety', 'nsfw', 'blocked', 'censored', 'filter', 'content policy']):
                results['blocks_explicit'] = True
                results['human_readable_status'] = f"🚫 {model_name} BLOCKS EXPLICIT CONTENT - The model censored the test prompt. Not suitable for uncensored content."
                print(f"   🚫 BLOCKED - Model censors explicit content")
            else:
                results['has_errors'] = True
                results['error_message'] = error[:100]
                results['human_readable_status'] = f"❌ {model_name} HAS ISSUES - Error: {error[:80]}. May need endpoint configuration or model deployment."
                print(f"   ❌ ERROR - {error[:60]}")
                
    except Exception as e:
        results['has_errors'] = True
        results['error_message'] = str(e)[:100]
        results['human_readable_status'] = f"❌ {model_name} BROKEN - Exception: {str(e)[:80]}. Check endpoint or model configuration."
        print(f"   ❌ EXCEPTION - {str(e)[:60]}")
    
    return results

async def main():
    """Test all models and generate human-readable report"""
    print("🚀 WEBSITE FUNCTIONALITY TEST")
    print("Testing all models with explicit language to see what works...\n")
    
    # Load endpoints
    endpoints_path = Path(__file__).parent.parent / "endpoints.json"
    if not endpoints_path.exists():
        print("❌ endpoints.json not found")
        sys.exit(1)
    
    with open(endpoints_path, 'r') as f:
        endpoints = json.load(f)
    
    # Load model names
    config_path = Path(__file__).parent.parent.parent / "config" / "models.json"
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    model_names = {m['id']: m['name'] for m in config.get('models', [])}
    
    # Test each model
    all_results = []
    for model_id, info in endpoints.items():
        result = await test_model_functionality(
            model_id, 
            info['endpoint_id'], 
            model_names.get(model_id, model_id)
        )
        all_results.append(result)
    
    # Also test models without endpoints (use default)
    default_endpoint = "4znje87s0eaktv"
    for model in config.get('models', []):
        if model['id'] not in endpoints:
            result = await test_model_functionality(
                model['id'],
                default_endpoint,
                model['name']
            )
            all_results.append(result)
    
    # Save results
    output = {
        'tested_at': datetime.utcnow().isoformat(),
        'results': all_results
    }
    
    results_path = Path(__file__).parent.parent / "model_test_results.json"
    with open(results_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    # Print human-readable summary
    print(f"\n{'='*70}")
    print("📊 TEST RESULTS SUMMARY")
    print(f"{'='*70}\n")
    
    working = [r for r in all_results if r['works']]
    blocked = [r for r in all_results if r['blocks_explicit']]
    broken = [r for r in all_results if r['has_errors'] and not r['blocks_explicit']]
    
    print(f"✅ WORKING MODELS ({len(working)}):")
    for r in working:
        print(f"   • {r['human_readable_status']}")
    
    if blocked:
        print(f"\n🚫 CENSORED MODELS ({len(blocked)}):")
        for r in blocked:
            print(f"   • {r['human_readable_status']}")
    
    if broken:
        print(f"\n❌ BROKEN MODELS ({len(broken)}):")
        for r in broken:
            print(f"   • {r['human_readable_status']}")
            if r['error_message']:
                print(f"     Error: {r['error_message']}")
    
    print(f"\n📄 Results saved to: {results_path}")
    print(f"💡 These results will appear on the website!")

if __name__ == "__main__":
    asyncio.run(main())
