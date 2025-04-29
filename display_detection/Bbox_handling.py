
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
