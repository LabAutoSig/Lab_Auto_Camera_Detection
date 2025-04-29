#______________________________________________
#1. Import the necessary libraries
#______________________________________________
import pandas as pd
import sys
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
            for x in range(len(dataframe["Names"])):
                print(names[x])
                if names[x] != "OFF":
                    print(f"In row: {x} a value unequal to OFF is found")
                    dataframe.drop(labels = x, axis =0, inplace = True)#dataframe erase label at i
                    #dataframe = dataframe.reset_index(drop=True) #reset indexes
                    print(f"Dataframe after row drop:\n {dataframe}")
                #x = 0
                elif names[x] == "OFF":
                    dataframe = dataframe.reset_index(drop=True) #reset indexes
            
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
