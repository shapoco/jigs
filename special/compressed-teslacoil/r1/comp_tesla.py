import cadquery as cq
import math

coil_d = 80  # コイルの直径
bobin_inner_wall_t = 2  # ボビンの内壁の厚み
bobin_lane_depth = 5  # ボビンの溝の深さ
bobin_end_wall_t = 2  # ボビンの端の壁の厚み

l1_lane_width = 5  # 1次コイルの溝の幅

l2_lane_width = 1  # 2次コイルの溝の幅
l2_lane_step = 2  # 2次コイルの溝の間隔
l2_wall_t = l2_lane_step - l2_lane_width  # 2次コイルの溝の壁の厚み
l2_num_lanes = 15  # 2次コイルの溝の数
l2_walll_chamfer = 0.3

slit_width = 5

chamfer = 0.5

# ボビンの高さ
bobin_h = (
    bobin_end_wall_t
    + l1_lane_width
    + bobin_end_wall_t
    + (l2_lane_width + l2_wall_t) * (l2_num_lanes - 1)
    + l2_lane_width
    + bobin_end_wall_t
)

# ボビンの直径
bobin_d = coil_d + bobin_lane_depth * 2

# ボビンの断面形状を生成
r0 = coil_d / 2 - bobin_inner_wall_t
r1 = coil_d / 2
r2 = coil_d / 2 + bobin_lane_depth
y0 = 0
y1 = y0 + bobin_end_wall_t
y2 = y1 + l1_lane_width
y3 = y2 + bobin_end_wall_t
y_end = y3
verts = [
    (r0, y0),
    (r2 - chamfer, y0),
    (r2, y0 + chamfer),
    (r2, y1 - chamfer),
    (r2 - chamfer, y1),
    (r1, y1),
    (r1, y2),
    (r2, y2),
    (r2 - chamfer, y2),
    (r2, y2 + chamfer),
]
for i in range(l2_num_lanes):
    verts.append((r2, y_end - l2_walll_chamfer))
    verts.append((r2 - l2_walll_chamfer, y_end))
    verts.append((r1, y_end))
    verts.append((r1, y_end + l2_lane_width))
    verts.append((r2 - l2_walll_chamfer, y_end + l2_lane_width))
    verts.append((r2, y_end + l2_lane_width + l2_walll_chamfer))
    y_end += l2_lane_step
y_end -= l2_wall_t
y_end += bobin_end_wall_t
verts.append((r2, y_end - chamfer))
verts.append((r2 - chamfer, y_end))
verts.append((r0, y_end))

bobin = cq.Workplane("XZ").polyline(verts).close().revolve()


def gen_slit_cutter(h):
    cutter = (
        cq.Workplane("XY")
        .box(999, slit_width, h + 0.2, centered=(False, True, False))
        .union(
            cq.Workplane("XY")
            .box(999, 999, 999, centered=(False, True, False))
            .translate((r2, 0, 0))
        )
        .edges("|Z")
        .fillet(2)
        .cut(cq.Workplane("XY").cylinder(999, coil_d / 2))
        .translate((0, 0, -0.1))
    )
    cutter = cutter.mirror("YZ")
    return cutter


cutter = gen_slit_cutter(bobin_end_wall_t)
bobin = bobin.cut(cutter)
bobin = bobin.cut(cutter.translate((0, 0, y3 - bobin_end_wall_t)))

if l2_num_lanes % 2 == 1:
    cutter = cutter.mirror("YZ")
bobin = bobin.cut(cutter.translate((0, 0, y_end - bobin_end_wall_t)))

cutter = gen_slit_cutter(l2_wall_t)
for i in range(l2_num_lanes - 1):
    c = cutter.translate((0, 0, y3 + l2_lane_width + l2_lane_step * i))
    if i % 2 == 0:
        c = c.mirror("YZ")
    bobin = bobin.cut(c)

floor_z = 2
x = bobin_d / 2 + floor_z
bobin = bobin.rotate((x, 0, 0), (x, 1, 0), 90).translate((-x - bobin_h / 2, 0, 0))


def gen_support_pattern(w, h):
    support_t = 0.45
    support_step = 2
    support_pattern_h = bobin_d / 2
    n = math.floor(w / (support_step * 2))
    support_pattern_w = n * support_step * 2
    support_pattern_x = -support_pattern_w / 2 + support_step
    support_pattern = (
        cq.Workplane("XY")
        .box(h, support_t, support_pattern_h, centered=(True, False, False))
        .translate((0, support_pattern_x, 0))
    )
    for i in range(n - 1):
        support_pattern = support_pattern.union(
            cq.Workplane("XY")
            .box(
                support_t,
                support_step + support_t,
                support_pattern_h,
                centered=(True, False, False),
            )
            .translate((h / 2, support_pattern_x + support_step * 2 * i, 0))
        )
        support_pattern = support_pattern.union(
            cq.Workplane("XY")
            .box(h, support_t, support_pattern_h, centered=(True, False, False))
            .translate((0, support_pattern_x + support_step * (2 * i + 1), 0))
        )
        support_pattern = support_pattern.union(
            cq.Workplane("XY")
            .box(
                support_t,
                support_step + support_t,
                support_pattern_h,
                centered=(True, False, False),
            )
            .translate((-h / 2, support_pattern_x + support_step * (2 * i + 1), 0))
        )
        support_pattern = support_pattern.union(
            cq.Workplane("XY")
            .box(h, support_t, support_pattern_h, centered=(True, False, False))
            .translate((0, support_pattern_x + support_step * (2 * i + 2), 0))
        )
    return support_pattern


support_w = 48
support_gap = 0.2

center_z = bobin_d / 2 + floor_z

cutter = (
    cq.Workplane("YZ")
    .cylinder(999, bobin_d / 2 + support_gap, centered=(True, True, True))
    .translate((0, 0, center_z))
)
support = gen_support_pattern(support_w, bobin_h).cut(cutter)


x = bobin_h / 2 + 1
y = bobin_d - 15
bridge_w = support_w
t1 = 5
t2 = 1
verts = [
    (x, 0),
    (x + t1, 0),
    (x + t1, y - x - t1),
    (0, y),
    (0, y - t1),
    (x, y - x - t1),
]
support_bridge = (
    cq.Workplane("XZ").polyline(verts).close().extrude(bridge_w / 2, both=True)
)
support_bridge = support_bridge.union(support_bridge.mirror("YZ"))
support_bridge = support_bridge.union(
    gen_support_pattern(bobin_h + 5, support_w - 1)
    .rotate((0, 0, 0), (0, 0, 1), 90)
    .translate((0, 0, bobin_d / 2))
    .intersect(
        cq.Workplane("YZ")
        .cylinder(
            999,
            (coil_d / 2) - bobin_inner_wall_t - support_gap,
            centered=(True, True, True),
        )
        .translate((0, 0, center_z))
    )
)
verts = [
    (0, 0),
    (x + t1 - t2, 0),
    (x + t1 - t2, y - x - t1),
    (0, y - t2),
]
cutter = cq.Workplane("XZ").polyline(verts).close().extrude(bridge_w / 2 - 1, both=True)
verts = [
    (0, 0),
    (x, 0),
    (x, y - x - t1),
    (0, y - t1),
]
cutter = cutter.union(
    cq.Workplane("XZ").polyline(verts).close().extrude(999, both=True)
)
cutter = cutter.union(cutter.mirror("YZ"))
support_bridge = support_bridge.cut(cutter)

support = support.union(support_bridge)
support = support.union(
    cq.Workplane("XY").box(
        bobin_h + t1 * 3, support_w, 0.5, centered=(True, True, False)
    )
)

bobin = bobin.union(support)

show_object(bobin, name="bobin", options={"alpha": 0.5, "color": (0.8, 0.8, 0.8)})

bobin.export("bobin.step")
