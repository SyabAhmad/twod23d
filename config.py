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

# Ensure output dir exists
os.makedirs(OUTPUT_DIR, exist_ok=True)