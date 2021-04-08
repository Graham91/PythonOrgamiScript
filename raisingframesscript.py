import bpy
import mathutils

centralObjectArray = bpy.context.scene['CentralObjectArray']
CentralHeightArray = bpy.context.scene['CentralHeightArray']
multipler = bpy.context.scene['Multipler']
beginframe = bpy.context.scene['beginFrame']

frameChanger = beginframe + 23
for index, objectName in enumerate(centralObjectArray):
    object = bpy.data.objects[objectName]
    heightraiser = CentralHeightArray[index] + 5
    object.keyframe_insert(data_path='location', frame=(beginframe))
    loc = object.location
    (x,y,z) = (0,0,5)
    object.location = loc + mathutils.Vector((x,y,z))
    object.keyframe_insert(data_path='location', frame=(beginframe + 20))
    object.keyframe_insert(data_path='location', frame=(frameChanger))
    frameChanger += 5
    