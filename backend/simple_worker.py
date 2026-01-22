#!/usr/bin/env python3
"""
Simple Image Generation Worker - Clean Version
Only supports OpenRouter Flux 2 Pro
"""

import os
import asyncio
import base64
import requests
import json
from datetime import datetime

class SimpleImageWorker:
    def __init__(self):
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.openrouter_api_key:
            print("❌ ERROR: OPENROUTER_API_KEY not set")
            print("Set it with: export OPENROUTER_API_KEY='sk-or-v1-...'")
        else:
            print(f"✅ OpenRouter API key configured")
    
    async def generate_image(self, prompt: str, width: int = 1024, height: int = 1024) -> dict:
        """Generate image using OpenRouter Flux 2 Pro"""
        try:
            print(f"🎨 Generating: {prompt[:50]}... ({width}x{height})")
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openrouter_api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://aprils-spielzeugkasten.netlify.app",
                    "X-Title": "Uncensored Studio"
                },
                json={
                    "model": "black-forest-labs/flux.2-pro",
                    "messages": [{"role": "user", "content": prompt}],
                    "modalities": ["image", "text"]
                },
                timeout=120
            )
            
            if response.status_code == 200:
                data = response.json()
                images = data.get('choices', [{}])[0].get('message', {}).get('images', [])
                
                if images:
                    image_data = images[0].get('image_url', {}).get('url')
                    if image_data and image_data.startswith('data:'):
                        img_b64 = image_data.split(',')[1]
                        print(f"✅ Success! Generated {len(img_b64)} bytes")
                        return {
                            'success': True,
                            'image_base64': img_b64,
                            'provider': 'openrouter',
                            'model': 'flux.2-pro'
                        }
                    else:
                        return {'success': False, 'error': 'No image data in response'}
                else:
                    return {'success': False, 'error': 'No images in response'}
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                error_msg = error_data.get('error', {}).get('message', f"HTTP {response.status_code}")
                return {'success': False, 'error': error_msg}
                
        except Exception as e:
            return {'success': False, 'error': f'Generation failed: {str(e)}'}

# Test function
async def test():
    worker = SimpleImageWorker()
    result = await worker.generate_image("2 people in love, claymation style")
    
    if result['success']:
        # Save test image
        img_data = base64.b64decode(result['image_base64'])
        with open('test_output.png', 'wb') as f:
            f.write(img_data)
        print(f"✅ Test image saved: test_output.png ({len(img_data)} bytes)")
    else:
        print(f"❌ Test failed: {result['error']}")

if __name__ == "__main__":
    asyncio.run(test())