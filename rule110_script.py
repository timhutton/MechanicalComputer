import bpy
import math

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

# initialize the rods that are undefined during some transitions
output1 = 0
output2 = 0
output3 = 0  # (this one doesn't need to be global)
output4 = 0
output5 = 0

num_pegs = 94


def set_state(a, b, c, frame):
    global output1, output2, output3, output4, output5

    travel = 0.2  # how far the inputs move

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
            set_state(*values, frame)
            frame += 1
        old_inputs = inputs

    bpy.data.scenes[0].frame_start = 0
    bpy.data.scenes[0].frame_end = frame - 1


def set_input_pegs(peg_values):
    # move each input peg to a [0,1] position
    track_zero = bpy.data.objects.get("TrackZero").location[0]
    track_one = bpy.data.objects.get("TrackOne").location[0]
    for peg_idx, peg_value in enumerate(peg_values):
        peg = bpy.data.objects.get(f"Peg.{peg_idx:03d}")
        peg.animation_data_clear()
        peg.location[0] = track_zero + (track_one - track_zero) * peg_value
        

set_input_pegs([0,1]*(num_pegs//2))
#demo_3bit_cycle()