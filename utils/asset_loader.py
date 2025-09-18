import os
import trimesh

_ASSET_CACHE = {}
_FEET_PER = {'m': 3.280839895, 'cm': 0.03280839895, 'mm': 0.003280839895, 'in': 1/12.0, 'ft': 1.0}

def load_asset_mesh(path: str):
    ap = os.path.abspath(path)
    if ap in _ASSET_CACHE:
        return _ASSET_CACHE[ap].copy()
    if not os.path.exists(ap):
        return None
    mesh = trimesh.load(ap, force='mesh')  # scene -> single mesh with transforms
    _ASSET_CACHE[ap] = mesh
    return mesh.copy()

def scale_asset_to_doc(mesh: trimesh.Trimesh, unit_scale_doc_per_ft: float, asset_unit: str = 'm'):
    feet_per_unit = _FEET_PER.get(asset_unit.lower(), 1.0)
    factor = unit_scale_doc_per_ft * feet_per_unit
    mesh.apply_scale(factor)
    return mesh