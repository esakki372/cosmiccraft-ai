import os
import torch
from PIL import Image

# Graceful loading of Stable Diffusion with CPU/GPU fallback handling
MODEL_ID = "runwayml/stable-diffusion-v1-5"
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32

pipe = None
try:
    from diffusers import StableDiffusionPipeline
    pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID, torch_dtype=dtype)
    pipe = pipe.to(device)
except Exception:
    pass  # Falls back to simulated placeholder generation if weights/hardware are unavailable

def generate_image(prompt: str, panel_num: int) -> str:
    """Generates an image via Stable Diffusion or creates a styled placeholder."""
    os.makedirs("static/panels", exist_ok=True)
    filename = f"static/panels/panel_{panel_num}_{os.urandom(4).hex()}.png"
    
    if pipe is not None:
        try:
            image = pipe(prompt, num_inference_steps=20).images[0]
            image.save(filename)
            return filename
        except Exception:
            pass
            
    # Fallback image renderer
    img = Image.new('RGB', (512, 512), color=(52, 73, 94))
    img.save(filename)
    return filename