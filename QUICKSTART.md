# Quick Start: Uncensored Image Models Testing Platform

Get up and running in 5 minutes!

## 1. Set Your RunPod API Key

```bash
export RUNPOD_API_KEY="your-runpod-api-key-here"
```

## 2. Set Up All Model Endpoints (One Command)

```bash
cd backend
python scripts/setup_all_models.py
```

This creates RunPod endpoints for all 10+ uncensored models. Wait 2-3 minutes for completion.

## 3. Test Which Models Are Truly Uncensored

```bash
python scripts/test_model_uncensored.py
```

This tests each model with explicit prompts and tells you which ones actually work.

## 4. Start the Frontend Testing Website

```bash
cd ../frontend
npm install
npm start
```

Open http://localhost:8080 in your browser.

## 5. Test Models on the Website

1. Select multiple models by clicking the model pills
2. Enter an explicit test prompt (or click "🧪 TEST ALL MODELS")
3. Click "GENERATE"
4. Compare results side-by-side in the gallery

## What You Get

✅ **10+ Uncensored Models** ready to test
✅ **Automatic Endpoint Setup** - no manual configuration needed
✅ **Side-by-Side Comparison** - test multiple models at once
✅ **Uncensored Verification** - know which models actually work
✅ **Beautiful Testing UI** - easy to use interface

## Models Included

- Pony V6 (High uncensored level)
- AbyssOrangeMix V3 (Very high)
- Realistic Vision V5 (High)
- Flux Dev Uncensored (Medium)
- SDXL Turbo (Medium)
- ChilloutMix (Very high)
- Deliberate V3 (High)
- DreamShaper V8 (High)
- EpicRealism V5 (High)
- Juggernaut XL V9 (High)

## Troubleshooting

**Endpoints not created?**
- Check your RunPod API key
- Verify you have RunPod credits
- Check RunPod account permissions

**Models not generating?**
- Run `test_model_uncensored.py` to see which models work
- Check endpoint IDs in `backend/endpoints.json`
- Verify RunPod balance

**Frontend not loading?**
- Make sure backend is running
- Check PocketBase connection
- Verify environment variables

## Next Steps

See `SETUP_GUIDE.md` for detailed documentation and advanced configuration.
