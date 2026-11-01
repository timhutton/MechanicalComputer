import bpy
import math

num_frames = 201
bpy.data.scenes[0].frame_start = 0
bpy.data.scenes[0].frame_end = num_frames

keyframes = [
        {'frame':0, 'a':0, 'b':0, 'c':0},
        {'frame':50, 'a':1, 'b':0, 'c':0},
        {'frame':60, 'a':1, 'b':0, 'c':0},
        {'frame':100, 'a':1, 'b':1, 'c':0},
        {'frame':110, 'a':1, 'b':1, 'c':0},
        {'frame':150, 'a':0, 'b':1, 'c':0},
        {'frame':160, 'a':0, 'b':1, 'c':0},
        {'frame':200, 'a':0, 'b':0, 'c':0}]
        
A = bpy.data.objects.get("A")
A.animation_data_clear()
B = bpy.data.objects.get("B")
B.animation_data_clear()
notA = bpy.data.objects.get("not_A")
notA.animation_data_clear()
notB = bpy.data.objects.get("not_B")
notB.animation_data_clear()
invertA = bpy.data.objects.get("invert_A")
invertA.animation_data_clear()
invertB = bpy.data.objects.get("invert_B")
invertB.animation_data_clear()
C = bpy.data.objects.get("C")
C.animation_data_clear()
Cgear = bpy.data.objects.get("C_gear")
Cgear.animation_data_clear()
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

travel = 0.2  # how far the inputs move
input_x_offset = 0.1
cd_x_offset = -0.135
cd_gear_x_offset = 0.16
gh_x_offset = 0.0
output12_x_offset = 0.43
j_x_offset = 0.59 
jgear_x_offset = 0.7
output3_x_offset = 0.85
rotation_factor = math.pi * 0.85  # radians per [0,1] distance travelled for meshing

for keyframe in keyframes:
    frame = keyframe['frame']
    a = keyframe['a']
    b = keyframe['b']
    not_a = 1 - a
    not_b = 1 - b
    c = (a + not_b) / 2
    g = c * 2 - 1
    h = -g
    output1 = max(g, min(a, not_b))  # pulled back by a and not_b, pushed forward by g
    output2 = max(h, min(not_a, b))  # pulled back by not_a and b, pushed forward by h
    j = (output1 + output2) / 2
    A.location[0] = input_x_offset + a * travel
    A.keyframe_insert(data_path="location", frame=frame, index=0)
    B.location[0] = input_x_offset + b * travel
    B.keyframe_insert(data_path="location", frame=frame, index=0)
    notA.location[0] = input_x_offset + not_a * travel
    notA.keyframe_insert(data_path="location", frame=frame, index=0)
    notB.location[0] = input_x_offset + not_b * travel
    notB.keyframe_insert(data_path="location", frame=frame, index=0)
    invertA.rotation_euler.y = -a * rotation_factor
    invertA.keyframe_insert(data_path="rotation_euler", frame=frame)
    invertB.rotation_euler.y = b * rotation_factor
    invertB.keyframe_insert(data_path="rotation_euler", frame=frame)
    C.location[0] = cd_x_offset + c * travel
    C.keyframe_insert(data_path="location", frame=frame, index=0)
    Cgear.location[0] = cd_gear_x_offset + c * travel
    Cgear.keyframe_insert(data_path="location", frame=frame, index=0)
    Cgear.rotation_euler.z = (not_b - a) * rotation_factor / 2
    Cgear.keyframe_insert(data_path="rotation_euler", frame=frame)
    E.rotation_euler.z = -c * rotation_factor
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
    K.rotation_euler.y = j * rotation_factor
    K.keyframe_insert(data_path="rotation_euler", frame=frame)
    L.rotation_euler.y = (g - h) * rotation_factor / 4
    L.keyframe_insert(data_path="rotation_euler", frame=frame)
    Output3.location[0] = output3_x_offset + 2 * j * travel
    Output3.keyframe_insert(data_path="location", frame=frame, index=0)
