#path to your FreeCAD.sp pr FreeCAD.pyd file
with open('three_D_reconstruction\\FreeCAD_path.txt', 'r') as file:
        # Read the path from the file
        FREECADPATH = rf"{file.readline().strip()}"
import sys
sys.path.append(FREECADPATH) #add FreeCAD path to system path
import FreeCAD as App
import Part
#import Draft


# Calculate real distances considering all cases
def calculate_distance(a, b):
    if (a < 0 and b > 0) or (a > 0 and b < 0):  # One negative, one positive
        return abs(a) + abs(b)
    else:  # Both positive or both negative
        return abs(a - b)
#______________________________________________
#Function that creates a box part in FreeCAD
#______________________________________________
def create_box(coord):
    # Create parts based on the marker coordinates
    print("Create box part")
    print(f"Coordinates: {coord}")
    # Extract coordinates from coord
    l_x = coord[0][0]
    l_y = coord[0][1]
    l_z = coord[0][2]
    r_x = coord[1][0]
    r_y = coord[1][1]
    r_z = coord[1][2]
    position = coord[2]  # L = ll ru, U = lu rl
    table = 0.16311  # real table height distance to base
    table_marker = coord[3]
    t_x = table_marker[0][0]
    t_y = table_marker[0][1]
    t_z = table_marker[0][2]
    pos = None
    width_y = 0
    height_z = 0
    distances = []
    length_x = calculate_distance(r_x, l_x)
    distances.append(length_x)  # X distance
    if position == "L":  # ll ru
        height_z = calculate_distance(r_z, t_z)
        width_y = calculate_distance(r_y, l_y)
        print("L")
        distances.append(width_y)
        distances.append(height_z)
        pos_x = ((l_x+50) * 1000) - length_x
        pos_y = ((r_y+50) * 1000) - width_y
        pos = App.Base.Vector(pos_x, pos_y, t_z * 10)  # positioning vector in FreeCAD
    elif position == "U":  # rl lu
        height_z = calculate_distance(l_z, t_z) 
        width_y = calculate_distance(l_y, r_y)
        print("U")
        distances.append(width_y)
        distances.append(height_z)
        pos_x = ((r_x+50) * 1000)
        pos_y = ((r_y+50) * 1000)
        pos = App.Base.Vector(pos_x, pos_y, table * 1000)  # positioning vector in FreeCAD
    #add safety distance to the box dimensions
    safety_distance = 50  # mm
    safety_distances = distances.copy()  # Create a copy of distances for safety distance calculation
    for i in range(len(distances)):
        safety_distances[i] = distances[i] + 50
    print(f"Dimensions in x,y,z direction without safety distance = {distances} mm")
    print(f"Dimensions in x,y,z direction with safety distance = {safety_distances} mm")
    
    # Open new Document from FreeCAD
    document = App.newDocument()  # open new Document from FreeCAD
    box = Part.makeBox(length_x, width_y, height_z, pos)  # make box part
    document.recompute()
    return box, distances

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