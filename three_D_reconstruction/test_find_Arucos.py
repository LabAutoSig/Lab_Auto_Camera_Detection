#______________________________________________
#Import necessary libraries
#______________________________________________
#Freecad libraries
import sys 
#Aruco marker and data handling libraries
import cv2
import cv2.aruco as aruco 
import numpy as np
import sys
import os
import traceback

 
def main():
    #Define the image, save and model paths for your individual folder structure
    # Display the undistorted image
    horst_file =r"three_D_reconstruction\HORST_world\World.FCStd"
    object_file =r"three_D_reconstruction\HORST_world\test.stp"
    save_file = r"three_D_reconstruction\HORST_world\Robot_with_object_new.FCStd"

    #___________Load Data_____________________
    marker_length = 25 #aruco marker side length
    # Load the camera parameters (you may need to calibrate your camera separately if you used a different camera)
    #Camera used: Raspberry Pi V2 camera module
    camera_matrix = [] #intrinsic camera matrix
    dist_coeffs = [] #distortion coefficients for the camera lense
    arucoDict = aruco.getPredefinedDictionary(aruco.DICT_4X4_1000) #define used aruco marker dicitonary
    #Load distortion coefficients and camera matrix from the npz file 
    with np.load(r'three_D_reconstruction\Calibration\calibration_parameters.npz') as data:
        camera_matrix = data['camera_matrix'] #the data is saved under defined names 
        dist_coeffs = data['dist_coeffs']
    print(f"Calibration parameters:")
    print("--"*30)
    print(f"Camera intrinsic matrix: \n {camera_matrix} \n \n Distortion coefficients: \n {dist_coeffs}")

    #_________Image 1___________
    #Load the first image --> change path
    img = cv2.imread(r'three_D_reconstruction\input\test.jpg')#modified
    camera_pose_file1 = r'three_D_reconstruction\input\camera_pose1.txt'#Load camera pose1 from txt files
    #cv2.imshow("Img1 resized", cv2.resize(img1,(900,900)))
    # Get the image shape
    h1, w1 = img.shape[:2] #get image height and width

    # Generate new camera matrix for undistorted image1
    new_camera_matrix1, _ = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs,
                                                        (w1, h1), 1, (img.shape[1], img.shape[0]))
    # Undistort the image 1
    undistorted_img1 = cv2.undistort(img, camera_matrix, dist_coeffs, None, new_camera_matrix1)

    #Call findArucoMarkers function:
    print("--"*30)
    print("Scanning images for ArUco markers...")

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
    draw = True
    if draw: #if draw == True draw Marker corners and ids
        aruco.drawDetectedMarkers(img, bboxs, ids) #Draw image with detected ids and bboxs
    #cv2.imshow("Image",img)
    img_rs = cv2.resize(img,(900,900)) #Resize image for better visualization
    #cv2.imshow("Resized Image",img_rs) #Show image
    print("--"*30)
    print(f"Number of detected markers: {num_ids}")
    print(f"Detected marker IDs: {ids.flatten()}") #Print detected ids
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