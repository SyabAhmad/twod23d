# utils/mesh_utils.py

import trimesh

def create_box_at(position, size, color=None):
    """Create a colored box at position"""
    mesh = trimesh.creation.box(extents=size)
    mesh.apply_translation(position)
    if color:
        mesh.visual.face_colors = color
    return mesh