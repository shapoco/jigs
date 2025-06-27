import cadquery as cq
import math
import os

# 円盤の直径
DISC_DIAMETER = 20

# 球面の半径
SPHERE_RADIUS = 20

# シャフトの直径
SHAFT_DIAMETER = 2.25

# シャフトの穴の直径マージン
SHAFT_HOLE_DIAMETER_MARGIN = 0.25

# シャフト取り付け穴の深さ
SHAFT_HOLE_DEPTH = 15

# シャフトガイドの壁厚
SHAFT_GUIDE_THICKNESS = 3

# 曲面のパラメータ
curve_angle = math.asin((DISC_DIAMETER / 2) / SPHERE_RADIUS)
curve_height = (1 - math.cos(curve_angle)) * SPHERE_RADIUS

# ディスクの最小厚さ
disc_min_thickness = 3

# キャップの最小厚さ
cap_min_thickness = 3

# シャフトガイドの直径
shaft_guide_diameter = SHAFT_DIAMETER + SHAFT_GUIDE_THICKNESS * 2

# シャフトガイドの長さ (穴を円盤の内部までめり込ますためその分短くする)
shaft_guide_length = SHAFT_HOLE_DEPTH - curve_height - disc_min_thickness / 2

# 円柱
cylinder_height = cap_min_thickness + curve_height + disc_min_thickness
cylinder = (
    cq.Workplane("XY")
    .cylinder(cylinder_height, DISC_DIAMETER / 2, centered=(True, True, False))
)

# 球面
sphere = (
    cq.Workplane("XY")
    .sphere(SPHERE_RADIUS)
    .translate((0, 0, SPHERE_RADIUS + cap_min_thickness))
)

# アタッチメント
attachment = (
    cylinder
    
    # 球面の形成
    .intersect(sphere)
    
    # シャフトガイドの押し出し
    .faces(">Z")
    .workplane()
    .pushPoints([(0, 0)])
    .circle(shaft_guide_diameter / 2)
    .extrude(shaft_guide_length)
    
    # シャフト用の穴
    .faces(">Z")
    .workplane()
    .pushPoints([(0, 0)])
    .circle((SHAFT_DIAMETER + SHAFT_HOLE_DIAMETER_MARGIN) / 2)
    .cutBlind(-SHAFT_HOLE_DEPTH)
    
    # 面取り
    .edges("%circle")
    .edges(">Z")[1]
    .chamfer(0.5)
    
    # 接地
    .translate((0, 0, -cap_min_thickness))
)

# シャフトガイドの根元の面取り
shaft_guide_chamfer = min(2, (DISC_DIAMETER - shaft_guide_diameter) / 2)
if shaft_guide_chamfer > 0:
    attachment = (
        attachment
        .edges("%circle")
        .edges(">>Z[-3]")[0]
        .chamfer(2)
    )

# やすり固定用のキャップ
cap = cylinder.cut(sphere)

# やすり固定用のパイプ
pipe_wall_thickness = 5
pipe_length = shaft_guide_length + 1
pipe_inner_diameter = max(DISC_DIAMETER - (pipe_wall_thickness * 2), shaft_guide_diameter + 1)
pipe_outer_diameter = pipe_inner_diameter + (pipe_wall_thickness * 2)
pipe = (
    # ボディ
    cq.Workplane("XY")
    .cylinder(pipe_length, pipe_outer_diameter / 2, centered=(True, True, False))
    
    # 穴
    .faces(">Z")
    .workplane()
    .pushPoints([(0, 0)])
    .circle(pipe_inner_diameter / 2)
    .cutBlind(-pipe_length - 1)
)

# シャフトガイドの根元の面取りに対応したパイプ内側の面取り
pipe_chamfer = min(pipe_wall_thickness / 2, 1 + (shaft_guide_diameter / 2 + shaft_guide_chamfer) - (pipe_inner_diameter / 2))
if pipe_chamfer > 0:
    pipe = (
        pipe
        .edges("%circle")
        .edges("<Z")[1]
        .chamfer(pipe_chamfer)
    )

# 表示
display_offset = DISC_DIAMETER + 10
show_object(attachment, name="Attachment")
show_object(cap.translate((display_offset, 0, 0)), name="Cap")
show_object(pipe.translate((-display_offset, 0, 0)), name="Pipe")

# 出力
for fmt in ["step", "stl"]:
    dir_name = f"d{DISC_DIAMETER}-r{SPHERE_RADIUS}-s{SHAFT_DIAMETER}/{fmt}"
    os.makedirs(dir_name, exist_ok=True)
    attachment.export(f"{dir_name}/attachment.{fmt}")
    cap.export(f"{dir_name}/cap.{fmt}")
    pipe.export(f"{dir_name}/pipe.{fmt}")
