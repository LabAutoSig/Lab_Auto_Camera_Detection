 #include <DateTimeConstants.au3>
#include <Date.au3>
#include <wd_helper.au3>
#include <wd_capabilities.au3>

;__________________________________User data_______________________________________

Global $user = $CmdLine[1]
Global $password = $CmdLine[2]
; Retrieve the output folder path from the command line
Global $img = $CmdLine[3] ;Bildpfad wird von Python übertragen
Global $url = "https://www.cutout.pro/photo-enhancer-sharpener-upscaler"

;Speicherpfad
Global $save_path = $CmdLine[4]

;Name für bearbeitetes Bild generieren; zur Dokumentation
$timestamp = _NowCalc()
$timestamp = StringReplace($timestamp, ":", "")
$timestamp = StringReplace($timestamp, "/", "")
$timestamp = StringReplace($timestamp, " ", "_")
$newimg = "enhanced_img" & "_" & $timestamp

;________________________________________Skript_____________________________________________
;mit WebDriver
Global $driver_edge = $CmdLine[5]
_WD_Option("Driver",$driver_edge)
_WD_Option("Port", 9515) ;Specify the correct port here
_WD_Startup()

If @error Then
	MsgBox(16, "Error", "Failed to start WebDriver. Exiting.")
	Exit
EndIf

Global $oWD = _WD_CreateSession()
_WD_Navigate($oWD, $url)
_WD_Window($oWD, "Maximize")
_WD_LoadWait($oWD)
 
;Login
_WD_WaitElement($oWD, $_WD_LOCATOR_ByXPath, "//button[contains(text(),'Log in / Sign up')]"  )
Local $Login = _WD_FindElement($oWD, $_WD_LOCATOR_ByXPath,"//button[contains(text(), 'Log in / Sign up')]" )
Sleep(2000)
_WD_ElementAction($oWD, $Login, 'click')
_WD_LoadWait($oWD)
Local $email = _WD_FindElement($oWD, $_WD_LOCATOR_ByXPATH, '//*[@id="input-157"]')
_WD_ElementAction($oWD, $email, "click")
_WD_LoadWait($oWD)
Sleep(100)
Send($user)
Sleep(500)
Send("{TAB}")
Sleep(200)
Send($password)
Sleep(500)
Send("{ENTER}")
Sleep(100)
Send("{ENTER}")
Sleep(100)

If @error Then
	MsgBox(16, "Error", "Failed to Log In. Exiting.")
	Exit
EndIf

;Bild hochladen
Local $Upload = _WD_FindElement($oWD, $_WD_LOCATOR_ByXPATH, '//*[@id="app"]/div/div[2]/div[1]/div/div/div[1]/div/div[1]/div')
_WD_ElementAction($oWD, $Upload, "click")
Sleep(100)
WinWaitActive("Öffnen")
Sleep(100)
Send($img)
Sleep(500)
Send("{ENTER}")
Sleep(100)

If @error Then
	MsgBox(16, "Error", "Failed to upload an image. Exiting")
	Exit
EndIf

;Bild wird bearbeitet und heruntergeladen
_WD_WaitElement($oWD, $_WD_LOCATOR_ByXPath, '//*[@id="app"]/div/div[1]/div/div/div[4]/div/div/div[2]/div[2]/div/div/div[1]/div/div[1]/button')
Local $Download = _WD_FindElement($oWD, $_WD_LOCATOR_ByXPath, '//*[@id="app"]/div/div[1]/div/div/div[4]/div/div/div[2]/div[2]/div/div/div[1]/div/div[1]/button')
_WD_ElementAction($oWD, $Download, "click")
Sleep(1000)
Send("^j")
Sleep(2000)
Send("{ENTER}")
Sleep(2000)
Send("^s")
Sleep(100)
WinWaitActive("Speichern unter")
Sleep(100)
Send($save_path & "enhanced_img")
Sleep(1000)
Send("{ENTER}")
Sleep(500)
Send("{LEFT}")
Sleep(100)
Send("{ENTER}")
Sleep(1000)

If @error Then
	MsgBox(16, "Error", "Failed to save enhanced image. Exeting.")
	Exit
EndIf

Send("^s")
Sleep(100)
WinWaitActive("Speichern unter")
Sleep(500)
Send($save_path & $newimg)
Sleep(1000)
Send("{ENTER}")
Sleep(100)


If @error Then
	MsgBox(16, "Error", "Failed to save enhanced image with new name (adding date and time). Exeting.")
	Exit
EndIf
Send("{ESC}")
Sleep(200)


;Programm schließen
_WD_DeleteSession($oWD)
If @error Then Return SetError (@error, @extended, 0)

;WebDriver schließen
_WD_Shutdown()
If @error Then Return SetError (@error, @extended, 0)
Exit