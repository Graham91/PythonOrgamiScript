import bpy 
import mathutils
import bmesh
from mathutils import Matrix, Vector
from math import sin, radians
from bpy.app import handlers

#obj = bpy.context.object
#obj.parent = None
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

foo_objs2 = [obj for obj in bpy.data.objects if obj.name.startswith("Curve")]
multipler = bpy.context.scene['Multipler']
beginframe = bpy.context.scene['beginFrame']
for index, obj in enumerate(foo_objs2):
  bpy.context.view_layer.objects.active = obj
  
  bpy.data.objects[obj.name].select_set(True)
  matrixcopy = obj.matrix_world.copy()
  obj.parent = None
  obj.matrix_world = matrixcopy

  meshName = obj.name
  

  bpy.ops.object.mode_set(mode='EDIT')
  #gets Length of path for Laser speed
  context = bpy.context
  ob = context.object
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
       

  #path length after computation        
  
  bpy.ops.object.mode_set(mode='OBJECT')
  
  bpy.ops.object.convert(target='CURVE')
  pathduration = multipler * segmentsnumber
  #set curve path duration

  obj.keyframe_insert(data_path='location', frame=(beginframe))
  bpy.data.objects[obj.name].select_set(False)
  bpy.context.view_layer.objects.active = None
  
  #copys laser
  laser = bpy.data.objects["laser"]
  tree_copy(laser, 1)
  newobj = bpy.context.object
  number = str(index)
  zfilledNumber = number.zfill(4)
  newobj.name = "Laserbeam" + zfilledNumber
  ob = bpy.context.object
  curve_ob = bpy.data.objects[obj.name]
  number2 = str(index + 1)
  zfilledNumber2 = number2.zfill(3)
  cylinder = "Cylinder." + zfilledNumber2
  sphere = "Sphere." + zfilledNumber2
  cylinderObject = bpy.data.objects[cylinder]
  sphereObject = bpy.data.objects[sphere]
  con = ob.constraints.new('FOLLOW_PATH')
  con.target = curve_ob

  curve_ob.data.path_duration = pathduration
  curve_ob.data.use_path = True
  anim = curve_ob.data.animation_data_create()
  anim.action = bpy.data.actions.new("%sAction" % curve_ob.data.name)

  fcu = anim.action.fcurves.new("eval_time")
  mod = fcu.modifiers.new('GENERATOR')
  mod.use_restricted_range = True 
  mod.frame_start = beginframe - pathduration
  mod.frame_end = beginframe 
  print("pathduration value: ", -pathduration) 
  print("sphereName: ", sphere)
  print(sphereObject)
  cylinderObject.hide_render = True
  cylinderObject.hide_viewport = True
  cylinderObject.keyframe_insert('hide_viewport', frame= 0) 
  cylinderObject.keyframe_insert(data_path="hide_render", frame= 0)  
  cylinderObject.hide_viewport = False
  cylinderObject.hide_render = False
  cylinderObject.keyframe_insert('hide_viewport', frame= beginframe - pathduration) 
  cylinderObject.keyframe_insert(data_path="hide_render", frame= beginframe - pathduration) 
  cylinderObject.hide_render = True
  cylinderObject.hide_viewport = True
  cylinderObject.keyframe_insert('hide_viewport', frame= beginframe) 
  cylinderObject.keyframe_insert(data_path="hide_render", frame= beginframe)  
  sphereObject.hide_render = True
  sphereObject.hide_viewport = True
  sphereObject.keyframe_insert('hide_viewport', frame= 0) 
  sphereObject.keyframe_insert(data_path="hide_render", frame= 0)  
  sphereObject.hide_viewport = False
  sphereObject.hide_render = False
  sphereObject.keyframe_insert('hide_viewport', frame= beginframe - pathduration) 
  sphereObject.keyframe_insert(data_path="hide_render", frame= beginframe - pathduration) 
  sphereObject.hide_render = True
  sphereObject.hide_viewport = True
  sphereObject.keyframe_insert('hide_viewport', frame= beginframe) 
  sphereObject.keyframe_insert(data_path="hide_render", frame= beginframe)  
#ob = bpy.context.scene.objects["Cube.006"]
#obj.parent = ob
#obj.matrix_parent_inverse = ob.matrix_world.inverted()
