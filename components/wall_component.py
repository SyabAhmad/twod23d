# components/wall_component.py

import trimesh
import numpy as np
from utils.mesh_utils import create_box_at
from config import *

def create_wall_mesh(start, end, height=WALL_HEIGHT, thickness=WALL_THICKNESS):
    """Create a 3D wall mesh from 2D line (start to end)"""
    dx = end.x - start.x
    dy = end.y - start.y
    length = np.sqrt(dx*dx + dy*dy)
    if length == 0:
        return None

    # Create box: [length, thickness, height]
    mesh = trimesh.creation.box(extents=[length, thickness, height])

    # Rotate to align with wall direction
    angle = np.arctan2(dy, dx)
    rotation_matrix = trimesh.transformations.rotation_matrix(
        angle=angle,
        direction=[0, 0, 1],  # rotate around Z-axis
        point=[0, 0, 0]
    )
    mesh.apply_transform(rotation_matrix)

    # Move to start position
    mesh.apply_translation([start.x + dx/2, start.y + dy/2, height/2])

    return mesh

def process_walls(msp):
    """Process all LINE and LWPOLYLINE entities as walls (ignores layer)"""
    line_entities = list(msp.query('LINE'))
    polyline_entities = list(msp.query('LWPOLYLINE'))
    wall_entities = line_entities + polyline_entities

    meshes = []
    for entity in wall_entities:
        if entity.dxftype() == 'LINE':
            start = entity.dxf.start
            end = entity.dxf.end
            wall_mesh = create_wall_mesh(start, end)
            if wall_mesh:
                meshes.append(wall_mesh)
        elif entity.dxftype() == 'LWPOLYLINE':
            points = entity.get_points()
            for i in range(len(points) - 1):
                start = points[i]
                end = points[i+1]
                start_3d = (start[0], start[1], 0)
                end_3d = (end[0], end[1], 0)
                wall_mesh = create_wall_mesh(
                    type('Point', (), {'x': start_3d[0], 'y': start_3d[1]}),
                    type('Point', (), {'x': end_3d[0], 'y': end_3d[1]})
                )
                if wall_mesh:
                    meshes.append(wall_mesh)

    print(f"🏗️ Created {len(meshes)} wall meshes")
    return meshes