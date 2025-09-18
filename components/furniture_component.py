# components/furniture_component.py

from models.furniture_lib import get_furniture_mesh
from config import *

def process_furniture(msp):
    """Process INSERT blocks by name (ignores layer)"""
    furniture_keywords = ["desk", "chair", "table", "sofa", "pc", "workstation", "seat", "cubicle"]

    furniture_entities = []
    for entity in msp.query('INSERT'):
        block_name = entity.dxf.name.lower()
        if any(kw in block_name for kw in furniture_keywords):
            furniture_entities.append(entity)

    meshes = []
    for entity in furniture_entities:
        block_name = entity.dxf.name.lower()
        mesh = None

        if "desk" in block_name:
            mesh = get_furniture_mesh("desk")
        elif "chair" in block_name:
            mesh = get_furniture_mesh("chair")
        elif "sofa" in block_name:
            mesh = get_furniture_mesh("sofa")
        elif "table" in block_name:
            mesh = get_furniture_mesh("table")

        if mesh:
            insert_point = entity.dxf.insert
            # Get height (Z-axis) = max_z - min_z
            height = mesh.extents[1][2] - mesh.extents[0][2]
            mesh.apply_translation([insert_point.x, insert_point.y, height / 2])
            meshes.append(mesh)
            print(f"🪑 Placed {block_name} at ({insert_point.x:.1f}, {insert_point.y:.1f})")

    print(f"🪑 Created {len(meshes)} furniture meshes")
    return meshes