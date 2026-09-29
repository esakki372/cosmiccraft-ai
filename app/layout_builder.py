def build_comic_layout(outline: str, image_paths: list, story_text: str):
    """Combines outline items, image assets, and scripts into a clean schema.
    
    Args:
        outline: Panel outline string
        image_paths: List of paths to generated images
        story_text: The generated narrative text
        
    Returns:
        List of panel dictionaries with all content combined
    """
    layout = []
    
    num_panels = min(4, len(image_paths))
    
    for i in range(num_panels):
        panel_layout = {
            "panel_number": i + 1,
            "title": f"Panel {i + 1}",
            "image_path": image_paths[i] if i < len(image_paths) else "",
            "scene_description": outline if i == 0 else f"Panel {i+1} continuation",
            "narration": story_text,
            "image_prompt": f"Comic panel {i + 1}"
        }
        layout.append(panel_layout)
    
    return layout
