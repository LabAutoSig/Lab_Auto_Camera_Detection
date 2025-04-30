#path to your FreeCAD.sp pr FreeCAD.pyd file
with open('three_D_reconstruction\\FreeCAD_path.txt', 'r') as file:
        # Read the path from the file
        FREECADPATH = rf"{file.readline().strip()}"
import sys
sys.path.append(FREECADPATH) #add FreeCAD path to system path
import FreeCAD as App
import Part
#import Draft
#______________________________________________
#Function that creates a box part in FreeCAD
#______________________________________________
def create_box(coord):
    # Create parts based on the marker coordinates
    print("Create box part")
    print(f"Coordinates: {coord}")
    #Extract coordinates from coord
    l_x = coord[0][0]
    l_y = coord[0][1]
    l_z = coord[0][2]
    r_x = coord[1][0]
    r_y = coord[1][1]
    r_z = coord[1][2]
    position = coord[2] # L = ll ru, U = lu rl
    table = 0.16311 #real table height distance to base 
    table_marker = coord[3] 
    t_x = table_marker[0][0]
    t_y = table_marker[0][1]
    t_z = table_marker[0][2]
    pos = None
    width_y = 0  
    height_z = 0
    length_x = ((abs(r_x) - abs(l_x))) + 50 #with safety distance
    #determine where the left and right coordinates are positioned
    if position == "L": #ll ru 
        height_z = ((abs(r_z)-abs(t_z))) +50 #with safety distance
        width_y = ((abs(r_y) - abs(l_y))) +50 # with saftey distance
        print("L")
        pos_x = (l_x*10) - length_x
        pos_y = (r_y*10) - width_y
        pos = App.Base.Vector(pos_x,pos_y,t_z*10) #positioning vector in freecad
    elif position == "U": #rl lu
        height_z = ((abs(l_z)-abs(t_z))) +50 # with saftey distance
        width_y = ((abs(l_y) - abs(r_y))) +50 # with saftey distance
        print("U")
        pos_x = (r_x*10)
        pos_y = (r_y*10)
        pos = App.Base.Vector(pos_x,pos_y,table*10) #positioning vector in freecad +0.01955


    print(f"length in x direction with safety distance = {length_x} mm")
    print(f"width in y direction with safety distance = {width_y} mm")
    print(f"height in z direction with safety distance = {height_z} mm")
    print(f"length in x direction = {length_x-50} mm")
    print(f"width in y direction = {width_y-50} mm")
    print(f"height in z direction = {height_z-50} mm")
    print("Distances in x,y and z directions:")
    print(f"X = {l_x-r_x} m")
    print(f"Y = {l_y-r_y} m")
    print(f"Z = {l_z-r_z} m")
    #open new Document from freecad
    document = App.newDocument()#open new Document from FreeCAD
    box = Part.makeBox(length_x, width_y, height_z, pos) #make box part
    document.recompute()
    return box

def import_object_in_HORST_world(Horst_path, object_path, new_file_name):
    # Open the existing STEP file
    document = App.openDocument(Horst_path)

    # Import the STL file
    imported_shape = Part.Shape()
    imported_shape.read(object_path)

    # Create a new Part feature from the imported shape
    part_feature = document.addObject("Part::Feature", "ImportedShape")
    part_feature.Shape = imported_shape

    # Update the document
    App.ActiveDocument.recompute()

    # Save the modified document under the new name
    App.getDocument(document.Name).saveAs(new_file_name)
    App.getDocument(document.Name).saveAs("New_assembly.step")
    # Export the document as a new STEP file
    #Draft.export([document], "Horst_with_object_new.step")
    #document.exportStep("test.stp")
    return 