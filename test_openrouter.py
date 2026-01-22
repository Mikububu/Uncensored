#!/usr/bin/env python3
"""
Test script for OpenRouter Flux schnell integration.
Run this to verify your OpenRouter API key is working.
"""

import os
import sys
import base64
import requests

def test_openrouter():
    """Test OpenRouter image generation"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("❌ ERROR: OPENROUTER_API_KEY not set")
        print("\nTo get an API key:")
        print("1. Go to https://openrouter.ai/keys")
        print("2. Create a new API key")
        print("3. Set it in your environment:")
        print("   export OPENROUTER_API_KEY='sk-or-v1-...'")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...{api_key[-4:]}")
    
    # Test image generation using chat completions endpoint
    print("\n🎨 Testing image generation...")
    print("   Prompt: 'A beautiful sunset over mountains, photorealistic'")
    print("   Model: black-forest-labs/flux.2-pro")
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8080",
                "X-Title": "Uncensored Studio Test"
            },
            json={
                "model": "black-forest-labs/flux.2-pro",
                "messages": [
                    {
                        "role": "user",
                        "content": "A beautiful sunset over mountains, photorealistic"
                    }
                ],
                "modalities": ["image", "text"]
            },
            timeout=120
        )
        
        response.raise_for_status()
        data = response.json()
        
        if not data.get('choices') or len(data['choices']) == 0:
            print("❌ No response from OpenRouter")
            return False
        
        message = data['choices'][0].get('message', {})
        images = message.get('images', [])
        
        if not images or len(images) == 0:
            print("❌ No images in OpenRouter response")
            print(f"Response: {data}")
            return False
        
        image_data = images[0].get('image_url', {}).get('url')
        
        if not image_data:
            print("❌ No image URL in OpenRouter response")
            return False
        
        print(f"✅ Success! Image received")
        
        # Parse and save the image
        if image_data.startswith('data:'):
            img_b64 = image_data.split(',')[1]
            img_data = base64.b64decode(img_b64)
        else:
            print(f"⬇️ Downloading image from URL...")
            img_response = requests.get(image_data, timeout=60)
            img_data = img_response.content
        
        # Save the image
        output_path = "/Users/michaelperinwogenburg/Desktop/big challenge/Uncensored/flux_test_output.png"
        with open(output_path, 'wb') as f:
            f.write(img_data)
        
        print(f"✅ Image saved to: {output_path}")
        print(f"   Image size: {len(img_data) / 1024:.1f} KB")
        
        return True
        
    except requests.exceptions.HTTPError as e:
        error_data = e.response.json() if e.response else {}
        error_msg = error_data.get('error', {}).get('message', str(e))
        print(f"❌ OpenRouter error: {error_msg}")
        if e.response:
            print(f"   Status: {e.response.status_code}")
            print(f"   Response: {e.response.text[:500]}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_openrouter()
    sys.exit(0 if success else 1)
