#!/usr/bin/env python3
"""
ComfyUI API Client
Helper script to interact with ComfyUI API for testing and integration
"""

import requests
import json
import sys
import time
import websocket
import uuid
from typing import Dict, Any, Optional

class ComfyUIClient:
    def __init__(self, server_address: str = "127.0.0.1:8188"):
        self.server_address = server_address
        self.client_id = str(uuid.uuid4())
        
    def queue_prompt(self, prompt: Dict[str, Any]) -> str:
        """Queue a prompt and return the prompt ID"""
        p = {"prompt": prompt, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')
        req = requests.post(f"http://{self.server_address}/prompt", data=data)
        return req.json()['prompt_id']
    
    def get_image(self, filename: str, subfolder: str = "", folder_type: str = "output") -> bytes:
        """Get generated image"""
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = "&".join([f"{k}={v}" for k, v in data.items()])
        response = requests.get(f"http://{self.server_address}/view?{url_values}")
        return response.content
    
    def get_history(self, prompt_id: str) -> Dict[str, Any]:
        """Get history for a prompt ID"""
        response = requests.get(f"http://{self.server_address}/history/{prompt_id}")
        return response.json()
    
    def get_queue(self) -> Dict[str, Any]:
        """Get current queue status"""
        response = requests.get(f"http://{self.server_address}/queue")
        return response.json()
    
    def wait_for_completion(self, prompt_id: str, timeout: int = 300) -> Optional[Dict[str, Any]]:
        """Wait for prompt to complete and return results"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            history = self.get_history(prompt_id)
            
            if prompt_id in history:
                return history[prompt_id]
            
            time.sleep(1)
        
        return None
    
    def create_simple_workflow(self, prompt: str, negative_prompt: str = "", 
                              steps: int = 20, cfg: float = 7.0, 
                              width: int = 512, height: int = 512,
                              model_name: str = "v1-5-pruned-emaonly.ckpt") -> Dict[str, Any]:
        """Create a simple SD 1.5 workflow"""
        import random
        seed = random.randint(1, 999999999)
        
        return {
            "3": {
                "inputs": {
                    "seed": seed,
                    "steps": steps,
                    "cfg": cfg,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": 1.0,
                    "model": ["4", 0],
                    "positive": ["6", 0],
                    "negative": ["7", 0],
                    "latent_image": ["5", 0]
                },
                "class_type": "KSampler"
            },
            "4": {
                "inputs": {
                    "ckpt_name": model_name
                },
                "class_type": "CheckpointLoaderSimple"
            },
            "5": {
                "inputs": {
                    "width": width,
                    "height": height,
                    "batch_size": 1
                },
                "class_type": "EmptyLatentImage"
            },
            "6": {
                "inputs": {
                    "text": prompt,
                    "clip": ["4", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "7": {
                "inputs": {
                    "text": negative_prompt,
                    "clip": ["4", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "8": {
                "inputs": {
                    "samples": ["3", 0],
                    "vae": ["4", 2]
                },
                "class_type": "VAEDecode"
            },
            "9": {
                "inputs": {
                    "filename_prefix": "ComfyUI",
                    "images": ["8", 0]
                },
                "class_type": "SaveImage"
            }
        }


def main():
    """Example usage"""
    if len(sys.argv) < 2:
        print("Usage: python3 comfyui_client.py <prompt> [negative_prompt]")
        print("Example: python3 comfyui_client.py 'a beautiful landscape' 'blurry, low quality'")
        sys.exit(1)
    
    prompt = sys.argv[1]
    negative = sys.argv[2] if len(sys.argv) > 2 else ""
    
    client = ComfyUIClient()
    
    print(f"🎨 Generating: {prompt}")
    print("📡 Connecting to ComfyUI...")
    
    # Check if ComfyUI is running
    try:
        queue = client.get_queue()
        print("✅ ComfyUI is running")
    except Exception as e:
        print(f"❌ Cannot connect to ComfyUI: {e}")
        print("💡 Make sure ComfyUI is running: python3 scripts/start_comfyui.py")
        sys.exit(1)
    
    # Create workflow
    workflow = client.create_simple_workflow(prompt, negative)
    
    # Queue prompt
    prompt_id = client.queue_prompt(workflow)
    print(f"📋 Prompt ID: {prompt_id}")
    print("⏳ Waiting for completion...")
    
    # Wait for completion
    result = client.wait_for_completion(prompt_id, timeout=300)
    
    if result:
        print("✅ Generation complete!")
        outputs = result.get('outputs', {})
        for node_id, node_output in outputs.items():
            if 'images' in node_output:
                for image_info in node_output['images']:
                    filename = image_info['filename']
                    subfolder = image_info.get('subfolder', '')
                    print(f"🖼️  Image saved: {subfolder}/{filename}")
    else:
        print("❌ Generation timed out or failed")


if __name__ == "__main__":
    main()
