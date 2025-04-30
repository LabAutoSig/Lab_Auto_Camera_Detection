#path to your FreeCAD.sp pr FreeCAD.pyd file
with open('reconstruction\\FreeCAD_path.txt', 'r') as file:
        # Read the path from the file
        FREECADPATH = file.readline().strip()
import FreeCAD as App
import Part
import Draft
#______________________________________________
#Function that creates a box part in FreeCAD
#______________________________________________
def create_box(coord):
    #doc = App.newDocument()#added
    # Create parts based on the marker coordinates
    print("Create box part")
    #print(coord)
    #Extract coordinates from coord
    l_x = coord[0][0]
    #print(f"Lx {l_x}")
    l_y = coord[0][1]
    #print(f"Ly {l_y}")
    l_z = coord[0][2]
    #print(f"Lz {l_z}")
    r_x = coord[1][0]
    #print(f"Rx {r_x}")
    r_y = coord[1][1]
    #print(f"Ry {r_y}")
    r_z = coord[1][2]
    #print(f"Rz {r_z}")
    position = coord[2] # L = ll ru, U = lu rl
    table = 0.16311 #real table height distance to base 
    table_marker = coord[3] 
    t_x = table_marker[0][0]
    t_y = table_marker[0][1]
    t_z = table_marker[0][2]
    #pos = FreeCAD.Base.Vector(l_x,l_y,l_z) #positioning vector in freecad
    pos = None
    width_y = 0  
    height_z = 0
    length_x = (abs(r_x) - abs(l_x))*1000 + 50 #with safety distance
    #determine where the left and right coordinates are positioned
    if position == "L": #ll ru 
        height_z = (abs(r_z)-abs(t_z))*1000 +50 #with safety distance
        width_y = (abs(r_y) - abs(l_y))*1000 +50 # with saftey distance
        print("L")
        pos_x = (l_x*1000) - length_x
        pos_y = (r_y*1000) - width_y
        pos = FreeCAD.Base.Vector(pos_x,pos_y,t_z*1000) #positioning vector in freecad
    elif position == "U": #rl lu
        height_z = (abs(l_z)-abs(t_z))*1000 +50 # with saftey distance
        width_y = (abs(l_y) - abs(r_y))*1000 +50 # with saftey distance
        print("U")
        pos_x = (r_x*1000)
        pos_y = (r_y*1000)
        pos = FreeCAD.Base.Vector(pos_x,pos_y,table*1000) #positioning vector in freecad +0.01955


    print(f"length in x direction with safety distance = {length_x}")
    print(f"width in y direction with safety distance = {width_y}")
    print(f"height in z direction with safety distance = {height_z}")
    print(f"length in x direction = {length_x-50}")
    print(f"width in y direction = {width_y-50}")
    print(f"height in z direction = {height_z-50}")
    print("Distances in x,y and z directions:")
    #print(r_x-l_x)
    print(f"X = {l_x-r_x}")
    #print(r_y-l_y)
    print(f"Y = {l_y-r_y}")
    print(f"Z = {l_z-r_z}")
    #print(r_z-l_z)

    #open new Document from freecad
    document = App.newDocument()#open new Document from FreeCAD
    box = Part.makeBox(length_x, width_y, height_z, pos) #make box part
    #doc.addObject(box)
    document.recompute()
    #App.ActiveDocument.saveAs('output.FCStd') #save box part
    #App.ActiveDocument.recompute()#added #recompute
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

    # Change the document label (name)
    #document.Label = "

    # Save the modified document under the new name
    App.getDocument(document.Name).saveAs(new_file_name)
    App.getDocument(document.Name).saveAs("Horst_with_object_new.step")
    # Export the document as a new STEP file
    #Draft.export([document], "Horst_with_object_new.step")
    #document.exportStep("test.stp")
    
    return 