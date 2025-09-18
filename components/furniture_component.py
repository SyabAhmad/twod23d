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

            # ✅ SAFETY CHECK: Ensure mesh.extents is valid
            try:
                # Get height from Z-axis: max_z - min_z
                min_z = mesh.bounds[0][2]  # [min_x, min_y, min_z]
                max_z = mesh.bounds[1][2]  # [max_x, max_y, max_z]
                height = max_z - min_z
                mesh.apply_translation([insert_point.x, insert_point.y, height / 2])
                meshes.append(mesh)
                print(f"🪑 Placed {block_name} at ({insert_point.x:.1f}, {insert_point.y:.1f})")
            except Exception as e:
                print(f"⚠️ Failed to place furniture '{block_name}': {e}")
                continue

    print(f"🪑 Created {len(meshes)} furniture meshes")
    return meshes