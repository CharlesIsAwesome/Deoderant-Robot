import cv2
import numpy as np
from PIL import Image
import time
from colorLimit import get_limits

skinTone = [140,180,210] #skinTone in BGR colorspace
cap = cv2.VideoCapture(0)   #Specifies what webcam is being used
detection_start_time = None  # Store the time of the initial detection

while True:
    ret, frame = cap.read() #Captures the frames within the webcam
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)#converts image from the bgr colour space to the rgb colour space
    lowerLimit, upperLimit = get_limits(color=skinTone)
    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)  #mask for all the qpixels that belong to the color desired
                        #hsvImage calls the function that has been defined within the util colorLimit.py file

    mask_ = Image.fromarray(mask) #Gets mask then calls image.fromarray, converting an image from numpy to pillow

      # Apply morphological operations to reduce noise
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)

      # Find contours in the cleaned mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  # Combine all contour bounding points to create one large bounding box
    if contours:
        x_min, y_min = np.inf, np.inf
        x_max, y_max = -np.inf, -np.inf

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            x_min = min(x_min, x)
            y_min = min(y_min, y)
            x_max = max(x_max, x + w)
            y_max = max(y_max, y + h)

        # Draw a single bounding box around the detected human body
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

   # Set detection start time if not set
        if detection_start_time is None:
            detection_start_time = time.time()

        # Check if 5 seconds have passed since detection
        elif time.time() - detection_start_time >= 5:
            print("Hello, World!")
            detection_start_time = None  # Reset timer to print only once per detection
    else:
        # Reset detection time if no contours are detected
        detection_start_time = None

    cv2.imshow('frame', frame) #Displays the frames

    if cv2.waitKey(1) & 0xff == ord('q'): 
        break
        #Upon pressing 'q' stop the capture

cap.release() #Release Memory
cv2.destroyAllWindows()
#Basic structure to display webcam stream
