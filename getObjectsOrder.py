import bpy
import fnmatch
from mathutils import Matrix, Vector

scene = bpy.context.scene

foo_objs2 = [obj for obj in bpy.data.objects if obj.name.startswith("Torus")]

objectHeightList = []
newNameList = []

class Obj:
  def __init__(self, name, height):
    self.name = name
    self.height = height

for x in foo_objs2:
  coords = [(x.matrix_world @ v.co) for v in x.data.vertices]
  newObj = []
  for Y in coords:
      newObj.append(Y.z)
  HighestValue = max(newObj)
  newObj = Obj(x.name, HighestValue)
  objectHeightList.append(newObj)
  
objectHeightList.sort(key=lambda x: x.height, reverse=True)

for x in objectHeightList:
    newNameList.append(x.name)
    print(x.name)
    print(x.height) 
    
print(newNameList)
framenumber = 150
beginframe = 0 

for booger in newNameList:
  bpy.data.objects[booger].select_set(True)
  selectedObject = bpy.data.objects[booger]

#create Origami from selected piece
  bpy.context.view_layer.objects.active = selectedObject
  bpy.ops.object.origamify()
#set scene 

#Get original Object Name
  object_name = booger

  #delete original object
  bpy.ops.object.delete()

  #get all plane names in unfolded object
  foo_objs = [obj.name for obj in scene.objects if obj.name.startswith(object_name)]

  #select central plane
  bpy.data.objects[foo_objs[0]].select_set(True)

  #select all planes for fold and unfold
  for object in foo_objs:
    bpy.data.objects[object].select_set(True)
    
  for obj in bpy.context.selected_objects:
    #obj.keyframe_insert(data_path='location', frame=(framenumber))
    obj.keyframe_insert(data_path='rotation_euler', frame=(framenumber))
#Unfold origami
  bpy.ops.object.origiamiunfold()
  framenumber += 10
#deselect after Unfold
  for object in foo_objs:
    bpy.data.objects[object].select_set(False)
  
#select parent object
  bpy.data.objects[foo_objs[0]].select_set(True)

  def scale_from_vector(v):
      mat = Matrix.Identity(4)
      for i in range(3):
          mat[i][i] = v[i]
      return mat
    
#select parent Object
  o2 = bpy.data.objects[foo_objs[0]]

#select Face of parent object
  face  = o2.data.polygons[0] 

#get scale information for rotation
  loc_dst, rot_dst, scale_dst = o2.matrix_world.decompose()

#find difference in rotation between Z-axis and object-Face
  q = face.normal.rotation_difference((0, 0, 1))

#adjust rotation of entire object
  o2.matrix_world = (
      Matrix.Translation(loc_dst) @ 
      q.to_matrix().to_4x4() @ 
      scale_from_vector(scale_dst)
  )

#get cordinates of the parent Object
  coords = [(o2.matrix_world @ v.co) for v in o2.data.vertices]

#get current height of plane
  height = - coords[0].z

#move plane to base
  o2.location = (0,0, height)

  #for object in foo_objs:
    #bpy.data.objects[object].select_set(True)
  #print(foo_objs)
  #bpy.ops.object.duplicate()
  #objectstring = foo_objs[0]+ ".001"
  #print(objectstring)
  #some_obj = bpy.data.objects[objectstring]
  #bpy.context.view_layer.objects.active = some_obj
  #bpy.ops.object.join()

  #bpy.ops.object.mode_set(mode='EDIT')
  #bpy.ops.mesh.select_all(action='SELECT')
  #bpy.ops.mesh.remove_doubles()
  #bpy.ops.mesh.dissolve_faces()
  #bpy.ops.object.mode_set(mode='OBJECT')
  #bpy.ops.object.select_all(action='DESELECT')
 
  for object in foo_objs:
    bpy.data.objects[object].select_set(True)

  for obj in bpy.context.selected_objects:
    obj.keyframe_insert(data_path='location', frame=(0))
    obj.keyframe_insert(data_path='rotation_euler', frame=(0))
    obj.keyframe_insert(data_path='location', frame=(beginframe))
    obj.keyframe_insert(data_path='rotation_euler', frame=(beginframe))
  newHeight = 100
  o2.location = (0,0, 100)
  for obj in bpy.context.selected_objects:
    obj.keyframe_insert(data_path='location', frame=(framenumber))
  #resetheight = 100 - height
  #o2.location = (0,0, resetheight)  
  o2.location = (0,0, height)
    
  beginframe += 5
  for object in foo_objs:
    bpy.data.objects[object].select_set(False)