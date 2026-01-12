#!/usr/bin/env python3
"""
Sync endpoint IDs from backend/endpoints.json to frontend MODELS object.
This ensures the frontend uses the correct endpoint IDs.
"""
import json
from pathlib import Path

# Load endpoints
endpoints_path = Path(__file__).parent.parent / "endpoints.json"
if not endpoints_path.exists():
    print("❌ endpoints.json not found")
    exit(1)

with open(endpoints_path, 'r') as f:
    endpoints = json.load(f)

# Load model config for names
config_path = Path(__file__).parent.parent.parent / "config" / "models.json"
with open(config_path, 'r') as f:
    config = json.load(f)

model_configs = {m['id']: m for m in config.get('models', [])}

# Generate updated MODELS object
models_js = "        const MODELS = {\n"
for model_id, info in endpoints.items():
    model_config = model_configs.get(model_id, {})
    name = info.get('name') or model_config.get('name', model_id)
    endpoint_id = info.get('endpoint_id')
    uncensored_level = model_config.get('uncensored_level', 'medium')
    
    models_js += f"            '{model_id}': {{ provider: 'runpod', endpoint_id: '{endpoint_id}', name: '{name}', uncensored_level: '{uncensored_level}' }},\n"

# Add models that don't have endpoints yet (use default)
default_endpoint = "4znje87s0eaktv"  # The existing endpoint we found
for model in config.get('models', []):
    if model['id'] not in endpoints:
        models_js += f"            '{model['id']}': {{ provider: 'runpod', endpoint_id: '{default_endpoint}', name: '{model['name']}', uncensored_level: '{model.get('uncensored_level', 'medium')}' }},\n"

models_js += "        };"

print("✅ Updated MODELS object:")
print(models_js)
print("\n📋 Copy this to frontend/index.html to replace the MODELS object")

# Also save to file
output_path = Path(__file__).parent.parent / "frontend_models_update.js"
with open(output_path, 'w') as f:
    f.write(models_js)

print(f"\n📄 Also saved to: {output_path}")
