# utils/dxf_loader.py

import ezdxf
from config import *

def load_dxf(filepath):
    """Load DXF and return modelspace + doc"""
    try:
        doc = ezdxf.readfile(filepath)
        msp = doc.modelspace()
        print(f"✅ Loaded DXF: {filepath}")
        return doc, msp
    except Exception as e:
        print(f"❌ Failed to load DXF: {e}")
        return None, None

def get_entities_by_layer(msp, layer_name):
    """Get all entities in a layer"""
    return list(msp.query(f'*[layer=="{layer_name}"]'))