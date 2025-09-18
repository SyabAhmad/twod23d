# utils/dwg_converter.py

import os
import subprocess
import sys
from config import INPUT_DXF_PATH

# ⚙️ CONFIGURE THIS PATH TO WHERE YOU EXTRACTED ODA CONVERTER
ODA_CONVERTER_PATH = r"C:\Program Files\ODA\ODAFileConverter 26.8.0\OdaFileConverter.exe"
def convert_dwg_to_dxf(dwg_path, output_dir=None):
    """
    Convert .dwg file to .dxf using ODA File Converter.
    Returns path to generated .dxf file.
    """
    if not os.path.exists(ODA_CONVERTER_PATH):
        print(f"❌ ODA File Converter not found at: {ODA_CONVERTER_PATH}")
        sys.exit(1)

    if not dwg_path.lower().endswith('.dwg'):
        print("❌ Input file is not a .dwg")
        return None

    # ✅ Use absolute paths
    dwg_abs = os.path.abspath(dwg_path)
    input_dir = os.path.dirname(dwg_abs)
    filename = os.path.basename(dwg_abs)

    if not os.path.exists(input_dir):
        print(f"❌ Input folder does not exist: {input_dir}")
        return None

    if output_dir is None:
        output_dir = os.path.dirname(dwg_abs)  # same as input dir
    output_dir = os.path.abspath(output_dir)

    # Create output dir if missing
    os.makedirs(output_dir, exist_ok=True)

    # Output DXF path
    dxf_filename = os.path.splitext(filename)[0] + ".dxf"
    dxf_path = os.path.join(output_dir, dxf_filename)

    # If DXF already exists, skip
    if os.path.exists(dxf_path):
        print(f"✅ DXF already exists: {dxf_path}")
        return dxf_path

    print(f"🔄 Converting {dwg_abs} → {dxf_path}...")

    # Build command with absolute paths
    cmd = [
        ODA_CONVERTER_PATH,
        input_dir,          # Input folder (absolute)
        output_dir,         # Output folder (absolute)
        "ACAD2018",         # Output version
        "DXF",              # Output type
        "0",                # Recurse? no
        "0"                 # Audit? no
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=input_dir)

        if result.returncode == 0 and os.path.exists(dxf_path):
            print(f"✅ Successfully converted to: {dxf_path}")
            return dxf_path
        else:
            print(f"❌ Conversion failed: {result.stderr}")
            return None

    except Exception as e:
        print(f"❌ Error running ODA converter: {e}")
        return None
    """
    Convert .dwg file to .dxf using ODA File Converter.
    Returns path to generated .dxf file.
    """
    if not os.path.exists(ODA_CONVERTER_PATH):
        print(f"❌ ODA File Converter not found at: {ODA_CONVERTER_PATH}")
        print("👉 Download from: https://www.opendesign.com/guestfiles/oda_file_converter")
        sys.exit(1)

    if not dwg_path.lower().endswith('.dwg'):
        print("❌ Input file is not a .dwg")
        return None

    if output_dir is None:
        output_dir = os.path.dirname(dwg_path) or "."

    # Output DXF path
    dxf_filename = os.path.splitext(os.path.basename(dwg_path))[0] + ".dxf"
    dxf_path = os.path.join(output_dir, dxf_filename)

    # If DXF already exists, skip conversion
    if os.path.exists(dxf_path):
        print(f"✅ DXF already exists: {dxf_path}")
        return dxf_path

    print(f"🔄 Converting {dwg_path} → {dxf_path}...")

    # Build command
    # ODA Converter CLI: input_dir output_dir version_type(ACAD2018) file_type(DXF) recurse(no) audit(no)
    input_dir = os.path.dirname(dwg_path)
    filename = os.path.basename(dwg_path)

    cmd = [
        ODA_CONVERTER_PATH,
        input_dir,          # Input folder
        output_dir,         # Output folder
        "ACAD2018",         # Output version
        "DXF",              # Output type
        "0",                # Recurse folders? 0 = no
        "0"                 # Audit? 0 = no
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=input_dir)

        if result.returncode == 0 and os.path.exists(dxf_path):
            print(f"✅ Successfully converted to: {dxf_path}")
            return dxf_path
        else:
            print(f"❌ Conversion failed: {result.stderr}")
            return None

    except Exception as e:
        print(f"❌ Error running ODA converter: {e}")
        return None