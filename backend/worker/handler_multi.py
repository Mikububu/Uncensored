#!/usr/bin/env python3
"""
RunPod Serverless Handler with ComfyUI - Multi-Model Support
Supports all uncensored models via ComfyUI workflows
"""

import runpod
import json
import base64
import io
import sys
import os
import random
from PIL import Image

# Add ComfyUI to path
sys.path.append('/comfyui')

# Import ComfyUI modules
try:
    from nodes import NODE_CLASS_MAPPINGS
    from comfy import model_management
except ImportError as e:
    print(f"❌ ComfyUI import error: {e}")
    print("Make sure ComfyUI is installed in /comfyui")
    raise

# Initialize ComfyUI nodes
CheckpointLoaderSimple = NODE_CLASS_MAPPINGS["CheckpointLoaderSimple"]()
CLIPTextEncode = NODE_CLASS_MAPPINGS["CLIPTextEncode"]()
KSampler = NODE_CLASS_MAPPINGS["KSampler"]()
VAEDecode = NODE_CLASS_MAPPINGS["VAEDecode"]()
EmptyLatentImage = NODE_CLASS_MAPPINGS["EmptyLatentImage"]()
SaveImage = NODE_CLASS_MAPPINGS["SaveImage"]()

# Global model cache (checkpoint name -> loaded model)
model_cache = {}

def load_model_config():
    """Load model configuration from file"""
    config_path = os.getenv("MODEL_CONFIG_PATH", "/app/config/models.json")
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load model config: {e}")
    return None

def get_model_checkpoint_name(model_id):
    """Get checkpoint filename for a model ID"""
    config = load_model_config()
    
    # Model ID to checkpoint name mapping
    # These should match files in /comfyui/models/checkpoints/
    MODEL_MAP = {
        "pony-v6": "ponyDiffusionV6XL_v6StartWithThisOne.safetensors",
        "abyssorangemix3": "abyssorangemix3.safetensors",
        "realistic-vision-v5": "realisticVisionV50_v50VAE.safetensors",
        "flux-dev-uncensored": "flux1-dev.safetensors",
        "sdxl-turbo-uncensored": "sd_xl_turbo_1.0_fp16.safetensors",
        "chilloutmix": "chilloutmix_NiPrunedFp32Fix.safetensors",
        "deliberate-v3": "deliberate_v3.safetensors",
        "dreamshaper-v8": "dreamshaper_8.safetensors",
        "epicrealism-v5": "epicrealism_natural_sin_rc1_vae.safetensors",
        "juggernaut-xl-v9": "juggernautXL_v9.safetensors"
    }
    
    # Try to get from config first
    if config and 'models' in config:
        for model in config['models']:
            if model['id'] == model_id:
                # Check if config has a checkpoint name
                if 'checkpoint_name' in model:
                    return model['checkpoint_name']
                # Try to infer from huggingface_id or civitai_id
                if 'civitai_id' in model and model['civitai_id']:
                    # Would need to download, but for now use mapping
                    pass
    
    # Fallback to mapping
    return MODEL_MAP.get(model_id, "ponyDiffusionV6XL_v6StartWithThisOne.safetensors")

def get_model_info(model_id):
    """Get model information from config"""
    config = load_model_config()
    if config and 'models' in config:
        for model in config['models']:
            if model['id'] == model_id:
                return model
    
    # Default fallback
    return {
        'recommended_steps': 25,
        'recommended_cfg': 7.5,
        'max_resolution': 1024
    }

def load_checkpoint(ckpt_name):
    """Load a checkpoint model (cached)"""
    global model_cache
    
    if ckpt_name in model_cache:
        return model_cache[ckpt_name]
    
    print(f"📦 Loading checkpoint: {ckpt_name}")
    try:
        checkpoint_output = CheckpointLoaderSimple.load_checkpoint(ckpt_name=ckpt_name)
        model_cache[ckpt_name] = checkpoint_output
        print(f"✅ Checkpoint loaded: {ckpt_name}")
        return checkpoint_output
    except Exception as e:
        print(f"❌ Error loading checkpoint {ckpt_name}: {e}")
        raise

def generate_image(job):
    """
    Generate image using ComfyUI workflow
    Supports all uncensored models
    """
    job_input = job.get("input", {})
    
    # Extract parameters
    prompt = job_input.get("prompt", "a beautiful landscape")
    negative_prompt = job_input.get("negative_prompt", "bad quality, blurry")
    width = int(job_input.get("width", 1024))
    height = int(job_input.get("height", 1024))
    steps = int(job_input.get("num_inference_steps", 25))
    cfg = float(job_input.get("guidance_scale", 7.5))
    seed = job_input.get("seed", random.randint(1, 999999999))
    model_id = job_input.get("model_id", "pony-v6")
    
    print(f"🎨 Generating: {prompt[:50]}...")
    print(f"   Model: {model_id}")
    print(f"   Size: {width}x{height}, Steps: {steps}, CFG: {cfg}, Seed: {seed}")
    
    # Get model info
    model_info = get_model_info(model_id)
    
    # Override steps/cfg with recommended if not provided
    if steps == 25 and 'recommended_steps' in model_info:
        steps = model_info['recommended_steps']
    if cfg == 7.5 and 'recommended_cfg' in model_info:
        cfg = model_info['recommended_cfg']
    
    # Clamp resolution
    max_res = model_info.get('max_resolution', 1024)
    width = min(width, max_res)
    height = min(height, max_res)
    # Ensure divisible by 8
    width = (width // 8) * 8
    height = (height // 8) * 8
    
    # Get checkpoint name
    ckpt_name = get_model_checkpoint_name(model_id)
    
    try:
        # Load checkpoint
        checkpoint_output = load_checkpoint(ckpt_name)
        model = checkpoint_output[0]
        clip = checkpoint_output[1]
        vae = checkpoint_output[2]
        
        # Encode prompts
        positive_cond = CLIPTextEncode.encode(clip=clip, text=prompt)[0]
        negative_cond = CLIPTextEncode.encode(clip=clip, text=negative_prompt)[0]
        
        # Create latent image
        latent = EmptyLatentImage.generate(width=width, height=height, batch_size=1)[0]
        
        # Sample
        samples = KSampler.sample(
            model=model,
            seed=seed,
            steps=steps,
            cfg=cfg,
            sampler_name="euler_ancestral",
            scheduler="normal",
            positive=positive_cond,
            negative=negative_cond,
            latent_image=latent,
            denoise=1.0
        )[0]
        
        # Decode
        decoded = VAEDecode.decode(samples=samples, vae=vae)[0]
        
        # Convert to PIL Image
        image_tensor = decoded[0]
        image_np = (255. * image_tensor.cpu().numpy()).astype('uint8')
        image = Image.fromarray(image_np)
        
        # Convert to base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        print("✅ Generation complete")
        
        return {
            "image_base64": img_base64,
            "prompt": prompt,
            "model_id": model_id,
            "seed": seed,
            "width": width,
            "height": height,
            "steps": steps,
            "cfg": cfg
        }
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Generation error: {error_msg}")
        return {
            "error": error_msg,
            "model_id": model_id,
            "prompt": prompt
        }


# Start RunPod serverless handler
print("🚀 ComfyUI Multi-Model Worker Starting...")
print("   ComfyUI path: /comfyui")
print("   Models directory: /comfyui/models/checkpoints")
runpod.serverless.start({"handler": generate_image})
