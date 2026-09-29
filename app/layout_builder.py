def build_comic_layout(outline: list, image_paths: list, story_text: str):
    """Combines outline items, image assets, and scripts into a clean schema.
    
    Args:
        outline: List of panel outline dictionaries
        image_paths: List of paths to generated images
        story_text: The generated narrative text
        
    Returns:
        List of panel dictionaries with all content combined
    """
    layout = []
    
    for i, panel in enumerate(outline):
        # Get image path for this panel
        img_path = image_paths[i] if i < len(image_paths) else ""
        
        # Create panel layout
        panel_layout = {
            "panel_number": panel.get("panel_number", i + 1),
            "title": panel.get("title", f"Panel {i + 1}"),
            "image_path": img_path,
            "scene_description": panel.get("scene_description", ""),
            "narration": story_text if isinstance(story_text, str) else str(story_text),
            "image_prompt": panel.get("image_prompt", f"Comic panel {i + 1}")
        }
        
        layout.append(panel_layout)
    
    return layout
