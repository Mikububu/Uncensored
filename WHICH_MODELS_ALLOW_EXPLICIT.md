# Which Models Allow Explicit Language? 🚫➡️✅

## Quick Answer: Best Models for Explicit Content

Based on uncensored level ratings and community testing:

### ✅ **VERY HIGH Uncensored Level** (Most Likely to Work)
These models are specifically designed for uncensored content:

1. **AbyssOrangeMix V3** (`abyssorangemix3`)
   - Anime/hentai style
   - **Very high** uncensored level
   - Model ID: `WarriorMama777/OrangeMixs`
   - ✅ **RECOMMENDED for explicit content**

2. **ChilloutMix** (`chilloutmix`)
   - Asian-style uncensored
   - **Very high** uncensored level
   - Model ID: `Linaqruf/chilloutmix`
   - ✅ **RECOMMENDED for explicit content**

### ✅ **HIGH Uncensored Level** (Should Work)
These models are known to allow explicit content:

3. **Pony Diffusion V6** (`pony-v6`)
   - High-quality uncensored
   - **High** uncensored level
   - Model ID: `PonyDiffusion/Pony-V6`
   - ✅ **Good for explicit content**

4. **Realistic Vision V5** (`realistic-vision-v5`)
   - Photorealistic uncensored
   - **High** uncensored level
   - Model ID: `SG161222/Realistic_Vision_V5.1_noVAE`
   - ✅ **Good for explicit content**

5. **Deliberate V3** (`deliberate-v3`)
   - Versatile uncensored
   - **High** uncensored level
   - Model ID: `XpucT/Deliberate`
   - ✅ **Good for explicit content**

6. **DreamShaper V8** (`dreamshaper-v8`)
   - High-quality versatile
   - **High** uncensored level
   - Model ID: `Lykon/DreamShaper`
   - ✅ **Good for explicit content**

7. **EpicRealism V5** (`epicrealism-v5`)
   - Photorealistic uncensored
   - **High** uncensored level
   - Model ID: `SG161222/EpicRealism`
   - ✅ **Good for explicit content**

8. **Juggernaut XL V9** (`juggernaut-xl-v9`)
   - SDXL-based uncensored
   - **High** uncensored level
   - Model ID: `RunDiffusion/Juggernaut-XL-v9`
   - ✅ **Good for explicit content**

### ⚠️ **MEDIUM Uncensored Level** (May Have Issues)
These models might block some explicit content:

9. **Flux Dev Uncensored** (`flux-dev-uncensored`)
   - Latest Flux model
   - **Medium** uncensored level
   - Model ID: `black-forest-labs/FLUX.1-dev`
   - ⚠️ **May block some explicit prompts**

10. **SDXL Turbo Uncensored** (`sdxl-turbo-uncensored`)
    - Fast SDXL model
    - **Medium** uncensored level
    - Model ID: `stabilityai/sdxl-turbo`
    - ⚠️ **May block some explicit prompts**

## How to Test Which Models Actually Work

### Method 1: Run the Automated Test Script

```bash
cd backend
export RUNPOD_API_KEY="your-api-key"
python scripts/test_model_uncensored.py
```

This will:
- Test each model with explicit prompts
- Identify which models block content
- Generate a report showing which models are truly uncensored

### Method 2: Test on the Website

1. Open the frontend website
2. Select multiple models
3. Enter an explicit test prompt like:
   - `"nude woman, full frontal nudity, explicit, detailed anatomy"`
   - `"explicit sexual content, detailed, high quality"`
   - `"pornographic content, explicit, uncensored"`
4. Click "GENERATE"
5. Compare results - models that block will show errors

### Method 3: Quick Test Script

I've created a simpler test script below that you can run to test specific models.

## Known Issues

### Models That May Censor:
- **Flux models** - Often have built-in safety checkers
- **SDXL Turbo** - May block explicit content
- **Official Stable Diffusion models** - Usually have safety filters

### Models That Usually Work:
- **Pony Diffusion** - Specifically designed for uncensored content
- **AbyssOrangeMix** - Very popular for uncensored anime content
- **ChilloutMix** - Known for uncensored Asian-style content
- **Realistic Vision** - Photorealistic uncensored model

## Recommendations

**For Maximum Uncensored Capability:**
1. Start with **AbyssOrangeMix V3** or **ChilloutMix** (very_high level)
2. If those don't work, try **Pony V6** or **Realistic Vision V5** (high level)
3. Avoid Flux and SDXL Turbo if you need explicit content

**For Testing:**
- Use the test script below to verify which models work with your specific prompts
- Test with progressively more explicit prompts to find the limits

## Safety Checker Disabling

The worker handler (`handler_multi.py`) automatically disables safety checkers:
```python
# Disable safety checker for uncensored models
if hasattr(pipe, 'safety_checker'):
    pipe.safety_checker = None
```

However, some models may still have censorship at the model level (trained into the weights), which can't be disabled.
