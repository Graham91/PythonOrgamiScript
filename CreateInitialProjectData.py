import bpy 
import mathutils
import bmesh
from mathutils import Matrix, Vector
from math import sin, radians
from bpy.app import handlers
import random


class LengthObject:
  def __init__(self, name, length, initialObject):
    self.name = name
    self.length = length
    self.initialObject = initialObject
    
mainObjectArray = []


class LaserColumn:
  def __init__(self, laserIndexList, laserTotal):
    self.laserIndexList = laserIndexList
    self.laserTotal = laserTotal
    
def organizeArray (nameArray, numberOfColumns):
  #Find length of all curves
  objectArray = createLengthArray(nameArray)
  #Sort lengths
  objectArray.sort(key=lambda x: x.length)
  #divide lasers into arrays
  arrayOfArrays = sortIntoArrays(objectArray, numberOfColumns)
  #Return array of arrays 
  print(arrayOfArrays)

def createLengthArray (nameArray):
  #addobject to main Array 
  for name in nameArray:
    object = bpy.data.objects[name]
    mainObjectArray.append(findLengthOfCurves(object))
  #return array
  return mainObjectArray
    
       
#create a tuple to pass through to Array of Arrays
def createTuple (object, previousEnd):
    name = object.name
    length = object.length
    initialObject = object.initialObject
    startFrame = previousEnd + 1
    endFrame = startFrame + length
    newTuple = (initialObject, length, startFrame, endFrame, name)
    return newTuple

def ChangeArrayOfArraysToTuples (arrayOfArrays):
    newArrayOfArrays = []
    for index, arrayOfObjects in enumerate(arrayOfArrays):
        previousEnd = index * 4
        for object in arrayOfObjects:
            newTuple = createTuple(object, previousEnd)
            previousEnd = newTuple[3]
            newArrayOfArrays.append(newTuple)
  
    return newArrayOfArrays
    
    
def sortIntoArrays (objectArray, numberOfColumns):
  #Get largest and divide into columns "numberOfColumns" Times
  #delete the one you added eachtime
  columnList = []
  ArrayOfArrays = []
  ArrayOfArraysObject = []
  objectArrayLength = len(objectArray) - numberOfColumns
  
  for index in range(0, numberOfColumns):
    nameArray = [objectArray[0]]
    laserLength = objectArray[0].length
    newLaserColumn = LaserColumn(nameArray, laserLength) 
    columnList.append(newLaserColumn)
    removeItem(objectArray, True)
    
  for index in range(0, objectArrayLength):
    columnList.sort(key=lambda x: x.laserTotal)
    sC = columnList[0]
    sO = objectArray[0]
    sOname = sO.initialObject
    sOlength = sO.length
    sCNumber = sC.laserTotal
    sCarray = sC.laserIndexList
    sCarray.append(sO)
    sC.laserIndexList = sCarray
    sC.laserTotal = int(sCNumber) + int(sOlength)
    removeItem(objectArray, True)
    
  numbertotals = []
  for column in columnList:
    array = column.laserIndexList
    random.shuffle(array)
  
  for column in columnList:
    ArrayOfArrays.append(column.laserIndexList)
  for column in columnList:
    numbertotals.append(column.laserTotal)
    
  print(numbertotals)
  bpy.context.scene['numberTotalsOrdered'] = numbertotals
  numbertotals.sort()
  bpy.context.scene['highestNumber'] = numbertotals[0]
  
  return ArrayOfArrays

    
def removeItem (array, front):
    #if true delete first in array
    if front:
      array.pop(0)
    #if false delete last in array
    else:
      array.pop()
    
#### SORTING FUNCTION END USE: organizeArray(Namelist, column#)
def findLengthOfCurves (object, initialObject):
  #return length/name object
  ob = object
  me = ob.data
  bm = bmesh.from_edit_mesh(me)    

  perimeter = [e for e in bm.edges if e.is_boundary]  
  ret = edge_line_segments(bm, edges=perimeter, tol_angle=radians(5))
  segments = [(sum(e.calc_length() for e in s), s)
        for s in ret["segments"]]
  segments.sort(key=lambda s: s[0])
  #pathlength
  segmentsnumber = 0
  #compute Path length
  for i, (length, edges) in enumerate(segments):
  
     for e in edges:
        e.select = i == len(segments) - 1 
        segmentsnumber = e.calc_length() + segmentsnumber
  #return to object mode    
  newLengthObject = LengthObject(object.name, segmentsnumber, initialObject)
  
  return newLengthObject

def copy_ob(ob, parent,  collection=bpy.context.collection):
    # copy ob
    copy = ob.copy()
    copy.parent = parent
    bpy.context.view_layer.objects.active = parent
    copy.matrix_parent_inverse = ob.matrix_parent_inverse.copy()
    # copy particle settings
    for ps in copy.particle_systems:
        ps.settings = ps.settings.copy()
    collection.objects.link(copy)
    return copy
    
def tree_copy(ob, parent, levels=3):
    def recurse(ob, parent, depth):
        if depth > levels: 
            return
        copy = copy_ob(ob, parent)
        
        for child in ob.children:
            recurse(child, copy, depth + 1)
    recurse(ob, ob.parent, 0)
    
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

foo_objs2 = [obj.name for obj in bpy.data.objects if obj.name.startswith("chick")]
scene = bpy.context.scene
lengtharray = []
objectArray = []
listOfPaths = []
for index, booger in enumerate(foo_objs2):
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
    #bpy.ops.object.delete()

    #get all plane names in unfolded object
    foo_objs = [obj.name for obj in scene.objects if obj.name.startswith(object_name)]
    newNamingObject = foo_objs[0]
    

    
    #select central plane
    bpy.data.objects[foo_objs[0]].select_set(True)

    #select all planes for fold and unfold
    for object in foo_objs:
      bpy.data.objects[object].select_set(True)
    

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
 
   

  def scale_from_vector(v):
      mat = Matrix.Identity(4)
      for i in range(3):
          mat[i][i] = v[i]
      return mat
    


  #select Face of parent object
  del foo_objs[0]
  for object in foo_objs:
    bpy.data.objects[object].select_set(True)
  
  print(foo_objs)
  bpy.ops.object.duplicate()
  objectstring = foo_objs[0]+ ".001"
  print(objectstring)
  listOfPaths.append(objectstring)
  some_obj = bpy.data.objects[objectstring]
  bpy.context.view_layer.objects.active = some_obj
  bpy.ops.object.join()
  
 
  bpy.ops.object.mode_set(mode='EDIT')
  bpy.ops.mesh.select_all(action='SELECT')
  bpy.ops.mesh.remove_doubles()
  bpy.ops.mesh.dissolve_faces()
  context = bpy.context
  ob = context.object
  segmentsnumber = findLengthOfCurves(ob, booger)
  
  #return to object mode    
  print("laserName: ", segmentsnumber.name, ",  lengthoflaserpath: ", segmentsnumber.length)   
  objectArray.append(segmentsnumber)
  bpy.ops.object.mode_set(mode='OBJECT')
  bpy.data.objects[objectstring].select_set(False)
  
  for object in foo_objs:
    bpy.data.objects[object].select_set(False)
  bpy.context.active_object.select_set(False)
  bpy.context.view_layer.objects.active = None
  for object in foo_objs:
    bpy.data.objects[object].select_set(True)
  bpy.ops.object.delete()

objectArray.sort(key=lambda object: object.length, reverse=True)
arrayOfArrays = sortIntoArrays(objectArray, 9)
#bpy.context.scene['ArrayOfArrays'] = arrayOfArrays
arrayOfArraysTuple = ChangeArrayOfArraysToTuples(arrayOfArrays)


#findLargestFrameNumber:

arrayOfArraysTuple.sort(key = lambda x: x[3], reverse=True)
print(arrayOfArraysTuple)
largestTuple = arrayOfArraysTuple[0]
largestFrameNumber = largestTuple[3]

bpy.context.scene['LargestFrameNumber'] = largestFrameNumber

initialObjectArray = []
lengthArray = []
startFrameArray = []
endFrameArray = []
nameArray = []

for tuple in arrayOfArraysTuple:
    initialObjectArray.append(tuple[0])
    lengthArray.append(tuple[1])
    startFrameArray.append(tuple[2])
    endFrameArray.append(tuple[3])
    nameArray.append(tuple[4])
    
bpy.context.scene['InitialObjectArray'] = initialObjectArray
bpy.context.scene['LengthArray'] = lengthArray
bpy.context.scene['StartFrameArray'] = startFrameArray
bpy.context.scene['EndFrameArray'] = endFrameArray
bpy.context.scene['NameArray'] = nameArray

       
for object in listOfPaths:
   bpy.data.objects[object].select_set(True)
bpy.ops.object.delete()
#divide lasers into arrays
#arrayOfArrays = sortIntoArrays(objectArray, numberOfColumns)
#Return array of arrays 
#print(arrayOfArrays)