#Detect Aruco markers in images
#______________________________________________
#1. Import the necessary libraries
#______________________________________________
import cv2
from cv2 import aruco as aruco
import numpy as np
from display_detection.Py_scripts.Image_enhancer import run_image_enhancer
#______________________________________________
#Function that finds Aruco markers in images and extracts the coordinates and marker ids
#______________________________________________
def findArucoMarkers(img,img_folder_path, id_list, totalMarkers=1000, draw = False): #image path is used
    # Define the desired dimensions for resizing
    new_width = 640 #new image width
    new_height = 640 #new image height
    image = cv2.resize(img, (new_width, new_height)) #resize the image
    #cv2.imshow("Image",image) #show the resized image
    key = getattr(aruco, f'DICT_4X4_1000') #Define marker dictionary
    arucoDict = aruco.Dictionary_get(key) #Transfer dictionary to aruco function
    arucoParam = aruco.DetectorParameters_create() #Create Detector parameters
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)#transform image into grayscale
    #cv2.imshow("Grayscale", gray)
    bboxs, ids, _ = aruco.detectMarkers(gray, arucoDict, parameters = arucoParam) #retrieve the marker corner coordinates and IDs
    
    print(f"Detected bounding bboxs: {bboxs} and IDs:{ids}") #Print the bboxs and IDs into the 
    #Detection of the marker coordinates & Ids
    if len(bboxs) <= 1: #Print if no markers are detected
        print("At least one marker was not detected. Image enhancement begins...")
        bboxs = None
        ids = None
        image_enhanced = run_image_enhancer(img_folder_path) #enhance image if at least one marker was not detected
        image_return = cv2.resize(image_enhanced, (new_width, new_height)) #resize enhanced image
        cv2.imshow("Enhanced image", image_return) #show enhanced image
        gray_enhanced = cv2.cvtColor(image_return, cv2.COLOR_BGR2GRAY)#transform image into grayscale for marker detection
        bboxs, ids, _ = aruco.detectMarkers(gray_enhanced, arucoDict, parameters = arucoParam) #retrieve marker corner coordinates and IDs after enhancement
        if draw: #if drwa parameter is True draw detected IDs and corners into image
            aruco.drawDetectedMarkers(image_return, bboxs, ids) #Draw image with detected ids and bboxs
            #cv2.imshow("Markers",resized_enhanced)
    elif len(bboxs) > 2: #if more than two markers were detected try to correct the data
        print("Too many markers detected. Identify defined ids")
        print(f"IDs: {ids}")
        for id_nr in range(len(ids)):
            if ids[id_nr] not in id_list:
                ids = np.delete(ids, id_nr)
        print(f"Ids corrected: {ids}")
        #print(ids)

        #Draw bounding box around marker
        if draw:
            aruco.drawDetectedMarkers(image, bboxs, ids) #Draw image with detected ids and bboxs
            # Resize the image
            resized_image = cv2.resize(img, (new_width, new_height))
            cv2.imshow("Markers",resized_image)
        image_return = image
        
    else:
        #print(ids)
        #Draw bounding box around marker
        if draw:
            aruco.drawDetectedMarkers(image, bboxs, ids) #Draw image with detected ids and bboxs
            # Resize the image
            resized_image = cv2.resize(img, (new_width, new_height))
            cv2.imshow("Markers",resized_image)
        image_return = image
            
    return bboxs,ids, image_return #return bounding box coordinates and ids
