#!/bin/bash
# Start ComfyUI Server
# This script starts ComfyUI on the default port (8188)

cd "$(dirname "$0")/../comfyui"

echo "🎨 Starting ComfyUI..."
echo "📍 URL: http://localhost:8188"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python3 main.py --listen 0.0.0.0 --port 8188
