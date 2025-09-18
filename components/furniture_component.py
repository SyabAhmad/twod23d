# components/furniture_component.py
import math
import os
import numpy as np
import trimesh
from models.furniture_lib import get_furniture_mesh
from utils.asset_loader import load_asset_mesh, scale_asset_to_doc
from config import ASSETS_DIR, ASSET_UNIT, ASSET_KEYWORDS

def _pick_asset(block_name: str):
    name = block_name.lower()
    # longest-keyword first
    for kw in sorted(ASSET_KEYWORDS.keys(), key=len, reverse=True):
        if kw in name:
            return os.path.join(ASSETS_DIR, ASSET_KEYWORDS[kw])
    return None

def process_furniture(msp, unit_scale):
    inserts = list(msp.query('INSERT'))
    meshes = []
    for entity in inserts:
        block_name = str(entity.dxf.name or "").lower()

        # Try to load a real asset by keyword
        asset_path = _pick_asset(block_name)
        if asset_path:
            mesh = load_asset_mesh(asset_path)
            if mesh is not None:
                scale_asset_to_doc(mesh, unit_scale, ASSET_UNIT)
            else:
                mesh = None
                print(f"⚠️ Asset not found for '{block_name}': {asset_path}")
        else:
            mesh = None

        # Fallback to simple library proxies if we didn’t load an asset
        if mesh is None:
            if "phone" in block_name:
                mesh = get_furniture_mesh("phone")
            elif "printer" in block_name or "copy machine" in block_name:
                mesh = get_furniture_mesh("printer")
            elif "desk" in block_name:
                mesh = get_furniture_mesh("desk")
            elif ("chair" in block_name) or ("seat" in block_name):
                mesh = get_furniture_mesh("chair")
            elif "sofa" in block_name:
                mesh = get_furniture_mesh("sofa")
            elif ("table" in block_name) or ("workstation" in block_name):
                mesh = get_furniture_mesh("table")
            else:
                mesh = trimesh.creation.box(extents=[2.0, 2.0, 3.0])  # ft
            mesh.apply_scale(unit_scale)

        # Block non-uniform scale
        sx = float(getattr(entity.dxf, 'xscale', 1.0))
        sy = float(getattr(entity.dxf, 'yscale', 1.0))
        sz = float(getattr(entity.dxf, 'zscale', 1.0))
        S = np.eye(4); S[0,0], S[1,1], S[2,2] = sx, sy, sz
        mesh.apply_transform(S)

        # Rotation about Z
        rot_deg = float(getattr(entity.dxf, 'rotation', 0.0))
        Rz = trimesh.transformations.rotation_matrix(math.radians(rot_deg), [0, 0, 1])
        mesh.apply_transform(Rz)

        # Place on floor and move to insert
        z_half = mesh.extents[2] / 2.0
        insert = entity.dxf.insert
        mesh.apply_translation([0, 0, z_half])
        mesh.apply_translation([insert.x, insert.y, 0.0])

        meshes.append(mesh)
        print(f"🪑 {block_name} at ({insert.x:.2f}, {insert.y:.2f}) rot {rot_deg:.1f}°")

    print(f"🪑 Created {len(meshes)} furniture meshes")
    return meshes