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
D = bpy.data.objects.get("D")
D.animation_data_clear()
Cgear = bpy.data.objects.get("C_gear")
Cgear.animation_data_clear()
Dgear = bpy.data.objects.get("D_gear")
Dgear.animation_data_clear()

travel = 0.2  # how far the inputs move
input_x_offset = 0.3
cd_x_offset = 0.1
cd_gear_x_offset = 0.25

for keyframe in keyframes:
    frame = keyframe['frame']
    a = keyframe['a']
    b = keyframe['b']
    not_a = 1 - a
    not_b = 1 - b
    c = (a + not_b) / 2
    d = (not_a + b) / 2
    A.location[0] = input_x_offset + a * travel
    A.keyframe_insert(data_path="location", frame=frame, index=0)
    B.location[0] = input_x_offset + b * travel
    B.keyframe_insert(data_path="location", frame=frame, index=0)
    notA.location[0] = input_x_offset + not_a * travel
    notA.keyframe_insert(data_path="location", frame=frame, index=0)
    notB.location[0] = input_x_offset + not_b * travel
    notB.keyframe_insert(data_path="location", frame=frame, index=0)
    invertA.rotation_euler.y = -a * math.pi
    invertA.keyframe_insert(data_path="rotation_euler", frame=frame)
    invertB.rotation_euler.y = b * math.pi
    invertB.keyframe_insert(data_path="rotation_euler", frame=frame)
    C.location[0] = cd_x_offset + c * travel
    C.keyframe_insert(data_path="location", frame=frame, index=0)
    D.location[0] = cd_x_offset + d * travel
    D.keyframe_insert(data_path="location", frame=frame, index=0)
    Cgear.location[0] = cd_gear_x_offset + c * travel
    Cgear.keyframe_insert(data_path="location", frame=frame, index=0)
    Cgear.rotation_euler.z = (not_b - a) * math.pi / 2
    Cgear.keyframe_insert(data_path="rotation_euler", frame=frame)
    Dgear.location[0] = cd_gear_x_offset + d * travel
    Dgear.keyframe_insert(data_path="location", frame=frame, index=0)
    Dgear.rotation_euler.z = (not_a - b) * math.pi / 2
    Dgear.keyframe_insert(data_path="rotation_euler", frame=frame)
