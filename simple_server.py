#!/usr/bin/env python3
"""
Simple Frontend Server - Clean Version
Only serves static files and handles OpenRouter API
"""

import os
import json
import asyncio
import base64
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# OpenRouter API
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('frontend', path)

@app.route('/api/generate', methods=['POST'])
async def generate():
    """Generate image using OpenRouter"""
    try:
        data = request.json
        prompt = data.get('prompt', '').strip()
        width = data.get('width', 1024)
        height = data.get('height', 1024)
        
        if not prompt:
            return jsonify({'success': False, 'error': 'Prompt required'}), 400
        
        if not OPENROUTER_API_KEY:
            return jsonify({'success': False, 'error': 'OpenRouter API key not configured'}), 500
        
        print(f"🎨 Generating: {prompt[:50]}... ({width}x{height})")
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
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
                    return jsonify({
                        'success': True,
                        'image_base64': img_b64,
                        'provider': 'openrouter',
                        'model': 'flux.2-pro'
                    })
                else:
                    return jsonify({'success': False, 'error': 'No image data in response'}), 400
            else:
                return jsonify({'success': False, 'error': 'No images in response'}), 400
        else:
            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
            error_msg = error_data.get('error', {}).get('message', f"HTTP {response.status_code}")
            return jsonify({'success': False, 'error': error_msg}), response.status_code
            
    except Exception as e:
        return jsonify({'success': False, 'error': f'Generation failed: {str(e)}'}), 500

@app.route('/api/status', methods=['GET'])
def status():
    """Check API status"""
    return jsonify({
        'openrouter_configured': bool(OPENROUTER_API_KEY),
        'api_key_preview': OPENROUTER_API_KEY[:15] + "..." if OPENROUTER_API_KEY else None
    })

if __name__ == '__main__':
    print("🚀 Starting Simple Image Generation Server")
    print(f"   OpenRouter: {'✅ Configured' if OPENROUTER_API_KEY else '❌ Not configured'}")
    print("   Visit: http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)