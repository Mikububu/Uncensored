# Uncensored Image Models Setup Guide

This guide will help you set up and test multiple uncensored image generation models on RunPod with a testing website.

## Overview

This project provides:
- **10+ uncensored image models** configured and ready to deploy
- **Automatic RunPod endpoint setup** for each model
- **Testing website** to compare models side-by-side
- **Uncensored testing suite** to verify which models truly allow adult content

## Models Included

1. **Pony Diffusion V6** - High-quality uncensored model
2. **AbyssOrangeMix V3** - Popular anime-style uncensored
3. **Realistic Vision V5** - Photorealistic uncensored
4. **Flux Dev Uncensored** - Latest Flux without filters
5. **SDXL Turbo Uncensored** - Fast SDXL model
6. **ChilloutMix** - Asian-style uncensored
7. **Deliberate V3** - Versatile uncensored
8. **DreamShaper V8** - High-quality versatile
9. **EpicRealism V5** - Photorealistic
10. **Juggernaut XL V9** - SDXL-based uncensored

## Prerequisites

1. **RunPod Account** with API key
2. **Python 3.9+** installed
3. **Node.js** (for frontend)
4. **Fly.io account** (optional, for hosting)

## Step 1: Set Up RunPod Endpoints

### Automatic Setup (Recommended)

```bash
cd backend
export RUNPOD_API_KEY="your-runpod-api-key"
python scripts/setup_all_models.py
```

This will:
- Create RunPod templates for each model
- Create serverless endpoints for each model
- Save endpoint IDs to `backend/endpoints.json`

### Manual Setup

If you prefer to set up endpoints manually, you can use the existing scripts:
- `scripts/create_runpod_endpoint.py` - Create single endpoint
- `scripts/create_new_endpoint.py` - Alternative endpoint creation

## Step 2: Build and Deploy Workers

### Option A: Use Multi-Model Worker (Recommended)

The multi-model worker (`handler_multi.py`) can handle multiple models dynamically:

```bash
cd backend/worker
docker build -f Dockerfile.multi -t uncensored-multi-worker .
```

Then push to RunPod registry and update your template to use this image.

### Option B: Individual Model Workers

For better isolation, you can create separate workers for each model using `handler.py` with model-specific configurations.

## Step 3: Configure Backend

1. **Set environment variables:**

```bash
export RUNPOD_API_KEY="your-api-key"
export RUNPOD_ENDPOINT_ID="default-endpoint-id"  # Fallback
export PB_URL="https://uncensored-engine-db.fly.dev"
export PB_ADMIN_EMAIL="admin@example.com"
export PB_ADMIN_PASS="your-password"
```

2. **Update endpoint mapping:**

After running `setup_all_models.py`, the `backend/endpoints.json` file will be created. The backend will automatically use this to route requests to the correct endpoint for each model.

## Step 4: Test Models for Uncensored Capability

Run the testing suite to verify which models truly allow adult content:

```bash
cd backend
export RUNPOD_API_KEY="your-api-key"
python scripts/test_model_uncensored.py
```

This will:
- Test each model with explicit prompts
- Identify which models block content
- Generate a report in `backend/uncensored_test_results.json`

## Step 5: Deploy Frontend

The frontend includes a model comparison interface:

```bash
cd frontend
npm install
npm start
```

Or deploy to Fly.io:

```bash
fly deploy
```

## Step 6: Using the Testing Website

1. **Select Models**: Click on model pills to select which models to test
2. **Enter Prompt**: Type your test prompt (or use explicit test prompts)
3. **Generate**: Click "GENERATE" to test all selected models
4. **Compare Results**: View side-by-side comparison in the gallery

### Quick Test Feature

Click the "🧪 TEST ALL MODELS" button to automatically test all selected models with an explicit prompt to verify uncensored capability.

## Model Configuration

Models are configured in `config/models.json`. You can:

- Add new models
- Adjust recommended settings (steps, CFG scale)
- Update HuggingFace model IDs
- Configure test prompts

## Troubleshooting

### Models Not Loading

- Check that HuggingFace model IDs are correct
- Verify RunPod endpoint IDs in `endpoints.json`
- Check RunPod API key and balance

### Censorship Issues

- Some models may have built-in safety checkers
- Use `test_model_uncensored.py` to identify which models are truly uncensored
- Models marked as "very_high" uncensored level are most likely to work

### Endpoint Creation Fails

- Verify RunPod API key has proper permissions
- Check GPU availability (some models need larger GPUs)
- Review RunPod account limits

## Cost Considerations

- **SD 1.5 models**: Can run on smaller GPUs (RTX 3080, ~$0.50/hr)
- **SDXL/Flux models**: Need larger GPUs (RTX 3090/A40, ~$0.70/hr)
- **Serverless endpoints**: Only pay when generating (idle timeout: 5 minutes)

## Next Steps

1. Run the setup script to create all endpoints
2. Test models with `test_model_uncensored.py`
3. Deploy frontend and start testing
4. Compare results to find the best uncensored models for your needs

## Support

For issues or questions:
- Check RunPod logs: `scripts/check_runpod_logs.py`
- Verify endpoint health: `scripts/get_endpoint_health_full.py`
- Check job status: `scripts/check_job_status_v2.py`
