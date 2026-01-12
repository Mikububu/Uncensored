# ComfyUI Setup Guide

ComfyUI has been installed in this project! 🎨

## Quick Start

### Option 1: Using the Shell Script
```bash
./scripts/start_comfyui.sh
```

### Option 2: Using the Python Script
```bash
python3 scripts/start_comfyui.py
# Or with custom port:
python3 scripts/start_comfyui.py 9000
```

### Option 3: Direct Start
```bash
cd comfyui
python3 main.py --listen 0.0.0.0 --port 8188
```

## Access ComfyUI

Once started, open your browser and go to:
- **Local**: http://localhost:8188
- **Network**: http://YOUR_IP:8188

## Directory Structure

```
comfyui/
├── main.py              # Main ComfyUI server
├── models/              # Model files (checkpoints, VAE, LoRAs, etc.)
│   ├── checkpoints/     # Stable Diffusion models (.ckpt, .safetensors)
│   ├── vae/            # VAE models
│   ├── loras/          # LoRA models
│   └── ...
├── input/              # Input images
├── output/             # Generated images
└── custom_nodes/       # Custom ComfyUI extensions
```

## Installing Models

### Method 1: Manual Download
1. Download models from [CivitAI](https://civitai.com) or [HuggingFace](https://huggingface.co)
2. Place checkpoint files in `comfyui/models/checkpoints/`
3. Place VAE files in `comfyui/models/vae/`
4. Place LoRA files in `comfyui/models/loras/`

### Method 2: Using the Web UI
- ComfyUI has a built-in model manager in the web interface
- Look for the "Manager" button in the UI

## Installing Custom Nodes

Custom nodes extend ComfyUI functionality:

1. Go to `comfyui/custom_nodes/`
2. Clone custom node repositories:
   ```bash
   cd comfyui/custom_nodes
   git clone https://github.com/author/custom-node-name.git
   ```
3. Install dependencies (if any):
   ```bash
   cd custom-node-name
   pip install -r requirements.txt
   ```
4. Restart ComfyUI

## Popular Custom Nodes

- **ComfyUI Manager**: Manage nodes and models from UI
- **ControlNet**: Advanced control for image generation
- **AnimateDiff**: Video generation
- **IPAdapter**: Face/character consistency

## Integration with This Project

ComfyUI can be used alongside the existing RunPod workers:

- **Local Development**: Use ComfyUI for testing workflows
- **RunPod Workers**: Use ComfyUI workflows in RunPod serverless endpoints
- **Hybrid**: Test locally, deploy to RunPod

## API Usage

ComfyUI provides a REST API for programmatic access:

```python
import requests
import json

# Queue a prompt
url = "http://localhost:8188/prompt"
workflow = {
    # Your ComfyUI workflow JSON
}
response = requests.post(url, json={"prompt": workflow})
```

## Troubleshooting

### Port Already in Use
```bash
# Use a different port
python3 scripts/start_comfyui.py 9000
```

### Models Not Loading
- Check file format (.ckpt or .safetensors)
- Verify model is in correct directory
- Check ComfyUI console for error messages

### Out of Memory
- Use smaller models (SD 1.5 instead of SDXL)
- Reduce image resolution
- Close other applications

## Next Steps

1. **Download Models**: Get your favorite uncensored models
2. **Create Workflows**: Build custom generation workflows
3. **Test Integration**: Connect ComfyUI with the backend API
4. **Deploy**: Use ComfyUI workflows in RunPod workers

## Resources

- [ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI)
- [ComfyUI Documentation](https://github.com/comfyanonymous/ComfyUI/wiki)
- [ComfyUI Examples](https://github.com/comfyanonymous/ComfyUI_examples)
- [CivitAI Models](https://civitai.com)
