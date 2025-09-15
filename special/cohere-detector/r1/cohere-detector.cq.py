import cadquery as cq
import math
import os

D_INNER = 16
D_OUTER = 20
LENGTH = 45

D_MOTOR = 7
T_MOTOR_HOLDER = 2

cap = cq.Workplane("XY").cylinder(
    D_INNER * 2, D_INNER / 2, centered=(True, True, False)
)
cap = cap.union(
    cq.Workplane("XY").cylinder(1, D_INNER / 2 + 2 - 0.1, centered=(True, True, False))
)

verts = [
    (-D_INNER / 2, 0),
    (-D_INNER / 2, 2),
    (D_INNER / 2, D_INNER + 2),
    (D_INNER / 2, 0),
]

intersector = cq.Workplane("XZ").polyline(verts).close().extrude(D_INNER, both=True)

cap = cap.intersect(intersector)
cap = cap.faces("<Z").workplane().hole(2.5, 7)

verts = [
    (LENGTH / 2 + 3, 0),
    (LENGTH / 2, 0),
    (LENGTH / 2, -D_OUTER / 2 - 4),
    (LENGTH / 2 - 1, -D_OUTER / 2 - 5),
    (0, -D_OUTER / 2 - 5),
    (0, -D_OUTER / 2 - 8),
    (LENGTH / 2, -D_OUTER / 2 - 8),
    (LENGTH / 2 + 3, -D_OUTER / 2 - 5),
]

arm = cq.Workplane("XZ").polyline(verts).close().extrude(5, both=True)
arm = arm.edges("(>Y or <Y) and (not (<X or >Z))").chamfer(0.5)

cutter = (
    cq.Workplane("YZ")
    .cylinder(10, D_OUTER / 2 + 0.5, centered=(True, True, False))
    .translate((LENGTH / 2 - 8, 0, 0))
)
arm = arm.cut(cutter)

cutter = (
    cq.Workplane("YZ")
    .cylinder(10, D_OUTER / 2 - 0.5, centered=(True, True, False))
    .translate((LENGTH / 2 + 2, 0, 0))
)
arm = arm.cut(cutter)

verts = [
    (LENGTH / 2 + 1.25, D_OUTER / 2 + 0.1),
    (LENGTH / 2, D_OUTER / 2 + 0.1),
    (LENGTH / 2, D_OUTER / 2 + 0.5),
    (LENGTH / 2 + 0.5, D_OUTER / 2 + 1),
    (LENGTH / 2 + 1.5, D_OUTER / 2 + 1),
    (LENGTH / 2 + 3, D_OUTER / 2 - 0.5),
    (LENGTH / 2 + 3, D_OUTER / 2 - 1.5),
    (LENGTH / 2 + 2.5, D_OUTER / 2 - 2),
    (LENGTH / 2 + 1.25, D_OUTER / 2 - 2),
]

ring = cq.Workplane("XY").polyline(verts).close().revolve(360, (0, 0, 0), (1, 0, 0))

arm = arm.union(ring)

arm = arm.union(arm.mirror("YZ"))

arm = arm.faces("<Z").workplane().hole(3.5, 10).edges("%circle")[7].chamfer(1.5)


mh_part0 = cq.Workplane("XY").cylinder(
    5, D_MOTOR / 2 + T_MOTOR_HOLDER, centered=(True, True, False)
)
mh_part0 = mh_part0.cut(
    cq.Workplane("XY").cylinder(5, D_MOTOR / 2 - 0.2, centered=(True, True, False))
)
mh_part0 = mh_part0.cut(
    cq.Workplane("XY").polyline([(0, 0), (100, 60), (-100, 60)]).close().extrude(10)
)
mh_part0 = mh_part0.translate(
    (0, D_MOTOR / 2 + D_OUTER / 2 + T_MOTOR_HOLDER, 0)
)

mh_part1 = cq.Workplane("XY").cylinder(
    5, D_OUTER / 2 + T_MOTOR_HOLDER, centered=(True, True, False)
)
mh_part1 = mh_part1.cut(
    cq.Workplane("XY").cylinder(5, D_OUTER / 2 - 0.2, centered=(True, True, False))
)
mh_part1 = mh_part1.cut(
    cq.Workplane("XY").polyline([(0, 0), (100, -80), (-100, -80)]).close().extrude(10)
)

motor_holder = mh_part0.union(mh_part1)

motor_holder = motor_holder.chamfer(0.5)

spacer = cq.Workplane("XY").cylinder(
    5, 3, centered=(True, True, False)
)
spacer = spacer.faces(">Z").workplane().hole(3.5, 10)


# 表示
show_object(cap, name="cap")
show_object(arm, name="arm")
show_object(motor_holder.translate((0, 20, 0)), name="motor_holder")
show_object(spacer.translate((0, 20, 0)), name="spacer")

# 出力
for fmt in ["step", "stl"]:
    cap.export(f"cap_d{D_INNER}.{fmt}")
    arm.export(f"arm_d{D_OUTER}_l{LENGTH}.{fmt}")
    motor_holder.export(f"motor_holder_d{D_OUTER}_d{D_OUTER}.{fmt}")
    spacer.export(f"spacer.{fmt}")
