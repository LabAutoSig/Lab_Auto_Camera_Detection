#New Camera calibration
#https://sharad-rawat.medium.com/raspberry-pi-camera-module-calibration-using-opencv-f75ff9fc1441
#Import necessary libraries
import cv2
import cv2.aruco as aruco
import glob
import numpy as np
import math
import uuid
import os
import sys 
import traceback
def read_chessboards(images, board):
    allCorners = []
    allIds = []
    decimator = 0
    imsize = None

    for im in images:
        frame = cv2.imread(im)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict)

        if len(corners) > 0:
            for corner in corners:
                cv2.cornerSubPix(
                    gray, corner,
                    winSize=(3, 3),
                    zeroZone=(-1, -1),
                    criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.00001)
                )
            res2 = cv2.aruco.interpolateCornersCharuco(corners, ids, gray, board)
            if res2[1] is not None and res2[2] is not None and len(res2[1]) > 3:
                allCorners.append(res2[1])
                allIds.append(res2[2])
            else:
                print(f"Not enough Charuco corners detected in image: {im}")

        imsize = gray.shape

    print(f"Number of detected Charuco corners: {len(allCorners)}")
    print(f"Number of detected Charuco IDs: {len(allIds)}")
    return allCorners, allIds, imsize

def calibrate_camera(allCorners, allIds, imsize, board):
    if len(allCorners) == 0 or len(allIds) == 0:
        print("Error: No valid Charuco corners or IDs detected.")
        exit()

    print("CAMERA CALIBRATION")
    ret, camera_matrix, dist_coeffs, r_vecs, t_vecs = cv2.aruco.calibrateCameraCharuco(
        charucoCorners=allCorners,
        charucoIds=allIds,
        board=board,
        imageSize=imsize,
        cameraMatrix=None,
        distCoeffs=None
    )
    return ret, camera_matrix, dist_coeffs, r_vecs, t_vecs


def main(sqWidth, sqHeight, chess, aruco_marker, aruco_dict, images, save_path_calib):
    board = cv2.aruco.CharucoBoard([sqWidth,sqHeight],chess,aruco_marker,aruco_dict)

    allCorners,allIds,imsize=read_chessboards(images, board)
    print(f"Number of detected Charuco corners: {len(allCorners)}")
    print(f"Number of detected Charuco IDs: {len(allIds)}")
    ret, mtx, dist, rvecs, tvecs = calibrate_camera(allCorners,allIds,imsize, board)
    print("camera matrix")
    print(mtx)
    print("distortion coefficients")
    print(dist)

    # Save the calibration parameters to a file
    np.savez(save_path_calib, camera_matrix=mtx, dist_coeffs=dist)
    print(f"Calibration parameters saved to {save_path_calib}")
    return 
def run_with_error_handling(sqWidth, sqHeight, chess, aruco_marker, aruco_dict, images, save_path_calib):
    try:
        main(sqWidth, sqHeight, chess, aruco_marker, aruco_dict, images,save_path_calib)
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Error details:")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback_details = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        print(traceback_details)
        print("Please check the input files and paths.")
        sys.exit(1)
#_________________Input_____________________
images = []
# Define the folder path containing the calibration images
calibration_images_folder = r'Camera_calibration\02_05_2025'
if not os.path.exists(calibration_images_folder):
    print(f"Folder {calibration_images_folder} does not exist.")
    exit()
# Load calibration images from the folder
calibration_image_paths = glob.glob(f"{calibration_images_folder}/*.jpg")
for image_path in calibration_image_paths:
    images.append(image_path)
    print(f"Loaded image: {image_path}")
    
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_1000)     
sqWidth = 5 #number of squares width
sqHeight = 7 #number of squares height
chess = 0.034
aruco_marker = 0.025
save_path_calib = r"Camera_calibration\calibration_parameters_new_images_02_05_25_v2_rasps.npz"
run_with_error_handling(sqWidth, sqHeight, chess, aruco_marker, aruco_dict, images, save_path_calib)



