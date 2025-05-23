#______________________________________________
#Import necessary libraries
#______________________________________________
#Freecad libraries
import sys 
#Aruco marker and data handling libraries
import cv2
from cv2 import aruco 
import numpy as np
import sys
import os
import traceback
from three_D_reconstruction.reconstruction_functions import findArucoMarkers, stereoVision, getCoords
def main():
    #Define the image, save and model paths for your individual folder structure
    # Display the undistorted image
    horst_file =r"three_D_reconstruction\HORST_world\World.FCStd"
    object_file =r"three_D_reconstruction\HORST_world\test.stp"
    save_file = r"three_D_reconstruction\HORST_world\Robot_with_object_new.FCStd"
    marker_file = r"three_D_reconstruction\marker_placement.txt"
    folder_path = r"three_D_reconstruction\input"
    calibration_file = r"three_D_reconstruction\Calibration\calibration_parameters_new_images_02_05_25_v2_rasps.npz"
    #___________Load Data_____________________
    marker_length = 25 #aruco marker side length
    # Load the camera parameters (you may need to calibrate your camera separately if you used a different camera)
    #Camera used: Raspberry Pi V2 camera module
    camera_matrix = [] #intrinsic camera matrix
    dist_coeffs = [] #distortion coefficients for the camera lense
    arucoDict = aruco.getPredefinedDictionary(aruco.DICT_4X4_1000) #define used aruco marker dicitonary
    #Load distortion coefficients and camera matrix from the npz file 
    with np.load(calibration_file) as data:
        camera_matrix = data['camera_matrix'] #the data is saved under defined names 
        dist_coeffs = data['dist_coeffs']
    print(f"Calibration parameters:")
    print("--"*30)
    print(f"Camera intrinsic matrix: \n {camera_matrix} \n \n Distortion coefficients: \n {dist_coeffs}")
    with open(marker_file, 'r') as file:
        lines = file.readlines()
        table_marker_id = int(lines[0].strip())
    #_________Image 1___________
    #Load the first image --> change path
    img1 = cv2.imread(folder_path + r"\1.jpg")#modified
    camera_pose_file1  = folder_path + r"\camera_pose1.txt" #Load camera pose1 from txt files
    h1, w1 = img1.shape[:2] #get image height and width
    #_________Image 1___________
    #Load the second image --> change path
    img2 = cv2.imread(folder_path + r'\2.jpg')#modified
    camera_pose_file2 = folder_path + r'\camera_pose2.txt' #Load camera pose2 from txt files
    h2, w2 = img2.shape[:2] #get image height and width

    # Generate new camera matrix for undistorted image1
    new_camera_matrix1, _ = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs,
                                                        (w1, h1), 1, (img1.shape[1], img1.shape[0]))
    # Generate new camera matrix for undistorted image 2
    new_camera_matrix2, _ = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs,
                                                        (w2, h2), 1, (img2.shape[1], img2.shape[0]))
    # Undistort the image 1
    undistorted_img1 = cv2.undistort(img1, camera_matrix, dist_coeffs, None, new_camera_matrix1)

    # Undistort the image 2
    undistorted_img2 = cv2.undistort(img2, camera_matrix, dist_coeffs, None, new_camera_matrix2)

    #Call findArucoMarkers function:
    print("--"*30)
    print("Scanning images for ArUco markers...")
    ids1, bboxs1 = findArucoMarkers(undistorted_img1, arucoDict)
    ids2, bboxs2 = findArucoMarkers(undistorted_img2, arucoDict)
    if len(ids1) != 3 and len(ids2) != 3:
        print("Missing or undetectable ArUco markers in both images.")
        sys.exit()
    elif len(ids1) != 3 and len(ids2) == 3:
        print("Missing or undetectable ArUco markers in image 1.")
        sys.exit()
    elif len(ids1) == 3 and len(ids2) != 3:
        print("Missing or undetectable ArUco markers in image 2.")
        sys.exit()
    #Call the stereoVision function
    ids, num_ids, coords_3d, new_tvecs, rvecs = stereoVision(ids1,ids2,bboxs1,bboxs2,
                                                                              undistorted_img1,
                                                                              undistorted_img2,marker_length,
                                                                              new_camera_matrix1, new_camera_matrix2,
                                                                              dist_coeffs, camera_pose_file1,camera_pose_file2)
    #Manage the coordinates with the getCoords function:
    coord, image_axis1, distances = getCoords(ids,num_ids,table_marker_id,coords_3d, new_tvecs,
                                                                             rvecs, marker_length,new_camera_matrix1,
                                                                             dist_coeffs,undistorted_img2, horst_file, object_file, save_file)
    #Save the coordinates and distances in a csv file 
    file_name1 = os.path.splitext(os.path.basename(camera_pose_file1))[0]
    file_name2 = os.path.splitext(os.path.basename(camera_pose_file2))[0]# Extract the file name without extension
    file_name = f"_{file_name1}_{file_name2}"
    print(f"Coordinates: {coord}")
    with open(folder_path + rf'\coordinates{file_name}.csv', 'w') as f:
        f.write("Coordinates:\n")
        for i in range(len(coord)):
            f.write(f"{coord[i]}\n")
        f.write("\nDistances:\n")
        for i in range(len(distances)):
            f.write(f"{distances[i]}\n")
    # Display the image with ArUco marker detections and marker coordinate systems
    img_rs1 = cv2.resize(image_axis1,(900,900))
    cv2.imshow("Axis Image1",img_rs1)
    print("Finished lab mapping.")
    cv2.waitKey(3000)  # Wait for 30 seconds (30000 milliseconds)
    cv2.destroyAllWindows() #end the script
    return
def run_with_error_handling():
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Error details:")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback_details = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        print(traceback_details)
        print("Please check the input files and paths.")
        sys.exit(1)
    return
run_with_error_handling()
sys.exit()