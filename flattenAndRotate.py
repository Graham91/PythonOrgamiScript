import bpy
import fnmatch
import bmesh
from mathutils import Matrix, Vector
from math import sin, radians

def tag(iterable, value):
    for x in iterable:
        x.tag = value    

def vec(e):
    v0, v1 = e.verts
    return (v1.co - v0.co).normalized()

def parallel(e1, e2, tol_angle=0):
    return abs(vec(e1).dot(vec(e2)) - 1) <= sin(tol_angle)

def line_select_extend(edge, v, tol_angle=0):  
    edges = []
    while v:
        segments = [e for e in v.link_edges
                if not e is edge
                and e.tag
                and parallel(e, edge, tol_angle)]
        if segments:
            edge = segments[0]
            edges.extend(segments)
            v = edge.other_vert(v)
        else:
            v = None  
    return edges     

def select_segment(edge, tol_angle=0):
    v0, v1 = edge.verts
    edges = line_select_extend(edge, v0, tol_angle)
    edges.reverse()
    edges.append(edge)
    edges.extend(line_select_extend(edge, v1, tol_angle))
    return edges

def edge_line_segments(bm, edges=[], tol_angle=0):
    ret = {"segments" : []}
    tag(bm.edges, False)
    tag(edges, True)
    edges = set(edges)
    while edges:
        segments = select_segment(next(iter(edges)))
        ret["segments"].append(segments)
        edges -= set(segments)
    tag(bm.edges, False)
    return ret

scene = bpy.context.scene

class objectInfo:
  def __init__(self, initialObject, length, startFrame, endFrame, name, curve, height):
    self.initialObject = initialObject
    self.length = length
    self.startFrame = startFrame
    self.endFrame = endFrame
    self.name = name
    self.height = height
    self.curve = curve
    
    
objectArrayInfo = []  

def recreateObjectArray ():
    initialObjectArray = bpy.context.scene['InitialObjectArray']
    lengthArray = bpy.context.scene['LengthArray']
    startFrameArray = bpy.context.scene['StartFrameArray']
    endFrameArray= bpy.context.scene['EndFrameArray']
    nameArray = bpy.context.scene['NameArray']
    for index, objectName in enumerate(initialObjectArray):
       newObject = objectInfo(objectName, lengthArray[index], startFrameArray[index], endFrameArray[index], nameArray[index], "", 0)
       objectArrayInfo.append(newObject)
       
recreateObjectArray()       
print(objectArrayInfo[0].initialObject)

#foo_objs2 = [obj for obj in bpy.data.objects if obj.name.startswith("chick")]

objectHeightList = []
#newNameList = []
errorfixer = []

#class Obj:
  #def __init__(self, name, height):
    #self.name = name
    #self.height = height

for infoObject in objectArrayInfo:
  initialObjectName = infoObject.initialObject
  x = bpy.data.objects[initialObjectName]
  coords = [(x.matrix_world @ v.co) for v in x.data.vertices]
  newObj = []
  for Y in coords:
      newObj.append(Y.z)
  HighestValue = max(newObj)
  infoObject.height = HighestValue
  #newObj = Obj(x.name, HighestValue)
  #objectHeightList.append(newObj)
  
objectArrayInfo.sort(key=lambda x: x.height, reverse=True)

#for x in objectHeightList:
    #newNameList.append(x.name)
    #print(x.name)
    #print(x.height) 
    
#print(newNameList)
longestDistance = bpy.context.scene['LargestFrameNumber']
multipler = 1 
shiftFrame = longestDistance * multipler
framenumber = 150 + shiftFrame
beginframe = 0 + shiftFrame
centralobjectarray = []
centralHeightArray = []
shiftframe2 = 0

bpy.context.scene['beginFrame'] = beginframe
bpy.context.scene['Multipler'] = multipler

print("initial compute done")
for index, infoObject in enumerate(objectArrayInfo):
  booger = infoObject.initialObject
  bpy.data.objects[booger].select_set(True)
  objData = len(bpy.data.objects[booger].data.polygons)
  
      
  selectedObject = bpy.data.objects[booger]

  #create Origami from selected piece
  bpy.context.view_layer.objects.active = selectedObject
  if objData > 1:
    bpy.ops.object.origamify()
    #set scene 

    #Get original Object Name
    object_name = booger

    #delete original object
    bpy.ops.object.delete()

    #get all plane names in unfolded object
    foo_objs = [obj.name for obj in scene.objects if obj.name.startswith(object_name)]
    newNamingObject = foo_objs[0]
    

    
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
    #deselect after Unfold
    for object in foo_objs:
      bpy.data.objects[object].select_set(False)
  
    #select parent object
    bpy.data.objects[foo_objs[0]].select_set(True)
    
    #select parent Object
    o2 = bpy.data.objects[foo_objs[0]]
    
  else:
    o2 = selectedObject
    newNamingObject = o2.name
    o2.keyframe_insert(data_path='rotation_euler', frame=(framenumber))
  infoObject.name = newNamingObject    
  framenumber += 3
  def scale_from_vector(v):
      mat = Matrix.Identity(4)
      for i in range(3):
          mat[i][i] = v[i]
      return mat
    


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
  if objData > 1:
    for object in foo_objs:
      bpy.data.objects[object].select_set(True)
    print(foo_objs)
    bpy.ops.object.duplicate()
    objectstring = foo_objs[0]+ ".001"
    print(objectstring)
    some_obj = bpy.data.objects[objectstring]
    bpy.context.view_layer.objects.active = some_obj
    bpy.ops.object.join()

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.mesh.dissolve_faces()
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
  else: 
    C = bpy.context
    src_obj = bpy.data.objects[booger]
    new_obj = src_obj.copy()
    new_obj.data = src_obj.data.copy()
    new_obj.name = booger + "111"
    C.collection.objects.link(new_obj)
    objectstring = new_obj.name
  #return to object mode       
  
  pathobject = bpy.ops.object.data
  print(pathobject)
  

  #grab curve object
  curve_obj = bpy.data.objects[objectstring]
 
  #duration
  
  #reNamecurveobject
  number = str(index)
  zfilledNumber = number.zfill(4)
  curveName = "Curve" + zfilledNumber
  curve_obj.name = curveName
  infoObject.curve = curveName
  errorfixer.append(curveName)
  errorfixer.append(booger)
  bpy.ops.object.select_all(action='DESELECT')

  objects = bpy.data.objects
  b = objects[curveName]

  b.parent = o2
  b.matrix_parent_inverse = o2.matrix_world.inverted()
  if objData > 1:
    for object in foo_objs:
       bpy.data.objects[object].select_set(True)
  else:
    bpy.data.objects[booger].select_set(True)

    
  o2.keyframe_insert(data_path='location', frame=(beginframe))
 
  
  for obj in bpy.context.selected_objects:
     obj.keyframe_insert(data_path='rotation_euler', frame=(beginframe))
     obj.keyframe_insert(data_path='rotation_euler', frame=(beginframe + shiftframe2 + 20))

  newHeight = 200
  o2.location = (0,0, 200)
  shiftframe2 += 3
       
  #for obj in bpy.context.selected_objects:
  o2.keyframe_insert(data_path='location', frame=(framenumber))
  #resetheight = 100 - height
  #o2.location = (0,0, resetheight)  
  o2.location = (0,0, height)
  #"height" Now means something Different 
  infoObject.height = height
  #centralHeightArray.append(height)
  
   
  for object in foo_objs:
    bpy.data.objects[object].select_set(False)

initialObjectArray = []
lengthArray = []
startFrameArray = []
endFrameArray = []
nameArray = []
heightArray = []
curveArray = []

for object in objectArrayInfo:
    initialObjectArray.append(object.initialObject)
    lengthArray.append(object.length)
    startFrameArray.append(object.startFrame)
    endFrameArray.append(object.endFrame)
    nameArray.append(object.name)
    heightArray.append(object.height)
    curveArray.append(object.curve)
    
bpy.context.scene['InitialObjectArray'] = initialObjectArray
bpy.context.scene['LengthArray'] = lengthArray
bpy.context.scene['StartFrameArray'] = startFrameArray
bpy.context.scene['EndFrameArray'] = endFrameArray
bpy.context.scene['NameArray'] = nameArray
bpy.context.scene['CurveArray'] = curveArray 
bpy.context.scene['HeightArray'] = heightArray 
#print(errorfixer)
