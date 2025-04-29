;Include libraries ------------------------------------------------------------------------------------
#include <File.au3>
#include <Excel.au3>
#include <Date.au3>
#include <Lab_devices_2.au3>
;Define variables to recieve measuring time and day -----------------------------------------------------------------------------------------
Global $newdate = @MDAY & "." & @MON & "." & @YEAR ;measurement day	
Global $newtime = _NowTime () ;measuring time hh:mm:ss
Global $file
Local $scitePath = "C:\Users\wienbruch\autoit-v3\install\SciTe\SciTe.exe"
Global $user = "C:\Users\wienbruch"
;MsgBox(0,"Filename", $file)

;Open SciTe and Output-File ----------------------------------------------------------------------------------------------------------------------
Sleep (100)
Global $csvDatei = "C:\Users\wienbruch\venv311\Detection_system_06_02_24\output.csv" 
; Retrieve the output folder path from the command line
;Global $csvDatei = $CmdLine[1]
Sleep (100)
;Open Scite
Global $SciTe = Run($scitePath)
Sleep(200)
;Open output file
Send("^o")
Sleep (300)
Send ($csvDatei) ;Send output file path
Sleep (200)
Send("{ENTER}")
Sleep (100)
;Add time and date to output file--------------------------------------------------------------
Send ($newdate & @CRLF)
Sleep (200)
Send ($newtime & @CRLF)
Sleep (200)
;Save output file ----------------------------------
Send("^s")

;Count output file lines -----------------------------------------------------------------------------------------------------------
Global $anzahlzeilen = _FileCountLines ($csvDatei)
Sleep (100)

;Extract date from line 1 -------------------------------------------------------------------------------------------------------------------
Global $readline1 = (FileReadLine ($csvDatei, 1)) ;save line 1 to clipboard
Sleep (100)

;Extract time from line 2 -------------------------------------------------------------------------------------------------------------------
Global $readline2 = (FileReadLine ($csvDatei, 2)) 
Sleep (100)

;Read marker ID from line 4 for Excel file identification-------------------------------------------------------------------------
Global $readline4 = ClipPut (FileReadLine ($csvDatei, 4)) ;ClipPut = Save text in clipboard
Sleep (100)
Global $einfuegenID1 = ClipGet () ;ClipGet = call text from clipboard

;Read marker ID from line 5 for Excel file identification -------------------------------------------------------------------------
Global $readline5 = ClipPut (FileReadLine ($csvDatei, 5))
Sleep (100)
Global $einfuegenID2 = ClipGet ()

;Read measurement value from line 7 for diagram ----------------------------------------------
Global $readline7 = (FileReadLine ($csvDatei, 7)) 


;Open correct Excel file --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Global $oExcel = _Excel_Open() ; Start Excel
Sleep (200)
If @error Then Exit MsgBox($MB_SYSTEMMODAL, "Excel UDF: _Excel_BookOpen Example", "Error creating the Excel application object." &@CRLF&"@error = "&@error&", @extended = "&@extended)
Sleep (100)
Device()
prepareExcelFile()
addData_Excel()
prepare_new()

Func prepareExcelFile()
	
	;MsgBox(0,"File",$file)	
	Global $oWorkbook =  _Excel_BookOpen($oExcel , $user &"\camera_detection_system\display_detection\Data_processing\" & $file & ".xlsx") ;Open specified Excel file  
	Sleep (200)
	Global $vWorksheet = _Excel_SheetAdd($oWorkbook, 1, True, 1, $newdate) ;Open new Excel Sheet for every new day
	;MsgBox(0,"Worksheet", $vWorksheet)
	Sleep (200)

	;Build diagram -----------------------------------------------------------------------------------------------------------------------
	; Check if the chart with the current date already exists
	If $vWorksheet <> 0 Then
		; Create a new chart only if it doesn't exist
		Send ("!i") ; Shortcut add
		Sleep (200)
		Local $diagramm = Send ("!pu") ;Shortcut point diagram
		Sleep (200)
		Send ("{ENTER}") ;Chose diagram
		Sleep (300)
		Send ("!jt") ;Shortcut diagram design
		Sleep (300)
		Send ("!t") ;Shortcut chose data
		Sleep (300)
		Send ("=" & $newdate & "{!}" & "$A$2:$ZZ$3") ;chose diagram area
		Sleep (300)
		Send ("{ENTER}") 
		Sleep (400)
		
	;Diagram elements
		Send ("!jt") ;Shortcut Diagram design
		Sleep (500)
		Send ("!d") ;Add diagram element
		Sleep (200)
		Send ("!m") ;Diagram title
		Sleep (200)
		Send ("!ü") ;Set title over diagram
		Sleep (200)
		
	;Send diagram title depending on device
		Send ($title & @CRLF) ;Scale KERN FCE 3K1N_
		Sleep (200)
		
		;Add axis title
		Send ("!jt") ;Shortcut diagram design (jc or jt depending on Excel version)
		Sleep (100)
		Send ("!d") ;Add element to diagram
		Sleep (100)
		Send ("!a") ;axis title
		Sleep (100)
		Send ("!h") ;primary horizontal axis
		Sleep (100)
		Send ("Time" & @CRLF) 
		Sleep (100)
		
		Send ("!jt") ;Shortcut diagram design (jc or jt depending on Excel version)
		Sleep (100)
		Send ("!d") ;Add element to diagram
		Sleep (100)
		Send ("!a") ;axis title
		Sleep (100)
		Send ("!p") ;primary vertical axis
		Sleep (100)
		; Add axis title depending on device
		Send ($axis_title & @CRLF) ;Scales KERN FCE 3K1N
		Sleep (200)
		;Close diagram area
		Send("{ESC 3}") ;Close diagram area, back to last used excel line
		Sleep(100)
	EndIf
EndFunc

Func addData_Excel()
	;Add data pair for diagram ----------------------------------------------------------------------------------------------
	Send (("{TAB}"))
	Sleep (100)
	Send ("Measuring value1 and time" & @CRLF & ("{TAB}")) ;Line one in Excel
	Sleep (100)
	Send ($readline2 & @CRLF & ("{TAB}")) ;call saved time (line 2 in Excel)
	Sleep (100)
	Send ($readline7 & @CRLF & @CRLF) ;Measurement value without unit (line 3 in Excel)
	Sleep (100)

	;Add date and time in Excel --------------------------------------------------------------------------------------------------
	Send ("Date:" & ("{TAB}") & $readline1 & @CRLF) ;saved date
	Sleep (100)
	Send ("Time:" & ("{TAB}") & $readline2 & @CRLF) ;saved time

	;Add data in Excel line 3 to 6 -------------------------------------------------------------------------------------------------
	For $step = 3 To 6 
		Global $readline = ClipPut (FileReadLine ($csvDatei, $step)) ;Data to clipboard
		Sleep (100)
		$einfuegen = ClipGet () ;Call data from clipboard
		Sleep (100)
		Send ($einfuegen & @CRLF) ;Add data from clipboard to excel 
		Sleep (100)
	Next

	;Call line 7 and add unit in Excel --------------------------------------------------------------
	;Global $readline7 = (FileReadLine ($csvDatei, 7))
	;Sleep (100)

	Send ($readline7 & ("{TAB}") & $line7_unit & @CRLF) ; Scales KERN FCE 3K1N
	Sleep (100)

	;Read line 8 value and add unit in Excel --------------------------------------------------------------
	Global $readline8 = (FileReadLine ($csvDatei, 8)) ;Zeile 8 in Zwischenablage speichern
	Sleep (100)
	Send ($readline8 & ("{TAB}") & $line8_unit & @CRLF) ;XSInstruments pH 50+ DHS S/N180356077
	Sleep (100)

	;Inhalt in Excel einfügen ab Zeile 9 bis Ende (wird von $anzahlzeilen bestimmt) ----------------------------------------------------
	For $step = 9 To $anzahlzeilen
		Global $readline = ClipPut (FileReadLine ($csvDatei, $step)) ;Text ab Zeile 9 in Zwischenablage speichern
		Sleep (100)
		$einfuegen = ClipGet () ;Text ab Zeile 9 von Zwischenablage abrufen
		Sleep (100)
		Send ($einfuegen & @CRLF) ;Text ab Zeile 9 von Zwischenablage in Excel eintragen
		Sleep (100)
	Next
	Sleep (100)
EndFunc

Func prepare_new()
	;New column for new measurement ---------------------------------------------------------------------------------------------------------
	Send ("{TAB 2}")
	Sleep (100)
	Send ("{UP 15}")
	Sleep (100)
	Send ("{UP 15}") ;
	Sleep (100)

	MsgBox (0, "Information", "All values were transferred into the Excelfile.", 1) ;control Messagebox

	;Excel save and close ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	Send ("!2") ;Safe Excel sheet
	Sleep (100)
	_Excel_Close ($oExcel) ;Close Excel
	If @error Then Exit MsgBox($MB_SYSTEMMODAL, "Excel UDF: _Excel_Close Example 3", "Error closing the Excel application." & @CRLF & "@error = " & @error & ", @extended = " & @extended)
	;Close Scite
	ProcessClose($SciTe)
	Exit ;Ends the AutoIT script
EndFunc