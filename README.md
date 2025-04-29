# Lab_Auto_Camera_Detection
1	Detection system installation guide
The usage of the detection system requires installing AutoIt, FreeCAD, and multiple Python versions, along with their respective libraries. To manage different Python library versions on the same computer, virtual environments are necessary. This section provides a guide for installing AutoIt, FreeCAD and Python in virtual environments on a Windows computer. If you choose not to use the automated Python installation script we provided (AutoIt script) or wish to install additional Python versions, a detailed guide is included below. Additionally, two configuration files must be updated with your installation paths.
1.1	AutoIt 3 installation and interface
The AutoIt 3 package can be downloaded from the official website (AutoIt Downloads - AutoIt (autoitscript.com)). You can either download the executable “AutoIt Full Installation” and the AutoIt Script Editor (SciTe) installers, or download the AutoIt self-extracting archive (zip folder), if you lack administrative rights. After installation, type “SciTe” into the Windows search bar to open the editor. SciTe allows you to open existing AutoIt scripts or create new ones. 
1.2	Python installation guide
To install Python, download the desired version’s executable installer from the official Python website. For example, laboratory mapping requires Python 3.8.1, which can be downloaded from the Python 3.8.1 release page. Locate the “Files” section at the bottom of the page to find the executable installer. After download, first, start the installer and check the “Add to Path” option and secondly click “Install now” to complete the installation. This process must be repeated for Python 3.11.2 and Python 3.12.0, which are required for display detection and camera calibration, respectively. 
1.3	Virtual environments
If you use multiple Python version with version-specific libraries, create virtual environments. This is already the case if you want to use our display recognition and 3D reconstruction system on the same computer. 
1.3.1	Automated Python installation script
We provide an automated AutoIt script for virtual environment and Python package installation, which you can use as follows: 
1.	Install AutoIt (see chapter 1.1)
2.	Download the necessary Python versions (see chapter 1.2)
3.	Double-click the “Python_installation.au3” script in the “camera_detection_system\Python_installation\” file 
4.	Wait until a message box is displayed that states that the last virtual environment is installed
1.3.2	Manual virtual environment and package installations
If you want to install other Python versions or additional libraries we provide a detailed guide below. The guide is written for the laboratory mapping Python version, but can be adjusted for any other Python version. 
1.	Python installation (chapter 1.2)
2.	Open Windows command window with [Windows]+[R], type “cmd”, and press ENTER.
3.	Run the following commands: 
a.	Write “py -3.8 -m pip install virtualenv” (replace “3.8” with your Python version) and press ENTER.
b.	Write “py -3.8 -m virtualenv venv38” to create a virtual environment named “venv38” and press ENTER. 
4.	To activate the virtual environment, type: venv38\Scripts\activate and press ENTER.
5.	Once activated, install libraries using: py -m pip install <library name> == <version> and press ENTER.
6.	Deactivate the environment by typing: venv38\Scripts\deactivate and press ENTER.
If you want to create the virtual environment in another path or access another virtual environment path, write “cd” followed by the desired system path and press ENTER. Afterwards, the current location is changed to the new path and you can type in the commands for virtual environment creation or library installation. The necessary libraries for our system are listed below (chapter 2.1, 0 and 2.3.).
1.4	Python usage without an interpreter
To change the Python code without an interpreter (e.g. Eclipse, Visual studio), go into the “venvXY\Scripts” folder and click on the “Python.exe” file. In the Python.exe write: “import idlelib.idle” and press ENTER to open the Python IDLE. There you can open and manipulate existing Python scripts or write your own. We still recommend to use an interpreter like Visual studio or Eclipse. To change file paths use “/" or “\\” or r’path\to\something’ to define a folder location. Save the changed Python program afterwards. To test the Python program in the IDLE press F5.
Python scripts can be executed over the Windows command line, which is done automatically with our detection system. For manual script execution do the following: 
1.	Activate the virtual environment 
a.	Open the Windows command window (Windows + R  cmd) 
b.	Write your virtual environment activate path e.g.: “venv38\Scripts\activate” and press ENTER
c.	Write “cd C:\Users\name\camera_detection_system\” and press ENTER. Now, the Windows path changed to the detection system folder. 
d.	Start the Python program by typing “3D_reconstruction.py” and press ENTER. 
1.5	FreeCAD installation
Download the FreeCAD installer from the FreeCAD official website. Choose either the executable installer or the portable ZIP file. After installation, update the “FreeCAD_path.txt” file in the “camera_detection_system\3D_reconstruction\” directory with your FreeCAD installation path. 
1.6	User-specific path alterations
Some paths in the detection system are user-specific. Update the following files in the camera_detection_system folder: 
•	“display_detection\detection_requirements.txt”: Insert your “Cutout.pro” user name and password, the input image path and the save path of the enhanced image, as shown in Table S1. 
•	“3D_reconstruction\FreeCad_path.txt”: Update the FreeCAD bin folder path (“C:\\Users\\users\\AppData\\Local\\Programs\\FreeCAD_0_21\\bin”).
Text file line	User interaction
1	Cutout.pro e-mail
2	Cutout.pro password
3	C:\Users\userXY\camera_detection_system\display_detection\Input_img\rawimg.jpg

4	C:\Users\userXY\camera_detection_system\display_detection\Enhanced_imgs

Table S1: Display detection system requirements text file. The paths in bold must not be changed by the user. To use Cutout.pro, the user must define their password and user name. Line 3 and 4 have to adjusted to the user’s directory.

 
2	Python software and package versions
In this section we provide detailed information about Python versions and libraries required for each subsystem.
2.1	Display detection with Python 3.11.2
Install the libraries listed in Table S2 for display detection. The system only works with the listed library versions. 
Library name	Version	Command
NumPy	1.24.2	py –m pip install numpy == 1.24.2
OpenCV contrib	4.6.0.66	py -m pip install opencv-contrib-python==4.6.0.66
OpenCV	4.6.0.66	Py -m pip install opencv-python == 4.6.0.66
Imutils	0.5.4	py –m pip install imutils == 0.5.4
UUID	1.30	py –m pip install uuid == 1.30
Ultralytics	8.1.8	py –m pip install Ultralytics == 8.1.8
PyTorch	Torch vision:  0.16.0
Torch: 2.1.0	py –m pip install torch ==2.1.0
py -m pip install torchvision == 0.16.0
Pandas	2.0.1	py -m pip install pandas == 2.0.1
Dill	0.3.8	py -m pip install dill == 0.3.8
OpenPyXL	3.1.5	py -m pip install openpyxl == 3.1.5
Selenium	4.26.1	py -m pip install selenium == 4.26.1
Webdriver manager	4.0.2	py -m pip install webdriver-manager == 4.0.2
PyAutoGUI	0.9.54	py -m pip install pyautogui

Table S2: Required Python libraries for Python 3.11.2 display detection. 
2.2	3D reconstruction with Python 3.8.1
Using FreeCAD in Python, requires the adaption of the FreeCAD bin folder path in the “FreeCad_path.txt” file. Install the libraries listed in Table S3 for 3D reconstruction.
Library name	Version	Command
NumPy	1.24.2	py –m pip install numpy == 1.24.2
OpenCV contrib	4.6.0.66	py -m pip install opencv-contrib-python==4.6.0.66
OpenCV	4.6.0.66	Py -m pip install opencv-python == 4.6.0.66
Pandas	2.0.1	py -m pip install pandas == 2.0.1
Scipy	1.10.1	py -m pip install scipy == 1.10.1
PySide2	5.15.2.1	py -m pip install PySide2 == 5.15.2.1
Wheel	0.41.2	py -m pip install wheel == 0.41.2

Table S3: Required Python libraries for Python 3.8.1 3D reconstruction.
2.3	Camera calibration with Python 3.12.0
Use the commands in Table S4 to install the required libraries.
Library name	Version	Command
NumPy	1.26.2	py –m pip install numpy == 1.26.2
OpenCV	4.8.1.78	py -m pip install opencv-contrib-python ==4.8.1.78
UUID	1.30	py –m pip install uuid == 1.30

Table S4: Required Python libraries for Python 3.12.0 camera calibration
