import bpy
import math
import numpy as np
import os

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
L = bpy.data.objects.get("L")
L.animation_data_clear()
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

# rod positions that have hysteresis
a = 0
b = 0
c = 0
output1 = 0
output2 = 0
output4 = 0
output5 = 0

num_pegs = 94
pegs = [bpy.data.objects.get(f"Peg.{peg_idx:03d}") for peg_idx in range(num_pegs)]
temp_pegs = [bpy.data.objects.get(f"TempPeg.{peg_idx:03d}") for peg_idx in range(num_pegs)]
peg_radius = 0.095
travel = 0.2  # how far the inputs move
peg_separation = abs(pegs[1].matrix_world.translation[1] - pegs[0].matrix_world.translation[1])
sensor_square_radius = travel / math.sqrt(2)  # distance from diamond center to edge midpoint

track_zero = bpy.data.objects.get("TrackZero").matrix_world.translation[0]
track_one = bpy.data.objects.get("TrackOne").matrix_world.translation[0]
temp_zero = bpy.data.objects.get("TempZero").matrix_world.translation[0]
temp_one = bpy.data.objects.get("TempOne").matrix_world.translation[0]


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
    updater_x_offset = 0.494529

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
    L.rotation_euler.y = (g - h) * rotation_factor / 4
    L.keyframe_insert(data_path="rotation_euler", frame=frame)
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
    # iterate the carriage through inputs abc: 000, 001, 010, ... , 110, 111, 000
    inputs_int = [0,1,2,3,4,5,6,7,0]
    inputs_bin = [format(v,'03b') for v in inputs_int]

    transition_frames = 40
    static_frames = 10

    frame = 0
    old_inputs = '000'
    for inputs in inputs_bin:
        # transition to the new input values
        for i in range(transition_frames):
            u = i / float(transition_frames-1)
            values = [int(old_inputs[j]) * (1-u) + int(inputs[j]) * u for j in range(3)]
            set_state(*values, frame)
            frame += 1
        # a period of stasis
        values = [int(inputs[j]) for j in range(3)]
        for i in range(static_frames):
            set_state(values[0], values[1], values[2], 0, 0, frame)
            frame += 1
        old_inputs = inputs

    bpy.data.scenes[0].frame_start = 0
    bpy.data.scenes[0].frame_end = frame - 1
    # update the scene to the current frame
    bpy.context.scene.frame_set(bpy.context.scene.frame_current)


def set_input_pegs(peg_values):
    """Move each input peg to a [0,1] position."""
    for peg_idx, peg_value in enumerate(peg_values):
        peg = bpy.data.objects.get(f"Peg.{peg_idx:03d}")
        peg.animation_data_clear()
        peg.location[0] = track_zero + (track_one - track_zero) * peg_value
        # Duplicate onto the temp teack
        temp_peg = bpy.data.objects.get(f"TempPeg.{peg_idx:03d}")
        temp_peg.animation_data_clear()
        temp_peg.location[0] = temp_zero + (temp_one - temp_zero) * peg_value
        # temp_peg.location[1] = peg.location[1]  # fix the y-alignment (was only needed once)


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
        one_x = temp_zero - travel / 2  # sensor = 1  => sensor is at track zero
        zero_x = temp_one + travel / 2  # sensor = 0  => sensor is at track one
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
    # TODO: just a simple technique for now, couldn't get pretend physics to work
    #new_ = sensor_x_to_value(sensor_pos[0], is_temp)
    if peg_pos[0] > sensor_pos[0]:
        return min(1, max(0, sensor_x_to_value(sensor_pos[0] - expected_travel, is_temp)))
    else:
        return min(1, max(0, sensor_x_to_value(sensor_pos[0] + expected_travel, is_temp)))
    # iteratively tweak sensor_pos until no more overlap
    # (an analytic solution certainly exists but it was too hard to work out)
    print(f"sensor_pos = {sensor_pos}  peg_pos = {peg_pos}")
    while True:
        # vector from sensor center to peg center
        v = peg_pos - sensor_pos
        v[2] = 0
        # rotate 45 degrees around the z-axis so that the sensor is now axis-aligned (and ignore z-coordinate)
        rotated_peg_pos = np.array([math.sqrt(2) * (v[0] - v[1]) / 2, math.sqrt(2) * (v[0] + v[1]) / 2, 0])
        # clamp to lie in/on the sensor
        p = np.clip(rotated_peg_pos, -sensor_square_radius, sensor_square_radius)
        # test if this point is inside the peg
        d = np.linalg.norm(p - rotated_peg_pos)
        print(f"v = {v}  p = {p}  rotated_peg_pos = {rotated_peg_pos}  d = {d}  peg_radius = {peg_radius}  sensor_square_radius = {sensor_square_radius}\n")
        if d > peg_radius:
            print(f"sensor_pos = {sensor_pos}  peg_pos = {peg_pos}")
            print(f"|sensor_pos.x - peg_pos.x| = {abs(sensor_pos[0] - peg_pos[0])}")
            print("sensor not touching peg")
            break  # sensor does not overlap peg and more, we are done
        if peg_pos[0] > sensor_pos[0]:
            sensor_pos[0] -= peg_radius / 10
        if peg_pos[0] < sensor_pos[0]:  
            sensor_pos[0] += peg_radius / 10
        new_value = sensor_x_to_value(sensor_pos[0])
        print(f"Moved sensor. sensor_pos = {sensor_pos}  new_value = {new_value}")
        if new_value < 0 or new_value > 1:
            print(f"WARNING: sensor was pushed off the track! Will clip value")
            break
    new_value = sensor_x_to_value(sensor_pos[0])
    new_value = min(max(new_value, 0), 1)
    print(f"get_new_input_position() returning {new_value}")
    return new_value


def set_carriage_state_from_input_pegs(frame, frames_per_peg):
    """Given the current position of the carriage and the input pegs, set the internal carriage state to match."""
    global a, b, c  # the inputs before the carriage moved to this position (hysteresis)
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
    bpy.context.evaluated_depsgraph_get().update()  # (trigger matrix_world updates after moving objects)
    # print(f"After setting state got sensorC.matrix_world.translation[0] == {sensorC.matrix_world.translation[0]}")


def animate_carriage(start_peg_idx, end_peg_idx, frames_per_peg=20):
    """peg_start and peg_end are indices of the peg to be at SensorB"""
    num_frames = abs(end_peg_idx - start_peg_idx) * frames_per_peg + 1
    bpy.data.scenes[0].frame_start = 0
    bpy.data.scenes[0].frame_end = num_frames - 1
    start_peg = bpy.data.objects.get(f"Peg.{start_peg_idx:03d}")
    end_peg = bpy.data.objects.get(f"Peg.{end_peg_idx:03d}")
    # animate the carriage movement
    carriage = bpy.data.objects.get("Carriage")
    carriage.animation_data_clear()
    sensorB = bpy.data.objects.get("SensorB")
    sensorB.animation_data_clear()
    carriage_offset = carriage.location[1] - sensorB.matrix_world.translation[1]
    a = b = c = 0
    left = right = 0 
    set_state(a, b, c, left, right, 0)
    bpy.context.evaluated_depsgraph_get().update()  # (trigger matrix_world updates after moving objects)
    for frame in range(num_frames):
        # print("\nSetting inputs for new carriage position.\n")
        carriage.location[1] = carriage_offset + start_peg.matrix_world.translation[1] + (end_peg.matrix_world.translation[1] - start_peg.matrix_world.translation[1]) * frame / (num_frames - 1)
        carriage.keyframe_insert(data_path="location", frame=frame, index=1)
        set_carriage_state_from_input_pegs(frame, frames_per_peg)
    # finally update the scene to the current frame
    bpy.context.scene.frame_set(bpy.context.scene.frame_current)
    print("Done")


os.system("cls")
peg_values = [0] * num_pegs
peg_values[46] = 1
set_input_pegs(peg_values)
#demo_3bit_cycle() 
animate_carriage(42, 49, frames_per_peg = 30)
