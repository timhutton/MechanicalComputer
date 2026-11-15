import bpy
import math
import numpy as np
import os

dark_yarn = (0.263, 0.212, 0.247, 1.0)  # RGBA for the 1 symbols (darker)
light_yarn = (0.667, 0.663, 0.545, 1.0)  # RGBA for the 0 symbols (lighter)

# access the objects we will be moving
A = bpy.data.objects.get("A")
A.animation_data_clear()
B = bpy.data.objects.get("B")
B.animation_data_clear()
C = bpy.data.objects.get("C")
C.animation_data_clear()
notA = bpy.data.objects.get("not_A")
notA.animation_data_clear()
notB = bpy.data.objects.get("not_B")
notB.animation_data_clear()
notC = bpy.data.objects.get("not_C")
notC.animation_data_clear()
invertA = bpy.data.objects.get("invert_A")
invertA.animation_data_clear()
invertB = bpy.data.objects.get("invert_B")
invertB.animation_data_clear()
invertC = bpy.data.objects.get("invert_C")
invertC.animation_data_clear()
F = bpy.data.objects.get("F")
F.animation_data_clear()
Fgear = bpy.data.objects.get("F_gear")
Fgear.animation_data_clear()
E = bpy.data.objects.get("E")
E.animation_data_clear()
G = bpy.data.objects.get("G")
G.animation_data_clear()
H = bpy.data.objects.get("H")
H.animation_data_clear()
Output1 = bpy.data.objects.get("output1")
Output1.animation_data_clear()
Output2 = bpy.data.objects.get("output2")
Output2.animation_data_clear()
J = bpy.data.objects.get("J")
J.animation_data_clear()
Jgear = bpy.data.objects.get("J_gear")
Jgear.animation_data_clear()
K = bpy.data.objects.get("K")
K.animation_data_clear()
Output3 = bpy.data.objects.get("output3")
Output3.animation_data_clear()
M = bpy.data.objects.get("M")
M.animation_data_clear()
Mgear = bpy.data.objects.get("M_gear")
Mgear.animation_data_clear()
N = bpy.data.objects.get("N")
N.animation_data_clear()
P = bpy.data.objects.get("P")
P.animation_data_clear()
Output4 = bpy.data.objects.get("output4")
Output4.animation_data_clear()
Q = bpy.data.objects.get("Q")
Q.animation_data_clear()
R = bpy.data.objects.get("R")
R.animation_data_clear()
S = bpy.data.objects.get("S")
S.animation_data_clear()
T = bpy.data.objects.get("T")
T.animation_data_clear()
Output5 = bpy.data.objects.get("output5")
Output5.animation_data_clear()
UpdaterLeft = bpy.data.objects.get("UpdaterLeft")
UpdaterLeft.animation_data_clear()
UpdaterRight = bpy.data.objects.get("UpdaterRight")
UpdaterRight.animation_data_clear()
OutputActuatorCenter = bpy.data.objects.get("OutputActuatorCenter")
UpdaterLeftCenter = bpy.data.objects.get("UpdaterLeftCenter")
UpdaterRightCenter = bpy.data.objects.get("UpdaterRightCenter")
StitchOutputLocationXZ = bpy.data.objects.get("StitchOutputLocationXZ")
sensorB = bpy.data.objects.get("SensorB")
carriage = bpy.data.objects.get("Carriage")
handles = [bpy.data.objects.get(f"Sensor{k}Handle") for k in ["A", "B", "C"]]  # for showing how sensors work
sensor_labels = [bpy.data.objects.get(f"Label{k}") for k in ["A", "B", "C"]]
input_beams = [bpy.data.objects.get("A_beam"), B, C]
mechanism_parts = [notA, notB, notC, invertA, invertB, invertC, F, Fgear, E, G, H, Output1,
    Output2, J, Jgear, K, Output3, M, Mgear, N, P, Output4, Q, R, S, T, Output5,
    bpy.data.objects.get("OutputActuator")]
sensorsAC = [bpy.data.objects.get("SensorA"), bpy.data.objects.get("SensorC")]
handlesAC = [bpy.data.objects.get(f"Sensor{k}Handle") for k in ["A", "C"]]
handlesB = [bpy.data.objects.get(f"SensorBHandle")]

# rod positions that have hysteresis
output1 = 0
output2 = 0
output4 = 0
output5 = 0

num_pegs = 94
pegs = [bpy.data.objects.get(f"Peg.{peg_idx:03d}") for peg_idx in range(num_pegs)]
temp_pegs = [bpy.data.objects.get(f"TempPeg.{peg_idx:03d}") for peg_idx in range(num_pegs)]
peg_values = [0] * num_pegs
peg_radius = 0.095
travel = 0.2  # how far the inputs move
peg_separation = abs(pegs[1].matrix_world.translation[1] - pegs[0].matrix_world.translation[1])

sensor_square_radius = travel / math.sqrt(2)  # distance from diamond center to edge midpoint

correctors = [bpy.data.objects.get(f"Corrector{idx + 1}") for idx in range(4)]
temp_correctors = [bpy.data.objects.get(f"TempCorrector{idx + 1}") for idx in range(2)]

track_zero = bpy.data.objects.get("TrackZero").matrix_world.translation[0]
track_one = bpy.data.objects.get("TrackOne").matrix_world.translation[0]
temp_zero = bpy.data.objects.get("TempZero").matrix_world.translation[0]
temp_one = bpy.data.objects.get("TempOne").matrix_world.translation[0]

num_stitches = 200
stitches = [bpy.data.objects.get(f"Stitch.{idx:03d}") for idx in range(num_stitches)]
next_available_stitch = 0
last_peg_stitched = -1
stitch_size = 0.2
stitches_on_peg = [[] for i in range(num_pegs)]

peg_slots = [bpy.data.objects.get(f"PegSlot.{idx:03d}") for idx in range(num_pegs)]
temp_peg_slots = [bpy.data.objects.get(f"PegSlot.{idx:03d}") for idx in range(num_pegs, num_pegs*2)]
correctors = [obj for obj in bpy.data.objects if "Corrector" in obj.name]
updaters = [obj for obj in bpy.data.objects if "Updater" in obj.name or "Left" in obj.name or "Right" in obj.name]
carriage_supports = bpy.data.objects.get("CarriageBody")
carriage_stuff = correctors + updaters + [carriage_supports]
track_things = pegs + peg_slots
temp_track_things = temp_pegs + temp_peg_slots


def set_state(a, b, c, left, right, frame):
    global output1, output2, output4, output5

    input_x_offset = 0.1
    fm_x_offset = -0.135
    fm_gear_x_offset = 0.0425
    gh_x_offset = 0.0
    output12_x_offset = 0.43
    j_x_offset = 0.85  
    jgear_x_offset = 0.7
    output3_x_offset = 0.85
    p_x_offset = -0.124
    rotation_factor = math.pi * 0.85  # radians per [0,1] distance travelled for meshing
    output4_x_offset = 0.193
    q_x_offset = 0.705
    t_x_offset = 0.695
    output5_x_offset = 1.16
    updater_x_offset = 0.482

    not_a = 1 - a
    not_b = 1 - b
    not_c = 1 - c
    m = (b + not_a) / 2
    f = (c + not_b) / 2
    g = f * 2 - 1
    h = -g
    p = m * 2 - 1
    output1 = max(g, output1)  # pushed forward by g
    output1 = min(min(c, not_b), output1)  # pulled back by c and not_b
    output2 = max(h, output2)  # pushed forward by h
    output2 = min(min(not_c, b), output2)  # pulled back by not_c and b
    j = (output1 + output2) / 2
    output3 = j * 2
    output4 = max(p, output4)  # pushed forward by p
    output4 = min(min(b, not_a), output4)  # pulled back by b and not_a
    q = (output3 + output4) / 2
    t = q * 2
    output5 = min(t, output5)  # pulled back by t
    output5 = max(max(output3, output4), output5)  # pushed forward by output3 and ouput4
    
    A.location[0] = input_x_offset + a * travel
    A.keyframe_insert(data_path="location", frame=frame, index=0)
    B.location[0] = input_x_offset + b * travel
    B.keyframe_insert(data_path="location", frame=frame, index=0)
    C.location[0] = input_x_offset + c * travel
    C.keyframe_insert(data_path="location", frame=frame, index=0)
    notA.location[0] = input_x_offset + not_a * travel
    notA.keyframe_insert(data_path="location", frame=frame, index=0)
    notB.location[0] = input_x_offset + not_b * travel
    notB.keyframe_insert(data_path="location", frame=frame, index=0)
    notC.location[0] = input_x_offset + not_c * travel
    notC.keyframe_insert(data_path="location", frame=frame, index=0)
    invertA.rotation_euler.y = -a * rotation_factor
    invertA.keyframe_insert(data_path="rotation_euler", frame=frame)
    invertB.rotation_euler.y = b * rotation_factor
    invertB.keyframe_insert(data_path="rotation_euler", frame=frame)
    invertC.rotation_euler.y = -c * rotation_factor
    invertC.keyframe_insert(data_path="rotation_euler", frame=frame)
    F.location[0] = fm_x_offset + f * travel
    F.keyframe_insert(data_path="location", frame=frame, index=0)
    Fgear.location[0] = fm_gear_x_offset + f * travel
    Fgear.keyframe_insert(data_path="location", frame=frame, index=0)
    Fgear.rotation_euler.z = (not_b - c) * rotation_factor / 2
    Fgear.keyframe_insert(data_path="rotation_euler", frame=frame)
    E.rotation_euler.z = -f * rotation_factor
    E.keyframe_insert(data_path="rotation_euler", frame=frame)
    G.location[0] = gh_x_offset + g * travel
    G.keyframe_insert(data_path="location", frame=frame, index=0)
    H.location[0] = gh_x_offset + h * travel
    H.keyframe_insert(data_path="location", frame=frame, index=0)
    Output1.location[0] = output12_x_offset + output1 * travel
    Output1.keyframe_insert(data_path="location", frame=frame, index=0)
    Output2.location[0] = output12_x_offset + output2 * travel
    Output2.keyframe_insert(data_path="location", frame=frame, index=0)
    J.location[0] = j_x_offset + j * travel
    J.keyframe_insert(data_path="location", frame=frame, index=0)
    Jgear.location[0] = jgear_x_offset + j * travel
    Jgear.keyframe_insert(data_path="location", frame=frame, index=0)
    Jgear.rotation_euler.y = (output2 - output1) * rotation_factor / 2
    Jgear.keyframe_insert(data_path="rotation_euler", frame=frame)
    K.rotation_euler.y = -j * rotation_factor
    K.keyframe_insert(data_path="rotation_euler", frame=frame)
    Output3.location[0] = output3_x_offset + output3 * travel
    Output3.keyframe_insert(data_path="location", frame=frame, index=0)
    M.location[0] = fm_x_offset + m * travel
    M.keyframe_insert(data_path="location", frame=frame, index=0)
    Mgear.location[0] = fm_gear_x_offset + m * travel
    Mgear.keyframe_insert(data_path="location", frame=frame, index=0)
    Mgear.rotation_euler.z = (not_a - b) * rotation_factor / 2
    Mgear.keyframe_insert(data_path="rotation_euler", frame=frame)
    N.rotation_euler.z = m * rotation_factor
    N.keyframe_insert(data_path="rotation_euler", frame=frame)
    M.location[0] = fm_x_offset + m * travel
    M.keyframe_insert(data_path="location", frame=frame, index=0)
    P.location[0] = p_x_offset + p * travel
    P.keyframe_insert(data_path="location", frame=frame, index=0)
    Output4.location[0] = output4_x_offset + output4 * travel
    Output4.keyframe_insert(data_path="location", frame=frame, index=0)
    Q.location[0] = q_x_offset + q * travel
    Q.keyframe_insert(data_path="location", frame=frame, index=0)
    Q.rotation_euler.y = (output4 - output3) * rotation_factor / 2
    Q.keyframe_insert(data_path="rotation_euler", frame=frame)
    R.location[0] = j_x_offset + q * travel
    R.keyframe_insert(data_path="location", frame=frame, index=0)
    S.rotation_euler.y = -q * rotation_factor
    S.keyframe_insert(data_path="rotation_euler", frame=frame)
    T.location[0] = t_x_offset + t * travel
    T.keyframe_insert(data_path="location", frame=frame, index=0)
    Output5.location[0] = output5_x_offset + output5 * travel
    Output5.keyframe_insert(data_path="location", frame=frame, index=0)
    UpdaterLeft.location[0] = updater_x_offset - left * travel
    UpdaterLeft.keyframe_insert(data_path="location", frame=frame, index=0)
    UpdaterRight.location[0] = updater_x_offset - right * travel
    UpdaterRight.keyframe_insert(data_path="location", frame=frame, index=0)


def demo_3bit_cycle():
    global frame
    # iterate the carriage through inputs abc: 000, 001, 010, ... , 110, 111, 000
    inputs_int = [0,1,2,3,4,5,6,7,0]
    inputs_bin = [format(v,'03b') for v in inputs_int]

    transition_frames = 40
    static_frames = 10

    old_inputs = '000'
    for inputs in inputs_bin:
        # transition to the new input values
        for i in range(transition_frames):
            u = i / float(transition_frames-1)
            values = [int(old_inputs[j]) * (1-u) + int(inputs[j]) * u for j in range(3)]
            set_state(values[0], values[1], values[2], 0, 0, frame)
            frame += 1
        # a period of stasis
        values = [int(inputs[j]) for j in range(3)]
        for i in range(static_frames):
            set_state(values[0], values[1], values[2], 0, 0, frame)
            frame += 1
        old_inputs = inputs


def set_pegs(peg_values, temp_peg_values):
    """Move each peg to a the specified position in [0, 1]."""
    for peg, peg_value in zip(pegs, peg_values):
        peg.location[0] = track_zero + (track_one - track_zero) * peg_value
    for peg, peg_value in zip(temp_pegs, temp_peg_values):
        peg.location[0] = temp_zero + (temp_one - temp_zero) * peg_value


def keyframe_pegs(frame):
    """Move each peg to a the specified position in [0, 1]."""
    for peg, peg_value in zip(pegs, peg_values):
        peg.location[0] = track_zero + (track_one - track_zero) * peg_value
        peg.keyframe_insert(data_path="location", frame=frame, index=0)
    for peg, peg_value in zip(temp_pegs, temp_peg_values):
        peg.location[0] = temp_zero + (temp_one - temp_zero) * peg_value
        peg.keyframe_insert(data_path="location", frame=frame, index=0)


def get_closest_peg(y_coordinate):
    """Returns the blender object for the peg that is closest to the supplied y-coordinate."""
    return min(pegs, key = lambda peg: abs(peg.matrix_world.translation[1] - y_coordinate))


def get_closest_temp_peg(y_coordinate):
    """Returns the blender object for the peg that is closest to the supplied y-coordinate."""
    return min(temp_pegs, key = lambda peg: abs(peg.matrix_world.translation[1] - y_coordinate))


def sensor_x_to_value(x, is_temp=False):
    """Given a sensor's x-coordinate, what [0,1] is the input position?"""
    if is_temp:
        # track_zero and track_one are their centers, and there's a middle track.
        one_x = temp_zero + travel / 2  # sensor = 1  => sensor is at track zero
        zero_x = temp_one - travel / 2  # sensor = 0  => sensor is at track one
        # print(f"In sensor_x_to_value({x}). zero_x = {zero_x}, one_x = {one_x}, returning {(x - zero_x) / (one_x - zero_x)}")
        return (x - zero_x) / (one_x - zero_x)
    else:
        # track_zero and track_one are their centers, and there's a middle track.
        one_x = track_zero - travel / 2  # sensor = 1  => sensor is at track zero
        zero_x = track_one + travel / 2  # sensor = 0  => sensor is at track one
        # print(f"In sensor_x_to_value({x}). zero_x = {zero_x}, one_x = {one_x}, returning {(x - zero_x) / (one_x - zero_x)}")
        return (x - zero_x) / (one_x - zero_x)


def get_new_input_position(peg, sensor, expected_travel, is_temp=False):
    "The carriage has moved sideways, what should this input rods new position be?"""
    bpy.context.evaluated_depsgraph_get().update()  # (trigger matrix_world updates after moving objects)
    sensor_pos = np.array(sensor.matrix_world.translation)
    peg_pos = np.array(peg.matrix_world.translation)
    if peg_pos[0] > sensor_pos[0]:
        return min(1, max(0, sensor_x_to_value(sensor_pos[0] - expected_travel, is_temp)))
    else:
        return min(1, max(0, sensor_x_to_value(sensor_pos[0] + expected_travel, is_temp)))


def add_stitch_at_current_peg_if_needed(peg, frame):
    global last_peg_stitched, next_available_stitch
    if next_available_stitch >= num_stitches:
        raise RuntimeError("No stitches left to animate")
    peg_idx = int(peg.name.split(".")[-1])
    if last_peg_stitched == peg_idx:  # we did this one already
        # keyframe all existing stitches to their current position
        for old_stitch in stitches[:next_available_stitch]:
            old_stitch.keyframe_insert(data_path="location", frame=frame, index=0)
            old_stitch.keyframe_insert(data_path="location", frame=frame, index=1)
            old_stitch.keyframe_insert(data_path="location", frame=frame, index=2)
        return 
    stitch = stitches[next_available_stitch]
    stitch.location[0] = StitchOutputLocationXZ.matrix_world.translation[0]
    stitch.location[1] = stitch.location[1] + peg.matrix_world.translation[1] - stitch.matrix_world.translation[1]
    stitch.location[2] = StitchOutputLocationXZ.matrix_world.translation[2]
    stitch.hide_viewport = False
    stitch.hide_render = False
    base_color_socket = stitch.data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Base Color"]
    if peg_values[peg_idx] > 0.5:
        stitch.data.materials[0].diffuse_color = dark_yarn
        base_color_socket.default_value = dark_yarn
    else:
        stitch.data.materials[0].diffuse_color = light_yarn
        base_color_socket.default_value = light_yarn
    stitch.data.materials[0].keyframe_insert(data_path="diffuse_color", frame=frame)
    base_color_socket.keyframe_insert(data_path="default_value", frame=frame)
    stitch.keyframe_insert(data_path="location", frame=frame, index=0)
    stitch.keyframe_insert(data_path="location", frame=frame, index=1)
    stitch.keyframe_insert(data_path="location", frame=frame, index=2)
    stitch.keyframe_insert(data_path="hide_viewport", frame=frame)
    stitch.keyframe_insert(data_path="hide_render", frame=frame)
    stitches_on_peg[peg_idx].append(stitch)
    last_peg_stitched = peg_idx    
    next_available_stitch += 1


def move_stitches_down(frame): 
    for stitch_list in stitches_on_peg:
        for stitch in stitch_list:
            stitch.location[2] += stitch_size * 2 
            stitch.keyframe_insert(data_path="location", frame=frame, index=2)


def set_carriage_state_from_pegs(frame, frames_per_peg):
    """Given the current position of the carriage and the input pegs, set the internal carriage state to match."""
    # set the inputs based on the closest pegs (TODO: animate pushing properly)
    bpy.context.evaluated_depsgraph_get().update()  # (trigger matrix_world updates after moving objects)
    sensorA = bpy.data.objects.get("SensorA")
    sensorB = bpy.data.objects.get("SensorB")
    sensorC = bpy.data.objects.get("SensorC")
    sensorLeft = bpy.data.objects.get("SensorLeft")
    sensorRight = bpy.data.objects.get("SensorRight")
    pegA = get_closest_peg(sensorA.matrix_world.translation[1])
    pegB = get_closest_peg(sensorB.matrix_world.translation[1])
    pegC = get_closest_peg(sensorC.matrix_world.translation[1])
    pegLeft = get_closest_temp_peg(sensorLeft.matrix_world.translation[1])
    pegRight = get_closest_temp_peg(sensorRight.matrix_world.translation[1])
    expected_travel = peg_separation / frames_per_peg  # since sensors have 45 degree angles
    a = get_new_input_position(pegA, sensorA, expected_travel)
    b = get_new_input_position(pegB, sensorB, expected_travel)
    c = get_new_input_position(pegC, sensorC, expected_travel)
    left = get_new_input_position(pegLeft, sensorLeft, expected_travel, True)
    right = get_new_input_position(pegRight, sensorRight, expected_travel, True)
    #print(f"Would set left = {left}, right = {right}")
    set_state(a, b, c, left, right, frame)
    add_stitch_at_current_peg_if_needed(pegB, frame)
    bpy.context.evaluated_depsgraph_get().update()  # (trigger matrix_world updates after moving objects)
    # print(f"After setting state got sensorC.matrix_world.translation[0] == {sensorC.matrix_world.translation[0]}")


def update_pegs(frame):
    """Push the pegs where moved by actuators, correctors and maybe sensors."""
    # actuators
    output_actuator_x = OutputActuatorCenter.matrix_world.translation[0]
    output_actuator_y = OutputActuatorCenter.matrix_world.translation[1]
    peg = get_closest_temp_peg(output_actuator_y)
    peg_x = peg.matrix_world.translation[0]
    peg_y = peg.matrix_world.translation[1]
    y_difference = abs(peg_y - output_actuator_y)
    allowed_x_range = [output_actuator_x - y_difference, output_actuator_x + y_difference]
    new_peg_x = min(allowed_x_range[1], max(allowed_x_range[0], peg_x))
    new_peg_value = (new_peg_x - temp_zero) / (temp_one - temp_zero)
    temp_peg_values[temp_pegs.index(peg)] = new_peg_value
    # updater actuators
    for actuator in [UpdaterLeftCenter, UpdaterRightCenter]:
        actuator_x = actuator.matrix_world.translation[0]
        actuator_y = actuator.matrix_world.translation[1]
        peg = get_closest_peg(actuator_y)
        peg_x = peg.matrix_world.translation[0]
        peg_y = peg.matrix_world.translation[1]
        y_difference = abs(peg_y - actuator_y)
        allowed_x_range = [actuator_x - y_difference, actuator_x + y_difference]
        new_peg_x = min(allowed_x_range[1], max(allowed_x_range[0], peg_x))
        new_peg_value = (new_peg_x - track_zero) / (track_one - track_zero)
        peg_values[pegs.index(peg)] = new_peg_value
    # main tape correctors
    for corrector in correctors:
        corrector_x = corrector.matrix_world.translation[0]
        corrector_y = corrector.matrix_world.translation[1]
        peg = get_closest_peg(corrector_y)
        peg_x = peg.matrix_world.translation[0]
        peg_y = peg.matrix_world.translation[1]
        corrector_half_width = travel / 2
        y_difference = abs(peg_y - corrector_y)
        if y_difference < corrector_half_width + peg_radius:  # (otherwise no effect)
            if peg_x > corrector_x:
                new_peg_x = max(peg_x, corrector_x - y_difference + corrector_half_width + peg_radius)
            else:
                new_peg_x = min(peg_x, corrector_x + y_difference - corrector_half_width - peg_radius)
            new_peg_value = (new_peg_x - track_zero) / (track_one - track_zero)
            peg_values[pegs.index(peg)] = new_peg_value
    # temp tape correctors
    for corrector in temp_correctors:
        corrector_x = corrector.matrix_world.translation[0]
        corrector_y = corrector.matrix_world.translation[1]
        peg = get_closest_temp_peg(corrector_y)
        peg_x = peg.matrix_world.translation[0]
        peg_y = peg.matrix_world.translation[1]
        corrector_half_width = travel / 2
        y_difference = abs(peg_y - corrector_y)
        if y_difference < corrector_half_width + peg_radius:  # (otherwise no effect)
            if peg_x > corrector_x:
                new_peg_x = max(peg_x, corrector_x - y_difference + corrector_half_width + peg_radius)
            else:
                new_peg_x = min(peg_x, corrector_x + y_difference - corrector_half_width - peg_radius)
            new_peg_value = (new_peg_x - temp_zero) / (temp_one - temp_zero)
            temp_peg_values[temp_pegs.index(peg)] = new_peg_value
    # finally set keyframes for all pegs in this frame
    keyframe_pegs(frame)


def animate_carriage(start_peg_idx, end_peg_idx, num_passes=1, frames_per_peg=20, move_pegs=True):
    global frame, last_peg_stitched
    """peg_start and peg_end are indices of the peg to be at SensorB"""
    total_number_of_stitches_produced = (abs(end_peg_idx - start_peg_idx) + 1) * num_passes
    if total_number_of_stitches_produced > num_stitches:
        raise RuntimeError(f"Too many stitches expected: {total_number_of_stitches_produced} > {num_stitches}")
    num_frames_per_pass = abs(end_peg_idx - start_peg_idx) * frames_per_peg + 1
    start_peg = bpy.data.objects.get(f"Peg.{start_peg_idx:03d}")
    end_peg = bpy.data.objects.get(f"Peg.{end_peg_idx:03d}")
    # animate the carriage movement
    carriage_offset = carriage.location[1] - sensorB.matrix_world.translation[1]
    # with current approach for pretend-physics we need to start the carriage in a valid (non-overlapping) state
    a = b = c = 0
    left = right = 0
    set_state(a, b, c, left, right, frame)
    if move_pegs:
        update_pegs(frame)
    bpy.context.evaluated_depsgraph_get().update()  # (trigger matrix_world updates after moving objects)
    for pass_idx in range(num_passes):
        for pass_frame in range(num_frames_per_pass):
            # print("\nSetting inputs for new carriage position.\n")
            if (pass_idx % 2) == 0:
                carriage.location[1] = carriage_offset + start_peg.matrix_world.translation[1] + (end_peg.matrix_world.translation[1] - start_peg.matrix_world.translation[1]) * pass_frame / (num_frames_per_pass - 1)
            else:
                carriage.location[1] = carriage_offset + end_peg.matrix_world.translation[1] + (start_peg.matrix_world.translation[1] - end_peg.matrix_world.translation[1]) * pass_frame / (num_frames_per_pass - 1)
            carriage.keyframe_insert(data_path="location", frame=frame, index=1)
            set_carriage_state_from_pegs(frame, frames_per_peg)
            if move_pegs:
                update_pegs(frame)
            frame += 1
        # prepare for next pass
        last_peg_stitched = -1
        move_stitches_down(frame)


def keyframe_visibility(objects, is_hidden, frame):
    for obj in objects:
        obj.hide_viewport = is_hidden
        obj.hide_render = is_hidden
        obj.keyframe_insert(data_path="hide_viewport", frame=frame)
        obj.keyframe_insert(data_path="hide_render", frame=frame)
            

os.system("cls")

bpy.context.scene.frame_set(0)

# clear keyframes on everything
for obj in bpy.data.objects:
    obj.animation_data_clear()
# also on those materials that are animated
for stitch in stitches:
    stitch.data.materials[0].animation_data_clear()  # clear the animation of the viewport color
    stitch.data.materials[0].node_tree.animation_data_clear()  # clear the animation of the rendered color

peg_values[46] = 1  # the initial 1 in the rule110 input pattern
peg_values[42] = 1  # the initial 1 in the rule110 input pattern
peg_values[41] = 1  # the initial 1 in the rule110 input pattern
temp_peg_values = [v for v in peg_values]  # keep it in sync with the main tape
set_pegs(peg_values, temp_peg_values)

frame = 0
keyframe_pegs(frame)

# show how a single sensor worka
keyframe_visibility(carriage_stuff + stitches + input_beams + mechanism_parts + sensor_labels + sensorsAC + handlesAC + temp_track_things, is_hidden=True, frame=frame)
keyframe_visibility(track_things + handlesB, is_hidden=False, frame=frame)
animate_carriage(34, 49, num_passes=2, frames_per_peg=10, move_pegs=False)

# show how three sensors work
keyframe_visibility(carriage_stuff + stitches + input_beams + mechanism_parts, is_hidden=True, frame=frame)
keyframe_visibility(track_things + handles + sensor_labels + sensorsAC, is_hidden=False, frame=frame)
animate_carriage(34, 49, num_passes=2, frames_per_peg=10, move_pegs=False)

# show how the central mechanism works
keyframe_visibility(track_things + carriage_stuff + stitches + handles, is_hidden=True, frame=frame)
keyframe_visibility(sensorsAC + sensor_labels + input_beams + mechanism_parts, is_hidden=False, frame=frame)
demo_3bit_cycle() 

# show the whole system in action
keyframe_pegs(frame - 1)  # should probably get used to keyframing everything on every frame even where unmoved and not visible

peg_values = [0] * num_pegs
peg_values[46] = 1  # the initial 1 in the rule110 input pattern
temp_peg_values = [v for v in peg_values]  # keep it in sync with the main tape
set_pegs(peg_values, temp_peg_values)

keyframe_visibility(track_things + carriage_stuff + temp_track_things, is_hidden=False, frame=frame)
keyframe_pegs(frame)
animate_carriage(34, 51, num_passes=2, frames_per_peg=10, move_pegs=True)

bpy.data.scenes[0].frame_start = 0
bpy.data.scenes[0].frame_end = frame - 1
bpy.context.scene.frame_set(0)
