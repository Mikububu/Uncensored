#!/bin/bash
# ComfyUI RunPod Worker Setup Utility (2025 XL)
# This script helps create specialized serverless endpoints for Pony V6 and Flux.

API_KEY=$(cat ../.env | grep RUNPOD_API_KEY | cut -d '=' -f2)
[ -z "$API_KEY" ] && echo "ERROR: RUNPOD_API_KEY not found in ../.env" && exit 1

# Default Template for ComfyUI (Change to your preferred one)
# Standard RunPod ComfyUI Worker template: "runpod/worker-comfy:latest"
COMFY_TEMPLATE_ID="7512t5qg4h" # Replace with your specific Comfy template if different

create_endpoint() {
    NAME=$1
    TEMPLATE=$2
    GPU=$3
    MIN=$4
    MAX=$5
    
    echo "🚀 Creating Endpoint: $NAME ($GPU)..."
    
    # GraphQL Mutation for Create Endpoint (Conceptual - use RunPod SDK or CLI if installed)
    # For now, we use a python helper to do the heavy lifting
    python3 <<EOF
import os
import requests

API_KEY = "$API_KEY"
NAME = "$NAME"
TEMPLATE_ID = "$TEMPLATE"
GPU_IDS = "$GPU"

url = "https://api.runpod.io/graphql"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

query = """
mutation createEndpoint(\$input: EndpointInput!) {
  saveEndpoint(input: \$input) {
    id
    name
  }
}
"""

payload = {
    "query": query,
    "variables": {
        "input": {
            "name": NAME,
            "templateId": TEMPLATE_ID,
            "gpuIds": GPU_IDS,
            "idleTimeout": 300,
            "scalerType": "QUEUE_DELAY",
            "scalerValue": 30,
            "workersMin": $MIN,
            "workersMax": $MAX
        }
    }
}

r = requests.post(url, json=payload, headers=headers)
print(r.json())
EOF
}

echo "--- Uncensored Infrastructure Scaling ---"
echo "1) Create Pony Diffusion V6 XL Endpoint (AMPERE_24)"
echo "2) Create Flux.1 Uncensored Endpoint (ADA_24)"
echo "3) List My Endpoints"
read -p "Selection: " CHOICE

case \$CHOICE in
    1) create_endpoint "z-pony-v6-uncensored" "$COMFY_TEMPLATE_ID" "AMPERE_24" 1 3 ;;
    2) create_endpoint "z-flux-uncensored" "$COMFY_TEMPLATE_ID" "ADA_24" 1 2 ;;
    3) python3 get_runpod_details.py ;;
    *) echo "Invalid choice." ;;
esac
