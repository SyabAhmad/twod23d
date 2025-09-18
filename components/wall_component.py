# components/wall_component.py

import trimesh
import numpy as np
from config import *

def create_wall_mesh(start, end, unit_scale, height_ft=WALL_HEIGHT, thickness_ft=WALL_THICKNESS):
    """Create a 3D wall mesh from 2D line using feet-based dims scaled to DXF units"""
    dx = end.x - start.x
    dy = end.y - start.y
    length = float(np.hypot(dx, dy))
    if length <= 0:
        return None

    height = height_ft * unit_scale
    thickness = thickness_ft * unit_scale

    # Create box: [length, thickness, height] in DOC units
    mesh = trimesh.creation.box(extents=[length, thickness, height])

    # Rotate to align with wall direction around Z
    angle = float(np.arctan2(dy, dx))
    Rz = trimesh.transformations.rotation_matrix(angle, [0, 0, 1])
    mesh.apply_transform(Rz)

    # Move to midpoint and lift by half height
    mesh.apply_translation([start.x + dx/2.0, start.y + dy/2.0, height/2.0])

    # Slight color to distinguish
    mesh.visual.face_colors = [220, 220, 230, 255]
    return mesh

def process_walls(msp, unit_scale):
    """Process LINE and LWPOLYLINE as walls (no layer requirement for now)"""
    line_entities = list(msp.query('LINE'))
    polyline_entities = list(msp.query('LWPOLYLINE'))
    wall_entities = line_entities + polyline_entities

    meshes = []
    for entity in wall_entities:
        if entity.dxftype() == 'LINE':
            start = entity.dxf.start
            end = entity.dxf.end
            wall_mesh = create_wall_mesh(start, end, unit_scale)
            if wall_mesh:
                meshes.append(wall_mesh)
        elif entity.dxftype() == 'LWPOLYLINE':
            # get_points returns tuples; first two are x,y
            pts = entity.get_points()
            for i in range(len(pts) - 1):
                sx, sy = pts[i][0], pts[i][1]
                ex, ey = pts[i+1][0], pts[i+1][1]
                start = type('P', (), {'x': sx, 'y': sy})
                end = type('P', (), {'x': ex, 'y': ey})
                wall_mesh = create_wall_mesh(start, end, unit_scale)
                if wall_mesh:
                    meshes.append(wall_mesh)

    print(f"🏗️ Created {len(meshes)} wall meshes")
    return meshes