
Func Check_Device($einfuegenID1, $einfuegenID2)
	Global $file
	Global $title
	Global $axis_title
	Global $line7_unit
	Global $line8_unit 
	MsgBox(0,"ID1",$einfuegenID1)
	MsgBox(0,"ID2",$einfuegenID2)
	;Open Excel file with correct marker ID path 
	;_____________VWR MicroStar 12 centrifuge________________________
	If ($einfuegenID1 == 4 AND $einfuegenID2 == 1) OR ($einfuegenID1 == 1 AND $einfuegenID2 == 4)  Then 
		Global $file = "centrifuge_VWR_MicroStar12"
		Global $title = "Centrifugal force"
		Global $axis_title = "RPM/RCF x 1000"
		Global $line7_unit = "[RPM/RCF*1000]"
		Global $line8_unit = "[min]"
		MsgBox(0,"Centrifuge","VWR MicroStar 12 centrifuge")

	;_____________________Scales KERN FCE 3K1N________________________________
	ElseIf ($einfuegenID1 == 42 AND $einfuegenID2 == 161) OR ($einfuegenID1 == 161 AND $einfuegenID2 == 42) Then 
		Global $file = "scales_KERN_FCE_3K1N"
		Global $title = "Weight measurement"
		Global $axis_title = "Gram [g]"
		Global $line7_unit = "[g]" 
		Global $line8_unit  = " "
		MsgBox(0,"Scales","KERN FCE 3K1N")

	;_____________________Scales CS Series CS200_________________________________
	ElseIf ($einfuegenID1 == 5 AND $einfuegenID2 == 8) OR ($einfuegenID1 == 8 AND $einfuegenID2 == 5) Then 
		Global $file = "scales_CS_Series_CS200"
		Global $title = "Weight measurement"
		Global $axis_title = "Gram [g]"
		Global $line7_unit = "[g]" 
		Global $line8_unit  = " "
		MsgBox(0,"Scales","CS Series CS200")
		
	;_____________________Thermo Scientific Digital Shaking Drybath 88880028___________
	ElseIf ($einfuegenID1 == 2 AND $einfuegenID2 == 314) OR ($einfuegenID1 == 314 AND $einfuegenID2 == 2)  Then 
		Global $file = "thermo_scientific_shaking_drybath"
		Global $title = "Temperature measurement"
		Global $axis_title = "Temperature [°C]"
		Global $line7_unit = "[°C]"
		Global $line8_unit = "[°C]"
		MsgBox(0,"Thermo Scientific","Digital Shaking Drybath")
		
	;_____________________Phoenix Instrument Heating and magnetic stirrer RSM-10HP ___________
	ElseIf ($einfuegenID1 == 2 AND $einfuegenID2 == 1) OR ($einfuegenID1 == 1 AND $einfuegenID2 == 2)  Then 
		Global $file = "heating_and_magnetic_stirrer_RSM_10HP"
		Global $title = "Heating Temperature"
		Global $axis_title = "Temperature [°C]"
		Global $line7_unit = "[°C]"
		Global $line8_unit = "[1/min]" 
		MsgBox(0,"Stirrer","Heating and magnetic")


	;_____________________XSInstruments pH 50+ DHS S/N180356077___________
	ElseIf ($einfuegenID1 == 3 AND $einfuegenID2 == 4 ) OR  ($einfuegenID1 == 4 AND $einfuegenID2 ==3) Then
		Global $file = "pH_meter_ph50_DHS"
		Global $title = "pH value"
		Global $axis_title = "pH" 
		Global $line7_unit =  "[pH]"
		Global $line8_unit = "[°C]"
		MsgBox(0,"pH_meter","PH Meter")
	
	EndIf
	Local $resultArray[5] = [$file, $title, $axis_title, $line7_unit, $line8_unit]
	MsgBox(0, "Return array", $resultArray)
	Return $resultArray
EndFunc

 