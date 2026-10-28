import bpy
import math

num_frames = 201
bpy.data.scenes[0].frame_start = 0
bpy.data.scenes[0].frame_end = num_frames

keyframes = [
        {'frame':0, 'a':0, 'b':0, 'c':0},
        {'frame':50, 'a':1, 'b':0, 'c':0},
        {'frame':100, 'a':1, 'b':1, 'c':0},
        {'frame':150, 'a':0, 'b':1, 'c':0},
        {'frame':200, 'a':0, 'b':0, 'c':0}]
        
A = bpy.data.objects.get("A")
B = bpy.data.objects.get("B")
notA = bpy.data.objects.get("not_A")
notB = bpy.data.objects.get("not_B")
d = 0.2  # how far the inputs move
x_offset = 0.3

for keyframe in keyframes:
    a = keyframe['a']
    b = keyframe['b']
    not_a = 1-a
    not_b = 1-b
    A.location[0] = x_offset + a*d
    A.keyframe_insert(data_path="location", frame=keyframe['frame'], index=0)
    B.location[0] = x_offset + b*d
    B.keyframe_insert(data_path="location", frame=keyframe['frame'], index=0)
    notA.location[0] = x_offset + not_a*d
    notA.keyframe_insert(data_path="location", frame=keyframe['frame'], index=0)
    notB.location[0] = x_offset + not_b*d
    notB.keyframe_insert(data_path="location", frame=keyframe['frame'], index=0)
