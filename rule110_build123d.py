from bd_animation import AnimationGroup, normalize_track
from build123d import *
from functools import reduce
from itertools import combinations
import math
from ocp_vscode import Animation, show
from py_gearworks import *


def check_proximity(parts, tolerance):
    """Check that all parts are separated by at least tolerance."""
    for a,b in combinations(parts, 2):
        if a.distance(b) < tolerance - 1e-6:
            print(f"WARNING: Objects too close ({a.distance(b)}): {a.label or a}, {b.label or b}")


def check_connected(parts):
    """Check that each part is a single connected piece."""
    for part in parts:
        if not len(part.solids()) == 1:
            print(f"WARNING: Disconnected/empty part: {part.label or part}")


# design parameters
prototype_label = "B"
if prototype_label == "A":
    travel = 30  # mm distance the sensors move between 0 and 1
    rod_thickness = 6  # mm
    rack_teeth = 8  # per distance of travel
    pinion_teeth = 12
    clearance = 1.0  # mm - parts closer than this may fuse during MJF printing
    axle_radius = 3
    min_thickness = 3  # nothing should be thinner than this
elif prototype_label == "B":
    travel = 20  # mm distance the sensors move between 0 and 1
    rod_thickness = 5  # mm
    rack_teeth = 6  # per distance of travel
    pinion_teeth = 10
    clearance = 0.7  # mm - parts closer than this may fuse during MJF printing
    axle_radius = 2
    min_thickness = 2  # nothing should be thinner than this
else:
    travel = 15  # mm distance the sensors move between 0 and 1
    rod_thickness = 4  # mm
    rack_teeth = 6  # per distance of travel
    pinion_teeth = 10
    clearance = 0.5  # mm - parts closer than this may fuse during MJF printing
    axle_radius = 2
    min_thickness = 2  # nothing should be thinner than this

peg_height_factor = 1
peg_separation_factor = 0.85
num_pegs = 3
peg_values = [0] * num_pegs
peg_values[1] = 1
peg_foot_radius = 3
track_thickness = 6
sensor_clearance = clearance * 3
updater_rod_thickness = 7
temp_track_offset = (0, -travel * 4, 0)

# implications
rack_pitch = travel / rack_teeth
module = rack_pitch / PI
rack_movement = rack_teeth  # how many teeth to move along?
axle_hole_radius = axle_radius + clearance
peg_radius = travel / 2 - clearance
peg_height = peg_radius * peg_height_factor
sensor_height = peg_height + updater_rod_thickness + sensor_clearance
slot_width = peg_foot_radius * 2 + clearance * 2
slot_length = travel * 2
track_width = travel * 3
sensor_diag = travel * 2
peg_separation = sensor_diag * peg_separation_factor

pinion = SpurGear(number_of_teeth=pinion_teeth, module=module, height=rod_thickness, backlash=clearance / 2)
rack = InvoluteRack(number_of_teeth=rack_teeth, module=module, height=rod_thickness, backlash=clearance / 2)
rack.mesh_to(pinion, target_dir=LEFT, offset=-rack_teeth / 2, backlash=clearance * 1.2, angle_bias=0)
pinion_part = pinion.build_part()
rack_part = rack.build_part()

# make a hole in the pinion for the axle
if pinion.r_base - axle_hole_radius < min_thickness:
    print("WARNING: Gear too small for safe axle")
hole_obj = pinion.center_location_top * Hole(radius=axle_hole_radius, depth=rod_thickness)
pinion_part = pinion_part.cut(hole_obj)

# make rack into a rod of the correct thickness
rack_base_height = rack_part.edges().filter_by(Axis.X)[0].length
rack_base = rack_part.faces().sort_by(Axis.X)[0]
rack_part += extrude(rack_base, amount=rod_thickness - rack_base_height)
rack_end1 = rack_part.faces().sort_by(Axis.Y)[0]
rack_part += extrude(rack_end1, amount=travel + rod_thickness * 2)
rack_end2 = rack_part.faces().sort_by(Axis.Y)[-1]
rack_part += extrude(rack_end2, amount=travel + rod_thickness * 2)

# add end stoppers to the rod
rack_part += Box(rod_thickness * 2, rod_thickness - clearance, rod_thickness).translate((rack_end1.center().X, travel + rod_thickness * 1.5 + clearance / 2, rod_thickness / 2))
rack_part += Box(rod_thickness * 2, rod_thickness - clearance, rod_thickness).translate((rack_end1.center().X, -(travel * 2 + rod_thickness * 1.5 + clearance / 2), rod_thickness / 2))

# make an axle to hold the pinion
axle_length = rod_thickness + clearance * 2
axle = Cylinder(radius=axle_radius, height=axle_length)
axle.location = Pos(0, 0, rod_thickness / 2)

# make a sleeve to stop the pinion from sliding off the axle
pinion_sleeve = Box(axle_radius * 2, pinion.r_base * 6, rod_thickness / 2).translate((0, 0, rod_thickness * 1.25 + clearance))
pinion_sleeve += Box(axle_radius * 2, rod_thickness, rod_thickness + clearance * 2).translate((0, pinion.r_base * 3 - rod_thickness / 2, rod_thickness / 2))
pinion_sleeve += Box(axle_radius * 2, rod_thickness, rod_thickness + clearance * 2).translate((0, -(pinion.r_base * 3 - rod_thickness / 2), rod_thickness / 2))

# make sleeves to support the rod
sleeve_sketch = Plane.XZ * Rectangle(rod_thickness * 2, rod_thickness * 2)
sleeve_sketch -= offset(sleeve_sketch, amount=-(rod_thickness / 2 - clearance))
sleeve1 = extrude(sleeve_sketch, amount = rod_thickness)
sleeve1.location = Pos(rack_end1.center())
sleeve2 = sleeve1.located(Pos(rack_end2.center() + 
                              (0, travel + rod_thickness, 0)))

# make a back piece to join the sleeves to the axle
back_height = axle_radius - sleeve1.faces().sort_by(Axis.X)[0].center().X
back_width = travel * 2 + rod_thickness * 4
back_thickness = rod_thickness / 2
back = Box(back_height, back_width, back_thickness)
back.location = Pos(-back_height / 2 + axle_radius, 0, -(back_thickness /2 + clearance))

support = back + axle + pinion_sleeve + sleeve1 + sleeve2

track_sketch = Rectangle(peg_separation * (num_pegs + 1), np.linalg.norm(temp_track_offset)) - \
    GridLocations(peg_separation, 0, num_pegs, 1) * \
    SlotOverall(width = slot_length + slot_width, height = slot_width, rotation=90)
track = extrude(track_sketch, track_thickness)
track2 = track.translate(temp_track_offset)

parts = [track + track2]

for peg_idx in range(num_pegs):
    peg_head = Cylinder(peg_radius, peg_height)
    peg_head = peg_head.translate((0, 0, track_thickness + peg_height / 2 + clearance))
    peg_foot = Cylinder(peg_foot_radius, track_thickness + clearance * 2).\
        translate((0, 0, track_thickness / 2))
    peg_root = Cylinder(peg_radius, peg_height / 2)
    peg_root = peg_root.translate((0, 0, - (peg_height / 4 + clearance)))
    peg = peg_head + peg_foot + peg_root
    peg = peg.translate(\
        (peg_separation * (peg_idx - (num_pegs - 1) / 2),\
        -slot_length / 2 + slot_length * peg_values[peg_idx],\
        0))
    peg.label = f"peg.{peg_idx:03d}"
    parts += peg
    temp_peg = peg.translate(temp_track_offset)
    parts += temp_peg

sensor = Box(sensor_diag / math.sqrt(2), sensor_diag / math.sqrt(2), sensor_height, rotation=(0, 0, 45))
sensor += Box(updater_rod_thickness, travel * 5, updater_rod_thickness).translate((0, 0, sensor_height / 2 - updater_rod_thickness / 2))
sensor = sensor.translate((0, -travel / 2, track_thickness + sensor_height / 2 + clearance * 2))
#sensor = sensor.translate((peg_separation / 2, travel / 2, 0))  # move to check it fits between two pegs
# TODO: hollow out sensor
parts += sensor

if True:  # track test
    show(parts)
else:  # rack and pinion test
    group = AnimationGroup(
        children={"rack": rack_part,
                "pinion": pinion_part,
                "support": support},
        label="assembly"
    )
    show(group)

    steps = 60
    time_track = np.linspace(0, 5, steps + 1)
    y_positions = np.linspace(0, travel, steps + 1)
    pinion_rotation = -360 * rack_movement / pinion_teeth
    rotation_track = np.linspace(0, pinion_rotation, steps + 1)

    animation = Animation()
    animation.add_track("/assembly/rack", "ty", time_track, normalize_track(y_positions))
    animation.add_track("/assembly/pinion", "rz", time_track, normalize_track(rotation_track))
    animation.animate(speed=1)

    # check tolerances and export to STL
    parts = group.children
    check_proximity(parts, tolerance=clearance)
    check_connected(parts)
    whole = reduce(lambda a, b: a + b, parts)
    export_stl(whole, f"rack_pinion_test_{prototype_label}.stl")
