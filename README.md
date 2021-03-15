# PythonOrgamiScript
This is just a Blender work flow enhancing script for the tiny monster project. 

This script does several things. First it determines which objects are highest on the model. Then begining with the highest object it creates a new origami object which can fold and unfold into shape. The object is then unfolded into flat position and rotated to be parallel to the XY plane. It is then lowered to ground level. The script also creates animation keyframes at intervals so that the object comes together top to bottom. Some movement and reseting of 0 ground level key frames may be required as the objects line up randomly.     

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
ReName the initial object by adding a .999 to it

You can now run script with nothing selected.
