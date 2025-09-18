# models/furniture_lib.py

import trimesh

FURNITURE_LIBRARY = {
    "desk": {
        "size": (5.0, 2.5, 2.5),  # L x W x H (feet)
        "mesh": trimesh.creation.box(extents=[5.0, 2.5, 2.5])
    },
    "chair": {
        "size": (2.0, 2.0, 3.0),
        "mesh": trimesh.creation.box(extents=[2.0, 2.0, 3.0])
    },
    "sofa": {
        "size": (7.0, 3.0, 2.5),
        "mesh": trimesh.creation.box(extents=[7.0, 3.0, 2.5])
    },
    "table": {
        "size": (4.0, 4.0, 2.8),
        "mesh": trimesh.creation.box(extents=[4.0, 4.0, 2.8])
    }
}

def get_furniture_mesh(name):
    if name in FURNITURE_LIBRARY:
        # Return a COPY so we can transform it
        return FURNITURE_LIBRARY[name]["mesh"].copy()
    else:
        print(f"⚠️ Furniture '{name}' not found in library")
        return None