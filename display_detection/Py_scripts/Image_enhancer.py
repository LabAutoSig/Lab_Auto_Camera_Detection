import subprocess
import sys
import cv2
import os

def run_image_enhancer(image_path):
    # Open the text file in read mode
    with open('display_detection\detection_requirements.txt', 'r') as file:
        # Read the path from the file
        cutout_user = file.readline().strip()
        cutout_password = file.readline().strip()
    # Path to your AutoIt script
    #get current working directory
    directory = os.getcwd()
    print(directory)
    img_folder_path = os.path.join(directory, image_path)
    autoit_exe_path = os.path.join(directory, r'autoit-v3\install\AutoIt3.exe')
    driver_edge_path = os.path.join(directory, r'autoit-v3\edgedriver_win64\msedgedriver.exe')
    autoit_script_path = os.path.join(directory,r'display_detection\Scripts\enhancer_new.au3')
    enhanced_save_path = os.path.join(directory,r'display_detection\Enhanced_imgs')
    # Build the command to execute with the image folder path as a command-line argument
    command = [autoit_exe_path, autoit_script_path,cutout_user,cutout_password, img_folder_path, enhanced_save_path,driver_edge_path, directory]
    # Use subprocess to run the AutoIt script
    subprocess.run(command)
    img_enhanced = cv2.imread(r"display_detection\Enhanced_imgs\enhanced_img.png")

    return img_enhanced