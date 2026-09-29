import os
import torch
from PIL import Image, ImageDraw, ImageFont
import random

# Graceful loading of Stable Diffusion with CPU/GPU fallback handling
MODEL_ID = "runwayml/stable-diffusion-v1-5"
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32

# Note: Stable Diffusion model loading is disabled for Render deployment
# to avoid memory and storage constraints. Model is ~4GB and requires significant resources.
# For production use with image generation, consider using an API service like:
# - Stability AI API
# - Replicate API
# - OpenAI DALL-E API

pipe = None
try:
    # Only attempt to load model if in local development (not Render)
    if os.getenv("ENVIRONMENT") != "render" and os.getenv("RENDER") is None:
        from diffusers import StableDiffusionPipeline
        pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID, torch_dtype=dtype)
        pipe = pipe.to(device)
except Exception as e:
    print(f"Note: Stable Diffusion model not loaded: {str(e)}")
    print("Falling back to placeholder image generation.")
    pass

def generate_placeholder_image(prompt: str, panel_num: int) -> Image.Image:
    """Generate a styled placeholder image with text overlay"""
    # Color palette for variety
    colors = [
        (52, 73, 94),    # Dark blue
        (44, 62, 80),    # Darker blue
        (142, 68, 173),  # Purple
        (155, 89, 182),  # Light purple
        (52, 152, 219),  # Bright blue
        (26, 188, 156),  # Teal
    ]
    
    bg_color = random.choice(colors)
    img = Image.new('RGB', (512, 512), color=bg_color)
    
    # Add text overlay with prompt
    try:
        draw = ImageDraw.Draw(img)
        # Draw panel number
        text = f"Panel {panel_num}"
        draw.text((20, 20), text, fill=(255, 255, 255))
        
        # Draw prompt (truncated)
        prompt_short = prompt[:50] + "..." if len(prompt) > 50 else prompt
        draw.text((20, 480), prompt_short, fill=(200, 200, 200))
    except Exception:
        pass  # If font rendering fails, just skip text
    
    return img

def generate_image(prompt: str, panel_num: int) -> str:
    """Generates an image via Stable Diffusion or creates a styled placeholder.
    
    On Render/limited environments, generates placeholder images only.
    For full image generation, deploy with sufficient resources or use an API service.
    
    Args:
        prompt: The text prompt describing the image
        panel_num: The panel number for naming
        
    Returns:
        Path to the generated image file
    """
    os.makedirs("static/panels", exist_ok=True)
    filename = f"static/panels/panel_{panel_num}_{os.urandom(4).hex()}.png"
    
    if pipe is not None:
        try:
            image = pipe(prompt, num_inference_steps=20).images[0]
            image.save(filename)
            return filename
        except Exception as e:
            print(f"Error generating image with model: {str(e)}")
    
    # Fallback: Generate styled placeholder
    try:
        img = generate_placeholder_image(prompt, panel_num)
        img.save(filename)
        return filename
    except Exception as e:
        print(f"Error generating placeholder: {str(e)}")
        # Last resort: plain colored image
        img = Image.new('RGB', (512, 512), color=(52, 73, 94))
        img.save(filename)
        return filename
