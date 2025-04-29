#1.
#import the necessary libraries and costum functions
import sys
import pandas as pd
import display_detection.Bbox_handling as bbox_h
from display_detection.Point_handling import add_point_in_df

#Function that corrects the data based on the device specific limits
def control_data(ids, dataframe1, dataframe2, values):
    df1_corrected = []
    df2_corrected = []
    print(f"Control predicted and corrected data...")
    print(f"Dataframe1 before correction: {dataframe1}")
    print(f"Dataframe2 before correction: {dataframe2}")
    #Drop '.' if it is the first value in the dataframe
    if len(dataframe1) != 0 and dataframe1["Names"][0]!="OFF":
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

#Function that evaluates if the predicted value is in the device specific value limits
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
                dataframe = bbox_h.second_overlap_control(dataframe)
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
            dataframe = bbox_h.second_overlap_control(dataframe)
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

#Function that controls if the predicted value should/shouldn't have decimal places
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
                    dataframe = bbox_h.second_overlap_control(dataframe)
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
                    dataframe = bbox_h.second_overlap_control(dataframe)
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
                    dataframe = bbox_h.second_overlap_control(dataframe)
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
