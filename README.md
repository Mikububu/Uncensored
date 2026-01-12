# Uncensored Studio - Multi-Model Testing Platform

A comprehensive platform for testing and comparing uncensored image generation models. Includes 10+ pre-configured models, automatic RunPod setup, and a beautiful testing website to verify which models truly allow adult content generation.

## Project Structure

```
Uncensored/
├── backend/           # Python backend worker (z-image-turbo-backend)
│   ├── server.py      # Fly.io API server
│   ├── z_image_worker.py  # Main image generation worker
│   ├── base_worker.py # Base worker utilities
│   ├── worker/        # RunPod worker handler
│   ├── scripts/       # Utility & diagnostic scripts
│   └── demo/          # Demo HTML pages
│
├── frontend/          # Web frontend (uncensored-studio-web)
│   ├── server.js      # Express server
│   ├── index.html     # Main UI
│   └── runpod_worker/ # Legacy RunPod worker (may be deprecated)
│
└── comfyui/           # ComfyUI installation (local)
    ├── main.py        # ComfyUI server
    ├── models/        # Model files (checkpoints, VAE, LoRAs)
    └── custom_nodes/  # Custom ComfyUI extensions
```

## Deployments

| Component | URL | Platform |
|-----------|-----|----------|
| Frontend | https://uncensored-studio-web.fly.dev/ | Fly.io |
| Backend | https://z-image-turbo-backend.fly.dev/ | Fly.io |
| GPU Workers | RunPod Serverless | RunPod |

## Quick Start

See [QUICKSTART.md](QUICKSTART.md) for a 5-minute setup guide.

### Full Setup

1. **Set up RunPod endpoints for all models:**
```bash
cd backend
export RUNPOD_API_KEY="your-api-key"
python scripts/setup_all_models.py
```

2. **Test which models are truly uncensored:**
```bash
python scripts/test_model_uncensored.py
```

3. **Start the frontend:**
```bash
cd frontend
npm install
npm start
```

4. **Open http://localhost:8080** and start testing!

## Features

- ✅ **10+ Uncensored Models** - Pre-configured and ready to deploy
- ✅ **Automatic Setup** - One command to set up all RunPod endpoints
- ✅ **Model Comparison** - Test multiple models side-by-side
- ✅ **Uncensored Testing** - Verify which models actually allow adult content
- ✅ **Beautiful UI** - Modern, easy-to-use testing interface
- ✅ **RunPod Integration** - Serverless GPU workers for cost-effective generation
- ✅ **ComfyUI Included** - Local ComfyUI installation for workflow testing

## Models Included

All models are configured in `config/models.json`:

- **Pony Diffusion V6** - High-quality uncensored
- **AbyssOrangeMix V3** - Anime-style, very high uncensored level
- **Realistic Vision V5** - Photorealistic uncensored
- **Flux Dev Uncensored** - Latest Flux without filters
- **SDXL Turbo Uncensored** - Fast SDXL model
- **ChilloutMix** - Asian-style, very high uncensored
- **Deliberate V3** - Versatile uncensored
- **DreamShaper V8** - High-quality versatile
- **EpicRealism V5** - Photorealistic
- **Juggernaut XL V9** - SDXL-based uncensored

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed setup and configuration guide
- **[COMFYUI_SETUP.md](COMFYUI_SETUP.md)** - ComfyUI installation and usage guide

## ComfyUI

ComfyUI is installed locally in this project! Use it for:
- **Local Testing** - Test workflows before deploying to RunPod
- **Workflow Development** - Build complex generation workflows
- **Model Management** - Download and manage models locally

**Quick Start:**
```bash
# Start ComfyUI server
python3 scripts/start_comfyui.py

# Or use the shell script
./scripts/start_comfyui.sh
```

Then open http://localhost:8188 in your browser.

See [COMFYUI_SETUP.md](COMFYUI_SETUP.md) for full documentation.

## Consolidated From

This project was consolidated from:
- `/Desktop/empty Cursor` → `backend/` (z-image-turbo-backend)
- `/Desktop/uncensored` → `frontend/` (uncensored-studio-web)

---
*Consolidated on 2026-01-11*
