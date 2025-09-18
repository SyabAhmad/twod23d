# main.py (updated)

import os
from utils.dwg_converter import convert_dwg_to_dxf
from utils.dxf_loader import load_dxf
from utils.units import feet_to_doc_scale
from components.wall_component import process_walls
from components.furniture_component import process_furniture
from components.room_component import create_floor
from config import *
from config import INPUT_DXF_PATH
import trimesh

def main():
    print("🚀 Starting AutoCAD 2D → 3D Converter...")

    # Choose input: prefer DWG if provided, else DXF
    input_path = INPUT_DWG_PATH if INPUT_DWG_PATH.lower().endswith('.dwg') else INPUT_DXF_PATH

    if input_path.lower().endswith('.dwg'):
        print(f"📥 Detected .dwg file: {input_path}")
        dxf_path = convert_dwg_to_dxf(input_path, OUTPUT_DIR)
        if not dxf_path:
            print("❌ Failed to convert DWG to DXF. Exiting.")
            return
        input_path = dxf_path
    else:
        print(f"📥 Using DXF file: {input_path}")

    # Load DXF
    doc, msp = load_dxf(input_path)
    if not msp:
        return

    # Units detection
    unit_scale, unit_name = feet_to_doc_scale(doc)
    print(f"📏 DXF units: {unit_name} | scaling feet→DXF by {unit_scale}")

    # Optional quick peek
    print("🔍 === ALL LAYERS ===")
    for layer in doc.layers:
        print(f" - {layer.dxf.name}")
    print("\n🔍 === SAMPLE ENTITIES (first 10) ===")
    for i, e in enumerate(msp):
        if i >= 10:
            break
        print(f" - {e.dxftype()} on layer '{e.dxf.layer}'")

    all_meshes = []

    # Add floor
    floor_mesh = create_floor(msp, unit_scale)
    if floor_mesh:
        all_meshes.append(floor_mesh)

    # Process walls
    wall_meshes = process_walls(msp, unit_scale)
    all_meshes.extend(wall_meshes)

    # Process furniture (with rotation/scale)
    furniture_meshes = process_furniture(msp, unit_scale)
    all_meshes.extend(furniture_meshes)

    if not all_meshes:
        print("❌ No meshes created. Check layer names and DXF structure.")
        return

    # Combine into scene
    scene = trimesh.Scene(all_meshes)
    print(f"✅ Combined {len(all_meshes)} meshes into scene")

    # Export
    output_path = os.path.join(OUTPUT_DIR, f"output_model.{OUTPUT_FORMAT}")
    scene.export(output_path)
    print(f"💾 Saved 3D model to: {output_path}")

if __name__ == "__main__":
    main()