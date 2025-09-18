# components/room_component.py

import trimesh
import numpy as np
from config import *

def create_floor(msp, bounds=None):
    """Create a floor mesh covering the entire plan or given bounds"""
    if bounds is None:
        # Auto-calculate bounds from entities
        all_points = []
        for entity in msp:
            if hasattr(entity, 'dxf') and hasattr(entity.dxf, 'start'):
                all_points.append((entity.dxf.start.x, entity.dxf.start.y))
            if hasattr(entity, 'get_points'):
                pts = entity.get_points()
                for p in pts:
                    all_points.append((p[0], p[1]))

        if not all_points:
            return None

        xs = [p[0] for p in all_points]
        ys = [p[1] for p in all_points]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
    else:
        min_x, min_y, max_x, max_y = bounds

    width = max_x - min_x
    depth = max_y - min_y

    floor_mesh = trimesh.creation.box(extents=[width, depth, FLOOR_THICKNESS])
    floor_mesh.apply_translation([
        min_x + width/2,
        min_y + depth/2,
        -FLOOR_THICKNESS/2  # sits at z=0
    ])
    floor_mesh.visual.face_colors = [150, 150, 150, 255]  # gray floor

    print(f"🪵 Created floor: {width:.1f} x {depth:.1f} ft")
    return floor_mesh