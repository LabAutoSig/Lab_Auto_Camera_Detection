#cs ----------------------------------------------------------------------------

 AutoIt Version: 3.3.14.5
 Author:         N.Rupp | Feb 2024

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
#include <Array.au3>

;Linux variablen
global $save = "/home/fruitcore/fruitcore/save/" ;horst program that should be executed
global $z_folder = "/home/fruitcore/fruitcore/save/z_folder" ;library of all horst programs
global $desktop = "/home/fruitcore/Desktop/"
;cam variablen
global $img = "http://192.168.4.1:8080/img"    ;get current image with markers
global $raw = "http://192.168.4.1:8080/rawimg" ;get current raw image
Global $list = "http://192.168.4.1:8080/list"  ;get all visible IDs
Global $pos = "http://192.168.4.1:8080/"       ;+ID to get position of specific ID

$pic = ""

#Region ### GUI definition $gui_task ###
Opt("GUIOnEventMode",1)
$gui_task = GUICreate("HORST Task Selector", 480, 389, 500, 200)
GUISetBkColor(0x99B4D1)
GUICtrlCreateLabel("Please provide the ID of Aruco's from left to right placed.",48,20,600,50)
GUICtrlSetFont(-1, 12, 300, 0, "MS Sans Serif")

;____________________________________SCAN Display________________________________________
$check_scan = GUICtrlCreateCheckbox("Scan Display", 48, 60, 161, 33)
GUICtrlSetFont(-1, 12, 800, 0, "MS Sans Serif")
GUICtrlSetColor(-1, 0x000000)
GUICtrlSetOnEvent(-1,"_scan")

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
GUICtrlSetOnEvent(-1,"_map")

$lab_mapid1 = GUICtrlCreateLabel("1. ID", 250, 112, 38, 24)
GUICtrlSetFont(-1, 12, 400, 0, "MS Sans Serif")
GUICtrlSetColor(-1, 0x000000)

$lab_mapid2 = GUICtrlCreateLabel("2. ID", 250, 152, 38, 24)
GUICtrlSetFont(-1, 12, 400, 0, "MS Sans Serif")
GUICtrlSetColor(-1, 0x000000)

$lab_mapid3 = GUICtrlCreateLabel("3. ID", 250, 192, 38, 24)
GUICtrlSetFont(-1, 12, 400, 0, "MS Sans Serif")
GUICtrlSetColor(-1, 0x000000)

$inp_map1 = GUICtrlCreateInput("", 300, 112, 65, 21, $ES_Number)
GUICtrlSetState(-1, $GUI_disable)

$inp_map2 = GUICtrlCreateInput("", 300, 152, 65, 21, $ES_Number)
GUICtrlSetState(-1, $GUI_disable)

$inp_map3 = GUICtrlCreateInput("", 300, 192, 65, 21, $ES_Number)
GUICtrlSetState(-1, $GUI_disable)
;__________________________________________________________________________________________

$but_exe = GUICtrlCreateButton("execute", 128, 288, 177, 41)
GUICtrlSetFont(-1, 12, 400, 0, "MS Sans Serif")
GUICtrlSetColor(-1, 0x000000)
GUICtrlSetOnEvent(-1,"_execute")

GUISetOnEvent($GUI_EVENT_CLOSE,"end")

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

Func _scan()
	If GUICtrlRead($check_scan) = $GUI_Checked Then
		GUICtrlSetState($inp_scan1, $GUI_enable)
		GUICtrlSetState($inp_scan2, $GUI_enable)
		GUICtrlSetState($lab_scanid1, $GUI_enable)
		GUICtrlSetState($lab_scanid2, $GUI_enable)

		GUICtrlSetState($check_map, $GUI_disable)
		GUICtrlSetState($lab_mapid1, $GUI_disable)
		GUICtrlSetState($lab_mapid2, $GUI_disable)
		GUICtrlSetState($lab_mapid3, $GUI_disable)
		GUICtrlSetState($inp_map1, $GUI_disable)
		GUICtrlSetState($inp_map2, $GUI_disable)
		GUICtrlSetState($inp_map3, $GUI_disable)

	ElseIf GUICtrlRead($check_scan) = $GUI_Unchecked Then
		GUICtrlSetState($inp_scan1, $GUI_disable)
		GUICtrlSetState($inp_scan2, $GUI_disable)
		GUICtrlSetState($lab_scanid1, $GUI_disable)
		GUICtrlSetState($lab_scanid2, $GUI_disable)

		GUICtrlSetState($check_map, $GUI_enable)
		GUICtrlSetState($lab_mapid1, $GUI_disable)
		GUICtrlSetState($lab_mapid2, $GUI_disable)
		GUICtrlSetState($lab_mapid3, $GUI_disable)
		GUICtrlSetState($inp_map1, $GUI_disable)
		GUICtrlSetState($inp_map2, $GUI_disable)
		GUICtrlSetState($inp_map3, $GUI_disable)
	EndIf
EndFunc

Func _map()
	If GUICtrlRead($check_map) = $GUI_Checked Then
		GUICtrlSetState($check_scan, $GUI_disable)

		GUICtrlSetState($lab_mapid1, $GUI_enable)
		GUICtrlSetState($lab_mapid2, $GUI_enable)
		GUICtrlSetState($lab_mapid3, $GUI_enable)
		GUICtrlSetState($inp_map1, $GUI_enable)
		GUICtrlSetState($inp_map2, $GUI_enable)
		GUICtrlSetState($inp_map3, $GUI_enable)

		GUICtrlSetState($check_scan, $GUI_disable)
		GUICtrlSetState($inp_scan1, $GUI_disable)
		GUICtrlSetState($inp_scan2, $GUI_disable)
		GUICtrlSetState($lab_scanid1, $GUI_disable)
		GUICtrlSetState($lab_scanid2, $GUI_disable)

	ElseIf GUICtrlRead($check_scan) = $GUI_Unchecked Then
		GUICtrlSetState($inp_scan1, $GUI_disable)
		GUICtrlSetState($inp_scan2, $GUI_disable)
		GUICtrlSetState($lab_scanid1, $GUI_disable)
		GUICtrlSetState($lab_scanid2, $GUI_disable)

		GUICtrlSetState($check_scan, $GUI_enable)
		GUICtrlSetState($lab_mapid1, $GUI_disable)
		GUICtrlSetState($lab_mapid2, $GUI_disable)
		GUICtrlSetState($lab_mapid3, $GUI_disable)
		GUICtrlSetState($inp_map1, $GUI_disable)
		GUICtrlSetState($inp_map2, $GUI_disable)
		GUICtrlSetState($inp_map3, $GUI_disable)
EndIf
EndFunc

Func _execute()
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
			MsgBox(0,"Incomplete information", "Please provide the IDs of Aruco before continue.")
		Else
			Global $program = "Scan4SandM.js"
			global $id1 = GUICtrlRead ($inp_scan1)
			global $id2 = GUICtrlRead ($inp_scan2)
			;MsgBox(0,"",$id1 & $id2)
			GUISetState(@SW_HIDE)
			get_value()
		EndIf

	ElseIf GUICtrlRead($check_map) = $GUI_Checked Then
		If GUICtrlRead($inp_map1) = "" Or GUICtrlRead($inp_map2) = "" Or GUICtrlRead($inp_map3) = "" Then
			MsgBox(0,"Incomplete information", "Please provide the IDs of Aruco before continue.")
		Else
			Global $program = "Scan4SandM.js"
			global $id1 = GUICtrlRead ($inp_map1)
			global $id2 = GUICtrlRead ($inp_map2)
			global $id3 = GUICtrlRead ($inp_map3)
			;MsgBox(0,"",$id1 & $id2 &$id3)
			GUISetState(@SW_HIDE)
			map_lab()
		EndIf
	EndIf
EndFunc
#EndRegion

#Region ### Linux handling functions ###
	Func _TightVNC() ;sollte funktionieren
	If WinExists("horst-218:0 - TightVNC Viewer") Then  ;if TightVNC exists
		Sleep(100)
	Else
		Send("{LWIN}")									;start TightVNC
		Sleep(1000)
		Send("tight")
		Sleep(1000)
		Send("{ENTER}")
		WinWaitActive("New TightVNC Connection")		;Activate Software
		Sleep(1000)
		Send("{ENTER}")
		Sleep(100)
		WinWaitActive("Vnc Authentication")				;password window
		Sleep(500)
		Send("horst:pc")								;password
		Sleep(500)
		Send("{ENTER}")
	EndIf
	WinActivate("horst-218:0 - TightVNC Viewer")
	WinWaitActive("horst-218:0 - TightVNC Viewer")
	WinSetState("horst-218:0 - TightVNC Viewer","",@SW_MAXIMIZE)
EndFunc

Func Select_script()
	Send("{CTRLDOWN}t");Terminal
	Sleep(200)
	Send("{CTRLUP}")
	Sleep(500)
	Send("cp "&$z_folder&"/"&$program&" "&$save) ;program shift from library to executing folder
	Sleep(200)
	Send("{ENTER}")
	Sleep(500)
	Send("exit")
	Sleep(200)
	Send("{ENTER}")
EndFunc

Func load_script()
	Send("{CTRLDOWN}{ALTDOWN}{Right}");HorstFX
	Sleep(200)
	Send("{CTRLUP}{ALTUP}");HorstFX
	Sleep(500)
	Send("{F11}")
	Sleep(1000)
	MouseClick("",1437,435) ;load program
	Sleep(500)
	MouseClick("",825,638) ;choose script
	Sleep(500)
	MouseClick("",1525,952) ;load program
	sleep(5000)
EndFunc

Func graphScriptStart()
	WinActivate("horst-218:0 - TightVNC Viewer")
	WinWaitActive("horst-218:0 - TightVNC Viewer")
	Sleep(500)
	MouseClick("",416,939) ; Play
	Sleep(500)
	MouseClick("",1604,812) ;Program start
	Sleep(200)
EndFunc

Func textScriptStart()
	WinActivate("horst-218:0 - TightVNC Viewer")
	WinWaitActive("horst-218:0 - TightVNC Viewer")
	Sleep(500)
	MouseClick("",1132,907) ;Play
	Sleep(1000)
	MouseClick("",1615,810) ;Program start
	MouseMove(200,200)
	Sleep(500)
	$pix = PixelChecksum(1524,746,1711,867)
	Do
		Sleep(20)
	Until PixelChecksum(1524,746,1711,867) <> $pix
EndFunc

Func textScriptEnd()
	WinActivate("horst-218:0 - TightVNC Viewer")
	WinWaitActive("horst-218:0 - TightVNC Viewer")
	Sleep(500)
	MouseClick("",1704,535) ;close
	Sleep(500)
	MouseClick("",1395,92) ;main menu
	Sleep(500)
	MouseClick("",1052,746) ;save not
	Sleep(500)
	Send("{F11}")
	Sleep(200)
	Send("{CTRLDOWN}{ALTDOWN}{Left}")
	Sleep(200)
	Send("{CTRLUP}{ALTUP}")
	sleep(200)
EndFunc

Func graphScriptEnd()
	WinActivate("horst-218:0 - TightVNC Viewer")
	WinWaitActive("horst-218:0 - TightVNC Viewer")
	Sleep(500)
	MouseClick("",1704,542) ;stop program
	Sleep(500)
	MouseClick("",1704,542) ;close program
	Sleep(500)
	MouseClick("", 1395,92) ;home
	Sleep(500)
	MouseClick("",1045,748) ;leave program
	Sleep(500)
	Send("{F11}")			;start point
	Sleep(500)
	Send("{CTRLDOWN}{ALTDOWN}{Left}")
	Sleep(200)
	Send("{CTRLUP}{ALTUP}")
	sleep(200)
EndFunc

Func delete_script()
	WinActivate("horst-218:0 - TightVNC Viewer")
	WinWaitActive("horst-218:0 - TightVNC Viewer")
	sleep(500)
	Send("{CTRLDOWN}t")   ;HorstFX
	Sleep(200)
	Send("{CTRLUP}")      ;HorstFX
	Sleep(500)
	Send("rm "&$save & "/" & $program)
	Sleep(200)
	Send("{ENTER}")
	Sleep(500)
	Send("exit")
	Sleep(200)
	Send("{ENTER}")
	Sleep(500)
EndFunc

#EndRegion

#Region ### scan display functions   ###

Func get_value()
	_TightVNC() 												;start VNC viewer
	Select_script() 											;shift desired program
	load_script()												;load program
	graphScriptStart()											;start graph.script
	Scan_coord_calc()											;detect left aruco marker, save image
EndFunc

Func Scan_coord_calc()
	ShellExecute($pos) 											;camera main menu
	WinWaitActive("LARS CONTROL – Mozilla Firefox")
	Sleep(500)
	Send("{CTRLDOWN}k{CTRLUP}")
	Sleep(500)
	Send("{BACKSPACE}")
	Send($pos&$id1)
	Sleep(1000)
	Send("{ENTER}")
	Sleep(1500)
	Do
		Send("{F5}")
		Sleep(2000)
	Until WinGetTitle("[ACTIVE]") = "Mozilla Firefox"
	Sleep(250)
	graphScriptEnd()
	delete_script()
	WinActivate("Mozilla Firefox")
	WinWaitActive("Mozilla Firefox")
	Sleep(500)
	Send("{CTRLDOWN}k{CTRLUP}")
	Sleep(500)
	Send("{BACKSPACE}")
	Send($pos&$id2)
	Sleep(1000)
	Send("{ENTER}")
	Sleep(1500)
	Send("{F5}")
	Sleep(2000)
	If WinGetTitle("[ACTIVE]") = "Mozilla Firefox" Then	;If second Aruco is visible, image is saved otherwise exit
		$pic = "image"
		savePic()
		MsgBox(0,"","python skript aufrufen")
		global $pythonfile = ""
		python()
		exit
	ElseIf WinGetTitle("[ACTIVE]") = "500 Internal Server Error – Mozilla Firefox" Then
		MsgBox(0,"Attention!","Aruco ID "&$id2&" is out of camera range! Please start the process again.")
		exit
	EndIf
EndFunc

#EndRegion

#Region ### map laboratory function  ###

Func map_lab()
	global $count = 1
	_TightVNC() 												;start VNC
	Select_script() 											;shift scan program
	load_script()												;load script
	graphScriptStart()											;start graph. script
	Map_coord_calc()											;detect coord, save image & position, move distance, save image & position
EndFunc

Func Map_coord_calc()
	ShellExecute($pos) 											;camera menu
	WinWaitActive("LARS CONTROL – Mozilla Firefox")
	Sleep(500)
	Send("{CTRLDOWN}k{CTRLUP}")
	Sleep(500)
	Send("{BACKSPACE}")
	Send($pos&$id1)
	Sleep(1000)
	Send("{ENTER}")
	Sleep(1500)
	If $count = 1 then
	Do
		Send("{F5}")
		Sleep(1500)
	Until WinGetTitle("[ACTIVE]") = "Mozilla Firefox"
	Sleep(250)
	graphScriptEnd()
	delete_script()
	EndIf
	;__________________________________________________Check if other markers are in range
	WinActivate("Mozilla Firefox")
	WinWaitActive("Mozilla Firefox")
	Sleep(500)
	Send("{CTRLDOWN}k{CTRLUP}")
	Sleep(500)
	Send("{BACKSPACE}")
	Send($pos&$id2)
	Sleep(1000)
	Send("{ENTER}")
	Sleep(2000)
	If WinGetTitle("[ACTIVE]") = "500 Internal Server Error – Mozilla Firefox" Then
		MsgBox(0,"Attention!","Aruco ID "&$id2&" is out of camera range! Please start the process again.")
		exit
	ElseIf WinGetTitle("[ACTIVE]") = "Mozilla Firefox" Then
		sleep(1000)
		Send("{CTRLDOWN}k{CTRLUP}")
		Sleep(500)
		Send("{BACKSPACE}")
		Send($pos&$id3)
		Sleep(1000)
		Send("{ENTER}")
		Sleep(2000)
		If WinGetTitle("[ACTIVE]") = "500 Internal Server Error – Mozilla Firefox" Then
			MsgBox(0,"Attention!","Aruco ID "&$id3&" is out of camera range! Please start the process again.")
			exit
		EndIf
	EndIf
	sleep(500)
	$pic = "image"&$count
	savePic()
	If $count = 1  then
		get_coord()
		move_distanz()
	ElseIf $count = 2 then
		get_coord()
		MsgBox(0,"","python skript aufrufen")
		global $pythonfile = ""
		python()
	EndIf
EndFunc

Func move_distanz()
	global $count = 2
	Global $xpkt = 0
	global $ypkt = -0.05
	global $zpkt = 0
	global $xrot = 0
	global $yrot = 0
	global $zrot = 0
	global $program = "initial.js"
	_TightVNC()
	Select_script()
	load_script()
	move_rel()
	textScriptStart()
	textScriptEnd()
	Map_coord_calc()
EndFunc

Func get_coord()
	WinActivate("horst-218:0 - TightVNC Viewer")
	WinWaitActive("horst-218:0 - TightVNC Viewer")
	sleep(200)
	$program = "initial.js"
	Select_script()
	load_script()
	;
	Mouseclick("",950,256)									;current position
	sleep(500)
	MouseClick("",927,657)
	MouseClick("",927,657)
	MouseClick("",927,657)
	sleep(250)
	send("{ctrldown}c{ctrlup}")
	sleep(300)
	send("{LWIN}")
	sleep(500)
	send("editor")
	sleep(200)
	Send("{ENTER}")
	WinWaitActive("Unbenannt - Editor")
	sleep(200)
	Send("{ctrldown}v{ctrlup}")
	sleep(200)
	Send("{CTRLDOWN}s{CTRLUP}")
	sleep(200)
	Send("{CTRLDOWN}l{CTRLUP}")
	sleep(500)
	Send("C:\Users\rupp\Desktop\images")
	sleep(500)
	Send("{ENTER}")
	sleep(500)
	MouseClick("",660,400)
	sleep(500)
	Send("{ALTDOWN}n{ALTUP}")
	sleep(500)
	Send("pos"&$count)
	sleep(500)
	Send("{ENTER}")
	Sleep(200)
	Send("{ALTdown}d")
	sleep(200)
	Send("b")
	Sleep(200)
	Send("{Altup}")
	textScriptEnd()
	delete_script()
EndFunc

Func move_rel()
	Sleep(500)
	MouseClick("",170,600)
	Sleep(500)
	Send ("move({")
	Send("{ENTER}")
	Send("""speed.ratio"": 0.75,")
	Send("{ENTER}")
	Send("""movetype"" : ""JOINT"",")
	Send("{ENTER}")
	Send("""poserelation"" : ""RELATIVE"",")
	Send("{ENTER}")
	Send("""coord"" : ""CARTESIAN_TCP"",")
	Send("{ENTER}")
	Send("""target"" : {""xyz")
	Send("{+}")
	Send("euler"" : [")
	Send($xpkt&","&$ypkt&","&$zpkt&","&$xrot&","&$yrot&","&$zrot&"]},")
	Send("{ENTER}")
	Send("""blendradius.xyz"" : 0.12,")
	Send("{ENTER}")
	Send("""blendradius.orient"" : 180,")
	Send("{ENTER}")
	Send("})")
	Send("{ENTER}")
EndFunc

#EndRegion

#Region ### process functions        ###

Func python()
	Send("{LWIN}")
	sleep(500)
	send("cmd")
	sleep(500)
	Send("{ENTER}")
	WinWaitActive("Eingabeaufforderung")
	Sleep(500)
	Send($pythonfile)
	Sleep(300)
	;Send("{ENTER}")
	;weitere eingaben
EndFunc

Func savePic()
		Sleep(500)
		Send("{CTRLDOWN}k{CTRLUP}")
		Sleep(500)
		Send("{BACKSPACE}")
		Send($raw) 											;show image
		sleep(200)
		Send("{ENTER}")
		WinWaitActive("rawimg (JPEG-Grafik, 2400 × 2400 Pixel) - Skaliert (38%) – Mozilla Firefox")
		sleep(2000)
		MouseClick("right",950,550)
		sleep(200)
		Send("u")
		WinWaitActive("Grafik speichern")
		sleep(200)
		Send("{CTRLDOWN}l{CTRLUP}")
		sleep(500)
		Send("C:\Users\rupp\Desktop\images")
		sleep(500)
		Send("{ENTER}")
		sleep(500)
		WinActivate("Grafik speichern")
		WinWaitActive("Grafik speichern")
		MouseClick("",750, 350)
		sleep(500)
		Send("{ALTDOWN}n{ALTUP}")
		sleep(500)
		Send($pic)
		sleep(500)
		Send("{ENTER}")
		Sleep(200)
EndFunc

#EndRegion





