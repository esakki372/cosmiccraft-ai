def build_comic_layout(outline: list, image_paths: list, story_text: str):
    """Combines outline items, image assets, and scripts into a clean schema."""
    layout = []
    for i, panel in enumerate(outline):
        layout.append({
            "panel_number": panel.get("panel_number", i+1),
            "title": panel.get("title", f"Panel {i+1}"),
            "image_path": image_paths[i] if i < len(image_paths) else "",
            "scene_description": panel.get("scene_description", ""),
            "narration": story_text,
            "image_prompt": panel.get("image_prompt", "")
        })
    return layout