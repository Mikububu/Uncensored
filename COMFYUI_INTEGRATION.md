# ComfyUI Integration Guide

ComfyUI is now fully integrated into the project! You can use it in three ways:

## 🎯 Three Ways to Use ComfyUI

### 1. **In Cursor (Simple Browser)**
Open ComfyUI directly in Cursor's built-in browser:

```bash
./scripts/open_comfyui_in_cursor.sh
```

This will:
- Start ComfyUI server on `http://localhost:8188`
- Wait for it to be ready
- Open it in your default browser (you can then open it in Cursor's Simple Browser)

**To open in Cursor:**
1. Run the script above
2. In Cursor, press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
3. Type "Simple Browser: Show"
4. Enter URL: `http://localhost:8188`

### 2. **On the Website (Image Generation)**
Use ComfyUI as a provider for image generation on your website!

**How it works:**
1. Select **"ComfyUI (Local)"** from the model list
2. Enter your prompt
3. Click generate
4. The backend will connect to your local ComfyUI instance and generate the image

**Requirements:**
- ComfyUI must be running locally on `http://localhost:8188`
- Start it with: `python3 scripts/start_comfyui.py`

### 3. **Standalone (Direct Access)**
Just run ComfyUI normally:

```bash
python3 scripts/start_comfyui.py
```

Then open `http://localhost:8188` in any browser.

## 🔧 Backend Integration

The backend now supports ComfyUI as a provider:

```python
# In z_image_worker.py
async def generate_with_comfyui(self, task: dict, input_data: dict) -> dict:
    """Generate image using local ComfyUI instance"""
    # Automatically creates workflow, queues prompt, and polls for results
```

**Features:**
- ✅ Automatic workflow generation
- ✅ Model selection (default: SD 1.5)
- ✅ Customizable width/height/steps/guidance
- ✅ 60-second timeout (same as RunPod)
- ✅ Error handling for connection issues

## 🎨 Frontend Integration

The frontend now includes ComfyUI as a model option:

```javascript
'comfyui-local': { 
    provider: 'comfyui', 
    endpoint_id: null, 
    name: 'ComfyUI (Local)', 
    uncensored_level: 'very_high' 
}
```

**Usage:**
1. The model pill will appear in the model selection
2. Select it like any other model
3. Generate images using your local ComfyUI instance

## 📋 Configuration

### ComfyUI URL
By default, ComfyUI runs on `http://127.0.0.1:8188`. You can change this:

**In the frontend (when creating jobs):**
```javascript
params: {
    provider: 'comfyui',
    comfyui_url: 'http://localhost:8188',  // Optional, defaults to 127.0.0.1:8188
    model_name: 'your-model.safetensors',  // Optional, defaults to SD 1.5
    // ... other params
}
```

### Model Selection
Place your models in `comfyui/models/checkpoints/` and specify them:

```javascript
params: {
    provider: 'comfyui',
    model_name: 'ponyDiffusionV6XL_v6StartWithThisOne.safetensors',
    // ...
}
```

## 🚀 Quick Start

1. **Start ComfyUI:**
   ```bash
   python3 scripts/start_comfyui.py
   ```

2. **Download Models** (optional):
   - Place `.safetensors` or `.ckpt` files in `comfyui/models/checkpoints/`
   - Or use the ComfyUI Manager in the web UI

3. **Use on Website:**
   - Open your website
   - Select "ComfyUI (Local)" model
   - Generate images!

4. **Or Use in Cursor:**
   ```bash
   ./scripts/open_comfyui_in_cursor.sh
   ```

## 🔍 Troubleshooting

### "Cannot connect to ComfyUI"
- Make sure ComfyUI is running: `python3 scripts/start_comfyui.py`
- Check the URL is correct (default: `http://127.0.0.1:8188`)
- Verify ComfyUI is accessible: `curl http://localhost:8188`

### "ComfyUI generation timed out"
- Check ComfyUI logs for errors
- Try a smaller image size (512x512 instead of 1024x1024)
- Reduce steps (20 instead of 30)
- Make sure you have a model installed

### Model Not Found
- Place models in `comfyui/models/checkpoints/`
- Use the exact filename (case-sensitive)
- Check ComfyUI console for model loading errors

## 📝 Example Workflow

The backend automatically creates this workflow structure:

```
CheckpointLoaderSimple → CLIPTextEncode (positive) → KSampler
                     ↓                              ↓
                     CLIPTextEncode (negative)     EmptyLatentImage
                                                   ↓
                                              VAEDecode → SaveImage
```

You can customize this by modifying `_get_comfy_workflow()` in `z_image_worker.py`.

## 🎯 Benefits

1. **Local Processing**: No API costs, no rate limits
2. **Full Control**: Use any model, any workflow
3. **Privacy**: Everything runs locally
4. **Uncensored**: No content filters (if your models are uncensored)
5. **Fast**: Direct connection, no network latency

## 🔄 Next Steps

- **Custom Workflows**: Modify `_get_comfy_workflow()` for advanced workflows
- **Model Management**: Use ComfyUI Manager to download models
- **Custom Nodes**: Install extensions for more features
- **Workflow Templates**: Save and reuse complex workflows

Enjoy using ComfyUI! 🎨
