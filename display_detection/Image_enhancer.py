import subprocess
import sys
import cv2

def run_image_enhancer(img_folder_path):
    # Open the text file in read mode
    with open('display_detection\detection_requirements.txt', 'r') as file:
        # Read the path from the file
        autoit_exe_path = file.readline().strip()
        cutout_user = file.readline().strip()
        cutout_password = file.readline().strip()
        enhanced_save_path = file.readline().strip()
        driver_edge_path = file.readline().strip()
        #image_folder_path = file.readline().strip()
        image_folder_path = img_folder_path

    # Path to your AutoIt script
    autoit_script_path = r'display_detection\Scripts\enhancer.au3'

    # Build the command to execute with the image folder path as a command-line argument
    command = [autoit_exe_path, autoit_script_path,cutout_user,cutout_password, image_folder_path, enhanced_save_path,driver_edge_path]
    # Use subprocess to run the AutoIt script
    subprocess.run(command)
    img_enhanced = cv2.imread(r"display_detection\Enhanced_imgs\enhanced_img.png")

    return img_enhanced
