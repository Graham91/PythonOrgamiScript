import bpy


class objectInfo:
  def __init__(self, initialObject, length, startFrame, endFrame, name, curve, height, smokeObject, paintObject):
    self.initialObject = initialObject
    self.length = length
    self.startFrame = startFrame
    self.endFrame = endFrame
    self.name = name
    self.height = height
    self.curve = curve
    self.smokeobject = smokeObject
    self.paintObject = paintObject
    
objectArrayInfo = []  

def recreateObjectArray ():
    initialObjectArray = bpy.context.scene['InitialObjectArray']
    lengthArray = bpy.context.scene['LengthArray']
    startFrameArray = bpy.context.scene['StartFrameArray']
    endFrameArray= bpy.context.scene['EndFrameArray']
    nameArray = bpy.context.scene['NameArray']
    curveArray = bpy.context.scene['CurveArray']
    heightArray = bpy.context.scene['HeightArray']
    smokeObjectArray = bpy.context.scene['SmokeObjectArray']  
    paintObjectArray = bpy.context.scene['PaintObjectArray']
    for index, objectName in enumerate(initialObjectArray):
       newObject = objectInfo(objectName, lengthArray[index], startFrameArray[index], endFrameArray[index], nameArray[index], curveArray[index], heightArray[index], smokeObjectArray[index], paintObjectArray[index])
       objectArrayInfo.append(newObject)
       

def addPaintBrushes(objectName, start, end):
    some_obj = bpy.data.objects[objectName]
    startframe = start - 1  
    bpy.context.view_layer.objects.active = some_obj
    some_obj.modifiers.new(name='Dynamic Paint', type='DYNAMIC_PAINT')
    some_obj.modifiers['Dynamic Paint'].ui_type = 'BRUSH' 
    bpy.ops.dpaint.type_toggle(type='BRUSH') 
    some_obj.modifiers['Dynamic Paint'].brush_settings.paint_color = (0, 0, 0)                                                    
    some_obj.modifiers['Dynamic Paint'].brush_settings.paint_source = 'VOLUME_DISTANCE'            
    some_obj.modifiers["Dynamic Paint"].brush_settings.invert_proximity = True
    some_obj.modifiers["Dynamic Paint"].brush_settings.paint_alpha = 0
    some_obj.modifiers["Dynamic Paint"].brush_settings.keyframe_insert(data_path="paint_alpha", frame= startframe)
    some_obj.modifiers["Dynamic Paint"].brush_settings.paint_alpha = 1
    some_obj.modifiers["Dynamic Paint"].brush_settings.keyframe_insert(data_path="paint_alpha", frame= start)
    some_obj.modifiers["Dynamic Paint"].brush_settings.paint_alpha = 0
    some_obj.modifiers["Dynamic Paint"].brush_settings.keyframe_insert(data_path="paint_alpha", frame= end)
    some_obj.modifiers["Dynamic Paint"].brush_settings.paint_distance = 0.001
    bpy.context.view_layer.objects.active = None

def addSmoke(objectName, start, end):
    some_obj = bpy.data.objects[objectName]
    startframe = start - 1  
    bpy.context.view_layer.objects.active = some_obj
    some_obj.modifiers.new(name='Smoke', type='FLUID')
    some_obj.modifiers['Smoke'].fluid_type = 'FLOW'
    some_obj.modifiers['Smoke'].flow_settings.flow_type = 'SMOKE'
    
    #some_obj.modifiers["Dynamic Paint"].brush_settings.paint_alpha = 0
    #some_obj.modifiers["Dynamic Paint"].brush_settings.keyframe_insert(data_path="paint_alpha", frame= startframe)
    #some_obj.modifiers["Dynamic Paint"].brush_settings.paint_alpha = 1
    #some_obj.modifiers["Dynamic Paint"].brush_settings.keyframe_insert(data_path="paint_alpha", frame= start)
    #some_obj.modifiers["Dynamic Paint"].brush_settings.paint_alpha = 0
    #some_obj.modifiers["Dynamic Paint"].brush_settings.keyframe_insert(data_path="paint_alpha", frame= end) 
    
recreateObjectArray()  

class TestObjectInfo:
  def __init__(self, startFrame, endFrame, smokeObject, paintObject):
    self.startFrame = startFrame
    self.endFrame = endFrame
    self.smokeObject = smokeObject
    self.paintObject = paintObject
    
#newobject = TestObjectInfo(0, 100, "SmokeSphere", "Sphere")   
#objectArrayInfo.append(newobject)

for objectInfo in objectArrayInfo:
    start = objectInfo.startFrame
    end = objectInfo.endFrame
    smokeObject = objectInfo.smokeObject
    paintObject = objectInfo.paintObject
    addPaintBrushes(paintObject, start, end)
    #addSmoke(smokeObject, start, end)