# PythonOrgamiScript
This is just a Blender work flow enhancing script for the tiny monster project. 

This script does several things. First it determines which objects are highest on the model. Then begining with the highest object it creates a new origami object, using the origamify addon, which can fold and unfold into shape. The object is then unfolded into flat position and rotated to be parallel to the XY plane. It is then lowered to ground level. The script also creates animation keyframes at intervals so that the object comes together top to bottom. Some movement and reseting of 0 ground level key frames may be required as the objects line up randomly.     

In order for this to work you will need the Origamify addon installed. 
https://github.com/aconz2/blender-addon-origamify

& You will need to break up your object in to multiple objects
I do this by using the smart UV project.

Step 1:
Open UV editor and get seams for islands

Step 2:
in edit mode
select seams and mark sharp

Step 3: 
in obect mode
Run the edge split modifier on sharp only

Step 4: 
In edit mode
seperate By loose parts

Step 5: 
In object mode 
ReName the initial object by adding a .999 or anynumber not used to it

You can now run script with nothing selected.

script runs as follows at this point
1. run CreateInitialProjectData.py
2. run flattenAndRotate.py
3. using outliner command click each obect and then drag to desired location on XY plane.
4. run Setlaserpaths.py 
5. Add a dynamic smoke box covering entire area.
6. run paintAndSmoke.py
7. add plane to cover main area
8. add material to plane and all faces
9. UV project all faces at the same time
10. make material a new texture
11. make plane dynamic paint canvas
12. bake image set with texture as intial color and using UVmap
13. use image set as new material
