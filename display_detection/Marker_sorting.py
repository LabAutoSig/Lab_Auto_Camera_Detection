#______________________________________________
#1. Import the necessary libraries
#______________________________________________
import numpy as np

#______________________________________________
#Function that sorts the pixel coordinates of the marker corners to have the same orientation of the markers
#______________________________________________
def sorted_corners(bboxes):

    sorted_bboxes = []

    for bbox_tuple in bboxes:
        bbox = bbox_tuple[0]
        #print(f"Bounding box before sorting {bbox}")
        #indexed_arr = [(i, subarr) for i, subarr in enumerate(bbox)] #subarrays are indexed
        #print(f"Indexed array before sorting {indexed_arr}")
        
        if len(bbox) >= 1:

            # Sort the bbox depending on the y coordinate using the sorted lambda key
            sorted_coordinates = sorted(bbox, key=lambda x: x[1], reverse=False)

            # Convert the result back to a NumPy array
            sorted_coordinates = np.array(sorted_coordinates)
            #print(f"Sorted coordinates {sorted_coordinates}")
            #Split array into upper and lower coordinate corners
            upper_coordinates = sorted_coordinates[:2]
            lower_coordinates = sorted_coordinates[2:]
            #print(f"Upper coordinates: {upper_coordinates}")
            #print(f"Lower coordinates: {lower_coordinates}")

            # Sort the upper corners depending on the x coordinate using the sorted lambda key 
            sorted_upper = sorted(upper_coordinates, key=lambda x: x[0], reverse=False)

            # Convert the result back to a NumPy array
            sorted_upper= np.array(sorted_upper)
            #print(f"Sorted upper {sorted_upper}")
            
            # Sort the lower coordinates based on the x-coordinate in descending order
            sorted_lower = sorted(lower_coordinates, key=lambda x: x[0], reverse=True)

            # Convert the result back to a NumPy array
            sorted_lower= np.array(sorted_lower)
            #print(f"Sorted lower {sorted_lower}")

            # Concatenate the sorted upper and lower coordinates
            sorted_bbox = np.concatenate((sorted_upper, sorted_lower), axis=0)
            #print(f"Sorted bounding box {sorted_bbox}")

            #convert the result back to an array
            sorted_arrays = np.array([sorted_bbox])
            #print(f"Sorted bounding boxes: {sorted_bboxes}")

        else:
            # If only one set of corners, no need to sort
            sorted_arrays = bbox

        #print(f"Sorted Array: {sorted_arrays}")
        sorted_bboxes.append((sorted_arrays,))

    return sorted_bboxes
