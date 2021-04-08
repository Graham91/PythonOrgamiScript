import bpy

foo_objs2 = [obj.name for obj in bpy.data.objects if obj.name.startswith("Sphere")]
print(foo_objs2)

def addpaintbrushes():
 for name in foo_objs2:
  some_obj = bpy.data.objects[name]
  bpy.context.view_layer.objects.active = some_obj
  print(some_obj)
  
  some_obj.modifiers.new(name='Dynamic Paint', type='DYNAMIC_PAINT')
  some_obj.modifiers.new(name='Smoke', type='SMOKE')
  some_obj.modifiers["Smoke"].smoke_type = 'FLOW'
  some_obj.modifiers['Dynamic Paint'].ui_type = 'BRUSH' 
  bpy.ops.dpaint.type_toggle(type='BRUSH') 
  bpy.context.object.modifiers["Smoke"].flow_settings.smoke_color = (0.7, 0.195761, 0.115268) 
  some_obj.modifiers['Dynamic Paint'].brush_settings.paint_color = (0, 0, 0)                                                    
  some_obj.modifiers['Dynamic Paint'].brush_settings.paint_source = 'VOLUME_DISTANCE'            
  some_obj.modifiers["Dynamic Paint"].brush_settings.invert_proximity = True
  some_obj.modifiers["Dynamic Paint"].brush_settings.paint_alpha = 0
  some_obj.modifiers["Dynamic Paint"].brush_settings.keyframe_insert(data_path="paint_alpha", frame=186)
  some_obj.modifiers["Dynamic Paint"].brush_settings.paint_alpha = 1
  some_obj.modifiers["Dynamic Paint"].brush_settings.keyframe_insert(data_path="paint_alpha", frame=196)
  some_obj.modifiers["Dynamic Paint"].brush_settings.paint_distance = 0.001
  bpy.context.view_layer.objects.active = None
        
def deletepaint():
    for name in foo_objs2:
       some_obj = bpy.data.objects[name]
       bpy.context.view_layer.objects.active = some_obj
       if "Dynamic Paint" in some_obj.modifiers:
              some_obj.modifiers.remove(some_obj.modifiers['Dynamic Paint'])

addpaintbrushes()
