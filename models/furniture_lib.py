import trimesh
from .procedural_assets import (
    make_chair, make_desk, make_table, make_sofa,
    make_printer, make_plant, make_door_single, make_door_double
)

# Sizes are implicit in the procedural builders (feet)
FURN_MAP = {
    "desk": make_desk,
    "chair": make_chair,
    "sofa": make_sofa,
    "table": make_table,
    "printer": make_printer,
    "plant": make_plant,
    "door_single": make_door_single,
    "door_double": make_door_double,
}

def get_furniture_mesh(name: str):
    key = name.lower()
    if key in FURN_MAP:
        return FURN_MAP[key]()
    # fallbacks by heuristic
    if "single door" in key or "door_single" in key:
        return make_door_single()
    if "double door" in key or "door_double" in key:
        return make_door_double()
    if "chair" in key or "seat" in key:
        return make_chair()
    if "desk" in key:
        return make_desk()
    if "table" in key or "workstation" in key:
        return make_table()
    if "sofa" in key or "couch" in key:
        return make_sofa()
    if "plant" in key:
        return make_plant()
    if "printer" in key or "copy machine" in key:
        return make_printer()
    # generic small box
    return trimesh.creation.box(extents=[2.0, 2.0, 3.0])