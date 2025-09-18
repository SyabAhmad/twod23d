# config.py

import os

# Paths
INPUT_DWG_PATH = "input/Drawing1.dwg"
INPUT_DXF_PATH = "input/Drawing1.dxf"
OUTPUT_DIR = "output/"
OUTPUT_FORMAT = "glb"  # or "obj"

# Dimensions
WALL_HEIGHT = 10.0      # feet
WALL_THICKNESS = 0.5    # feet
FLOOR_THICKNESS = 0.5   # if you add floor

# Layers (match your AutoCAD layer names)
LAYER_WALLS = "WALLS"
LAYER_FURNITURE = "FURNITURE"
LAYER_DOORS = "DOORS"
LAYER_WINDOWS = "WINDOWS"

# 3D asset library (put .glb/.obj files here)
ASSETS_DIR = "assets"
ASSET_UNIT = "m"  # units used by your assets: m|cm|mm|in|ft
# Example names we’ll try to match (you can change file names to what you have)
ASSET_KEYWORDS = {
    "single door": "door_single.glb",
    "double door": "door_double.glb",
    "doube door": "door_double.glb",
    "chair": "chair.glb",
    "desk": "desk.glb",
    "table": "table.glb",
    "sofa": "sofa.glb",
    "plant": "plant.glb",
    "copy machine": "printer.glb",
    "phone": "phone.glb",
    "workstation": "workstation.glb",
    "call center disk 2": "workstation_cluster.glb",
}

# Ensure output dir exists
os.makedirs(OUTPUT_DIR, exist_ok=True)