from build123d import *
import itertools
from ocp_vscode import show
from py_gearworks import *


def check_proximity(parts, tolerance):
    """Check that all parts are separated by at least tolerance."""
    for a,b in itertools.combinations(parts, 2):
        if a.distance(b) < tolerance:
            print(f"WARNING: Objects too close ({a.distance(b)}): {a}, {b}")


length, width, base_height = 110, 50, 20

base_plan = Rectangle(length, width) - Circle(10)
base = extrude(base_plan, amount=base_height)
base.label = "base"

rod_plan = Circle(8)
rod = extrude(rod_plan, amount=base_height*2, both=True)
rod.label = "rod"

gear2 = SpurGear(number_of_teeth=8, height=4, backlash=0.05)
gear2.center = LEFT * 10
rack2 = InvoluteRack(number_of_teeth=10, height=4, backlash=0.05)
rack2.mesh_to(gear2, target_dir=LEFT, offset=0, backlash=0.2, angle_bias=0)


gear2_part = gear2.build_part()
rack2_part = rack2.build_part()

hole_obj = gear2.center_location_top * Hole(radius=1, depth=6)
gear2_part = gear2_part.cut(hole_obj)

parts = [gear2_part, rack2_part]

# export as single object for print-in-place
whole = gear2_part + rack2_part
export_stl(whole, "rack_pinion_test.stl")

check_proximity(parts, tolerance=0.05)
show(whole)