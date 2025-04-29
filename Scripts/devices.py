
def call(ids):
    #First value
    name1 = None
    
    lower_limit1 = None
    upper_limit1 = None
    lower_len1 = None
    upper_len1 = None
    dec_places1 = None
    #Second value
    name2 = None
    lower_limit2 = None
    upper_limit2 = None
    lower_len2 = None
    upper_len2 = None
    dec_places2 = None
    
    second_value = None

    
    # _____________VWR MicroStar 12 centrifuge________________________
    if ids[0] == 4 and ids[1] == 1 or ids[0] == 1 and ids[1] == 4:
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
    return df1_corrected,df2_corrected


