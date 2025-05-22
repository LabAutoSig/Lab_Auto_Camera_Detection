#include <wd_helper.au3>
#include <wd_core.au3>
#include <wd_capabilities.au3>

;__________________________________Variables_______________________________________
;Retrieve cutout login data, image path, image save path, edge driver path and download folder path from Python command line input
Global $user = $CmdLine[1]
Global $password = $CmdLine[2]
Global $img = $CmdLine[3]
Global $save_path = $CmdLine[4]
Global $driver_edge = $CmdLine[5]
Global $directory = $CmdLine[6]
Global $targetFolder = $save_path
Global $srcFolder = @UserProfileDir & "\Downloads"
Global $newFileName = "enhanced_img.png"
Global $url = "https://www.cutout.pro/photo-enhancer-sharpener-upscaler"
Global $fixed_port = 9515
; Main script

; Manually run EdgeDriver on fixed port
Run('"' & $driver_edge & '" --port=' & $fixed_port)
; Let it start
Sleep(1000)
_WD_Option("Driver",$driver_edge)
_WD_Option("Port", $fixed_port) ;Specify the correct port here
; Do NOT let AutoIt launch the driver again — it's already running!
#_WD_Startup(False) ; False = don't auto-run the driver process
If @error Then
	MsgBox(16, "Error", "Failed to start WebDriver. Exiting.")
	Exit
EndIf
;____________Start Webdriver session___________________
Global $oWD = _WD_CreateSession() ; creates a session
_WD_Navigate($oWD, $url) ;goes to cutout.pro url
_WD_Window($oWD, "Maximize") ; maximizes window size
_WD_LoadWait($oWD); waits until the page is fully loaded before proceeding

;__________________Login page cutout.pro___________________
;all webpage buttons and fields are searched by html XPaths
;Program waits until Login button is loaded
_WD_WaitElement($oWD, $_WD_LOCATOR_ByXPath, "//button[contains(text(),'Log in / Sign up')]"  )
;Searches for Log in/Sign up button
Local $Login = _WD_FindElement($oWD, $_WD_LOCATOR_ByXPath,"//button[contains(text(), 'Log in / Sign up')]" )
Sleep(2000)
_WD_ElementAction($oWD, $Login, 'click'); Clicks on login
_WD_LoadWait($oWD); waits until page is fully loaded
;find email input field
Local $email = _WD_FindElement($oWD, $_WD_LOCATOR_ByXPATH, '//*[@id="input-157"]')
_WD_ElementAction($oWD, $email, "click"); clicks on email field
_WD_LoadWait($oWD); load page
Sleep(100)
Send($user);Username is send to email input field
Sleep(500)
Send("{TAB}"); Sends Key to switch to password input
Sleep(500)
Send($password); Sends password to input field
Sleep(500)
Send("{ENTER}");Switch to Login field
Sleep(200)
Send("{ENTER}") ;Clicks Login
Sleep(100)

If @error Then
	MsgBox(16, "Error", "Failed to Log In. Exiting.")
	Exit
EndIf

;___________Image upload and enhancement_______________________
;Find upload button
Local $Upload = _WD_FindElement($oWD, $_WD_LOCATOR_ByXPATH, '//*[@id="app"]/div/div[2]/div[1]/div/div/div[1]/div/div[1]/div')
_WD_ElementAction($oWD, $Upload, "click"); Click upload button
Sleep(100)
WinWaitActive("Öffnen"); Wait until "Öffnen" window is active --> exchange Öffnen with "Open" if you have an english system
Sleep(100)
Send($img);Sends the image path
Sleep(500)
Send("{ENTER}"); Loads image and starts enhancement
Sleep(100)
If @error Then
	MsgBox(16, "Error", "Failed to upload an image. Exiting")
	Exit
EndIf

;_____________Enhanced image download__________________
;Wait until download button is there
_WD_WaitElement($oWD, $_WD_LOCATOR_ByXPath, '//*[@id="app"]/div/div[1]/div/div/div[4]/div/div/div[2]/div[2]/div/div/div[1]/div/div[1]/button')
Local $Download = _WD_FindElement($oWD, $_WD_LOCATOR_ByXPath, '//*[@id="app"]/div/div[1]/div/div/div[4]/div/div/div[2]/div[2]/div/div/div[1]/div/div[1]/button')
Sleep(3000) ; Wait for 3 secons until image is completely loaded
_WD_ElementAction($oWD, $Download, "click"); Clicks on Download button
Sleep(2000) ; Wait for 2 seconds for download
;Move the latest file
Global $search = FileFindFirstFile($srcFolder & "\*.png") ; Search for new png image in download folder
If $search <> -1 Then ; if search was succesfull
    Global $file = FileFindNextFile($search); Retrieve image path
    FileMove($srcFolder & "\" & $file, $targetFolder & "\" & $newFileName, 1); Move file and rename it
    FileClose($search); Close the searched file
EndIf
If @error Then
	MsgBox(16, "Error", "Failed to save enhanced image. Exeting.")
	Exit
EndIf
;____________End webdriver session_______________
_WD_DeleteSession($oWD);Closes webdriver session
If @error Then Return SetError (@error, @extended, 0)
_WD_Shutdown();Shutsdown webdriver
If @error Then Return SetError (@error, @extended, 0)
Exit;Exits AutoIt script and returns to Python script