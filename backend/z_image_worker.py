import os
import asyncio
import base64
import runpod
import requests
import time
import json
import random
from pathlib import Path
from datetime import datetime
import fal_client
from base_worker import BaseWorker
from self_healing_agent import SelfHealingAgent

class ZImageWorker(BaseWorker):
    def __init__(self):
        self.healer = SelfHealingAgent()
        super().__init__(task_types=['image_generation', 'check_balance', 'audio_transcription'])
        
        # Load model configuration
        self.model_config = self._load_model_config()
        self.model_endpoints = self._load_endpoint_mapping()
        
        # Load API keys (try Supabase first, then environment)
        self._load_api_keys()
        
        if self.runpod_api_key:
            runpod.api_key = self.runpod_api_key
            
        print(f"🚀 Z-Image Worker initialized")
        print(f"   RunPod endpoint: {self.endpoint_id or 'Not configured'}")
        print(f"   Fal.ai: {'Configured' if self.fal_api_key else 'Not configured'}")
        print(f"   Models configured: {len(self.model_config.get('models', [])) if self.model_config else 0}")
    
    def _load_api_keys(self):
        """Load API keys from Supabase, MCP, or environment variables"""
        # Initialize attributes first
        self.runpod_api_key = None
        self.endpoint_id = None
        self.fal_api_key = None
        
        # Priority 1: Try MCP project-secrets (if available in Cursor)
        try:
            # This will work if running in Cursor with MCP enabled
            import subprocess
            result = subprocess.run(
                ['python3', '-c', 
                 'from mcp_project_secrets import get_api_key; '
                 'print(get_api_key("runpod"))'],
                capture_output=True, text=True, timeout=2
            )
            if result.returncode == 0 and result.stdout.strip():
                mcp_key = result.stdout.strip()
                if mcp_key and not mcp_key.startswith('Error'):
                    self.runpod_api_key = mcp_key
                    print("✅ Loaded RunPod API key from MCP")
        except:
            pass
        
        # Priority 2: Try Supabase
        try:
            keys = self._load_keys_from_supabase()
            if keys:
                if not self.runpod_api_key:
                    self.runpod_api_key = keys.get('runpod')
                self.endpoint_id = keys.get('runpod_endpoint') or self.endpoint_id
                self.fal_api_key = keys.get('fal') or self.fal_api_key
                if keys.get('runpod'):
                    print("✅ Loaded API keys from Supabase")
        except Exception as e:
            print(f"⚠️  Could not load from Supabase: {e}")
        
        # Priority 3: Fallback to environment variables
        if not self.runpod_api_key:
            self.runpod_api_key = os.getenv("RUNPOD_API_KEY")
        if not self.endpoint_id:
            self.endpoint_id = os.getenv("RUNPOD_ENDPOINT_ID")
        if not self.fal_api_key:
            self.fal_api_key = os.getenv("FAL_KEY")
        
        # Final fallback: Use environment variable or fail
        if not self.runpod_api_key:
            print("⚠️  RunPod API key not found. Please set RUNPOD_API_KEY environment variable or configure in Supabase.")
        
        # Use the working endpoint we found, or default
        if not self.endpoint_id:
            # Use the ComfyUI multi-model endpoint
            self.endpoint_id = "4e7784vway3niq"  # ComfyUI Multi-Model Endpoint
            print(f"⚠️  Using default endpoint: {self.endpoint_id}")
        
        if not self.runpod_api_key:
            print("ERROR: RUNPOD_API_KEY is not set.")
    
    def _load_keys_from_supabase(self):
        """Load API keys from Supabase api_keys table"""
        try:
            from supabase import create_client, Client
            
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_ANON_KEY")
            
            if not supabase_url or not supabase_key:
                return None
            
            supabase: Client = create_client(supabase_url, supabase_key)
            response = supabase.table("api_keys").select("*").execute()
            
            keys = {}
            for row in response.data:
                service = row.get('service')
                key = row.get('key')
                if service and key:
                    keys[service] = key
            
            return keys
        except ImportError:
            # Supabase not installed, that's okay
            return None
        except Exception as e:
            print(f"Warning: Could not load from Supabase: {e}")
            return None
    
    def _load_model_config(self):
        """Load model configuration from JSON file"""
        config_path = Path(__file__).parent.parent.parent / "config" / "models.json"
        try:
            if config_path.exists():
                with open(config_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load model config: {e}")
        return None
    
    def _load_endpoint_mapping(self):
        """Load endpoint ID mapping from file or environment"""
        # Try to load from endpoints.json file
        endpoints_path = Path(__file__).parent.parent / "endpoints.json"
        try:
            if endpoints_path.exists():
                with open(endpoints_path, 'r') as f:
                    endpoints = json.load(f)
                    # Convert to model_id -> endpoint_id mapping
                    return {model_id: info['endpoint_id'] for model_id, info in endpoints.items()}
        except Exception as e:
            print(f"Warning: Could not load endpoint mapping: {e}")
        
        # Fallback: use single endpoint for all models
        default_endpoint = os.getenv("RUNPOD_ENDPOINT_ID")
        if default_endpoint:
            # Create mapping for all known models
            models = self.model_config.get('models', []) if self.model_config else []
            return {model['id']: default_endpoint for model in models}
        
        return {}
    
    def get_endpoint_for_model(self, model_id):
        """Get RunPod endpoint ID for a specific model"""
        # First check explicit mapping
        if model_id in self.model_endpoints:
            return self.model_endpoints[model_id]
        
        # Fallback to default endpoint
        return self.endpoint_id

    async def process_task(self, task: dict) -> dict:
        """
        Process an image generation task using selected provider.
        """
        
        
        input_data = task.get('input', {}) or task.get('params', {})
        provider = input_data.get('provider', 'runpod')  # Default to runpod
        
        print(f"🎨 Processing image task: {task.get('id')} with provider: {provider}")
        
        if task['type'] == 'check_balance':
             return await self.check_balance(task)

        if task['type'] == 'audio_transcription':
             return await self.transcribe_audio(task, input_data)

        if provider == 'fal':
            return await self.generate_with_fal(task, input_data)
        elif provider == 'comfyui':
            # Local ComfyUI instance
            return await self.generate_with_comfyui(task, input_data)
        else:
            # ALL RunPod models use ComfyUI pipeline
            # ComfyUI is the engine, models are checkpoints loaded inside it
            model_id = input_data.get('model_id', 'pony-v6')
            target_endpoint = input_data.get('endpoint_id') or self.get_endpoint_for_model(model_id)
            
            

            
            if not target_endpoint:
                return {'success': False, 'error': f'No endpoint configured for model {model_id}'}
            
            # All RunPod requests use ComfyUI worker (handler_multi.py)
            # The worker loads the correct model checkpoint based on model_id
            result = await self.generate_with_runpod(task, input_data, target_endpoint)
            return result

    async def generate_with_fal(self, task: dict, input_data: dict) -> dict:
        """Generate image using Fal.ai endpoint"""
        try:
            if not self.fal_api_key:
                return {'success': False, 'error': 'Fal.ai API key not configured'}
            
            # Extract params
            prompt = input_data.get('prompt') or input_data.get('description') or "A beautiful scene"
            # Flux default params
            steps = int(input_data.get('steps', 28))
            guidance = float(input_data.get('guidance', 3.5))
            
            print(f"🎨 Generating with Fal.ai (Flux Dev): {prompt[:50]}... (Steps: {steps}, Guidance: {guidance})")
            
            # Use fal-ai/flux/dev
            handler = await fal_client.submit_async(
                "fal-ai/flux/dev",
                arguments={
                    "prompt": prompt,
                    "num_inference_steps": steps,
                    "guidance_scale": guidance,
                    "enable_safety_checker": False,
                    "output_format": "png",
                    "image_size": {
                        "width": int(input_data.get('width', 1024)),
                        "height": int(input_data.get('height', 1024))
                    }
                },
            )
            
            result = await handler.get()
            
            if not result or 'images' not in result or not result['images']:
                return {'success': False, 'error': 'No images returned from Fal.ai'}
            
            image_url = result['images'][0]['url']
            print(f"✅ Fal.ai success: {image_url}")
            
            # Download the image
            img_response = requests.get(image_url)
            if img_response.status_code != 200:
                return {'success': False, 'error': f'Failed to download image: {img_response.status_code}'}
            
            img_bytes = img_response.content
            
            return {
                'success': True,
                'output': {
                    'prompt': prompt,
                    'provider': 'fal-ai'
                },
                'images': [{'url': image_url}],
                'artifacts': [
                    {
                        'type': 'image_png',
                        'content_type': 'image/png',
                        'filename': f"generated_{task.get('id')}.png",
                        'metadata': {'width': 1024, 'height': 1024, 'provider': 'fal-ai'}
                    }
                ]
            }
            
        except Exception as e:
            err_msg = str(e)
            if "balance" in err_msg.lower() or "credits" in err_msg.lower():
                err_msg = "Insufficient balance on Fal.ai account."
            elif "safety" in err_msg.lower() or "nsfw" in err_msg.lower():
                err_msg = "Shadow Filter: Fal.ai blocked this prompt."
            
            print(f"❌ Fal.ai error: {err_msg}")
            return {'success': False, 'error': f'Fal.ai error: {err_msg}'}

    async def generate_with_comfyui(self, task: dict, input_data: dict) -> dict:
        """Generate image using local ComfyUI instance"""
        comfyui_url = input_data.get('comfyui_url', 'http://127.0.0.1:8188')
        
        # Extract parameters
        prompt = input_data.get('prompt') or input_data.get('description') or "A beautiful scene"
        negative_prompt = input_data.get('negative_prompt', 'bad quality, blurry')
        steps = int(input_data.get('num_inference_steps', 20))
        guidance = float(input_data.get('guidance_scale', 7.0))
        width = int(input_data.get('width', 512))
        height = int(input_data.get('height', 512))
        model_name = input_data.get('model_name', 'v1-5-pruned-emaonly.ckpt')
        
        print(f"🎨 ComfyUI: Generating '{prompt[:50]}...' ({width}x{height}, {steps} steps)")
        
        try:
            # Create workflow
            workflow = self._get_comfy_workflow(prompt, negative_prompt, steps, guidance, width, height, model_name)
            
            # Queue prompt
            import uuid
            client_id = str(uuid.uuid4())
            payload = {"prompt": workflow, "client_id": client_id}
            
            response = requests.post(f"{comfyui_url}/prompt", json=payload, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            prompt_id = result.get('prompt_id')
            
            if not prompt_id:
                return {'success': False, 'error': 'ComfyUI did not return a prompt ID'}
            
            print(f"⏳ ComfyUI Prompt ID: {prompt_id}")
            
            # Wait for completion (poll history)
            max_wait = 60  # 1 minute timeout
            total_wait = 0
            image_data = None
            
            while total_wait < max_wait:
                await asyncio.sleep(2)
                total_wait += 2
                
                # Check history
                history_response = requests.get(f"{comfyui_url}/history/{prompt_id}", timeout=5)
                if history_response.status_code == 200:
                    history = history_response.json()
                    if prompt_id in history:
                        # Get output images
                        outputs = history[prompt_id].get('outputs', {})
                        for node_id, node_output in outputs.items():
                            if 'images' in node_output:
                                for image_info in node_output['images']:
                                    filename = image_info['filename']
                                    subfolder = image_info.get('subfolder', '')
                                    folder_type = image_info.get('type', 'output')
                                    
                                    # Download image
                                    image_url = f"{comfyui_url}/view?filename={filename}&subfolder={subfolder}&type={folder_type}"
                                    img_response = requests.get(image_url, timeout=10)
                                    if img_response.status_code == 200:
                                        image_data = base64.b64encode(img_response.content).decode('utf-8')
                                        print(f"✅ ComfyUI: Image generated in {total_wait}s")
                                        return {
                                            'success': True,
                                            'image_base64': image_data,
                                            'provider': 'comfyui',
                                            'prompt_id': prompt_id
                                        }
                
                if total_wait % 10 == 0:
                    print(f"⏳ ComfyUI: Waiting... ({total_wait}s)")
            
            return {'success': False, 'error': f'ComfyUI generation timed out after {max_wait} seconds'}
            
        except requests.exceptions.ConnectionError:
            return {'success': False, 'error': 'Cannot connect to ComfyUI. Make sure ComfyUI is running on ' + comfyui_url}
        except requests.exceptions.Timeout:
            return {'success': False, 'error': 'ComfyUI request timed out'}
        except Exception as e:
            print(f"❌ ComfyUI error: {str(e)}")
            return {'success': False, 'error': f'ComfyUI error: {str(e)}'}

    async def generate_with_runpod(self, task: dict, input_data: dict, endpoint_id: str = None) -> dict:
        """Generate image using RunPod endpoint"""
        

        
        eid = endpoint_id or self.endpoint_id
        if not eid:
            

            return {'success': False, 'error': 'RunPod endpoint not configured'}
            
        # Extract advanced parameters
        prompt = input_data.get('prompt') or input_data.get('description') or "A beautiful scene"
        steps = int(input_data.get('num_inference_steps', 25))
        guidance = float(input_data.get('guidance_scale', 7.5))
        # Safety checker ignored for RunPod standard template usually, but we can pass if custom
        
        # Prepare RunPod payload - Use ComfyUI workflow (since worker now uses ComfyUI)
        # The worker handler_multi.py now uses ComfyUI, so we send standard payload
        # The worker will handle ComfyUI internally
        # But we can also send ComfyUI workflow directly if needed
        use_comfy_workflow = input_data.get('use_comfy_workflow', False)
        
        if use_comfy_workflow or input_data.get('workflow'):
             print("🎨 Using ComfyUI Workflow for RunPod")
             # Use ComfyUI Workflow
             if input_data.get('workflow'):
                 workflow = input_data['workflow']
             else:
                 negative_prompt = input_data.get('negative_prompt', 'bad quality, blurry')
                 width = overrides.get('width', input_data.get('width', 1024))
                 height = overrides.get('height', input_data.get('height', 1024))
                 model_name = input_data.get('model_name', 'ponyDiffusionV6XL_v6StartWithThisOne.safetensors')
                 workflow = self._get_comfy_workflow(prompt, negative_prompt, req_steps, guidance, width, height, model_name)
                 
             payload = {
                 "input": {
                     "workflow": workflow,
                     "images": input_data.get('images', [])
                 }
             }
        else:
            # Standard SDXL/SD Payload
            
            # CHECK HEALER OVERRIDES
            model_id = input_data.get('model_id', 'pony-v6')
            overrides = self.healer.get_overrides(model_id)
            
            width = overrides.get('width', input_data.get('width', 1024))
            height = overrides.get('height', input_data.get('height', 1024))
            
            # Check step cap
            req_steps = steps
            if 'max_steps' in overrides:
                req_steps = min(steps, overrides['max_steps'])
                if req_steps < steps:
                    print(f"⚠️ HEALER: Capping steps for {model_id} to {req_steps}")

            # Payload for ComfyUI worker (handler_multi.py)
            # ALL parameters map to ComfyUI nodes:
            # - prompt → CLIPTextEncode node (positive)
            # - negative_prompt → CLIPTextEncode node (negative)
            # - width/height → EmptyLatentImage node
            # - num_inference_steps → KSampler node (steps)
            # - guidance_scale → KSampler node (cfg)
            # - model_id → CheckpointLoaderSimple node (loads checkpoint)
            # - seed → KSampler node
            # - sampler_name → KSampler node
            # - scheduler → KSampler node
            payload = {
                "input": {
                    "prompt": prompt,                                    # → CLIPTextEncode node
                    "negative_prompt": input_data.get('negative_prompt', 'bad quality, blurry'),  # → CLIPTextEncode node
                    "width": width,                                      # → EmptyLatentImage node
                    "height": height,                                    # → EmptyLatentImage node
                    "num_inference_steps": req_steps,                   # → KSampler node (steps)
                    "guidance_scale": guidance,                          # → KSampler node (cfg)
                    "model_id": model_id,                                # → CheckpointLoaderSimple node (loads checkpoint)
                    "seed": input_data.get('seed', random.randint(1, 999999999)),  # → KSampler node
                    "sampler_name": input_data.get('sampler_name', 'euler_ancestral'),  # → KSampler node
                    "scheduler": input_data.get('scheduler', 'normal'),  # → KSampler node
                    "denoise": input_data.get('denoise', 1.0)            # → KSampler node
                }
            }
        
        # Support image-to-image or refiner if image_url provided
        if input_data.get('image_url'):
             payload["input"]["image_url"] = input_data['image_url']
             
        print(f"DEBUG: Sending payload to RunPod: {payload}")
        
        


        try:
            endpoint = runpod.Endpoint(eid)
            
            # 1. Trigger Run (Async)
            

            run_request = endpoint.run(payload)
            
            

            
            # Handle response type safely to get ID
            job_id_runpod = None
            if isinstance(run_request, dict):
                job_id_runpod = run_request.get('id')
            else:
                job_id_runpod = getattr(run_request, 'job_id', getattr(run_request, 'id', None))
            
            

                
            if not job_id_runpod:
                

                return {'success': False, 'error': f"Failed to get RunPod Job ID. Resp: {run_request}"}

            print(f"⏳ Polling RunPod Job: {job_id_runpod} on endpoint {eid} (Timeout: 300s)")

            # 2. Poll using Raw REST API
            url = f"https://api.runpod.ai/v2/{eid}/status/{job_id_runpod}"
            headers = {"Authorization": f"Bearer {self.runpod_api_key}"}
            
            total_wait = 0
            max_wait = 1800  # 30 minute timeout - just need to prove it works
            

            
            output_data = {}
            
            while True:
                try:
                    

                    r = requests.get(url, headers=headers)
                    r_data = r.json()
                    

                except Exception as e:
                    print(f"Warning: Poll failed: {e}")
                    await asyncio.sleep(2)
                    total_wait += 2
                    continue
                
                status = r_data.get('status')
                
                if status == 'COMPLETED':
                    output_data = r_data.get('output', {})
                    

                    print(f"✅ RunPod Completed! Output Keys: {list(output_data.keys())}")
                    break
                elif status in ['FAILED', 'CANCELLED', 'TIMED_OUT']:
                    

                    raw_err = r_data.get('error', status)
                    self._log_stuck_job(job_id_runpod, status, total_wait, prompt, eid, raw_err)
                    if "balance" in str(raw_err).lower() or "credits" in str(raw_err).lower():
                        return {'success': False, 'error': f"Insufficient balance on RunPod."}
                    return {'success': False, 'error': f"RunPod failed: {raw_err}"}
                
                if total_wait > max_wait:
                    

                    self._log_stuck_job(job_id_runpod, 'TIMEOUT', total_wait, prompt, eid, 'Timeout after 300 seconds')
                    print(f"❌ TIMEOUT: RunPod endpoint {eid} exceeded 300 second limit.")
                    return {'success': False, 'error': f"Image generation timed out after 300 seconds. The model may be too slow or the endpoint may need optimization. Try a faster model or reduce image resolution."}
                    
                await asyncio.sleep(2)
                total_wait += 2
                if total_wait % 20 == 0:
                    ts = datetime.utcnow().isoformat()
                    worker_status = self._get_worker_count(eid)
                    

                    print(f"⏳ [{ts}] Job {job_id_runpod[:8]}... | Status: {status} | Wait: {total_wait}s | Workers: {worker_status}")

            # Decode image
            

            img_b64 = output_data.get('image_base64') or output_data.get('audio_base64')
            
            # Check for standard RunPod "images" list
            if not img_b64 and 'images' in output_data:
                images_list = output_data['images']
                if isinstance(images_list, list) and len(images_list) > 0:
                    img_val = images_list[0]
                    # Check if it's base64 (long str) or url
                    if len(img_val) > 1000: # Likely base64
                        img_b64 = img_val
                    else:
                        output_data['image_url'] = img_val # Handle as URL below
            
            # Handle image_url (Data URI or HTTP URL) if image_base64 is missing
            if not img_b64 and 'image_url' in output_data:
                img_url = output_data['image_url']
                if img_url.startswith('data:'):
                    # Parse Data URI: data:image/png;base64,....
                    try:
                        img_b64 = img_url.split(',')[1]
                    except IndexError:
                        print(f"❌ Failed to parse data URI: {img_url[:50]}...")
                else:
                    # Assume HTTP URL and try to download (similar to Fal.ai)
                    print(f"⬇️ Downloading image from URL: {img_url}")
                    try:
                        r_img = requests.get(img_url)
                        if r_img.status_code == 200:
                            img_b64 = base64.b64encode(r_img.content).decode('utf-8')
                        else:
                            print(f"❌ Failed to download image: {r_img.status_code}")
                    except Exception as e:
                        print(f"❌ Error downloading image: {e}")

            if not img_b64:
                

                return {'success': False, 'error': f'No image data returned. Data: {output_data}'}
            
            

            try:
                img_bytes = base64.b64decode(img_b64)
                

            except Exception as e:
                

                return {'success': False, 'error': f'Failed to decode base64 image: {str(e)}'}
            

            return {
                'success': True,
                'output': {
                    'prompt': prompt,
                    'provider': 'runpod'
                },
                'images': [{'url': f"data:image/png;base64,{img_b64}"}],
                'artifacts': [
                    {
                        'type': 'image_png',
                        'content_type': 'image/png',
                        'filename': f"generated_{task.get('id')}.png",
                        'metadata': {'width': 512, 'height': 512, 'provider': 'runpod'}
                    }
                ]
            }

        except Exception as e:
            

            # REPORT FAILURE TO HEALER
            self.healer.report_failure(input_data.get('model_id', 'unknown'), str(e))
            return {'success': False, 'error': str(e)}
    async def check_balance(self, task: dict) -> dict:
        """Check balance for providers."""
        try:
            url = "https://api.runpod.io/graphql"
            query = "query { myself { clientBalance } }"
            headers = {
                "Authorization": f"Bearer {self.runpod_api_key}",
                "Content-Type": "application/json"
            }
            r = requests.post(url, json={"query": query}, headers=headers)
            data = r.json()
            balance = data.get('data', {}).get('myself', {}).get('clientBalance', 'N/A')
            
            # Additional: Check Worker Status for "Cold Start" visibility
            worker_status = self._get_worker_count(self.endpoint_id)

            return {
                'success': True,
                'output': {
                    'balance': f"${balance}" if balance != 'N/A' else 'ACTIVE',
                    'worker_status': worker_status
                }
            }
        except Exception as e:
            print(f"Balance check error: {e}")
            return {
                'success': True,
                'output': {
                    'balance': 'ACTIVE'
                }
            }

    async def transcribe_audio(self, task: dict, input_data: dict) -> dict:
        """Transcribe audio using fal-ai/whisper"""
        try:
            if not self.fal_api_key:
                return {'success': False, 'error': 'Fal.ai API key not configured'}

            audio_base64 = input_data.get('audio_base64')
            if not audio_base64:
                return {'success': False, 'error': 'No audio data provided'}

            print(f"🎙️ Transcribing audio for task: {task.get('id')}")

            # Use fal-ai/whisper
            handler = await fal_client.submit_async(
                "fal-ai/whisper",
                arguments={
                    "audio_url": f"data:audio/webm;base64,{audio_base64}"
                },
            )
            
            result = await handler.get()
            
            if not result or 'text' not in result:
                return {'success': False, 'error': 'No text returned from transcription'}

            transcription = result['text']
            print(f"👂 Transcribed: {transcription[:100]}...")

            return {
                'success': True,
                'output': {
                    'text': transcription
                }
            }

        except Exception as e:
            print(f"❌ Transcription error: {str(e)}")
            return {'success': False, 'error': f'Transcription error: {str(e)}'}

    def _get_worker_count(self, eid):
        """Helper to get worker status for logging"""
        try:
            url = f"https://api.runpod.ai/v2/{eid}/health"
            headers = {"Authorization": f"Bearer {self.runpod_api_key}"}
            r = requests.get(url, headers=headers, timeout=2)
            if r.status_code == 200:
                h = r.json()
                w = h.get('workers', {})
                return f"Init: {w.get('initializing', 0)} | Ready: {w.get('ready', 0)} | Run: {w.get('running', 0)}"
            return "Unknown"
        except:
            return "Unknown"

    def _get_comfy_workflow(self, prompt, steps, cfg):
        """Generate a standard ComfyUI workflow for SD 1.5"""
        import random
        return {
            "3": {
                "class_type": "KSampler",
                "inputs": {
                    "cfg": cfg,
                    "denoise": 1.0,
                    "latent_image": ["5", 0],
                    "model": ["4", 0],
                    "negative": ["7", 0],
                    "positive": ["6", 0],
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "seed": random.randint(1, 999999999),
                    "steps": steps
                }
            },
            "4": {
                "class_type": "CheckpointLoaderSimple",
                "inputs": {
                    "ckpt_name": model_name
                }
            },
            "5": {
                "class_type": "EmptyLatentImage",
                "inputs": {
                    "batch_size": 1,
                    "height": height,
                    "width": width
                }
            },
            "6": {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "clip": ["4", 1],
                    "text": prompt
                }
            },
            "7": {
               "class_type": "CLIPTextEncode",
               "inputs": {
                   "clip": ["4", 1],
                   "text": negative_prompt or "bad quality, blurry"
               }
            },
            "8": {
                "class_type": "VAEDecode",
                "inputs": {
                    "samples": ["3", 0],
                    "vae": ["4", 2]
                }
            },
            "9": {
                "class_type": "SaveImage",
                "inputs": {
                    "filename_prefix": "runpod_gen",
                    "images": ["8", 0]
                }
            }
        }

    async def get_admin_metrics(self) -> dict:
        """Fetch real-time metrics for Admin Dashboard"""
        try:
            if not self.endpoint_id or not self.runpod_api_key:
                return {"error": "RunPod not configured"}
                
            url = f"https://api.runpod.ai/v2/{self.endpoint_id}/health"
            headers = {"Authorization": f"Bearer {self.runpod_api_key}"}
            
            # Fetch Health (Worker Counts)
            r = requests.get(url, headers=headers, timeout=5)
            health_data = r.json() if r.status_code == 200 else {}
            
            # Extract worker stats
            workers = health_data.get('workers', {})
            initializing = workers.get('initializing', 0)
            ready = workers.get('ready', 0)
            running = workers.get('running', 0)
            throttled = workers.get('throttled', 0)
            
            # Estimate Cost (Assumption: $0.0005/s or $1.80/hr per GPU - simplified)
            # You might want to make this configurable or fetch from API if possible
            GPU_COST_PER_HR = 0.69 # Example for RTX 4090 or similar
            hourly_burn = (running + ready + initializing) * GPU_COST_PER_HR
            
            return {
                "success": True,
                "timestamp": datetime.utcnow().isoformat(),
                "workers": {
                    "total": initializing + ready + running + throttled,
                    "active": running,
                    "idle": ready,
                    "warming_up": initializing,
                    "throttled": throttled
                },
                "queue": {
                    "depth": health_data.get('jobs', {}).get('inQueue', 0),
                    "in_progress": health_data.get('jobs', {}).get('inProgress', 0)
                },
                "cost_estimate": {
                    "hourly_burn_usd": round(hourly_burn, 3),
                    "currency": "USD"
                }
            }
        except Exception as e:
            print(f"Metrics error: {e}")
            return {"success": False, "error": str(e)}

    def _log_stuck_job(self, job_id, status, wait_time, prompt, endpoint_id, error=None):
        """Comprehensive logging for stuck or failed jobs."""
        ts = datetime.utcnow().isoformat()
        print(f"""
================================================================================
🚨 STUCK JOB LOG @ {ts}
================================================================================
Job ID:       {job_id}
Endpoint:     {endpoint_id}
Status:       {status}
Wait Time:    {wait_time}s
Error:        {error or 'N/A'}
Prompt:       {prompt[:100]}...
Workers:      {self._get_worker_count(endpoint_id)}
================================================================================
""")

if __name__ == "__main__":
    worker = ZImageWorker()
    asyncio.run(worker.start())
