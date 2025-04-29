
;Linux variables
global $save = "/home/fruitcore/fruitcore/save/" ;horst program that should be executed
global $z_folder = "/home/fruitcore/fruitcore/save/z_folder" ;library of all horst programs
global $desktop = "/home/fruitcore/Desktop/"
;cam variables
global $img = "http://192.168.4.1:8080/img"    ;get current image with markers
global $raw = "http://192.168.4.1:8080/rawimg" ;get current raw image
Global $list = "http://192.168.4.1:8080/list"  ;get all visible IDs
Global $pos = "http://192.168.4.1:8080/"       ;+ID to get position of specific ID
Global $program = "Scan4SandM.js"
$pic = "rawimg"

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

Func get_value($id1, $id2)
	global $id1
	global $id2
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
		MsgBox(0,"","Display detection python script executing",2)
		displaydetection()
		exit
	ElseIf WinGetTitle("[ACTIVE]") = "500 Internal Server Error – Mozilla Firefox" Then
		MsgBox(0,"Attention!","Aruco ID "&$id2&" is out of camera range! Please start the process again.")
		exit
	EndIf
EndFunc

#EndRegion

#Region ### map laboratory function  ###

Func map_lab($id1, $id2, $id3)
	global $id1
	global $id2
	global $id3
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
		MsgBox(0,"","Reconstruction Python script execution",2)
		reconstruction()
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
	Send("display_detection\Input_img")
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

#Region  ### process functions        ###
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
		Send("display_detection\Input_img")
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