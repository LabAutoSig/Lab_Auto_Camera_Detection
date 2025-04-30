
#Aruco marker and data handling libraries
import cv2
import cv2.aruco as aruco 
import numpy as np
import math
from scipy.spatial.transform import Rotation
from three_D_reconstruction.FreeCAD_functions_new_distance_measurement import create_box, import_object_in_HORST_world
#______________________________________________
#Function that finds Aruco markers in images and extracts the coordinates and marker ids
#______________________________________________
def findArucoMarkers(img, marker_length,camera_matrix, dist_coeffs,
                     arucoDict, totalMarkers=1000, draw=True):
    #find aruco markers in the image with given marker size and camera intrinsics
    # Detect markers and estimate their poses
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#transform image into grayscale
    arucoParam = aruco.DetectorParameters_create() #Create Detector parameters
    #Detection of the marker corner coordinates & Ids
    bboxs, ids, _ = aruco.detectMarkers(gray, arucoDict, parameters = arucoParam)
    num_ids = len(ids) #number of ids detected
    if num_ids == 0: #Print if no markers are detected
        print("No markers detected.")
    #Draw bounding box around marker
    if draw: #if draw == True draw Marker corners and ids
        aruco.drawDetectedMarkers(img, bboxs, ids) #Draw image with detected ids and bboxs
    #cv2.imshow("Image",img)
    img_rs = cv2.resize(img,(900,900)) #Resize image for better visualization
    #cv2.imshow("Resized Image",img_rs) #Show image
    print("--"*30)

    return ids,num_ids, bboxs,img_rs #return bounding box coordinates and ids
#______________________________________________
#Function that sorts the pixel coordinates of the marker corners to have the same orientation
#______________________________________________
def sorted_corners(bbox):
    bboxs = bbox[0]
    sorted_bboxes = []
    print(f"Bbox before sorting {bbox}")
    print(f"Bbox before sorting reduced dimensions{bbox[0]}")
      
    if len(bboxs) >= 1:

        # Sort the bbox depending on the y coordinate using the sorted lambda key
        sorted_coordinates = sorted(bboxs, key=lambda x: x[1], reverse=False)

        # Convert the result back to a NumPy array
        sorted_coordinates = np.array(sorted_coordinates)
        print(f"Sorted coordinates {sorted_coordinates}")
        #Split array into upper and lower coordinate corners
        upper_coordinates = sorted_coordinates[:2]
        lower_coordinates = sorted_coordinates[2:]
        print(f"Upper coordinates: {upper_coordinates}")
        print(f"Lower coordinates: {lower_coordinates}")

        # Sort the upper corners depending on the x coordinate using the sorted lambda key 
        sorted_upper = sorted(upper_coordinates, key=lambda x: x[0], reverse=False)

        # Convert the result back to a NumPy array
        sorted_upper= np.array(sorted_upper)
        print(f"Sorted upper {sorted_upper}")
            
        # Sort the lower coordinates based on the x-coordinate in descending order
        sorted_lower = sorted(lower_coordinates, key=lambda x: x[0], reverse=True)

        # Convert the result back to a NumPy array
        sorted_lower= np.array(sorted_lower)
        print(f"Sorted lower {sorted_lower}")

        # Concatenate the sorted upper and lower coordinates
        sorted_bbox = np.concatenate((sorted_upper, sorted_lower), axis=0)
        print(f"Sorted bounding box {sorted_bbox}")

        #convert the result back to an array
        sorted_arrays = np.array([sorted_bbox])
        print(f"Sorted bounding boxes: {sorted_arrays}")

    else:
        # If only one set of corners, no need to sort
        sorted_arrays = bbox

    return sorted_arrays
#______________________________________________
#Function that reads a text file containing the cameras position in the world coordinate system
#and tranforms the coordinate system 
#______________________________________________
def read_camera_pose_from_txt(file_path):
    # Read camera poses from the text file
    # Two lines in txt file: first line translation vector, second line rotation vector
    camera_pose = []
    with open(file_path, 'r') as file: #r for read
        for line in file:
            #print(line)
            newline = line.replace('{"xyz+euler": [',"")
            #print(newline)
            newline = newline.replace(']}',"")
            #print(newline)
            newline = newline.replace(','," ")
            #print(newline)
            pose = [float(val) for val in newline.strip().split()] #split values when space
            camera_pose.append(pose) #add value to camera_pose

    tvec_cam = np.array(camera_pose[0][0:3]) #first line of txt file = translation vector
    adjusted_tvec = np.array([tvec_cam[0], tvec_cam[1], tvec_cam [2]])
    rvec_deg = np.array(camera_pose[0][3:]) #second line of txt file = rotation vector in degrees
    adjusted_rvec = np.array([rvec_deg[0], rvec_deg[1], rvec_deg[2]+90]) # rotate counter-clockwise around z
    rvec_cam = []
    
    for deg in adjusted_rvec: # transform rotation vector from degrees to radians
        radians = deg * (math.pi / 180) #transform for each value in rvec_deg
        rvec_cam.append(radians) #add value to array
    rvec_cam = np.array(rvec_cam) #transform into numpy array
    return rvec_cam, adjusted_tvec, tvec_cam
#________________________________________________________
#Function that creates local second camera translation vector
#___________________________________________________________
def camera_distance(tvec_cam1, tvec_cam2):
    tvec_cam2_local = tvec_cam2 - tvec_cam1
    return np.array(tvec_cam2_local)
#________________________________________________________
#Function that creates local second camera rotation vector
#___________________________________________________________
def camera_rotation_distance(rvec_cam1, rvec_cam2):
    # Convert rotation vectors to quaternion
    quat_cam1 = Rotation.from_rotvec(rvec_cam1).as_quat()
    quat_cam2 = Rotation.from_rotvec(rvec_cam2).as_quat()
    # Calculate relative rotation quaternion
    quat_relative = Rotation.from_quat(quat_cam2) * Rotation.from_quat(quat_cam1).inv()
    # Convert relative rotation quaternion to rotation vector
    rvec_relative = quat_relative.as_rotvec()
    return rvec_relative #np.array(rvec_cam2_local)
#______________________________________________
#Function that creates a camera projection matrix in the right handed camera coordinate system
#______________________________________________
def create_proj_matx(rvec_cam,adjusted_tvec, camera_matrix): #create camera projection matrix in camera coordinate system
    #Convert the rotation vectors to rotation matrices
    camR, _ = cv2.Rodrigues(rvec_cam)
    tvec_cam_reshaped = adjusted_tvec.reshape(3, 1)  # Reshape adjusted_tvec to have 3 dimensions
    # Determine if the first value of tvec_cam_reshaped is positive or negative
    tvec_sign = "positive" if tvec_cam_reshaped[0] >= 0 else "negative" #determine if x axis is +/-
    extrinsic_matrix = np.hstack((camR, tvec_cam_reshaped))
    proj_Mat = camera_matrix @ np.hstack((camR, tvec_cam_reshaped))
    #stack the translation vector and rotation matrix horizontally
    print(f"Projection matrix:\n{proj_Mat}")
    print("-"*30)
    #print(proj_Mat.shape)
    return proj_Mat, camR
#______________________________________________
#Function that recreates the 3d coordinate points in the costum world coordinate system
#______________________________________________
def return_to_world(translation_original, point_local):
    point_local[:, 0] = -point_local[:, 0] 
    point_local[:, 2] = -point_local[:, 2]
    #print(f"Point local adjusted to world coordinates: {point_local}")
    P_world = translation_original + point_local
    return P_world
#______________________________________________
#Function that performs point triangulation to recreate the 3d coordinate points
#______________________________________________
def stereoVision(ids1,ids2,num_ids1,num_ids2,bboxs1,bboxs2,image1,image2,marker_length,
                 camera_matrix1, camera_matrix2, dist_coeffs,camera_pose_file1,camera_pose_file2):
    #Use detected marker corners in pixel coordinates and camera extrinsics in the new 
    #camera coordinate system for triangulation
    print("Apply Stereo Vision:")
    print("--"*30)
    image_height1, image_width1 = image1.shape[:2] #retrieve the height and width of the image
    image_height2, image_width2 = image2.shape[:2]
    ids = []
    #_________________________________________________
    #Compare ids for equality and order
    #_________________________________________________
    if np.array_equal(ids1,ids2)==True:#if the two image marker ids are equal/same order
        ids = ids1 #append ids1 to ids
        print(f"IDs are the same:\n {ids}")

    elif np.array_equal(ids1,ids2)==False: #if the two image marker ids are not equal/same order
        print("IDs are not the same or have a different order. Try sorting...")
        # Find the common IDs in both images
        common_ids = np.intersect1d(ids1, ids2) #get the intersection between the retrieved markers
        print(f" Common ids: {common_ids}")
        sorted_ids2 = []
        sorted_bboxs2 = []
        for id_ in ids1: #loop through ids1
            if id_ in common_ids: #if the id in ids1 is a common id
                index_in_ids2 = np.where(ids2 == id_)[0][0] #index where in ids2 the common id is
                sorted_ids2.append(id_) #append sorted id to array
                sorted_bboxs2.append(bboxs2[index_in_ids2]) #append sorted bbox to array
        sorted_ids2 = np.array(sorted_ids2) #convert to numpy array
        sorted_bboxs2 = tuple(sorted_bboxs2) #convert into tuple

        # Now you have sorted IDs and corresponding sorted bounding boxes for each camera
        print("Sorted IDs and BBoxes for Camera 1:", ids1, bboxs1)
        print("Sorted IDs and BBoxes for Camera 2:", sorted_ids2, sorted_bboxs2)
        bboxs2 = sorted_bboxs2
        ids2 = sorted_ids2
        ids = ids1

    #Convert camera poses from txt files into rotation and translation vectors
    #Transormation from world to camera coordinate system
    rvec_cam1, tvec_cam1, tvec_world_cam1 = read_camera_pose_from_txt(camera_pose_file1)
    rvec_cam2, tvec_cam2, tvec_world_cam2 = read_camera_pose_from_txt(camera_pose_file2)
    #Adjust coordinate system to a local camera coordinate system
    rvec_cam1_local = np.zeros(3)
    tvec_cam1_local = np.zeros(3)
    tvec_cam2_local= camera_distance(tvec_cam1, tvec_cam2)
    rvec_cam2_local = camera_rotation_distance(rvec_cam1, rvec_cam2)
    #create projection matrices with adjusted translation camera positions
    #returns projection matrix, and rotation matrix
    proj_Mat1, camR1 = create_proj_matx(rvec_cam1_local,tvec_cam1_local, camera_matrix1)
    proj_Mat2, camR2 = create_proj_matx(rvec_cam2_local,tvec_cam2_local, camera_matrix2)

    #____________________________________________________________________________________________
    # Sort marker poses in both images and triangulate their 3D coordinates
    #____________________________________________________________________________________________
    # Initialize lists to store marker poses and their 3D coordinates
    camera_differences =[]
    marker_coordinates_3d = []
    new_tvecs =[]
    rvecs1 = []

    rvecs2 = []
    rmtx = []
    for common_id in ids: #loop through all ids
        # Find marker id index for common ID in both images
        idx = np.where(ids == common_id)[0][0]
        # Sort the corners for both images common marker before estimating poses
        sorted_corners1 = sorted_corners(bboxs1[idx])
        sorted_corners2 = sorted_corners(bboxs2[idx])
        # Reshape the sorted corners to have the shape (4, 2) for 2D points
        sorted_corners1_2d = sorted_corners1[0].T.reshape(2, 4)
        sorted_corners2_2d = sorted_corners2[0].T.reshape(2, 4)
        #undistort the pixel coordinate corner points of the markers to increase the accuracy
        undistorted_corners1 = cv2.undistortPoints(sorted_corners1, camera_matrix1,
                                                   dist_coeffs, P=camera_matrix1)
        undistorted_corners2 = cv2.undistortPoints(sorted_corners2, camera_matrix2,
                                                   dist_coeffs, P=camera_matrix2)
        #print(f"Undistorted corners 1: {undistorted_corners1}")
        undistorted_corners1 = undistorted_corners1.T.reshape(2, -1)
        undistorted_corners2 = undistorted_corners2.T.reshape(2, -1)
        #print(f"Undistorted corners 1: {undistorted_corners1}")
        #print(f"Undistorted corners 2: {undistorted_corners2}")
       
        # Estimate marker translation and rotation vectors
        # for drawing the marker coordinate systems into the images
        rvec1, tvec1, _ = aruco.estimatePoseSingleMarkers(sorted_corners1, marker_length,
                                                          camera_matrix1, dist_coeffs)
        rvec2, tvec2, _ = aruco.estimatePoseSingleMarkers(sorted_corners2, marker_length,
                                                          camera_matrix2, dist_coeffs)
        #rvecs1.append(rvec1)
        rvecs2.append(rvec2)
        new_tvecs.append(tvec2)
        # Convert the rotation vectors to rotation matrices
        R2, _ = cv2.Rodrigues(rvec2)
        rmtx.append(R2)
        #_________________________________________________
        # Triangulate the sorted and undistorted Points with the corrected camera projection matrices
        #_________________________________________________
        points4D_homogeneous = cv2.triangulatePoints(proj_Mat1, proj_Mat2,
                                                     undistorted_corners1,
                                                     undistorted_corners2)
        #points4D_homogeneous returns homogenous coordinate points
        #_________________________________________________
        #Cartesian points in camera coordinate system: +x right, +y down, +z far
        #_________________________________________________

        points3D_cartesian = points4D_homogeneous[:3,:] / points4D_homogeneous[3,:][np.newaxis,:]
        points3D = points3D_cartesian.T # Coordinates in cartesian coordinate system
        # Convert the homogeneous 4D points to Cartesian coordinates
        points_world = return_to_world(tvec_cam1, points3D)
        #_________________________________________________
        #Convert to world coordinate system: -x right, -y far, +z up
        #_________________________________________________
        # 'marker_coordinates_3D' contains the 3D points in Cartesian
        marker_coordinates_3d.append(points_world)
        #End of loop
    num_ids = len(ids) # returns the number of common ids
    print("--"*30)
    
    return ids, num_ids, marker_coordinates_3d, new_tvecs, rvecs2, rmtx
#Function that identifies the corners of the ArUco markers
def identify_ArUco_corners(coord):
    lu = coord[0]
    ru = coord[1]
    rl = coord[2]
    ll = coord[3]
    print(lu)
    print(ru)
    print(rl)
    print(ll)
    print("--"*30)
    return lu, ru, rl, ll
#Function that sorts the 3d coordinates of the ArUco markers
#to have the same orientation in the world coordinate system
def sort_ArUco_placement(lu_a,ll_a,ru_a,rl_a,lu_b,ll_b,ru_b,rl_b, id_a, id_b):
    a = []
    #comparison of the left upper coordinate points of the two ids
    #if left upper x-coordinate value of id3 is smaller than of id2
    if lu_a[0] > lu_b[0]:
        #left marker == a --> lu/ll
        #right marker == b --> ru/rl
        if lu_a[1] > lu_b[1]: #if y-coordinate id2 greater
            #ida lower marker --> ida_ll
            #idb upper marker --> idb_ru
            print(f"ID{id_a} == left lower")
            print(f"ID{id_b} == right upper")
            #add values to array "a"
            a.append(ll_a)
            a.append(ru_b)
            a.append("L") #identifier for ll and ru
        elif lu_a[1] < lu_b[1]: #if y-coordinate id2 smaller
            #ida upper marker --> ida_lu
            #idb lower marker --> idb_rl
            print(f"ID{id_a} == left upper")
            print(f"ID{id_b} == right lower")
            a.append(lu_a)
            a.append(rl_b)
            a.append("U") #identifier for lu and rl
                                
    # else if left upper x-coordinate value of idb is greater than of ida
    elif lu_a[0] < lu_b[0]:
        #left marker == id_b --> lu/ll
        #right marker == id_a --> ru/rl
        if lu_a[1] > lu_b[1]: #if y-coordinate ida greater
            #ida lower marker --> ida_rl
            #idb upper marker --> idb_lu
            print(f"ID{id_b} == left upper")
            print(f"ID{id_a} == right lower")
            a.append(lu_b)
            a.append(rl_a)
            a.append("U")  #identifier for lu and rl
        elif lu_a[1] < lu_b[1]: #if y-coordinate ida smaller
            print(f"ID{id_a} == right upper")
            print(f"ID{id_b} == left lower")
            #ida upper marker  --> ida_ru
            #idb lower marker --> idb_ll
            a.append(ll_b)
            a.append(ru_a)
            a.append("L") #identifier for ll and ru
    return a
#______________________________________________
#Function that sorts the 3d coordinates in the world coordinate system
#______________________________________________
def getCoords(ids,num_ids,coords_3d,new_tvecs, rvecs, rmtx, marker_length,
              camera_matrix, dist_coeffs, image, horst_file, object_file, save_file):
    #Define the variables
    box_coords = [] # array for the cad coordinates
    if num_ids >= 1: #if there are more than or one marker
        id1 = ids[0]
        coord1 = coords_3d[0]
        # Draw the coordinate frame axes on the image for marker 1
        image = cv2.drawFrameAxes(image, camera_matrix, dist_coeffs, rvecs[0],
                                  new_tvecs[0], marker_length * 0.5)
        print(f"Coordinates ID1:{id1} ")
        #Identify left uppper = lu, right upper = ru, right lower = rl,
        #left lower = ll corners
        lu_id1,ru_id1,rl_id1,ll_id1 = identify_ArUco_corners(coord1)
        
        if num_ids >= 2: #if there are more than or exactly two markers
            id2 = ids[1]
            coord2 = coords_3d[1]
            # Draw the coordinate frame axes on the image for marker 1
            image = cv2.drawFrameAxes(image, camera_matrix, dist_coeffs, rvecs[1],
                                      new_tvecs[1], marker_length * 0.5)
            print(f"Coordinates ID2:{id2}")
            lu_id2,ru_id2,rl_id2,ll_id2 = identify_ArUco_corners(coord2)
            
            if num_ids >= 3: #if there are more than or exactly three markers
                id3 = ids[2]
                coord3 = coords_3d[2]
                # Draw the coordinate frame axes on the image for marker 1
                image = cv2.drawFrameAxes(image, camera_matrix, dist_coeffs, rvecs[2],
                                          new_tvecs[2], marker_length * 0.5)
                print(f"Coordinates ID3:{id3} ")
                lu_id3,ru_id3,rl_id3,ll_id3 = identify_ArUco_corners(coord3)
                
                if num_ids >= 4: #if there are more than or exactly four markers
                    print("Too many markers detected, adjust scanning process...")
                #______________________________________________________
                #if there are only three markers prepare for drawing a box
                #a later implemenation with four markers for round objects is possible
                #______________________________________________________
                elif num_ids == 3: # if no id4 == rectangle                    
                    #Use the right upper/right lower marker coordinates of the right marker
                    #Use the left lower/left upper marker coordinates of the left marker
                    #______________________________________________________________
                    #ID of the table marker has to be known for this state of the code
                    #______________________________________________________________
                    if id1 == 314: #identify marker with the value 23
                        #id1 = table marker --> distance between id2/id3 and id1 for height
                        print(f"ID{id1} = table marker")
                        box_coords = sort_ArUco_placement(lu_id2,ll_id2,ru_id2,rl_id2,lu_id3,ll_id3,ru_id3,rl_id3, id2, id3)
                        box_coords.append(coord1) #append table marker coordinates

                    elif id2 == 314: #identify marker with the value 23
                        #id2 = table marker --> distance between id1/id3 and id2 = height
                        print(f"ID{id2} = table marker")
                        box_coords = sort_ArUco_placement(lu_id1,ll_id1,ru_id1,rl_id1,lu_id3,ll_id3,ru_id3,rl_id3, id1, id3)
                        box_coords.append(coord2) #append table marker coordinates
   
                    elif id3 == 314: #identify marker with the value 23
                        #id3 = table marker --> distance between id1/id2 and id3 = height
                        print(f"ID{id3} = table marker")
                        box_coords = sort_ArUco_placement(lu_id1,ll_id1,ru_id1,rl_id1,lu_id2,ll_id2,ru_id2,rl_id2, id1, id2)
                        box_coords.append(coord3) #append table marker coordinates

                    box = create_box(box_coords) #Use coordinates to create a box
                    box.exportStep("test.stp")#export the created box as a STEP file
                    import_object_in_HORST_world(horst_file, object_file, save_file)
    else: #if no markers are detected
        print("No markers detected.")

    return box_coords,image

