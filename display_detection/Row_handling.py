#______________________________________________
#1. Import the necessary libraries
#______________________________________________
import pandas as pd

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
