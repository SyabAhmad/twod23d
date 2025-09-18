# utils/units.py
INSUNITS_MAP = {
    0:  ("Unitless", 1.0),      # assume 1 drawing unit per foot if unitless? We'll keep 1.0 scale from feet only when user sets; otherwise warn.
    1:  ("Inches",   12.0),     # 1 ft = 12 in
    2:  ("Feet",     1.0),      # 1 ft = 1 ft
    3:  ("Miles",    1.0/5280.0),
    4:  ("Millimeters", 304.8), # 1 ft = 304.8 mm
    5:  ("Centimeters", 30.48), # 1 ft = 30.48 cm
    6:  ("Meters",   0.3048),   # 1 ft = 0.3048 m
    7:  ("Kilometers", 0.0003048),
}

def feet_to_doc_scale(doc):
    """
    Return (scale, name) where 'scale' converts a length in feet
    into the DXF drawing units. E.g. if DXF is mm, scale=304.8.
    """
    code = int(doc.header.get("$INSUNITS", 0) or 0)
    name, scale = INSUNITS_MAP.get(code, ("Unknown", 1.0))
    return scale, name