#1. Import the necessary libraries
import cv2
import sys
#______________________________________________
#Function that processes the images for prediction
#______________________________________________
def processImage(bboxs, ids,img): # use the found aruco marker coordinates and ids
    #Define the variables
    id1 = None
    id2 = None
    bbox1 = None
    bbox2 = None
    img_res = None
    if  len(bboxs)!=0: # if the detected arucomarker array is not empty
        id1 = int(ids[0]) #define id 1
        id2 = int(ids[1]) #define id 2
        bbox1 = bboxs[0][0][0]   #define bbox1
        bbox2 = bboxs[1][0][0]   #define bbox2
        print("First ID is ", id1, " with the bounding box coordinates:\n",bbox1)
        print("Second ID is ", id2, " with the bounding box coordinates:\n",bbox2)
        #cv2.imshow('img',img)
    else:
        print("Not enough markers detected")
        sys.exit()
    #______________________________________________
    #Use IDs and bbox coordinates to crop the image to the display size
    #______________________________________________
    #define left upper corners of id1 and id2
    lu_id1 = bbox1[0]
    #print(f"Lu ID {id1}: {lu_id1[1]}")
    lu_id2 = bbox2[0]
    #define right upper corners of id1 and id2
    ru_id1 = bbox1[1]
    ru_id2 = bbox2[1]
    #define right lower corners of id1 and id2
    rl_id1 = bbox1[2]
    rl_id2 = bbox2[2]
    #define left lower corners of id1 and id2
    ll_id1 = bbox1[3]
    ll_id2 = bbox2[3]
    #Define which marker is left and right of the display
    #Use the right upper marker coordinates of the left marker
    #Use the left lower marker coordinates of the right marker
    if lu_id1[0] < lu_id2[0]: #if left upper x-coordinate value of id 2 is greater than of id1
        #Id1 = left upper marker --> ru corner coordinates used
        #print(f"left upper marker ID{id1}")
        ru_x = int(ru_id1[0]) 
        ru_y = int(ru_id1[1])
        ll_x = int(ll_id2[0]) 
        ll_y = int(ll_id2[1])
        #print(f"ru marker: {ru_x} , {ru_y} \n ll marker: {ll_x} , {ll_y}")
        img_res = img[ru_y:ll_y, ru_x:ll_x]#crop image
        #print(img_res)
        new_width = 200
        new_height = 100
        image = cv2.resize(img_res, (new_width, new_height))
        cv2.imshow("Image",image)
        cv2.imshow("Cropped", img_res)#Show cropped image
    elif lu_id1[0] > lu_id2[0]: # else if left upper x-coordinate value of id 1 is greater than of id2
        #print(f"right marker ID{id1}")
        #Id1 = lower right marker --> ll
        #print(f"right lower marker ID {ID1}")
        ru_x = int(ru_id2[0]) 
        ru_y = int(ru_id2[1])
        ll_x = int(ll_id1[0]) 
        ll_y = int(ll_id1[1])
        #print(f"ru marker: {ru_x} , {ru_y} \n ll marker: {ll_x} , {ll_y}")
        img_res = img[ru_y:ll_y, ru_x:ll_x]#crop image
        #print(img_res)
        new_width = 200
        new_height = 100
        image = cv2.resize(img_res, (new_width, new_height))
        cv2.imshow("Image",image)
        cv2.imshow("Cropped", img_res)#Show cropped image
    return img_res #return the cropped image
