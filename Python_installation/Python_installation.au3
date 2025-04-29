;automated Python installation

;Python 3.8.1 for 3D reconstruction
MsgBox(0,"Python 3.8.1", "Start Python 3.8.1 installation",1)
Sleep(100)
RunWait('cmd.exe /c py -3.8 -m pip install virtualenv && py -3.8 -m virtualenv venv38 && call venv38\Scripts\activate && py -m pip install -r requirements_3D_reconstruction.txt', '', @SW_MAXIMIZE)
Sleep(100)
MsgBox(0,"Finished", "The first installation is finished",1)

;Python 3.11.2 for display detection
MsgBox(0,"Python 3.11.2", "Start Python 3.11.2 installation",1)
Sleep(100)
RunWait('cmd.exe /c py -3.11 -m pip install virtualenv && py -3.11 -m virtualenv venv311 && call venv311\Scripts\activate && py -m pip install -r requirements_display_detection.txt', '', @SW_MAXIMIZE)
Sleep(100)
MsgBox(0,"Finished", "The second installation is finished",1)

;Python 3.11.2 for camera calibration
MsgBox(0,"Python 3.11.2", "Start Python 3.12.0 installation",1)
Sleep(100)
RunWait('cmd.exe /c py -3.12 -m pip install virtualenv && py -3.12 -m virtualenv venv312 && call venv312\Scripts\activate && py -m pip install -r requirements_camera_calibration.txt', '', @SW_MAXIMIZE)
Sleep(100)
MsgBox(0,"Finished", "The last installation is finished.",1)