# Lab_Auto_Camera_Detection
This GitHub repository is associated to our research Article: "Facilitating Laboratory Automation Using Robots: A Simple And Inexpensive Camera 
Detection System" in Scientific Reports. For further information take a look at our research article (insert link here).

## Our work 
Laboratory automation has transformed bioanalytical research, yet smaller research laboratories face challenges in adopting such technologies due to limited resources, time, and technical expertise, while already facing complex bioanalytical methods. To address these barriers, we developed a robotic-arm-based camera detection system featuring two software applications designed to simplify laboratory automation. Both applications use fiducial markers (Augmented Reality University of Cordoba (ArUco)), for object detection. The first application creates a 3D digital model of the robot's environment using ArUco markers and a Python-based Open Computer Vision (OpenCV) simulated stereo vision setup, enabling automated computer-aided design (CAD) in FreeCAD. This facilitates safe and efficient robot arm navigation. The second application integrates a deep learning neural network for automated digital display recognition, achieving an error rate of 1.81 %, comparable to manual readings. By leveraging low-cost hardware and open-source software available on GitHub, the system is accessible to smaller research facilities, reducing programming complexity and enabling broader adoption of laboratory automation in bioanalytical workflows. This work demonstrates an affordable and effective solution for integrating robotic arms into scientific workflows, enhancing reproducibility and efficiency in bioanalytical research.

## Detection System Installation Guide

This section provides a comprehensive guide for setting up the detection system, including the installation of AutoIt, FreeCAD, and multiple Python versions with their respective libraries. Virtual environments are recommended to manage different Python library versions on the same computer. If you prefer not to use the provided automated Python installation script or need to install additional Python versions, detailed instructions are included. Additionally, you must update two configuration files with your installation paths.

### 1. AutoIt 3 Installation and Interface

Download the AutoIt 3 package from the [official AutoIt website](https://www.autoitscript.com/site/autoit/downloads/). You can choose between the "AutoIt Full Installation" executable, the AutoIt Script Editor (SciTe) installers, or the self-extracting archive (ZIP folder) if administrative rights are unavailable. After installation, search for "SciTe" in the Windows search bar to open the editor. SciTe allows you to create or edit AutoIt scripts.

### 2. Python Installation Guide

To install Python, download the desired version's executable installer from the [official Python website](https://www.python.org/downloads/). For example:
- **Python 3.8.1**: Required for laboratory mapping.
- **Python 3.11.2**: Required for display detection.
- **Python 3.12.0**: Required for camera calibration.

During installation:
1. Check the "Add to Path" option.
2. Click "Install Now" to complete the process.

Repeat this process for each required Python version.

### 3. Virtual Environments

If you need to use multiple Python versions with version-specific libraries, virtual environments are essential. Follow the steps below to set up virtual environments.

#### 3.1 Automated Python Installation Script

We provide an AutoIt script to automate the installation of virtual environments and Python packages:
1. Install AutoIt (see section 1).
2. Download the required Python versions (see section 2).
3. Run the `Python_installation.au3` script located in the `camera_detection_system\Python_installation\` directory.
4. Wait for the confirmation message indicating the installation is complete.

#### 3.2 Manual Virtual Environment and Package Installation

For manual setup or additional Python versions:
1. Install Python (see section 2).
2. Open the Windows Command Prompt (`Windows + R`, type `cmd`, and press ENTER).
3. Run the following commands:
    - `py -3.8 -m pip install virtualenv` (replace `3.8` with your Python version).
    - `py -3.8 -m virtualenv venv38` to create a virtual environment named `venv38`.
4. Activate the virtual environment: `venv38\Scripts\activate`.
5. Install required libraries: `py -m pip install <library_name>==<version>`.
6. Deactivate the environment: `venv38\Scripts\deactivate`.

To create or access virtual environments in a different directory, use the `cd` command to navigate to the desired path before running the above commands.

### 4. FreeCAD Installation

Download FreeCAD from the [official FreeCAD website](https://www.freecadweb.org/downloads.php). After installation, update the `FreeCAD_path.txt` file in the `camera_detection_system\3D_reconstruction\` directory with your FreeCAD installation path.

### 5. User-Specific Path Updates

Update the following files with your specific paths:
- `display_detection\detection_requirements.txt`: Update with your Cutout.pro credentials.
- `3D_reconstruction\FreeCad_path.txt`: Update with the FreeCAD bin folder path.

Refer to the detailed instructions in the original guide for further customization.
