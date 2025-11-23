import cadquery as cq

BOARD_WIDTH = 60
BOARD_LENGTH = 67
BOARD_HEIGHT = 12

WALL_THICK = 2

CASE_WIDTH = BOARD_WIDTH + WALL_THICK * 2
CASE_LENGTH = BOARD_LENGTH + WALL_THICK * 2
CASE_HEIGHT = BOARD_HEIGHT + WALL_THICK * 2

DISPLAY_HEIGHT = 4.5
SCREEN_WIDTH = 42
SCREEN_LENGTH = 32
SCREEN_OFFSET = 2

FRONT_HEIGHT = CASE_HEIGHT - (WALL_THICK - 1)

KEY_OFFSET_X = 6 * 2.54
KEY_OFFSET_Y = -(BOARD_LENGTH / 2 - 16.5)
KEY_CONTACT_OFFSET = 8.5
KEY_DIR_WIDTH = 7
KEY_DIR_LENGTH = 24
KEY_ABXY_DIAMETER = 7
KEY_FLANGE_THICK = 0.5
KEY_HEIGHT = WALL_THICK + 2.5 + KEY_FLANGE_THICK
KEY_TOP_OFFSET = 0.5
KEY_HOLE_DEPTH = 1
KEY_HOLE_DIAMETER = 5.5

LED_HOLE_BODY_LENGTH = 16
LED_HOLE_BODY_WIDTH = 6
LED_HOLE_BODY_HEIGHT = 2
LED_HOLE_BODY_OFFSET = 13

VOLUME_HOLE_WIDTH = 14
VOLUME_HOLE_OFFSET = 6.5

SD_HOLE_LENGTH = 14
SD_HOLE_OFFSET = 28

USB_HOLE_OFFSET = 17.5
USB_HOLE_WIDTH = 9
USB_HOLE_HEIGHT = 5

POWER_SW_OFFSET_X = 9.5 * 2.54
POWER_SW_OFFSET_Y = 5.5
POWER_SW_HOLE_WIDTH = 6.5
POWER_SW_THICK = 2

SPEAKER_OFFSET_X = BOARD_WIDTH / 2 - 12
SPEAKER_OFFSET_Y = BOARD_LENGTH / 2 - 8

LOCK_LENGTH = 3
LOCK_HEIGHT = 1
LOCK_R0_Y = 16
LOCK_R1_Y = -5
LOCK_L0_Y = BOARD_LENGTH / 2 - 15
LOCK_L1_Y = -BOARD_LENGTH / 2 + 15

# ケースの前面
front = cq.Workplane("XY").box(
    CASE_WIDTH, CASE_LENGTH, FRONT_HEIGHT, centered=(True, True, False)
)
front = front.cut(
    cq.Workplane("XY")
    .box(BOARD_WIDTH, BOARD_LENGTH, FRONT_HEIGHT, centered=(True, True, False))
    .edges("|Z")
    .fillet(1)
    .translate((0, 0, WALL_THICK))
)

# スクリーンの穴
front = front.cut(
    cq.Workplane("XY").box(
        SCREEN_WIDTH, SCREEN_LENGTH, WALL_THICK * 2, centered=(True, True, False)
    )
    #    .edges("|Z")
    #    .fillet(1)
    .translate((0, (BOARD_LENGTH - SCREEN_LENGTH) / 2 - SCREEN_OFFSET, 0))
)

# LED の穴のガイド
front = front.union(
    cq.Workplane("XY")
    .box(
        LED_HOLE_BODY_WIDTH,
        LED_HOLE_BODY_LENGTH,
        LED_HOLE_BODY_HEIGHT,
        centered=(False, False, False),
    )
    .translate(
        (
            BOARD_WIDTH / 2 - LED_HOLE_BODY_WIDTH,
            BOARD_LENGTH / 2 - LED_HOLE_BODY_LENGTH - LED_HOLE_BODY_OFFSET,
            WALL_THICK,
        )
    )
)

# 角の面取り
front = front.faces(">X or <X").edges("|Z").fillet(1 + WALL_THICK)

# スクリーンの面取り
front = front.edges("<Z")[8:12].chamfer(WALL_THICK - 0.5)

# LED の穴
front = (
    front.faces("<Z")
    .workplane()
    .pushPoints(
        [
            (BOARD_WIDTH / 2 - 3.5, -BOARD_LENGTH / 2 + 17),
            (BOARD_WIDTH / 2 - 3.5, -BOARD_LENGTH / 2 + 17 + 2.54 * 3),
        ]
    )
    .hole(3)
)

# 十字キーの穴
cross_key = cq.Workplane("XY").box(
    KEY_DIR_WIDTH + 0.5, KEY_DIR_LENGTH + 0.5, 10, centered=(True, True, True)
)
cross_key = cross_key.union(cross_key.rotate((0, 0, 0), (0, 0, 1), 90))
cross_key = cross_key.edges("|Z").fillet(1)
front = front.cut(cross_key.translate((KEY_OFFSET_X, KEY_OFFSET_Y, 0)))

# ABXYキーの穴
front = (
    front.faces("<Z")
    .workplane()
    .pushPoints(
        [
            (-KEY_OFFSET_X - KEY_CONTACT_OFFSET, -KEY_OFFSET_Y),
            (-KEY_OFFSET_X + KEY_CONTACT_OFFSET, -KEY_OFFSET_Y),
            (-KEY_OFFSET_X, -KEY_OFFSET_Y - KEY_CONTACT_OFFSET),
            (-KEY_OFFSET_X, -KEY_OFFSET_Y + KEY_CONTACT_OFFSET),
        ]
    )
    .hole(KEY_ABXY_DIAMETER + 0.5)
)

# 前面の面取り
front = front.edges("<Z and %circle").chamfer(0.5)

# 基板のサポート (左右)
borad_support = (
    cq.Workplane("XY")
    .box(5, 2, DISPLAY_HEIGHT, centered=(False, True, False))
    .translate(
        (
            -BOARD_WIDTH / 2,
            -BOARD_LENGTH / 2 + 25,
            WALL_THICK,
        )
    )
)
front = front.union(borad_support)
front = front.union(borad_support.mirror("YZ"))

# 基板のサポート (下部)
borad_support = (
    cq.Workplane("XY")
    .box(2, 5, DISPLAY_HEIGHT, centered=(True, False, False))
    .translate(
        (
            6,
            -BOARD_LENGTH / 2,
            WALL_THICK,
        )
    )
)
front = front.union(borad_support)
front = front.union(borad_support.mirror("YZ"))

# 基板の押さえ (左右)
borad_support = (
    cq.Workplane("XY")
    .box(1, 2, DISPLAY_HEIGHT + 3, centered=(False, True, False))
    .translate(
        (
            -BOARD_WIDTH / 2,
            0,
            WALL_THICK,
        )
    )
)
front = front.union(borad_support.translate((0, BOARD_LENGTH / 2 - 17, 0)))
front = front.union(borad_support.translate((0, BOARD_LENGTH / 2 - 17, 0)).mirror("YZ"))
front = front.union(borad_support.translate((0, -BOARD_LENGTH / 2 + 6, 0)))
front = front.union(borad_support.translate((0, -BOARD_LENGTH / 2 + 6, 0)).mirror("YZ"))

# 電源スイッチ用の溝
front = front.cut(
    cq.Workplane("XY")
    .box(POWER_SW_HOLE_WIDTH, 10, 20, centered=(True, True, False))
    .translate((POWER_SW_OFFSET_X, BOARD_LENGTH / 2, 8 + WALL_THICK))
)

# SDカード用の溝
front = front.cut(
    cq.Workplane("XY")
    .box(10, SD_HOLE_LENGTH, 10, centered=(True, True, False))
    .edges("|X")
    .fillet(1)
    .translate((-BOARD_WIDTH / 2, BOARD_LENGTH / 2 - SD_HOLE_OFFSET, 7 + WALL_THICK))
)

# ボリューム用の溝
front = front.cut(
    cq.Workplane("XY")
    .box(VOLUME_HOLE_WIDTH, 10, 20, centered=(True, True, False))
    .edges("|Y")
    .fillet(1)
    .translate((VOLUME_HOLE_OFFSET, BOARD_LENGTH / 2, 6 + WALL_THICK))
)

# SDカード用の溝
front = front.cut(
    cq.Workplane("XY")
    .box(10, SD_HOLE_LENGTH, 10, centered=(True, True, False))
    .edges("|X")
    .fillet(1)
    .translate((-BOARD_WIDTH / 2, BOARD_LENGTH / 2 - SD_HOLE_OFFSET, 7 + WALL_THICK))
)

# USBポート用の溝
front = front.cut(
    cq.Workplane("XY")
    .box(USB_HOLE_WIDTH, 10, USB_HOLE_HEIGHT, centered=(True, True, True))
    .edges("|Y")
    .fillet(2)
    .translate((USB_HOLE_OFFSET, -BOARD_LENGTH / 2, WALL_THICK + DISPLAY_HEIGHT + 3.5))
)
front = front.cut(
    cq.Workplane("XY")
    .box(USB_HOLE_WIDTH + 4, 10, USB_HOLE_HEIGHT + 4, centered=(True, False, True))
    .edges("|Y")
    .fillet(4)
    .translate(
        (USB_HOLE_OFFSET, -BOARD_LENGTH / 2 - 11, WALL_THICK + DISPLAY_HEIGHT + 3.5)
    )
)

# ロック用の溝
lock_groove = (
    cq.Workplane("XY")
    .box(10, LOCK_LENGTH + 1, LOCK_HEIGHT + 1, centered=(False, True, False))
    .translate((-CASE_WIDTH / 2 + 1, 0, FRONT_HEIGHT - LOCK_HEIGHT - 3))
)
front = front.cut(lock_groove.translate((0, LOCK_R0_Y, 0)))
front = front.cut(lock_groove.translate((0, LOCK_R1_Y, 0)))
front = front.cut(lock_groove.mirror("YZ").translate((0, LOCK_L0_Y, 0)))
front = front.cut(lock_groove.mirror("YZ").translate((0, LOCK_L1_Y, 0)))

# 裏蓋
back = (
    cq.Workplane("XY")
    .box(CASE_WIDTH, CASE_LENGTH, 1, centered=(True, True, False))
    .edges("|Z")
    .fillet(1 + WALL_THICK)
)
back = back.union(
    cq.Workplane("XY")
    .box(
        BOARD_WIDTH - 0.5, BOARD_LENGTH - 0.5, WALL_THICK, centered=(True, True, False)
    )
    .edges("|Z")
    .fillet(1)
)

# ボリューム用の壁
back = back.union(
    cq.Workplane("XY")
    .box(VOLUME_HOLE_WIDTH - 0.5, WALL_THICK * 2, 5.5, centered=(True, False, False))
    .translate((-VOLUME_HOLE_OFFSET, BOARD_LENGTH / 2 - WALL_THICK, 0))
)
back = back.union(
    cq.Workplane("XY")
    .box(VOLUME_HOLE_WIDTH + 2, WALL_THICK - 0.25, 5.5, centered=(True, False, False))
    .translate((-VOLUME_HOLE_OFFSET, BOARD_LENGTH / 2 - WALL_THICK, 0))
)

# 電源スイッチ用の壁
back = back.union(
    cq.Workplane("XY")
    .box(POWER_SW_HOLE_WIDTH - 0.5, WALL_THICK * 2, 2, centered=(True, False, False))
    .translate((-POWER_SW_OFFSET_X, BOARD_LENGTH / 2 - WALL_THICK, 0))
)
# back = back.union(
#     cq.Workplane("XY")
#     .box(POWER_SW_HOLE_WIDTH + 2, 10 - 0.25, 2.5, centered=(True, False, False))
#     .translate((-POWER_SW_OFFSET_X, BOARD_LENGTH / 2 - 10, 0))
# )

# SDカード用の壁
back = back.union(
    cq.Workplane("XY")
    .box(3 - 0.25, SD_HOLE_LENGTH + 6, 4.5, centered=(False, True, False))
    .translate((BOARD_WIDTH / 2 - 3, BOARD_LENGTH / 2 - SD_HOLE_OFFSET, 0))
)
back = back.union(
    cq.Workplane("XY")
    .box(WALL_THICK * 2, SD_HOLE_LENGTH - 0.5, 4.5, centered=(False, True, False))
    .translate((BOARD_WIDTH / 2 - WALL_THICK, BOARD_LENGTH / 2 - SD_HOLE_OFFSET, 0))
)
back = back.cut(
    cq.Workplane("XY")
    .cylinder(10, 7, centered=(True, True, False))
    .translate((BOARD_WIDTH / 2 + 6, BOARD_LENGTH / 2 - SD_HOLE_OFFSET, 0))
)

# スピーカー用の穴
cutter = (
    cq.Workplane("XY")
    .box(2, 8, 10, centered=(True, True, True))
    .edges("|Z")
    .fillet(0.9)
    .translate((SPEAKER_OFFSET_X, SPEAKER_OFFSET_Y, 0))
)
back = back.cut(cutter.translate((-5, 0, 0)))
back = back.cut(cutter.translate((0, 0, 0)))
back = back.cut(cutter.translate((5, 0, 0)))

# ロック
verts = [
    (-0.25, 1),
    (-0.25, 3.25),
    (0.5, 3.25),
    (0.5, 4),
    (-0.5, 5),
    (-3, 5),
    (-4, 4),
    (-4, 1),
]
lock = cq.Workplane("XZ").polyline(verts).close().extrude(LOCK_LENGTH / 2, both=True)
back = back.union(lock.translate((BOARD_WIDTH / 2, LOCK_R0_Y, 0)))
back = back.union(lock.translate((BOARD_WIDTH / 2, LOCK_R1_Y, 0)))
back = back.union(lock.mirror("YZ").translate((-BOARD_WIDTH / 2, LOCK_L0_Y, 0)))
back = back.union(lock.mirror("YZ").translate((-BOARD_WIDTH / 2, LOCK_L1_Y, 0)))

# 裏蓋の面取り
back = back.faces("<Z").chamfer(0.5)

# 十字キー本体の作成
verts1 = [
    (-KEY_DIR_LENGTH / 2, 0),
    (-KEY_DIR_LENGTH / 2 + (1 + KEY_TOP_OFFSET), KEY_HEIGHT),
    (KEY_DIR_LENGTH / 2 - (1 + KEY_TOP_OFFSET), KEY_HEIGHT),
    (KEY_DIR_LENGTH / 2, 0),
]
verts2 = [
    (-KEY_DIR_WIDTH / 2, 0),
    (-KEY_DIR_WIDTH / 2 + KEY_TOP_OFFSET, KEY_HEIGHT),
    (KEY_DIR_WIDTH / 2 - KEY_TOP_OFFSET, KEY_HEIGHT),
    (KEY_DIR_WIDTH / 2, 0),
]
dir_key = (
    cq.Workplane("YZ").polyline(verts1).close().extrude(KEY_DIR_WIDTH / 2, both=True)
)
dir_key = dir_key.intersect(
    cq.Workplane("XZ").polyline(verts2).close().extrude(KEY_DIR_LENGTH / 2, both=True)
)
dir_key = dir_key.union(dir_key.rotate((0, 0, 0), (0, 0, 1), 90))
dir_key = dir_key.edges("not (>Z or <Z)").fillet(1)

# 十字キーのフランジ
dir_key_flange = (
    cq.Workplane("XY")
    .box(
        KEY_DIR_WIDTH + 2,
        KEY_DIR_LENGTH + 2,
        KEY_FLANGE_THICK,
        centered=(True, True, False),
    )
    .edges("|Z")
    .fillet(2)
)
dir_key_flange = dir_key_flange.union(dir_key_flange.rotate((0, 0, 0), (0, 0, 1), 90))
dir_key = dir_key.union(dir_key_flange)

# 十字キートップのくぼみ
dir_key = dir_key.cut(
    cq.Workplane("XY").sphere(150).translate((0, 0, KEY_HEIGHT + 150 - 0.4))
)

# 十字キートップの丸め
dir_key = dir_key.faces(">Z").fillet(0.5)

# 十字キー裏の穴
dir_key = (
    dir_key.faces("<Z")
    .workplane()
    .pushPoints(
        [
            (-KEY_CONTACT_OFFSET, 0),
            (KEY_CONTACT_OFFSET, 0),
            (0, -KEY_CONTACT_OFFSET),
            (0, KEY_CONTACT_OFFSET),
        ]
    )
    .hole(KEY_HOLE_DIAMETER, KEY_HOLE_DEPTH)
    .pushPoints([(0, 0)])
    .hole(2.5, KEY_HEIGHT - 1)
)

# ABXYキー本体の作成
verts = [
    (0, 0),
    (KEY_ABXY_DIAMETER / 2, 0),
    (KEY_ABXY_DIAMETER / 2 - KEY_TOP_OFFSET, KEY_HEIGHT),
    (0, KEY_HEIGHT),
]
abxy_key = (
    cq.Workplane("YZ")
    .polyline(verts)
    .close()
    .revolve(360, axisStart=(0, 0, 0), axisEnd=(0, 1, 0))
)

# ABXYキーのフランジ
abxy_key = abxy_key.union(
    cq.Workplane("XY").cylinder(
        KEY_FLANGE_THICK,
        KEY_ABXY_DIAMETER / 2 + 1,
        centered=(True, True, False),
    )
)

# 十字キートップのくぼみ
abxy_key = abxy_key.cut(
    cq.Workplane("XY").sphere(10).translate((0, 0, KEY_HEIGHT + 10 - 0.3))
)

# ABXYキートップの丸め
abxy_key = abxy_key.faces(">Z").fillet(0.5)

# ABXYキー裏の穴
abxy_key = abxy_key.faces("<Z").workplane().hole(KEY_HOLE_DIAMETER, KEY_HOLE_DEPTH)

# 電源スイッチ
verts = [
    (0, WALL_THICK + POWER_SW_THICK - 0.5),
    (0.5, WALL_THICK + POWER_SW_THICK),
    (1, WALL_THICK + POWER_SW_THICK - 0.5),
    (1.5, WALL_THICK + POWER_SW_THICK),
    (2, WALL_THICK + POWER_SW_THICK - 0.5),
    (2.5, WALL_THICK + POWER_SW_THICK),
    (3, WALL_THICK + POWER_SW_THICK - 0.5),
    (3.5, WALL_THICK + POWER_SW_THICK),
    (4, WALL_THICK + POWER_SW_THICK - 0.5),
    (4.5, WALL_THICK + POWER_SW_THICK),
    (5, WALL_THICK + POWER_SW_THICK - 0.5),
    (5, WALL_THICK + 0.25),
    (1.5, WALL_THICK + 0.25),
    (1.5, -0.25),
    (4, -0.25),
    (4, -POWER_SW_OFFSET_Y - 1.5),
    (3, -POWER_SW_OFFSET_Y - 2.5),
    (1, -POWER_SW_OFFSET_Y - 2.5),
    (1, -POWER_SW_OFFSET_Y + 0.5),
    (0, -POWER_SW_OFFSET_Y + 0.5),
]
power_switch = cq.Workplane("XY").polyline(verts).close().extrude(5)
power_switch = power_switch.union(power_switch.mirror("YZ"))
verts = [
    (WALL_THICK + 0.25, 10),
    (WALL_THICK + 0.25, 3),
    (-0.25, 3),
    (-0.25, 8),
    (-2, 8),
    (-2, 2),
    (-10, 2),
    (-10, 10),
]
power_switch = power_switch.cut(
    cq.Workplane("YZ").polyline(verts).close().extrude(10, both=True)
)

dir_key_step = dir_key.rotate((0, 0, 0), (0, 0, 1), 45).rotate((0, 0, 0), (1, 0, 0), 90)
abxy_key_step = abxy_key.rotate((0, 0, 0), (0, 0, 1), 45).rotate(
    (0, 0, 0), (1, 0, 0), 90
)

front.export("case_front.step")
back.export("case_back.step")
dir_key_step.export("dir_key.step")
abxy_key_step.export("abxy_key.step")
power_switch.export("power_switch.step")

back = back.rotate((0, 0, 0), (0, 1, 0), 180).translate((0, 0, CASE_HEIGHT + 10))

dir_key = dir_key.mirror("XY").translate(
    (KEY_OFFSET_X, KEY_OFFSET_Y, WALL_THICK + KEY_FLANGE_THICK + 0.5)
)

abxy_keys = abxy_key.translate((-KEY_CONTACT_OFFSET, 0, 0))
abxy_keys = abxy_keys.union(abxy_key.translate((KEY_CONTACT_OFFSET, 0, 0)))
abxy_keys = abxy_keys.union(abxy_key.translate((0, -KEY_CONTACT_OFFSET, 0)))
abxy_keys = abxy_keys.union(abxy_key.translate((0, KEY_CONTACT_OFFSET, 0)))
abxy_keys = abxy_keys.mirror("XY").translate(
    (-KEY_OFFSET_X, KEY_OFFSET_Y, WALL_THICK + KEY_FLANGE_THICK + 0.5)
)

power_switch = power_switch.rotate((0, 0, 0), (0, 1, 0), 180)
power_switch = power_switch.translate(
    (POWER_SW_OFFSET_X, BOARD_LENGTH / 2, CASE_HEIGHT - WALL_THICK - 0.75)
)

show_object(front, options={"color": "#ddd"})
show_object(back, options={"color": "#ddd"})
show_object(dir_key, options={"color": "#222"})
show_object(abxy_keys, options={"color": "#222"})
show_object(power_switch, options={"color": "#222"})
