Func display()
	 ;Start Digit Recognition 
	Run("C:\Windows\System32\cmd.exe")
	WinWaitActive("C:\Windows\System32\cmd.exe")
	Send("cd C:\Users\wienbruch\camera_detection_system\Python_installation" & "{ENTER}")
	Sleep(100)
	Send('venv311\Scripts\activate' & "{ENTER}")
	 Sleep(100)
	 Send("cd C:\Users\wienbruch\camera_detection_system" & "{ENTER}")
	 Sleep(100)
	 Send("displaydetection.py" & "{ENTER}")
 EndFunc
 
 display()