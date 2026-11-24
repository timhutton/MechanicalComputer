from bd_animation import AnimationGroup, normalize_track
from build123d import *
from functools import reduce
from itertools import combinations
from ocp_vscode import Animation, show
from py_gearworks import *


def check_proximity(parts, tolerance):
    """Check that all parts are separated by at least tolerance."""
    for a,b in combinations(parts, 2):
        if a.distance(b) < tolerance:
            print(f"WARNING: Objects too close ({a.distance(b)}): {a}, {b}")


pinion_teeth = 8
rack_teeth = 15
pinion = SpurGear(number_of_teeth=pinion_teeth, height=4, backlash=0.05)
rack = InvoluteRack(number_of_teeth=rack_teeth, height=4, backlash=0.05)
rack.mesh_to(pinion, target_dir=LEFT, offset=0, backlash=0.2, angle_bias=0)

pinion_part = pinion.build_part()
rack_part = rack.build_part()
hole_obj = pinion.center_location_top * Hole(radius=1, depth=6)
pinion_part = pinion_part.cut(hole_obj)

group = AnimationGroup(
    children={"rack": rack_part, "pinion": pinion_part},
    label="assembly"
)
show(group)

steps = 60
rack_movement = -5  # how many teeth to move along?
rack_pitch = PI  # (since module is 1)
time_track = np.linspace(0, 5, steps + 1)
y_positions = np.linspace(0, rack_pitch * rack_movement, steps + 1)
pinion_rotation = -360 * rack_movement / pinion_teeth
rotation_track = np.linspace(0, pinion_rotation, steps + 1)

animation = Animation(group)
animation.add_track("/assembly/rack", "ty", time_track, normalize_track(y_positions))
animation.add_track("/assembly/pinion", "rz", time_track, normalize_track(rotation_track))
animation.animate(speed=1)

# check tolerances and export to STL
parts = [pinion_part, rack_part]
check_proximity(parts, tolerance=0.05)
whole = reduce(lambda result, current: result + current, parts)
export_stl(whole, "rack_pinion_test.stl")
