#Detect Aruco markers in images
#Display text recognition with a trained model
#Detection with yolov8
#______________________________________________
#1. Import the necessary libraries
#______________________________________________
import cv2
import cv2.aruco as aruco 
import numpy as np
import imutils
import uuid
from ultralytics import YOLO
import torch
import pandas as pd
import subprocess
import sys
#______________________________________________
#Function that finds Aruco markers in images and extracts the coordinates and marker ids
#______________________________________________
def findArucoMarkers(img,img_folder_path, id_list ,user, user_path, totalMarkers=1000, draw = False): #image path is used
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
        image_enhanced = run_image_enhancer(img_folder_path, user, user_path) #enhance image if at least one marker was not detected
        resized_enhanced = cv2.resize(image_enhanced, (new_width, new_height)) #resize enhanced image
        image_return = resized_enhanced
        cv2.imshow("Enhanced image", resized_enhanced) #show enhanced image
        gray_enhanced = cv2.cvtColor(resized_enhanced, cv2.COLOR_BGR2GRAY)#transform image into grayscale for marker detection
        bboxs, ids, _ = aruco.detectMarkers(gray_enhanced, arucoDict, parameters = arucoParam) #retrieve marker corner coordinates and IDs after enhancement
        if draw: #if drwa parameter is True draw detected IDs and corners into image
            aruco.drawDetectedMarkers(resized_enhanced, bboxs, ids) #Draw image with detected ids and bboxs
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
#______________________________________________
#Function that sorts the pixel coordinates of the marker corners to have the same orientation of the markers
#______________________________________________
def sorted_corners(bboxes):

    sorted_bboxes = []

    for bbox_tuple in bboxes:
        bbox = bbox_tuple[0]
        #print(f"Bounding box before sorting {bbox}")
        #indexed_arr = [(i, subarr) for i, subarr in enumerate(bbox)] #subarrays are indexed
        #print(f"Indexed array before sorting {indexed_arr}")
        
        if len(bbox) >= 1:

            # Sort the bbox depending on the y coordinate using the sorted lambda key
            sorted_coordinates = sorted(bbox, key=lambda x: x[1], reverse=False)

            # Convert the result back to a NumPy array
            sorted_coordinates = np.array(sorted_coordinates)
            #print(f"Sorted coordinates {sorted_coordinates}")
            #Split array into upper and lower coordinate corners
            upper_coordinates = sorted_coordinates[:2]
            lower_coordinates = sorted_coordinates[2:]
            #print(f"Upper coordinates: {upper_coordinates}")
            #print(f"Lower coordinates: {lower_coordinates}")

            # Sort the upper corners depending on the x coordinate using the sorted lambda key 
            sorted_upper = sorted(upper_coordinates, key=lambda x: x[0], reverse=False)

            # Convert the result back to a NumPy array
            sorted_upper= np.array(sorted_upper)
            #print(f"Sorted upper {sorted_upper}")
            
            # Sort the lower coordinates based on the x-coordinate in descending order
            sorted_lower = sorted(lower_coordinates, key=lambda x: x[0], reverse=True)

            # Convert the result back to a NumPy array
            sorted_lower= np.array(sorted_lower)
            #print(f"Sorted lower {sorted_lower}")

            # Concatenate the sorted upper and lower coordinates
            sorted_bbox = np.concatenate((sorted_upper, sorted_lower), axis=0)
            #print(f"Sorted bounding box {sorted_bbox}")

            #convert the result back to an array
            sorted_arrays = np.array([sorted_bbox])
            #print(f"Sorted bounding boxes: {sorted_bboxes}")

        else:
            # If only one set of corners, no need to sort
            sorted_arrays = bbox

        #print(f"Sorted Array: {sorted_arrays}")
        sorted_bboxes.append((sorted_arrays,))

    return sorted_bboxes

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

#______________________________________________
#Function that predicts the values in an image
#______________________________________________
def yoloPredict(croppedimg, path, savepath,ids, cropped_path, output_path, user, user_path):
    #use the cropped image, the model path and the path for saving the images
    #YOLO Version: YOLOv8
    #Dataset from: Roboflow
    #Training source: Kaggle.com
    values = []
    print(f"Yolo predict image for ids: {ids}")
    #Load the model --> Change path depending on where you saved your model
    model = YOLO(path)
    #Predict the image values
    im2 = cropped
    results = model.predict(source=im2, save=True, show=False, save_txt=True)
    # print(results)
    if len(results) == 0:
        print("No predictions were made. Enhance the cropped image")
        #cropped_path = r'C:\Users\wienbruch\venv311\Display_detection_system_11_23\cropped_img.jpg'
        image_enhanced = run_image_enhancer(cropped_path, user, user_path)

    #don't save and show predicted image,save txt file
    # results saves predictions as labels
    res_plotted = results[0].plot(font_size=0.1, conf=False)
    #show plotted img, font size = text size, conf = confidence level

    #new_width = 300
    #new_height = 200
    #res = cv2.resize(res_plotted, (new_width, new_height))
    cv2.imshow("result", res_plotted)
    

    # Filename --> change path depending on your location
    filename = savepath + 'result_' + str(uuid.uuid4()) + '.jpg' #save image under random name
    # Save the image
    cv2.imwrite(filename, res_plotted) #save image

    #Define the variables
    b =[]
    #bn = []
    conf = []
    classes = []
    names = []

    #Extract results and save as numpy arrays
    for result in results:
        # detection
        #b = result.boxes.xyxy[0]   # box with xyxy format, (N, 4)
        #b = result.boxes.xywh   # box with xywh format, (N, 4)
        b = result.boxes.xyxyn  # box with xyxy format but normalized, (N, 4)
        #bn = result.boxes.xywhn  # box with xywh format but normalized, (N, 4)
        conf = result.boxes.conf   # confidence score, (N, 1)
        classes = result.boxes.cls    # cls, (N, 1)

        #convert values to numpy arrays
        b = b.numpy()
        #bn = bn.numpy()
        conf = conf.numpy()
        classes = classes.numpy()
        
        for c in result.boxes.cls: #Extract class names 
            n = model.names[int(c)] # Convert names to integers
            names.append(n) #Append Names to list names
            print(f"Names of the identified classes: {names}")
    #________________________________________________________________________
    # Sort and correct data
    #________________________________________________________________________

    #Build a dataframe
    df = pd.DataFrame(zip(names,classes,conf,b),columns=['Names','Classes',
                                                            'Confidence Interval',
                                                            'XYXYn'])
    if df.empty:
        print("No values predicted/detected")
        print("Enhance image...")
        #cropped_path = r'C:\Users\wienbruch\venv311\Display_detection_system_11_23\cropped_img.jpg'
        image_enhanced = run_image_enhancer(cropped_path)
        values = None
        return values
    
    #Split Coordinate column into separate x and y columns
    df['x_top'],df['y_top'],df['x_bottom'],df['y_bottom'] = zip(*list(df['XYXYn'].values))
    df_letters = df
    # Delete words/letters in dataframe
    words_to_remove = ['lid', 'T','E', 'M', 'P', 'g','min','numbers-and-things',
                       'numbers-weights', 'pH', 'temp','°C','-C', 'SV', 'Stop',
                       'Temp.',':','ATC','F','I','O','PV','R','RCF','RPM',
                       'Smiley','Stern','Time','U',]
    df_letters = df_letters[~df_letters['Names'].isin(words_to_remove)]
    #print(f" Dataframe without string values: \n {df_letters}")

    #Sort the dataframe values by the position of the bounding boxes in the picture
    df_new = df_letters.sort_values(by =['x_top'], ascending = True)
    df_new = df_new.reset_index(drop=True) # reset indexes 
    print(f"Sorted Dataframe from left to right: \n {df_new}")
    # Filter out rows with Confidence Interval smaller than 0.5
    df_new = df_new[df_new['Confidence Interval'] >= 0.4]
    df_new = df_new.reset_index(drop=True)  # Reset indexes
    print(f"Dataframe without numbers with a confidence interval smaller 0.4 \n {df_new}")
    df_new = drop_firstPoint(df_new)
    
    #_____________Split values when there are two rows______________________
    dataframe1, dataframe2 = check_row(df_new)

    if not dataframe1.empty:
        print(f"Sort data again, df1: {dataframe1}")
        #Sort the dataframe values by the position of the bounding boxes in the picture
        dataframe1 = dataframe1.sort_values(by =['x_bottom'], ascending = True)
        dataframe1 = dataframe1.reset_index(drop=True) # reset indexes
        print(f"Sorted df1: {dataframe1}")
    if not dataframe2.empty:
        #Sort the dataframe values by the position of the bounding boxes in the picture
        print(f"Sort data again, df2: {dataframe2}")
        dataframe2 = dataframe2.sort_values(by =['x_bottom'], ascending = True)
        dataframe2 = dataframe2.reset_index(drop=True) # reset indexes
        print(f"Sorted df2: {dataframe2}")
        dataframe2 = drop_firstPoint(dataframe2)

       
    # Filter out rows with Confidence Interval smaller than 0.5
    #dataframe1 = dataframe1[dataframe1['Confidence Interval'] >= 0.5]
    #dataframe1 = dataframe1.reset_index(drop=True)  # Reset indexes
    if dataframe1.empty:
        dataframe1_new = dataframe2
        dataframe2 = dataframe1
        dataframe1 = dataframe1_new
        #Sort the dataframe values by the position of the bounding boxes in the picture
        dataframe1 = dataframe1.sort_values(by =['x_bottom'], ascending = True)
        dataframe1 = dataframe1.reset_index(drop=True) # reset indexes
        #print(f"Dataframe 1 empty: \n {dataframe1}")
    print(f"Split dataframe 1: \n {dataframe1}")
    print(f"Split dataframe 2: \n {dataframe2}")
  

    #_________________Single row: Split data if there is a gap greater than the threshold_________________________
    if dataframe2.empty: #if there is no data in dataframe2
        #Sort the dataframe values by the position of the bounding boxes in the picture
        dataframe1 = dataframe1.sort_values(by =['x_bottom'], ascending = True)
        dataframe1 = dataframe1.reset_index(drop=True) # reset indexes
        dataframe1, dataframe2 = split_gap_single_row(dataframe1)
        
    #___________Correct data if two bounding boxes are nearly equal__________________
    
    dataframe1 = nearly_equal_bboxs(dataframe1)
    dataframe1 = drop_twin_point(dataframe1)
    if len(dataframe1) == 1 and dataframe1["Names"][0] == "OFF":
        print("Device value = OFF")
        value1 = None
    elif len(dataframe1) == 2:
        if dataframe1["Names"][0] == "OFF" or dataframe1["Names"][1] == "OFF":
            print("Device value = OFF")
            value1 = None
        else:
            value1 = float(''.join(map(str, dataframe1['Names'])))
    else:
        value1 = float(''.join(map(str, dataframe1['Names'])))
    
    #Save value1 as float --> join all values of names
    values.append(value1) #Append value1 to values
    #print(f"DATAFrame2 : {dataframe2}")
    
    if not dataframe2.empty: # when there are two rows
        #d_names2 = df2_dropped["Names"]
        dataframe2 = nearly_equal_bboxs(dataframe2)
        dataframe2 = drop_twin_point(dataframe2)
        
        #print("Corrected dataframe 2 for nearly equal bounding boxes: \n {dataframe2}")
        if dataframe2["Names"][0] != "OFF":
            value2 = float(''.join(map(str, dataframe2['Names'])))
        else:
            value2 = None
        #save value 2 as float --> join all values of names
    elif dataframe2.empty:
        value2 = None
    print("First value: ", value1)
    print("Second value: ",value2)
    #f.write(f"{value2} °C \n")
    #f.write(f"{value2}\n")
    values.append(value2) #append value2 to values
        

        
    #_________________Data correction: inspect data for missing/false points and data________________________
            
    #print(f"Dataframes before correction: df1 \n {dataframe1} \n df2 \n {dataframe2}")
    df1,df2 = control_data(ids,dataframe1,dataframe2, values)
    #print(f"Controlled data: \n {df1} and \n {df2}")
    value1 = float(''.join(map(str, df1["Names"]))) #join Name values 0 till j as float
    if not len(df2) == 0:
        value2 = float(''.join(map(str, df2["Names"]))) #join Name values j and the rest as float
    else:
        value2 = None
    values_corrected =[]
    values_corrected.append(value1)
    values_corrected.append(value2)
    combined_dataframe = pd.concat([df1[['Names', 'Confidence Interval']], df2[['Names', 'Confidence Interval']]], ignore_index=False)
    combined_df = pd.concat([df1[['Names', 'Confidence Interval']], df2[['Names', 'Confidence Interval']]], ignore_index=False)
    ids_df = pd.DataFrame(ids, columns = ["IDs"])
    results_df = pd.DataFrame(values_corrected, columns=["Predicted values"])
    print(f"Results df: {results_df}")
    print(f"Ids df: {ids_df}")
    ids_df.to_csv(output_path,sep='\t',mode= 'w', encoding='utf-8',index=False) # a = append, x = exclusive creation, w = truncate
    results_df.to_csv(output_path,sep='\t',mode= 'a', encoding='utf-8',index=False)
    combined_dataframe.to_csv(output_path,sep='\t',mode= 'a', encoding='utf-8',index=False)
    
    data_processing(output_path, user, user_path)
    
    return values_corrected #return the values

#___________Split dataframe if display has two rows____________
def check_row(df_new):
    dataframe1 = df_new
    dataframe2 = pd.DataFrame(data=None, columns=['Names', 'Classes', 'Confidence Interval', 'XYXYn', 'x_top', 'y_top', 'x_bottom', 'y_bottom'])
    result_rows = []  # List to store new rows
    dif = df_new["y_bottom"].diff()  # calculate difference between bottom y coordinates
    print(f"Difference y_bottom {dif}")
    height = df_new["y_bottom"]

    if len(df_new) > 1:
        is_active_dataframe = None # Flag to keep track of the active DataFrame
        i = 0
        while i in range(len(df_new["y_bottom"])-1):
            if dif[i] < -0.15 or dif[i] > 0.15:
                print(f"Detected two-row display at idx {i}. Sort data")

                height1 = height[i-1]
                height2 = height[i]

                if height1 > height2: #if y_bottom pixel coordinate  at i-1 is bigger
                    #i-1 is lower row and i upper row
                    print(f"Idx{i}-1 is lower row")
                    new_row = dataframe1.iloc[i-1]
                    dataframe1 = dataframe1.drop(labels = i-1, axis = 0)
                    print(f"Dataframe1 without lower row {dataframe1}")
                    
                    #print(f"new row: {new_row}")
                    result_rows.append(new_row)  # Append the new row to the list
                    print(f"Result row:\n {result_rows}")


                    #dataframe2 = dataframe2.append(new_row)
                    #print(f"Dataframe2 only with lower row {dataframe2}")
                    dataframe1 = dataframe1.reset_index(drop=True) #reset indexes
                    height = dataframe1["y_bottom"]
                    dif = dataframe1["y_bottom"].diff()
                    print(f"New df1 \n {dataframe1} with new difference y bottom \n {dif}")
                    i=0
                    
                elif height2 > height1: #if y_bottom pixel coordinate  at i is bigger
                    #i is lower row and i-1 upper row
                    print(f"{i} is lower row")
                    new_row = dataframe1.iloc[i]
                    dataframe1 = dataframe1.drop(labels = i, axis = 0)
                    print(f"Dataframe1 without lower row {dataframe1}")
                    
                    #print(f"new row: {new_row}")
                    result_rows.append(new_row)  # Append the new row to the list
                    print(f"Result row: \n {result_rows}")
                    #dataframe2 = dataframe2.append(new_row)
                    #print(f"Dataframe2 only with lower row {dataframe2}")
                    dataframe1 = dataframe1.reset_index(drop=True) #reset indexes
                    height = dataframe1["y_bottom"]
                    dif = dataframe1["y_bottom"].diff()
                    
                    print(f"New df1 \n {dataframe1} with new difference y bottom \n {dif}")
                    i=0
                
            elif i+1 < len(dataframe1):
                i+=1
                print(f"Set i to: {i}")
                #new_row = df_new.iloc[i]
                #print(f"new row: {new_row}")
                #result_rows.append(new_row)  # Append the new row to the list
                #print(f"Result row: {result_rows}")
            else:
                break
            
            

        dataframe2 = pd.DataFrame(result_rows)  # Create DataFrame from the list of rows
        dataframe1 = dataframe1.reset_index(drop=True) #reset indexes
        dataframe2 = dataframe2.reset_index(drop=True) #reset indexes
    else:
        dataframe1 = df_new

    print(f"Corrected dataframe1 for two rows: \n {dataframe1}")
    print(f"Corrected dataframe2 for two rows: \n {dataframe2}")

    return dataframe1, dataframe2

def split_gap_single_row(dataframe1):
    dataframe2 = pd.DataFrame(data = None,columns=['Names','Classes','Confidence Interval','XYXYn','x_top','y_top','x_bottom','y_bottom'])
    dif = dataframe1["x_bottom"].diff() #calculate difference between x_bottom values
    print(f"Difference x_bottom: \n {dif}")
    if len(dataframe1)> 1:
        print("Check if dataframe has to separate values")
        for j in range(len(dataframe1["x_bottom"])): #as long as j is in range of length x_bottom
                
            if dif[j] > 0.2: #if the difference is greater than 0.2
                print("Split data if there is a great gap in between the data")
                    
                #value = float(''.join(map(str, df["Names"]))) #join Name values
                df1 = dataframe1['Names'] #extract dataframe1 Names

                # Create a new dataframe with rows after the gap
                dataframe2 = dataframe1.loc[j:].reset_index(drop=True)
                
                # Update dataframe1 to keep only the rows before the gap
                dataframe1 = dataframe1.loc[:j-1].reset_index(drop=True)
                break #stop the loop when a difference bigger than 0.2 was found
    return dataframe1, dataframe2

#__________Drop first value if it is a point___________________
def drop_firstPoint(dataframe):
    df_names = dataframe["Names"]
    print("Drop first point")
    #print(dataframe["Names"][0])
    df = None
    if len(dataframe) == 1:
        print("Only one value in the dataframe")
        if dataframe["Names"][0] == ".":
            dataframe.drop(labels = 0, axis = 0, inplace = True)
            #dataframe erase label at 0
            df = dataframe.reset_index(drop=True) #reset indexes
            print("Dataframe is now empty")
        else:
            df = dataframe
        
    elif len(dataframe) > 1:
        print("Multiple values in the dataframe")

        for name in range(len(dataframe)):
            if dataframe["Names"][name] == ".":
                dataframe.drop(labels = name, axis = 0, inplace = True)
                #dataframe erase label at 0
            else:
                df = dataframe
                break
        df = dataframe.reset_index(drop=True) #reset indexes
    elif len(dataframe) == 0:
        df = dataframe
            
    print(f"Dataframe after point drop: \n {df}")
    return df

#____________Drop a point if two points are next to each other_________
def drop_twin_point(dataframe):
    names = dataframe["Names"]
    print(f"Drop twin points names: {names}")
    if len(names) > 0:
        if  names.str.contains('OFF').any():
            print("Value is OFF")
            for x in range(len(dataframe["Names"])-1):
                if names[x] != "OFF":
                    dataframe.drop(labels = x, axis =0, inplace = True)#dataframe erase label at i
                    dataframe = dataframe.reset_index(drop=True) #reset indexes
                    print(dataframe)
            
        else:
            a = 0
            while a in range(len(dataframe["Names"])-1):
                new_dataframe = dataframe
                if dataframe["Names"][a] == "." and dataframe["Names"][a+1]== ".":
                    conf = dataframe['Confidence Interval'] #Confidence Interval of dataframe
                    num1 = conf[a] # Confidence level at a
                    num2 = conf[a+1] #Confidence level at a+1
                    if num1 > num2: #if Confidence level at i is higher
                        dataframe.drop(labels = a+1, axis = 0, inplace = True)
                        #dataframe erase label at i+1
                        dataframe = dataframe.reset_index(drop=True) #reset indexes
                        a = 0
                        print(dataframe)
                    
                    elif num1 < num2: #if Confidence level at i+1 is higher
                        dataframe.drop(labels = a, axis =0, inplace = True)#dataframe erase label at i
                        dataframe = dataframe.reset_index(drop=True) #reset indexes
                        print(dataframe)
                        a = 0
                elif a+1 < len(dataframe):
                    a+=1
                    print(f"Set a to: {a}")
                else:
                   break
                        
    else:
        print("Dataframe is empty. False prediction")
        sys.exit()
    print(f"Corrected dataframe for twin points bounding boxes: \n {dataframe}")
                   
    return dataframe

def nearly_equal_bboxs(dataframe):
    #___________Correct data if two bounding boxes are nearly equal__________________

    dif = dataframe['x_bottom'].diff() #calculate difference between bottom x coordinates
    #dif.drop(labels = 0, axis =0, inplace = True)#dataframe erase label at i
    #dif = dif.reset_index(drop=True) #reset indexes
    print(f"Difference x_bottom {dif}")
    conf = dataframe['Confidence Interval'] #Confidence Interval of dataframe
    for i in range(len(dataframe["x_bottom"])): # if i is in range of the length of x_bottom
        print(i)
        if -0.0025 < dif[i] < 0.0025: #if the difference between the bottom x coordinates is...
            print(f"detected overlapping numbers. check confidence interval: at {i}")
            
            num1 = conf[i-1] # Confidence level at i-1
            num2 = conf[i] #Confidence level at i
            if num1 > num2: #if Confidence level at i-1 is higher
                dataframe.drop(labels = i, axis = 0, inplace = True)
                #dataframe erase label at i
        
            elif num1 < num2: #if Confidence level at i is higher
                dataframe.drop(labels = i-1, axis =0, inplace = True)#dataframe erase label at i-1
                #dataframe = dataframe.reset_index(drop=True) #reset indexes
    dataframe = dataframe.reset_index(drop=True) #reset indexes
    print(f"Corrected dataframe for nearly equal bounding boxes: \n {dataframe}")
    return dataframe

def second_overlap_control(dataframe):
    #___________Correct data if two bounding boxes are nearly equal__________________
    print("Wrong number predicted, look again for bounding box overlap...")
    dif = dataframe["x_bottom"].diff() #calculate difference between bottom x coordinates
    print(f"Bounding box x_bottom difference: \n {dif}")
    conf = dataframe['Confidence Interval'] #Confidence Interval of dataframe1
    for i in range(len(dataframe["x_bottom"])):
        if -0.0035 < dif[i] < 0.0035: #if the difference between the bottom x coordinates is...
            num1 = conf[i-1] # Confidence level at i-1
            num2 = conf[i] #Confidence level at i
            if num1 > num2: #if Confidence level at i-1 is higher
                dataframe.drop(labels = i, axis = 0, inplace = True)
                #dataframe erase label at i
                
            elif num1 < num2: #if Confidence level at i is higher
                dataframe.drop(labels = i-1, axis =0, inplace = True)#dataframe erase label at i-1
    dataframe = dataframe.reset_index(drop=True) #reset indexes
    print(f"Corrected dataframe for nearly equal bounding boxes: \n {dataframe}")
    return dataframe

def control_data(ids, dataframe1, dataframe2, values):
    df1_corrected = []
    df2_corrected = []
    print(f"Control predicted and corrected data...")
    print(f"Dataframe1 before correction: {dataframe1}")
    print(f"Dataframe2 before correction: {dataframe2}")
    #Drop '.' if it is the first value in the dataframe
    if len(dataframe1) != 0 and dataframe1["Names"][0]!="OFF":
        #df1 = drop_firstPoint(dataframe1)
        df1 =dataframe1
        val1 = float(''.join(map(str, df1["Names"]))) #join Name values
    
    elif len(dataframe1) != 0 and dataframe1["Names"][0]=="OFF":
        print("Heating function turned off")
        val1 = 0
        dataframe1["Names"][0] = 0
        dataframe2["Confidence Interval"] [0] = None
        df1 = dataframe1
    elif len(dataframe1) == 0:
        print("Dataframe 1 empty, error in number prediction")
        return
    
    if len(dataframe2) != 0 and dataframe2["Names"][0]!="OFF":
        #df2 = drop_firstPoint(dataframe2)
        print("Dataframe 2 not empty.")
        df2  = dataframe2
        val2 = float(''.join(map(str, df2["Names"]))) #join Name values
    
    elif len(dataframe2) != 0 and dataframe2["Names"][0]== "OFF":
        print("Stirring function turned off")
        val2 = 0
        dataframe2["Names"][0] = 0
        dataframe2["Confidence Interval"] [0] = None
        
        df2 = dataframe2
        
    elif len(dataframe2) == 0 and (ids[0] == 42 and ids[1] == 161) or (ids[0] == 161 and ids[1] == 42):
        print("Dataframe 2 empty,display is a scale")
    elif len(dataframe2) == 0 and (ids[0] == 5 and ids[1] == 8) or (ids[0] == 8 and ids[1] == 5):
        print("Dataframe 2 empty,display is a scale")
        
    else:
        print("Dataframe2 empty, false prediction")
        sys.exit()
        return
        
    # _____________VWR MicroStar 12 centrifuge________________________
    if ids[0] == 4 and ids[1] == 1 or ids[0] == 1 and ids[1] ==4:
        print("VWR MicroStar 12 centrifuge")
        #Speed 1.2-13.5 (d= 0.1)
        #timer 1-30 min (d = 1 min)
        #Check if speed value is in the limits and has the correct number of decimal places
        df1_corrected, val1_corrected = number_decimal(df1, val1, 0.1, 13.5, 3, 4, 1)
        #Check if speed value is in the limits and has the correct number of decimal places
        df2_corrected, val2_corrected = number_decimal(df2, val2, 1, 30, 1, 2, 0)
        print(f"Corrected speed dataframe \n {df1_corrected} \n with value: {val1_corrected}")
        print(f"Corrected time dataframe \n {df2_corrected} \n with value: {val2_corrected}")
        
    #_____________________Scales KERN FCE 3K1N________________________________
    elif ids[0] == 42 and ids[1] == 161 or ids[0] == 161 and ids[1] ==42:
        print("KERN FCE 3K1N scales")
        #KERN 0-3000 gram (d=1g)
        #Only one value --> df2 must be empty
        #Check if scale value is in the limits and has the correct number of decimal places
        df1_corrected, val1_corrected = number_decimal(df1, val1, 0, 3000, 1, 4, 0)
        df2_corrected = dataframe2
        print(f"Corrected scale dataframe \n {df1_corrected} \n with value: {val1_corrected}")


    #_____________________Scales CS Series CS200_________________________________
    elif ids[0] == 5 and ids[1] == 8 or ids[0] == 8 and ids[1] == 5:
        print("OHAUS CS Series CS200 scales")
        #CS Series 0-200 gram (d= 0,1g)
        #Only one value --> df2 must be empty
        #Check if speed value is in the limits and has the correct number of decimal places
        df1_corrected, val1_corrected = number_decimal(df1, val1, 0, 200, 3, 5, 1)
        #Check if speed value is in the limits and has the correct number of decimal places
        df2_corrected = dataframe2
        print(f"Corrected scale dataframe \n {df1_corrected} \n with value: {val1_corrected}")

        
    #_____________________Thermo Scientific Digital Shaking Drybath 88880028__________
    elif ids[0] == 2 and ids[1] == 314 or ids[0] == 314 and ids[1] == 2:
        print("Thermo Scientific Digital Shaking Drybath")
        #PV 5,0-100,0 °C (d = 0,1°C)
        #SV 0,0-100,0 °C (d = 0,1°C)
        #Two values --> both df not empty
        #Check if ambient temperature value is in the limits and has the correct number of decimal places
        df1_corrected, val1_corrected = number_decimal(df1, val1, 5.0, 100.0, 3, 5, 1)
        #Check if temperature value is in the limits and has the correct number of decimal places
        df2_corrected, val2_corrected = number_decimal(df2, val2, 0.0, 100.0, 3, 5, 1)              
        print(f"Corrected ambient temp dataframe \n {df1_corrected} \n with value: {val1_corrected}")
        print(f"Corrected temp dataframe \n {df2_corrected} \n with value: {val2_corrected}")

    #_____________________Phoenix Instrument Heating and magnetic stirrer RSM-10HP ___________
    elif ids[0] == 2 and ids[1] == 1 or ids[0] == 1 and ids[1] == 2:
        print("Phoenix Instrument Heating and magnetic stirrer RSM-10HP")
        #Heating 5-280 °C (d = 1°C) 
        #RPM 200-1500 1/min (d= 10rpm)
        #Check if heating temperature value is in the limits and has the correct number of decimal places
        print(df1)
        print(df2)
        if val1 == 0:
            print("Heating turned off. Value = None")
            df1["Names"][0] == 0
            df1["Confidence Interval"][0] = "OFF"
            if len(df1) == 2:
                #df1_corrected = df1[0]
                df1.drop(labels = 1, axis =0, inplace = True)#dataframe erase row at x
                df1_corrected= df1.reset_index(drop=True) #reset indexes
            elif len(df1) ==1:
                df1_corrected = df1
            val1_corrected = 0
        else: 
            df1_corrected, val1_corrected = number_decimal(df1, val1, 5, 280, 1, 3, 0)

        #Check if RPM value is in the limits and has the correct number of decimal places
        if val2 == 0:
            print("Stirring turned off. Value = None")
            df2["Names"][0] == 0
            df2["Confidence Interval"][0] = "OFF"
            df2_corrected = df2
            if len(df2) == 2:
                #df1_corrected = df1[0]
                df2.drop(labels = 1, axis =0, inplace = True)#dataframe erase row at x
                df2_corrected= df2.reset_index(drop=True) #reset indexes
            elif len(df1) ==1:
                df2_corrected = df1
            val2_corrected = 0
        else:
            #Check if stirring value is in the limits and has the correct number of decimal places
            df2_corrected, val2_corrected = number_decimal(df2, val2, 200, 1500, 3, 4, 0)             
        print(f"Corrected heating dataframe \n {df1_corrected} \n with value: {val1_corrected}")
        print(f"Corrected rpm dataframe \n {df2_corrected} \n with value: {val2_corrected}")

    #_____________________XSInstruments pH 50+ DHS S/N180356077___________
    elif ids[0] == 3 and ids[1] == 4 or ids[0] == 4 and ids[1] == 3:
        print("XSInstruments pH 50+ DHS")
        #pH 0-14 pH (d = 0,01 pH) 
        #Temperature 0-100,0°C (d= 0,1 °C)
        #Check if pH value is in the limits and     # Position to insert the row (index)

        df1_corrected, val1_corrected = number_decimal(df1, val1, 0.00, 14.00, 4, 5, 2)
        #Check if ambient temperature value is in the limits and has the correct number of decimal places
        df2_corrected, val2_corrected = number_decimal(df2, val2, 0.0, 100.0, 3, 5, 1)          
        print(f"Corrected pH dataframe \n {df1_corrected} \n with value: {val1_corrected}")
        print(f"Corrected temp dataframe \n {df2_corrected} \n with value: {val2_corrected}")

    else:
        print("ID pair is not defined for a device!")
        sys.exit()

    return df1_corrected, df2_corrected

def check_value_limits(dataframe, value, lower_limit, upper_limit, lower_dec, upper_dec, dec_places):
    #1.1.2 Check if value in limits, digit number in limits
    if lower_limit <= value <= upper_limit and lower_dec <= len(dataframe) <= upper_dec:
        print("Value in correct limits")
        df = dataframe
        print(df)
        val = value
    #1.1.3 Check if value out of limits
    elif lower_limit > value or value > upper_limit:
        #1.1.3.1 Check if number of digits is in limits
        if lower_dec <= len(dataframe) <= upper_dec:
            print("Value is not in limits but value length in limits. Wrong number predicted.")
            if value < lower_limit:
                print("Values is smaller than lower limit. False prediction. Try again or add number manually.")
                sys.exit()
            elif value > upper_limit:
                print("Value is bigger than upper limit. Looking for bbox overlap.")
                #look for overlap and conf
                dataframe = second_overlap_control(dataframe)
                value_new = float(''.join(map(str, dataframe["Names"]))) #join Name values
                if lower_limit > value_new or value_new > upper_limit:
                    #wrong value
                    print("Wrong prediction, try again or read out manually...")
                    sys.exit()
                elif lower_limit <= value_new <= upper_limit and lower_dec <= len(dataframe) <= upper_dec:
                    print("Value corrected")
                    val = value_new
                    df = dataframe        
        #1.1.3.2 Check if number of digits is out of limits
        elif lower_dec > len(dataframe):
            #too little digits
            print("Missing digits, too less predicted")
            print("False prediction. Try again or add number manually.")
            sys.exit()
        elif len(dataframe) > upper_dec:
            #too many digits
            print("Too many digits detected")
            #Check for overlapping bounding boxes
            dataframe = second_overlap_control(dataframe)
            value_new = float(''.join(map(str, dataframe["Names"]))) #join Name values
            if lower_limit > value_new or value_new > upper_limit:
                #wrong value
                print("Wrong prediction, try again or read out manually...")
                sys.exit()

            elif lower_limit <= value_new <= upper_limit and lower_dec <= len(dataframe) <= upper_dec:
                print("Value corrected")
                val = value_new
                df = dataframe

    return df, val

def number_decimal(dataframe, value, lower_limit, upper_limit, lower_dec, upper_dec, dec_places):
    df= []
    df_front = []
    df_dec = []
    val = None
    names_df = dataframe["Names"]
    dot_true = None
    for a in range(len(dataframe["Names"])):
        if names_df[a] == ".":
            dot_true = True
            print("Point in dataframe")
    
    
    #1. Check if value should not have decimal places
    #1.1_______________________Value with no decimal places________________
    if dec_places == 0: 
        print("Value should not have decimal places")
        #1.2__________Check if no point in Dataframe_________
        if dot_true == None: 
            print("Value has correctly no decimal places.")
            df,val = check_value_limits(dataframe, value, lower_limit, upper_limit, lower_dec, upper_dec, dec_places)
                       
        #1.3__________Check if point in Dataframe_______
        elif dot_true == True:
            #erase point in dataframe
            for x in range(len(dataframe["Names"])): # if i is in range of the length of x_bottom
                if names_df[x] == ".": #if a dot is in the dataframe 
                    dataframe.drop(labels = x, axis =0, inplace = True)#dataframe erase row at x
                    dataframe = dataframe.reset_index(drop=True) #reset indexes
            value_erased = float(''.join(map(str, dataframe["Names"]))) #join Name values
            #Check value and length after point erasing
            df,val = check_value_limits(dataframe, value_erased, lower_limit, upper_limit, lower_dec, upper_dec, dec_places)    

    #2. Check if value should have decimal places
    #2.1 ________________________Value with decimal places_______________________________               
    elif dec_places > 0: 
        print(f"Value should have {dec_places} decimal place. Testing...")
        #2.2_________Check if point in Dataframe___________
        if dot_true == True: #if a point is in the dataframe
            print("A point is in the dataframe. Look for correct number of decimal places...")
            for y in range(len(dataframe["Names"])):
                if names_df[y]==".":
                    # Create a new dataframe with rows before the decimal point
                    df_front = dataframe.loc[:y].reset_index(drop=True)
                    df_dec = dataframe.loc[y+1:].reset_index(drop=True)
            if len(df_dec) == dec_places:
                print("Number of decimal places is correct. Point is set correctly. Check value.")
                df, val = check_value_limits(dataframe, value, lower_limit, upper_limit, lower_dec, upper_dec, dec_places)
                    
            elif len(df_dec) < dec_places:  #missing dec_places
                print("Missing decimal places.")
                name = dataframe["Names"]
                if lower_dec <= len(dataframe) <= upper_dec:
                    #Digit length in limits, set point further to the left
                    for r in range(len(dataframe)):
                        if name[r] == ".":
                            row_to_move = dataframe.loc[r].copy() # Copy the row to be moved
                            df = dataframe.drop(r)  # Remove the row from its original position
                            dif_dec = dec_places - len(df_dec)
                            new_position = r - dif_dec
                            #df = df.iloc[:new_position].append(row_to_move).append(df.iloc[new_position:], ignore_index=True)
                            df = pd.concat([df.iloc[:new_position], row_to_move, df.iloc[new_position:]], ignore_index=True) # Insert the row at the new position
                    val = float(''.join(map(str, df["Names"]))) #join Name value
                    df,val = check_value_limits(dataframe, value, lower_limit, upper_limit, lower_dec, upper_dec, dec_places)
                elif lower_dec > len(dataframe):
                    #Digit length out of limits, missing predictions
                    print("Number of predicted digits too small. Try again or add number manually.")
                    sys.exit()
                    
                elif upper_dec < len(dataframe):
                    #Digit length out of limits, too many predictions. Try bboxs overlap
                    dataframe = second_overlap_control(dataframe)
                    value_new = float(''.join(map(str, dataframe["Names"]))) #join Name values
                    if lower_limit > value_new or value_new > upper_limit:
                        #wrong value
                        print("Wrong prediction, try again or read out manually...")
                        sys.exit()

                    elif lower_limit <= value_new <= upper_limit and lower_dec <= len(dataframe) <= upper_dec:
                        print("Value corrected. Set point further to the left...")
                        #Digit length in limits, set point further to the left
                        for r in range(len(dataframe)):
                            if name[r] == ".":
                                row_to_move = dataframe.loc[r].copy() # Copy the row to be moved
                                df = dataframe.drop(r)  # Remove the row from its original position
                                dif_dec = dec_places - len(df_dec)
                                new_position = r -dif_dec
                                #df = df.iloc[:new_position].append(row_to_move, ignore_index = True).append(df.iloc[new_position:], ignore_index=True)
                                df = pd.concat([df.iloc[:new_position], row_to_move, df.iloc[new_position:]], ignore_index=True)
                                # Insert the row at the new position
                        val = float(''.join(map(str, df["Names"]))) #join Name value
                        df, val = check_value_limits(df, val, lower_limit, upper_limit, lower_dec, upper_dec, dec_places)

            elif len(df_dec)> dec_places: #too many dec_places
                #set point further to the right
                print("Too many decimal places.")

                name = dataframe["Names"]
                if lower_dec <= len(dataframe) <= upper_dec:
                    #Digit length in limits, set point further to the right
                    print("Value length in limits.")
                    for r in range(len(dataframe)):
                        if name[r] == ".":
                            row_to_move = dataframe.loc[r].copy() # Copy the row to be moved
                            df = dataframe.drop(r)  # Remove the row from its original position
                            dif_dec = len(df_dec) - dec_places
                            new_position = r + dif_dec
                            #df = df.iloc[:new_position].append(row_to_move, ignore_index = True).append(df.iloc[new_position:], ignore_index=True)  # Insert the row at the new position
                            #df = pd.concat([df.iloc[:new_position], row_to_move, df.iloc[new_position:]], ignore_index=True)
                            row_to_move_df = pd.DataFrame(row_to_move).transpose()
                            df = pd.concat([df.iloc[:new_position], row_to_move_df, df.iloc[new_position:]], ignore_index=True)
                            print(df)
                    val = float(''.join(map(str, df["Names"]))) #join Name value
                    df, val = check_value_limits(df, val, lower_limit, upper_limit, lower_dec, upper_dec, dec_places)
                            
                elif lower_dec > len(dataframe):
                    #Digit length out of limits, missing predictions
                    print("Number of predicted digits too small. Try again or add number manually.")
                    sys.exit()
                    
                elif upper_dec < len(dataframe):
                    #Digit length out of limits, too many predictions. Try bboxs overlap
                    print("Value length out of limits, too many predictions. Try bboxs overlap.")
                    dataframe = second_overlap_control(dataframe)
                    value_new = float(''.join(map(str, dataframe["Names"]))) #join Name values
                    if lower_limit > value_new or value_new > upper_limit:
                        #wrong value
                        print("Wrong prediction, try again or read out manually...")
                        sys.exit()

                    elif lower_limit <= value_new <= upper_limit and lower_dec <= len(dataframe) <= upper_dec:
                        print("Value corrected. Set point further to the left...")
                        #Digit length in limits, set point further to the left
                        for r in range(len(dataframe)):
                            if name[r] == ".":
                                row_to_move = df.loc[r].copy() # Copy the row to be moved
                                df = dataframe.drop(r)  # Remove the row from its original position
                                dif_dec = len(df_dec) - dec_places
                                new_position = r + dif_dec
                                df = df.iloc[:new_position].append(row_to_move).append(df.iloc[new_position:], ignore_index=True)
                        # Insert the row at the new position
                        val = float(''.join(map(str, df["Names"]))) #join Name value
                        df, val = check_value_limits(df, val, lower_limit, upper_limit, lower_dec, upper_dec, dec_places)
                        
                
            
        #2.3_______Check if no point in Dataframe_______________        
        elif dot_true == None: #if a point is missing in the dataframe
            #check length decimal places and value length
            print("No point in dataframe. Add missing point...")

            #Todo: If value in limits and dec in limits check number necessary dec places, check if dec length still in limits if point added, add point
            #2.3.1__________Check if value in limit___________________
            if lower_limit <= value <= upper_limit:
                #Value in limits, add dot before number of necessary dec_places
                print("Value in limits add point.")
                dataframe_new, value_added = add_point_in_df(dataframe, dec_places)
                #Check value and length after point adding
                df,val = check_value_limits(dataframe_new, value_added, lower_limit, upper_limit, lower_dec, upper_dec, dec_places)
                
            #2.3.2__________Check if value over upper limit____________
            elif value > upper_limit:
                #value is bigger than the upper limit
                names = dataframe["Names"]
                print(f"Check dataframe length in limits: {len(names)}")
                if upper_dec >= len(dataframe["Names"])+1 >= lower_dec:
                    #if the maximum length of the value is smaller or exactly the upper limit, if a point is added
                    #add point
                    print("Value lenght in limits add point.")
                    dataframe_new, value_added = add_point_in_df(dataframe, dec_places,)
                    #Check value and length after point adding
                    df,val = check_value_limits(dataframe_new, value_added, lower_limit, upper_limit, lower_dec, upper_dec, dec_places)

                elif upper_dec < len(dataframe["Names"]) +1 : #upper_dec smaller than value length plus point
                    print("Too many values predicted. Look for overlapping bboxs")
                    dataframe = second_overlap_control(dataframe)
                    new_value = float(''.join(map(str, dataframe["Names"]))) #join Name values

                    if upper_dec >= len(dataframe["Names"])+1 >= lower_dec:
                        dataframe_new, value_added = add_point_in_df(dataframe, dec_places)
                        #Check value and length after point adding
                        df,val = check_value_limits(dataframe_new, value_added, lower_limit, upper_limit, lower_dec, upper_dec, dec_places)
                        
                    else: #new value still to long
                        print("Too many values predicted. Try again or add data manually.")
                        sys.exit()

                elif lower_dec > len(dataframe["Names"]) +1:
                        #new value in limits, add data point
                        print("Too few values predicted. Try again or add data manually.")
                        sys.exit()

            elif value < lower_limit:
                #value is smaller than the lower limit
                print(value)
                print("False measurement, missing values. Try again or add data manually.")
                sys.exit()

    return df, val

def add_point_in_df(dataframe, dec_places):
    # Position to insert the row (index)
    if len(dataframe) > 1:
        insert_index  = len(dataframe["Names"]) - dec_places
        # New row data
        new_row = {'Names': '.', 'Classes': "added", 'Confidence Interval': "added", 'XYXYn': "-"}
        # Insert the new row at the specified position
        dataframe_new = pd.concat([dataframe.loc[:insert_index-1], pd.DataFrame([new_row]), dataframe.loc[insert_index:]]).reset_index(drop=True)
        print(dataframe_new)
        dataframe_new.insert
        value_added = float(''.join(map(str, dataframe_new["Names"]))) #join Name values
    elif len(dataframe) == 1:
        print("Only one predicted number. Can not ensure that point belongs before or behind number.")
        print("Try again or add number manually.")
        sys.exit()
        
    return dataframe_new, value_added

def run_image_enhancer(img_folder_path, user, user_path):
    
    # Path to AutoIt executable (AutoIt3.exe)
    autoit_exe_path = user + r'\autoit-v3\install\AutoIt3.exe'

    # Path to your AutoIt script
    autoit_script_path = user_path + r'\Scripts\Cutout_Edge_WD_3_RW.au3'

    # Build the command to execute with the image folder path as a command-line argument
    command = [autoit_exe_path, autoit_script_path, img_folder_path]

    # Use subprocess to run the AutoIt script
    subprocess.run(command)
    img_enhanced = cv2.imread(user_path + r"\Enhanced_imgs\enhanced_img.png")

    return img_enhanced
    
def data_processing(data_folder_path, user, user_path):

    autoit_SciTe_path = user + r'\autoit-v3\install\SciTe\SciTe.exe'
    #subprocess.run(autoit_SciTe_path)
    
    # Path to AutoIt executable (AutoIt3.exe)
    autoit_exe_path = user + r'\autoit-v3\install\AutoIt3.exe'

    # Path to your AutoIt script
    autoit_script_path = user_path + r'Scripts\Projekt_V1_11_RW_english_07_02.au3'

    # Build the command to execute with the output folder path as a command-line argument
    command = [autoit_exe_path, autoit_script_path, data_folder_path]

    # Use subprocess to run the AutoIt script
    subprocess.run(command)
    return
#______________________________________________________________________________________
#_______________________Command Line___________________________________________________
#______________________________________________________________________________________
#Define the image, save and model paths for your individual folder structure
print("Start display detection process...")
#Load the image --> change path
user = r"C:\Users\wienbruch" #get from command line
user_path = user + r"\camera_detection_system\display_detection"
#autoit_SciTe_ path = #get from command line
#autoit_exe_path = #get from command line
img_path = user_path + r"\Input_img\Variation_lighting\rawimg102.jpg"
#r"C:\Users\wienbruch\venv311\Detection_system_06_02_24\Input_img\Variation_lighting\rawimg102.jpg"
img = cv2.imread(img_path)
#cv2.imshow("img",img)
#Define the model path 
yolo_path = user_path + r"\Trained_model\Model_2_3_2_best.pt"
#Define where the images should be saved
save_path = user_path + r'\Saved_Images\ '
cropped_path = user_path + r'\Processed_imgs\cropped_img.jpg'
output_path = user_path + r'\output.csv'
enhanced_path = user_path + r"\Enhanced_imgs\enhanced_img.png"
#___________Load Data_____________________
marker_length = 0.025 #aruco marker side length
# Load the camera parameters (you may need to calibrate your camera separately
#if you used a different camera)
#Camera used: Raspberry Pi V2 camera module
camera_matrix = [] #intrinsic camera matrix
dist_coeffs = [] #distortion coefficients for the camera lense
arucoDict = aruco.getPredefinedDictionary(aruco.DICT_4X4_1000)#define used aruco marker dicitonary
id_list = [1, 2, 3, 4,5, 8, 42, 161, 314]
#Call the functions:
bboxs, ids, image_return = findArucoMarkers(img, img_path, id_list, user, user_path)#Call aruco detection function
cv2.imshow("Image return", image_return)
print(f"Detected bounding boxes: {bboxs}")
print(f"Detected ids: {ids}")
bboxs_sorted = sorted_corners(bboxs)
print(f"Sorted bbox corners: {bboxs_sorted}")
cropped = processImage(bboxs_sorted, ids, image_return) #Call Image process function
cv2.imwrite(cropped_path,cropped)
prediction = yoloPredict(cropped, yolo_path, save_path, ids, cropped_path, output_path, user, user_path) #Call the prediction function
if prediction == None:
    cropped_enhanced = cv2.imread(enhanced_path)
    prediction_enhanced = yoloPredict(cropped_enhanced, yolo_path, save_path, ids, cropped_path, output_path, user, user_path) #Call the prediction function
    print(f"Predicted values: {prediction_enhanced}")
    if prediction_enhanced == None:
        print("Image is not predictable. Try another one...")
        sys.exit()
else:   
    print(f"Predicted values: {prediction}")

