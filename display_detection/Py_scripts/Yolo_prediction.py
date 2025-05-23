#______________________________________________
#1. Import the necessary libraries
#______________________________________________
import cv2
import imutils
import uuid
from ultralytics import YOLO
import torch
import pandas as pd
from datetime import datetime
#Import custom functions
import display_detection.Py_scripts.Point_handling as point_h
import display_detection.Py_scripts.Row_handling as row_h
import display_detection.Py_scripts.Bbox_handling as bbox_h
import display_detection.Py_scripts.Data_control as d_control
from display_detection.Py_scripts.Data_postprocessing_new import data_processing_excel
from display_detection.Py_scripts.Image_enhancer import run_image_enhancer
#______________________________________________
#Function that predicts the values in an image
#______________________________________________
def yoloPredict(croppedimg, path, savepath,ids, cropped_path, output_path):
    #use the cropped image, the model path and the path for saving the images
    #YOLO Version: YOLOv8
    #Dataset from: Roboflow
    #Training source: Kaggle.com
    values = []
    print(f"Yolo predict image for ids: {ids}")
    #Load the model --> Change path depending on where you saved your model
    model = YOLO(path)
    #Predict the image values
    results = model.predict(source=croppedimg, save=True, show=False, save_txt=True)
    # print(results)
    if len(results) == 0:
        print("No predictions were made. Enhance the cropped image")
        image_enhanced = run_image_enhancer(cropped_path)
    res_plotted = results[0].plot(font_size=0.1, conf=False)
    #show plotted img, font size = text size, conf = confidence level
    cv2.imshow("result", res_plotted)
    # Filename --> change path depending on your location
    filename = savepath + 'result_' + str(uuid.uuid4()) + '.jpg' #save image under random name
    # Save the image
    cv2.imwrite(filename, res_plotted) #save image
    #Define the variables
    b =[]
    conf = []
    classes = []
    names = []

    #Extract results and save as numpy arrays
    for result in results:
        # detection
        b = result.boxes.xyxyn  # box with xyxy format but normalized, (N, 4)
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
        image_enhanced = run_image_enhancer(cropped_path)
        values = None
        return values
    #Split Coordinate column into separate x and y columns
    df['x_top'],df['y_top'],df['x_bottom'],df['y_bottom'] = zip(*list(df['XYXYn'].values))
    df_letters = df
    # Delete words/letters in dataframe
    words_to_remove = ['lid', 'T','E', 'M', 'P', 'g','min','numbers-and-things',
                       'numbers-weights', 'pH', 'temp','°C','-C', 'SV', 'Stop',
                       'Temp.',':','ATC','F','I','O','PV','R','RCF','RPM','rpm',
                       'Smiley','Stern','Time','U',]
    df_letters = df_letters[~df_letters['Names'].isin(words_to_remove)]
    #print(f" Dataframe without string values: \n {df_letters}")
    df_letters = df_letters.replace('dot', '.', regex=True) #replace dot with .
    print(f"Dataframe with . instead of dot: \n {df_letters}")
    #Sort the dataframe values by the position of the bounding boxes in the picture
    df_new = df_letters.sort_values(by =['x_top'], ascending = True)
    df_new = df_new.reset_index(drop=True) # reset indexes 
    print(f"Sorted Dataframe from left to right: \n {df_new}")
    # Filter out rows with Confidence Interval smaller than 0.5
    df_new = df_new[df_new['Confidence Interval'] >= 0.4]
    df_new = df_new.reset_index(drop=True)  # Reset indexes
    print(f"Dataframe without numbers with a confidence interval smaller 0.4 \n {df_new}")
    df_new = point_h.drop_firstPoint(df_new)
    
    #_____________Split values when there are two rows______________________
    dataframe1, dataframe2 = row_h.check_row(df_new)
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
        dataframe2 = point_h.drop_firstPoint(dataframe2)
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
        dataframe1, dataframe2 = row_h.split_gap_single_row(dataframe1)
    #___________Correct data if two bounding boxes are nearly equal__________________
    dataframe1 = bbox_h.nearly_equal_bboxs(dataframe1)
    dataframe1 = point_h.drop_twin_point(dataframe1)
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
    if not dataframe2.empty: # when there are two rows
        #d_names2 = df2_dropped["Names"]
        dataframe2 = bbox_h.nearly_equal_bboxs(dataframe2)
        dataframe2 = point_h.drop_twin_point(dataframe2)
        if dataframe2["Names"][0] != "OFF":
            value2 = float(''.join(map(str, dataframe2['Names'])))
            #save value 2 as float --> join all values of names
        else:
            value2 = None
    elif dataframe2.empty:
        value2 = None
    print("First value: ", value1)
    print("Second value: ",value2)
    values.append(value2) #append value2 to values
    #_________________Data correction: inspect data for missing/false points and data________________________
    df1,df2 = d_control.control_data(ids,dataframe1,dataframe2, values)
    value1 = float(''.join(map(str, df1["Names"]))) #join Name values 0 till j as float
    if not len(df2) == 0:
        value2 = float(''.join(map(str, df2["Names"]))) #join Name values j and the rest as float
    else:
        value2 = None
    values_corrected =[]
    values_corrected.append(value1)
    values_corrected.append(value2)
    combined_dataframe = pd.concat([df1[['Names', 'Confidence Interval']], df2[['Names', 'Confidence Interval']]], ignore_index=False)
    ids_df = pd.DataFrame(ids, columns = ["IDs"])
    results_df = pd.DataFrame(values_corrected, columns=["Predicted values"])
    print(f"Results df: {results_df}")
    print(f"Ids df: {ids_df}")
    current_date_time = datetime.now()
    current_date = current_date_time.date()
    current_time = current_date_time.time()
    # Create a temporary dataframe with date and time in separate rows
    date_time_df = pd.DataFrame({'Info': ['Date', 'Time'], 'Value': [current_date, current_time]})
    date_time_df.to_csv(output_path,sep='\t',mode= 'w', encoding='utf-8',index=False) # a = append, x = exclusive creation, w = truncate
    ids_df.to_csv(output_path,sep='\t',mode= 'a', encoding='utf-8',index=False) # a = append, x = exclusive creation, w = truncate
    results_df.to_csv(output_path,sep='\t',mode= 'a', encoding='utf-8',index=False)
    combined_dataframe.to_csv(output_path,sep='\t',mode= 'a', encoding='utf-8',index=False)
    data_processing_excel(date_time_df,ids_df,results_df,combined_dataframe)  
    return values_corrected #return the values
