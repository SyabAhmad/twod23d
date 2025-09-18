import trimesh
from trimesh.util import concatenate as tm_concat

def _box(size, translate=(0, 0, 0), color=None):
    m = trimesh.creation.box(extents=size)
    m.apply_translation(translate)
    if color is not None:
        m.visual.face_colors = color
    return m

def _cyl(radius, height, translate=(0, 0, 0), color=None):
    m = trimesh.creation.cylinder(radius=radius, height=height, sections=24)
    m.apply_translation(translate)
    if color is not None:
        m.visual.face_colors = color
    return m

def _center(m):
    center = m.bounds.mean(axis=0)
    m.apply_translation(-center)
    return m

def make_chair():
    seat_w, seat_d, seat_t = 1.6, 1.6, 0.15
    seat_h = 1.5
    leg_w = 0.15
    back_h, back_t = 2.0, 0.15
    parts = []
    parts.append(_box((seat_w, seat_d, seat_t), (0, 0, seat_h)))
    offs = (seat_w/2 - leg_w/2, seat_d/2 - leg_w/2)
    for sx in (-1, 1):
        for sy in (-1, 1):
            parts.append(_box((leg_w, leg_w, seat_h), (sx*offs[0], sy*offs[1], seat_h/2)))
    parts.append(_box((seat_w, back_t, back_h), (0, -seat_d/2 + back_t/2, seat_h + back_h/2)))
    return _center(tm_concat(parts))

def make_desk():
    top_l, top_w, top_t = 5.0, 2.5, 0.2
    height = 2.5
    leg_w = 0.2
    parts = []
    parts.append(_box((top_l, top_w, top_t), (0, 0, height)))
    offs = (top_l/2 - leg_w/2, top_w/2 - leg_w/2)
    for sx in (-1, 1):
        for sy in (-1, 1):
            parts.append(_box((leg_w, leg_w, height), (sx*offs[0], sy*offs[1], height/2)))
    return _center(tm_concat(parts))

def make_table():
    top_l, top_w, top_t = 4.0, 4.0, 0.2
    height = 2.8
    leg_w = 0.2
    parts = [_box((top_l, top_w, top_t), (0, 0, height))]
    offs = (top_l/2 - leg_w/2, top_w/2 - leg_w/2)
    for sx in (-1, 1):
        for sy in (-1, 1):
            parts.append(_box((leg_w, leg_w, height), (sx*offs[0], sy*offs[1], height/2)))
    return _center(tm_concat(parts))

def make_sofa():
    seat_l, seat_w, seat_h = 7.0, 3.0, 1.2
    base_t = 0.4
    back_h = 2.0
    arm_w = 0.5
    parts = []
    parts.append(_box((seat_l, seat_w, base_t), (0, 0, base_t/2)))
    parts.append(_box((seat_l-2*arm_w, seat_w-0.4, seat_h), (0, 0.2, base_t + seat_h/2)))
    parts.append(_box((seat_l, 0.4, back_h), (0, -seat_w/2 + 0.2, base_t + seat_h + back_h/2)))
    parts.append(_box((arm_w, seat_w, seat_h+1.2), (-seat_l/2 + arm_w/2, 0, base_t + (seat_h+1.2)/2)))
    parts.append(_box((arm_w, seat_w, seat_h+1.2), ( seat_l/2 - arm_w/2, 0, base_t + (seat_h+1.2)/2)))
    return _center(tm_concat(parts))

def make_printer():
    body = _box((2.0, 1.5, 1.5), (0, 0, 0.75))
    tray = _box((1.6, 0.2, 0.1), (0, -0.85, 0.5))
    return _center(tm_concat([body, tray]))

def make_phone():
    base = _box((0.8, 1.2, 0.2), (0, 0, 0.1))
    handset = _box((0.3, 1.0, 0.2), (0.35, 0, 0.3))
    return _center(tm_concat([base, handset]))

def make_plant():
    trunk = _cyl(0.08, 2.0, (0, 0, 1.0))
    crown = trimesh.creation.icosphere(subdivisions=2, radius=0.8)
    crown.apply_translation((0, 0, 2.0))
    return _center(tm_concat([trunk, crown]))

def make_door_single():
    leaf_w, leaf_t, leaf_h = 3.0, 0.15, 7.0
    frame_t = 0.2
    leaf = _box((leaf_w, leaf_t, leaf_h), (leaf_w/2, 0, leaf_h/2))
    frame = _box((leaf_w+frame_t*2, frame_t, leaf_h+frame_t*2), (leaf_w/2, 0, (leaf_h+frame_t*2)/2))
    return _center(tm_concat([frame, leaf]))

def make_door_double():
    leaf_w, leaf_t, leaf_h = 3.0, 0.15, 7.0
    frame_t = 0.2
    left  = _box((leaf_w, leaf_t, leaf_h), (leaf_w/2, 0, leaf_h/2))
    right = _box((leaf_w, leaf_t, leaf_h), (leaf_w/2 + leaf_w, 0, leaf_h/2))
    frame = _box((leaf_w*2+frame_t*2, frame_t, leaf_h+frame_t*2), (leaf_w, 0, (leaf_h+frame_t*2)/2))
    return _center(tm_concat([frame, left, right]))
