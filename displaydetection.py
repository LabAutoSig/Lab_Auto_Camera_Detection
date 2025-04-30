#Detect Aruco markers in images
#Display text recognition with a trained model
#Detection with yolov8
#______________________________________________
#1. Import the necessary libraries
#______________________________________________
import cv2
import sys
#Import custom functions: 
from display_detection.ArUco_finder import findArucoMarkers
from display_detection.Marker_sorting import sorted_corners
from display_detection.Image_processer import processImage
from display_detection.Yolo_prediction import yoloPredict


def main_script():
    id_list = [1, 2, 3, 4, 5, 8, 42, 161, 314]
    #Call the functions:
    bboxs, ids, image_return = findArucoMarkers(img, img_path, id_list)#Call aruco detection function
    cv2.imshow("Image return", image_return)
    print(f"Detected bounding boxes: {bboxs}")
    print(f"Detected ids: {ids}")
    bboxs_sorted = sorted_corners(bboxs)
    print(f"Sorted bbox corners: {bboxs_sorted}")
    cropped = processImage(bboxs_sorted, ids, image_return) #Call Image process function
    cv2.imwrite(cropped_path,cropped)
    prediction = yoloPredict(cropped, yolo_path, save_path, ids, cropped_path, output_path) #Call the prediction function
    if prediction == None:
        cropped_enhanced = cv2.imread(enhanced_path)
        prediction_enhanced = yoloPredict(cropped_enhanced, yolo_path, save_path, ids, cropped_path, output_path) #Call the prediction function
        print(f"Predicted values: {prediction_enhanced}")
        if prediction_enhanced == None:
            print("Image is not predictable. Try another one...")
            sys.exit()
    else:   
        print(f"Predicted values: {prediction}")
        sys.exit()

def run_with_error_control():
    error_count = 0
    while error_count < 2:
        try:
            main_script()
            break  # Exit loop if no error
        except Exception as e:
            error_count += 1
            if error_count < 2:
                print("Error occurred, restarting script...")
            else:
                with open(output_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Error. Script failure"])
                print("Error occurred again, writing to output.csv and exiting.")
                break

if __name__ == "__main__":
    
    #______________________________________________________________________________________
    #_______________________Command Line___________________________________________________
    #______________________________________________________________________________________
    #Define the image, save and model paths for your individual folder structure
    print("Start display detection process...")
    #Load the image --> change path
    img_path = r"display_detection\Input_img\rawimg.jpg"
    img = cv2.imread(img_path)
    #cv2.imshow("img",img)
    #Define the model path 
    yolo_path = r"display_detection\Trained_model\best.pt" #Model_V10_best.pt in folder Models is the best one and used here
    #Define where the images should be saved
    save_path = r'display_detection\Saved_Images\ '
    cropped_path = r'display_detection\Processed_imgs\cropped_img.jpg'
    output_path = r'display_detection\output.csv'
    enhanced_path = r"display_detection\Enhanced_imgs\enhanced_img.png"
    #___________Load Data_____________________
    marker_length = 0.025 #aruco marker side length
    run_with_error_control()

