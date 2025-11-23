import cadquery as cq

EDGE = 5
HEIGHT = 3

solid = (
    cq.Workplane("XY")
    .box(EDGE, EDGE, HEIGHT, centered=(True, True, False))
    .edges("|Z and >XY").fillet(2)
    .edges("|Z and <XY").chamfer(1)
    .edges("<XY and >Z").chamfer(2.5)
)

SHIFT = EDGE * 3 / 4

solids = (
    solid.translate((-SHIFT, -SHIFT, 0))
    .union(solid.translate((SHIFT, -SHIFT, 0)))
)
solids = solids.union(
    solids.translate((0, SHIFT*2, 0))
)

raft = (
    cq.Workplane("XY")
    .box(30, 30, 0.5, centered=(True, True, False))
)
raft= raft.cut(
    cq.Workplane("XY")
    .box(EDGE*3, EDGE*3, 1, centered=(True, True, False))
)
runner = (
    cq.Workplane("XY")
    .box(30, 1, 0.5, centered=(True, True, False))
)
raft = raft.union(runner.translate((0, -SHIFT, 0)))
raft = raft.union(runner.translate((0, SHIFT, 0)))

solids = solids.union(raft)

show_object(solids)



solids.export("pivot.step")
