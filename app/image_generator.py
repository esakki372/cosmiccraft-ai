import os
from PIL import Image
import random

def generate_placeholder_image(prompt: str, panel_num: int) -> str:
    """Generate a styled placeholder image"""
    colors = [
        (52, 73, 94),
        (44, 62, 80),
        (142, 68, 173),
        (155, 89, 182),
        (52, 152, 219),
        (26, 188, 156),
    ]
    
    os.makedirs("static/panels", exist_ok=True)
    filename = f"static/panels/panel_{panel_num}_{os.urandom(4).hex()}.png"
    
    bg_color = random.choice(colors)
    img = Image.new('RGB', (512, 512), color=bg_color)
    
    try:
        img.save(filename)
    except Exception as e:
        print(f"Error saving image: {e}")
    
    return filename

def generate_image(prompt: str, panel_num: int) -> str:
    """Generates a placeholder image.
    
    Args:
        prompt: The text prompt describing the image
        panel_num: The panel number for naming
        
    Returns:
        Path to the generated image file
    """
    return generate_placeholder_image(prompt, panel_num)
