import runpod
import torch
from diffusers import ZImagePipeline
import base64
from io import BytesIO

# Load model globally for warm starts
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32

pipe = ZImagePipeline.from_pretrained(
    "Tongyi-MAI/Z-Image-Turbo",
    torch_dtype=dtype
)
pipe.to(device)

def handler(event):
    """
    RunPod serverless handler for Z-Image-Turbo
    """
    input_data = event.get("input", {})
    prompt = input_data.get("prompt")
    
    if not prompt:
        return {"error": "No prompt provided"}

    # Recommended parameters for Turbo
    image = pipe(
        prompt=prompt,
        height=input_data.get("height", 1024),
        width=input_data.get("width", 1024),
        num_inference_steps=input_data.get("num_inference_steps", 9),
        guidance_scale=0.0
    ).images[0]

    # Convert to base64 for direct return or upload to bucket (S3/RunPod)
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return f"data:image/png;base64,{img_str}"

runpod.serverless.start({"handler": handler})
