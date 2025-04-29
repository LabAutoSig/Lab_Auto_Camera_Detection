#include <GUIConstantsEx.au3>

GUICreate("HORST Task Selector", 300, 120)

GUICtrlCreateLabel("Choose an option:", 20, 20)
 Local $idButton_Scan = GUICtrlCreateButton("Scan Display", 20, 50, 120, 30)
 Local $idButton_Map = GUICtrlCreateButton("Map Laboratory", 160, 50, 120, 30)

GUISetState(@SW_SHOW)
While 1
    $msg = GUIGetMsg()
    
    Switch $msg
        Case $GUI_EVENT_CLOSE
            ExitLoop
    Case $idButton_Scan
	    ;Ask for Device IDs 
	    ;Scan with HORST
	    ;Retrieve Image
	    ;Save display image as input image in file 
	    display() ;Start display recognition
	    ExitLoop
    Case $idButton_Map
	    ;Ask for Device IDs 
	    ;Scan with HORST 
	    ;Retrieve two images and the camera HORST world translation and rotation vectors
	    ;Save images and translation and rotation vectors under cam1 and cam2
	    mapping() ;Start 3D reconstruction
	    ExitLoop
    EndSwitch
WEnd

GUIDelete()

Func mapping()
	;Start Laboratory mapping 
	Run("C:\Windows\System32\cmd.exe")
	WinWaitActive("C:\Windows\System32\cmd.exe")
	Send("cd C:\Users\wienbruch\" & "{ENTER}")
	Sleep(100)
	Send('venv38\Scripts\activate' & "{ENTER}")
	 Sleep(100)
	 Send("venv38\aktuelles_Script\CAD_sketch_in_Horst_world_12_01_quaternions.py" & "{ENTER}")
	 Sleep(2000)
EndFunc
 
 Func display()
	 ;Start Digit Recognition 
	Run("C:\Windows\System32\cmd.exe")
	WinWaitActive("C:\Windows\System32\cmd.exe")
	Send("cd C:\Users\wienbruch\" & "{ENTER}")
	Sleep(100)
	Send('venv311\Scripts\activate' & "{ENTER}")
	 Sleep(100)
	 Send("venv311\Display_detection_system_11_23\18_01_2024_Display_detection.py" & "{ENTER}")
EndFunc