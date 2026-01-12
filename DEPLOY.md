# Deployment Guide - ComfyUI Integration

## 🚀 Quick Deploy

I've prepared everything! Just run these commands:

```bash
cd "/Users/michaelperinwogenburg/Desktop/big challenge/Uncensored"

# Add all changes
git add .

# Commit
git commit -m "Add ComfyUI integration for all models"

# Push to GitHub
git push origin main
```

That's it! GitHub Actions will automatically:
1. Build the ComfyUI Docker image
2. Push to GitHub Container Registry
3. Make it available at: `ghcr.io/YOUR_USERNAME/uncensored-comfyui-worker:latest`

## 📋 What Gets Deployed

### New Files:
- `backend/worker/Dockerfile.multi` - ComfyUI worker image
- `backend/worker/handler_multi.py` - ComfyUI handler
- `backend/.github/workflows/build-comfyui-worker.yml` - CI/CD workflow
- `comfyui/` - ComfyUI installation
- `scripts/start_comfyui.py` - Local ComfyUI starter

### Updated Files:
- `backend/z_image_worker.py` - ComfyUI integration
- `frontend/index.html` - ComfyUI (Local) model option

## 🎯 After Push

1. **Check GitHub Actions:**
   - Go to: https://github.com/YOUR_USERNAME/YOUR_REPO/actions
   - Watch "Build ComfyUI Worker" workflow
   - Wait for it to complete (~5-10 minutes)

2. **Get Image URL:**
   - Image will be at: `ghcr.io/YOUR_USERNAME/uncensored-comfyui-worker:latest`
   - Or check: https://github.com/YOUR_USERNAME/YOUR_REPO/pkgs/container/uncensored-comfyui-worker

3. **Update RunPod:**
   - Go to RunPod Console → Templates
   - Create new template
   - Image: `ghcr.io/YOUR_USERNAME/uncensored-comfyui-worker:latest`
   - Container disk: 50GB+
   - Update endpoints to use new template

## ✅ That's It!

Once the image is built and you update RunPod templates, all models will use ComfyUI automatically!
