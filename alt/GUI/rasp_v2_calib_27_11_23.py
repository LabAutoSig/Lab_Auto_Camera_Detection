#New Camera calibration
#https://sharad-rawat.medium.com/raspberry-pi-camera-module-calibration-using-opencv-f75ff9fc1441
#Import necessary libraries
import cv2
import cv2.aruco as aruco
import glob
import numpy as np
import math
import uuid
def read_chessboards(images, board): #input images and board data
    """
    Charuco base pose estimation.
    """
    savepath = 'C:\\Users\\wienbruch\\venv312\\Camera_Calibration\\27_11_23_v2\\Saved_Images\\'
    print("POSE ESTIMATION STARTS:")
    allCorners = []
    allIds = []
    decimator = 0
    board = board
    # SUB PIXEL CORNER DETECTION CRITERION
    #criteria establishes the convergence criteria for an iterative algorithm
    #algorithm stops when desired accuracy or max iteration number is reached
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.00001)
                #desired accuracy       #max number of iterations   #number of iterations = 100 #desired accuracy/threshold for convergence = 0.00001
    for im in images:
        #print("=> Processing image {0}".format(im))
        frame = cv2.imread(im)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #convert image to gray scale
        #detect aruco marker in gray images
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict)

        if len(corners)>0:
            # SUB PIXEL DETECTION
            for corner in corners:
                #refine the positions of corners in an image --> improve accuracy of corner positions
                cv2.cornerSubPix(gray, corner,
                                 winSize = (3,3), # size of the window used for subpixel refinement
                                 zeroZone = (-1,-1),# no zone is used in this case (-1,-1)
                                 criteria = criteria)
            res2 = cv2.aruco.interpolateCornersCharuco(corners,ids,gray,board)#increase corner accuracy
            if res2[1] is not None and res2[2] is not None and len(res2[1])>3 and decimator%1==0:
                allCorners.append(res2[1]) #if res2 is not empty append values to the variables
                allIds.append(res2[2])
                frame = np.array(frame)
                
                aruco.drawDetectedCornersCharuco(frame,res2[1],res2[2])
                aruco.drawDetectedMarkers(frame,corners,ids)
                im_rs = cv2.resize(frame,(900,900))
                #cv2.imshow("Detected Corners",im_rs)
                # Filename --> change path depending on your location
                filename = savepath + 'result_calib_' + str(uuid.uuid4()) + '.jpg' #save image under random name
                # Save the image
                cv2.imwrite(filename, im_rs) #save image

                
        decimator+=1
    imsize = gray.shape
    return allCorners,allIds,imsize

def calibrate_camera(allCorners,allIds,imsize, board):
    """
    Calibrates the camera using the dected corners.
    """
    board = board

    print("CAMERA CALIBRATION")
    #print(f"Sensor width and height: {sensor_width} and {sensor_height}")

    (ret, camera_matrix, dist_coeffs,
     r_vecs, t_vecs) = cv2.aruco.calibrateCameraCharuco(
                      charucoCorners=allCorners,
                      charucoIds=allIds,
                      board=board,
                      imageSize=imsize,cameraMatrix=None,distCoeffs=None)

    return ret, camera_matrix, dist_coeffs, r_vecs, t_vecs

#_________________Input_____________________
images = []
# Define the folder path containing the calibration images
calibration_images_folder = 'C:\\Users\\wienbruch\\venv312\\Camera_Calibration\\27_11_23_v2'
# Load calibration images from the folder
calibration_image_paths = glob.glob(f"{calibration_images_folder}/*.png")
for image_path in calibration_image_paths:
    images.append(image_path)
    
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_1000)     
sqWidth = 5 #number of squares width
sqHeight = 7 #number of squares height
board = cv2.aruco.CharucoBoard([sqWidth,sqHeight],0.034,0.025,aruco_dict)

allCorners,allIds,imsize=read_chessboards(images, board)
ret, mtx, dist, rvecs, tvecs = calibrate_camera(allCorners,allIds,imsize, board)
print("camera matrix")
print(mtx)
print("distortion coefficients")
print(dist)

#Save the calibration parameters to a file 
np.savez("calibration_parameters_new_images_27_11_v2_rasps.npz", camera_matrix=mtx, dist_coeffs=dist)
