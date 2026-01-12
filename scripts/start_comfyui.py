#!/usr/bin/env python3
"""
Start ComfyUI Server
Simple wrapper to start ComfyUI with custom settings
"""

import os
import sys
import subprocess

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
comfyui_dir = os.path.join(project_root, "comfyui")

if not os.path.exists(comfyui_dir):
    print("❌ ComfyUI not found. Please run the installation first.")
    sys.exit(1)

# Change to ComfyUI directory
os.chdir(comfyui_dir)

# Default settings
listen_host = "0.0.0.0"
port = 8188

# Parse command line arguments
if len(sys.argv) > 1:
    port = int(sys.argv[1])

print("🎨 Starting ComfyUI...")
print(f"📍 URL: http://localhost:{port}")
print("")
print("Press Ctrl+C to stop")
print("")

# Start ComfyUI
try:
    subprocess.run([
        sys.executable, "main.py",
        "--listen", listen_host,
        "--port", str(port)
    ])
except KeyboardInterrupt:
    print("\n👋 ComfyUI stopped")
