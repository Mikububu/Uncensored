# Timeout Settings - 1 Minute Limit

## Current Configuration

All image generation is now limited to **60 seconds (1 minute)** maximum.

### Backend Timeout
- **Location**: `backend/z_image_worker.py`
- **Setting**: `max_wait = 60` seconds
- **Behavior**: If a job takes longer than 60 seconds, it's marked as failed with a timeout error

### Frontend Polling
- **Location**: `frontend/index.html`
- **Polling Interval**: Every 3 seconds
- **Timeout Display**: Shows "60 seconds" in logs

## What Happens on Timeout

If generation takes longer than 1 minute:
1. Backend stops polling
2. Job is marked as `failed` with error: "Image generation timed out after 60 seconds"
3. Frontend shows the error in the history sidebar
4. User can try again with a faster model or lower resolution

## Recommendations for Fast Generation

To stay under 1 minute:
- Use **fewer steps** (10-15 steps instead of 25-30)
- Use **lower resolution** (512x512 instead of 1024x1024)
- Use **turbo models** (SDXL Turbo, Flux Dev) which are faster
- Avoid **cold starts** (keep endpoints warm)

## Models That Should Work Under 1 Minute

- **SDXL Turbo** - 4 steps, very fast
- **Flux Dev** - Optimized for speed
- **SD 1.5 models** - Generally faster than SDXL
- **Pony V6** - Well optimized

## Models That May Timeout

- **High-step SDXL models** (30+ steps)
- **Large resolution** (1024x1024+)
- **Cold start** (first request after idle)
