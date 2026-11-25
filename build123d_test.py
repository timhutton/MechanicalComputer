from bd_animation import AnimationGroup, normalize_track
from build123d import *
from functools import reduce
from itertools import combinations
from ocp_vscode import Animation, show
from py_gearworks import *


def check_proximity(parts, tolerance):
    """Check that all parts are separated by at least tolerance."""
    for a,b in combinations(parts, 2):
        if a.distance(b) < tolerance - 1e-6:
            print(f"WARNING: Objects too close ({a.distance(b)}): {a.label or a}, {b.label or b}")

# design parameters
travel = 30  # mm distance the sensors move between 0 and 1
rod_thickness = 6  # mm
rack_teeth = 8  # per distance of travel
pinion_teeth = 12
clearance = 0.7  # mm - parts closer than this may fuse during MJF printing
axle_radius = 3

# implications
rack_pitch = travel / rack_teeth
module = rack_pitch / PI
rack_movement = rack_teeth  # how many teeth to move along?
axle_hole_radius = axle_radius + clearance

prescaled_height = rod_thickness / module  # (rack.mesh_to() only support module=1)
pinion = SpurGear(number_of_teeth=pinion_teeth, module=1, height=prescaled_height, backlash=clearance / 2)
rack = InvoluteRack(number_of_teeth=rack_teeth, module=1, height=prescaled_height, backlash=clearance / 2)
rack.mesh_to(pinion, target_dir=LEFT, offset=-rack_teeth / 2, backlash=clearance * 1.2, angle_bias=0)
pinion_part = pinion.build_part().scale(module)
rack_part = rack.build_part().scale(module)
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
rack_part += Box(rod_thickness, rod_thickness - clearance, rod_thickness).translate((-rod_thickness, travel + rod_thickness * 1.5 + clearance / 2, rod_thickness / 2))
rack_part += Box(rod_thickness, rod_thickness - clearance, rod_thickness).translate((-rod_thickness, -(travel * 2 + rod_thickness * 1.5 + clearance / 2), rod_thickness / 2))

# make an axle to hold the pinion
axle_length = rod_thickness + clearance * 2
axle = Cylinder(radius=axle_radius, height=axle_length)
axle_cap_radius = pinion.r_base
axle_cap_length = clearance * 2
axle_cap = Cylinder(radius=axle_cap_radius, height=axle_cap_length)
axle_cap.location = Pos([0, 0, rod_thickness / 2 + clearance * 2])
axle += axle_cap
axle.location = Pos([0, 0, rod_thickness / 2])

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

support = back + axle + sleeve1 + sleeve2

group = AnimationGroup(
    children={"rack": rack_part,
              "pinion": pinion_part,
              "support": support},
    label="assembly"
)
show(group)

steps = 60
time_track = np.linspace(0, 5, steps + 1)
y_positions = np.linspace(0, rack_pitch * rack_movement, steps + 1)
pinion_rotation = -360 * rack_movement / pinion_teeth
rotation_track = np.linspace(0, pinion_rotation, steps + 1)

animation = Animation()
animation.add_track("/assembly/rack", "ty", time_track, normalize_track(y_positions))
animation.add_track("/assembly/pinion", "rz", time_track, normalize_track(rotation_track))
animation.animate(speed=1)

# check tolerances and export to STL
parts = group.children
check_proximity(parts, tolerance=clearance)
whole = reduce(lambda a, b: a + b, parts)
export_stl(whole, "rack_pinion_test.stl")
