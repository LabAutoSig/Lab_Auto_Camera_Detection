#cs ----------------------------------------------------------------------------

 AutoIt Version: 3.3.14.5
 Author:         N.Rupp | Feb 2024
 Modified: 		R.Wienbruch | May 2025

 Script Function: Requirements: Access to HorstFx Linux surface via ThightVNC Viewer, access to LARS control via browser, folder named "images" on desktop
				  Providing a GUI that triggers one of two functions.
				  1. "Scan display"  of a lab device - requires 2 Aruco marker provided in GUI from left to right
				  Horst Scanns the environment until the left Aruco marker is in camera range, if the right Aruco is also in range, the image of camera is saved as "image"
				  Python script XXX is started by corresponding input of cmd window
				  2. "Map Laboratory" - requires 3 Aruco marker provided in GUI from left to right
				  Horst Scanns the environment until the left Aruco marker is in camera range, if the other two Arucos are also in range, the image of camera is saved as "image1"
				  Current position of Horst is saved as pos1.txt file in images folder
				  Horst moves in relative TCP y = 0.05 distance
				  If all Arucos are in camera range, the image is saved as "image2"
				  Current position of Horst is saved as pos2.txt file in images folder
				  Python script XXX is started by corresponding input of cmd window

#ce ----------------------------------------------------------------------------
#include <ButtonConstants.au3>
#include <EditConstants.au3>
#include <GUIConstantsEx.au3>
#include <StaticConstants.au3>
#include <WindowsConstants.au3>
#include <FileConstants.au3>
#include <Array.au3>
#include "Horst_implementation.au3"
HotKeySet("{ESC}", "Terminate") ;Define the script exit key
Func Terminate ()
	Exit
EndFunc
#Region ### GUI definition $gui_task ###
Opt("GUIOnEventMode",1)
$gui_task = GUICreate("Detection System Task Selector", 550, 400, 500, 200)
GUISetBkColor(0x99B4D1)
GUICtrlCreateLabel("Please provide the Aruco marker ID's as placed, from left to right.",48,20,600,50)
GUICtrlSetFont(-1, 12, 300, 0, "MS Sans Serif")
;____________________________________SCAN Display________________________________________
$check_scan = GUICtrlCreateCheckbox("Scan Display", 48, 60, 161, 33)
GUICtrlSetFont(-1, 12, 800, 0, "MS Sans Serif")
GUICtrlSetColor(-1, 0x000000)
;GUICtrlSetOnEvent(-1,"_scan")

$lab_scanid1 = GUICtrlCreateLabel("1. ID", 48, 112, 38, 24)
GUICtrlSetFont(-1, 12, 400, 0, "MS Sans Serif")
GUICtrlSetColor(-1, 0x000000)

$lab_scanid2 = GUICtrlCreateLabel("2. ID", 48, 152, 38, 24)
GUICtrlSetFont(-1, 12, 400, 0, "MS Sans Serif")
GUICtrlSetColor(-1, 0x000000)

$inp_scan1 = GUICtrlCreateInput("", 104, 112, 65, 21, $ES_Number)
GUICtrlSetState($inp_scan1, $GUI_disable)

$inp_scan2 = GUICtrlCreateInput("", 104, 152, 65, 21, $ES_Number)
GUICtrlSetState($inp_scan2, $GUI_disable)
;_______________________________MAP Lab__________________________________________________

$check_map = GUICtrlCreateCheckbox("Map Laboratory", 250, 60, 145, 33)
GUICtrlSetFont(-1, 12, 800, 0, "MS Sans Serif")
GUICtrlSetColor(-1, 0x000000)
;GUICtrlSetOnEvent(-1,"_map")

$lab_mapid1 = GUICtrlCreateLabel("1. ID", 250, 112, 38, 24)
GUICtrlSetFont(-1, 12, 400, 0, "MS Sans Serif")
GUICtrlSetColor(-1, 0x000000)

$lab_mapid2 = GUICtrlCreateLabel("2. ID", 250, 152, 38, 24)
GUICtrlSetFont(-1, 12, 400, 0, "MS Sans Serif")
GUICtrlSetColor(-1, 0x000000)

$lab_mapid3 = GUICtrlCreateLabel("Table marker", 250, 192, 100, 24)
GUICtrlSetFont(-1, 12, 400, 0, "MS Sans Serif")
GUICtrlSetColor(-1, 0x000000)

$inp_map1 = GUICtrlCreateInput("", 350, 112, 65, 21, $ES_Number)
GUICtrlSetState(-1, $GUI_disable)

$inp_map2 = GUICtrlCreateInput("", 350, 152, 65, 21, $ES_Number)
GUICtrlSetState(-1, $GUI_disable)

$inp_map3 = GUICtrlCreateInput("", 350, 192, 65, 21, $ES_Number)
GUICtrlSetState(-1, $GUI_disable)
;__________________________________Simulation Mode______________________________________
$check_simulation = GUICtrlCreateCheckbox("Simulation Mode", 128, 240, 161, 33)
GUICtrlSetFont(-1, 12, 800, 0, "MS Sans Serif")
GUICtrlSetColor(-1, 0x000000)
;GUICtrlSetOnEvent(-1,"_scan")
;__________________________________________________________________________________________
$but_exe = GUICtrlCreateButton("execute", 128, 288, 177, 41)
GUICtrlSetFont(-1, 12, 400, 0, "MS Sans Serif")
GUICtrlSetColor(-1, 0x000000)
GUICtrlSetOnEvent(-1,"_execute")
GUISetOnEvent($GUI_EVENT_CLOSE,"end")
GUICtrlSetOnEvent($check_simulation, "UpdateGUIState")
GUICtrlSetOnEvent($check_map, "UpdateGUIState")
GUICtrlSetOnEvent($check_scan, "UpdateGUIState")
GUISetState(@SW_SHOW)
#EndRegion ### END Koda GUI section ###

#Region ### GUI functions $gui_task  ###
GUISetState(@SW_SHOW)
While 1
	Sleep(10)
WEnd
Func end()
	Exit
EndFunc
Func UpdateGUIState()
    Local $sim = GUICtrlRead($check_simulation)
    Local $map = GUICtrlRead($check_map)
    Local $scan = GUICtrlRead($check_scan)

    ; First: Reset everything
    GUICtrlSetState($inp_map1, $GUI_DISABLE)
    GUICtrlSetState($inp_map2, $GUI_DISABLE)
    GUICtrlSetState($inp_map3, $GUI_DISABLE)
    GUICtrlSetState($lab_mapid1, $GUI_DISABLE)
    GUICtrlSetState($lab_mapid2, $GUI_DISABLE)
    GUICtrlSetState($lab_mapid3, $GUI_DISABLE)

    GUICtrlSetState($inp_scan1, $GUI_DISABLE)
    GUICtrlSetState($inp_scan2, $GUI_DISABLE)
    GUICtrlSetState($lab_scanid1, $GUI_DISABLE)
    GUICtrlSetState($lab_scanid2, $GUI_DISABLE)

    ; Default: all checkboxes enabled
    GUICtrlSetState($check_map, $GUI_ENABLE)
    GUICtrlSetState($check_scan, $GUI_ENABLE)

    If $sim = $GUI_Checked Then
        ; SIMULATION MODE
        ; Both checkboxes enabled
        ; If map is checked
        If $map = $GUI_Checked Then
            ; Only enable map3 fields
            GUICtrlSetState($inp_map3, $GUI_ENABLE)
            GUICtrlSetState($lab_mapid3, $GUI_ENABLE)
            GUICtrlSetState($lab_mapid3, $GUI_ENABLE)
			GUICtrlSetState($check_scan, $GUI_disable)
		ElseIf $scan = $GUI_Checked Then
			GUICtrlSetState($check_map, $GUI_disable)
        EndIf

        ; If scan is checked: inputs remain disabled, nothing else needed
        Return
    EndIf

    ; SIMULATION OFF → enforce exclusive selection
    If $map = $GUI_Checked Then
        ; Disable scan checkbox and uncheck it
        GUICtrlSetState($check_scan, $GUI_DISABLE)
        GUICtrlSetState($check_scan, $GUI_UNCHECKED)

        ; Enable full mapping fields
        GUICtrlSetState($inp_map1, $GUI_ENABLE)
        GUICtrlSetState($inp_map2, $GUI_ENABLE)
        GUICtrlSetState($inp_map3, $GUI_ENABLE)
        GUICtrlSetState($lab_mapid1, $GUI_ENABLE)
        GUICtrlSetState($lab_mapid2, $GUI_ENABLE)
        GUICtrlSetState($lab_mapid3, $GUI_ENABLE)

    ElseIf $scan = $GUI_Checked Then
        ; Disable map checkbox and uncheck it
        GUICtrlSetState($check_map, $GUI_DISABLE)
        GUICtrlSetState($check_map, $GUI_UNCHECKED)

        ; Enable scan fields
        GUICtrlSetState($inp_scan1, $GUI_ENABLE)
        GUICtrlSetState($inp_scan2, $GUI_ENABLE)
        GUICtrlSetState($lab_scanid1, $GUI_ENABLE)
        GUICtrlSetState($lab_scanid2, $GUI_ENABLE)
    EndIf
EndFunc
Func SaveTableMarker()
	Local $table_marker = GUICtrlRead($inp_map3)
	Local $hFile = FileOpen(@ScriptDir & "\three_D_reconstruction\marker_placement.txt", $FO_OVERWRITE)
    If $hFile = -1 Then
        MsgBox(16, "Error", "Failed to open file.")
        Return
    EndIf
    FileWrite($hFile, $table_marker & @CRLF)
    FileClose($hFile)
EndFunc
Func _execute()
	If GUICtrlRead($check_simulation) = $GUI_Checked Then ;Execute AutoIt script without robotic arm usage
		If GUICtrlRead($check_scan) = $GUI_Checked Then
			GUISetState(@SW_HIDE)
			displaydetection()
			end()

		ElseIf GUICtrlRead($check_map) = $GUI_Checked Then
			GUISetState(@SW_HIDE)

			SaveTableMarker()
			reconstruction()
			end()
		EndIf

	ElseIf GUICtrlRead($check_simulation) = $GUI_Unchecked Then ;Perform complete script with robot control
		ShellExecute("display_detection\Input_img")
		sleep(200)
		Send("{Ctrldown}a{ctrlup}")
		sleep(200)
		Send("{delete}")
		sleep(200)
		WinClose("images")
		WinWaitClose("images")
		If GUICtrlRead($check_scan) = $GUI_Checked Then
			If GUICtrlRead($inp_scan1) = "" Or GUICtrlRead($inp_scan2) = "" Then
				MsgBox(0,"Incomplete information", "Please provide the ArUco marker IDs before continuing.")
			Else
				global $id1 = GUICtrlRead ($inp_scan1)
				global $id2 = GUICtrlRead ($inp_scan2)
				;MsgBox(0,"",$id1 & $id2)
				GUISetState(@SW_HIDE)
				get_value($id1, $id2)
			EndIf

		ElseIf GUICtrlRead($check_map) = $GUI_Checked Then
			If GUICtrlRead($inp_map1) = "" Or GUICtrlRead($inp_map2) = "" Or GUICtrlRead($inp_map3) = "" Then
				MsgBox(0,"Incomplete information", "Please provide the ArUco marker IDs before continuing.")
			Else
				global $id1 = GUICtrlRead ($inp_map1)
				global $id2 = GUICtrlRead ($inp_map2)
				global $id3 = GUICtrlRead ($inp_map3)
				;MsgBox(0,"",$id1 & $id2 &$id3)
				GUISetState(@SW_HIDE)
				map_lab($id1,$id2,$id3)
			EndIf
		EndIf
	EndIf
EndFunc
#EndRegion

#Region ### process functions###

Func displaydetection()
    Local $basePath = @ScriptDir
    Local $venvPath = $basePath & "\Python_installation\venv311\Scripts\activate"
    Run(@ComSpec & ' /c "cd /d ' & $basePath & '\Python_installation && ' & $venvPath & ' && cd /d ' & $basePath & ' && displaydetection.py"', $basePath)
EndFunc

Func reconstruction()
	Local $basePath = @ScriptDir
    Local $venvPath = $basePath & "\Python_installation\venv38\Scripts\activate"
    Run(@ComSpec & ' /c "cd /d ' & $basePath & '\Python_installation && ' & $venvPath & ' && cd /d ' & $basePath & ' && reconstruction.py"', $basePath)

	EndFunc
#EndRegion