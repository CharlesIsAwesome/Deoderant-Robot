import cv2
from PIL import Image

from colorLimit import get_limits

skinTone = [147, 102, 89] #skinTone in RGB colorspace

cap = cv2.VideoCapture(0)   #Specifies what webcam is being used
while True:
    ret, frame = cap.read() #Captures the frames within the webcam

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)#converts image from the bgr colour space to the rgb colour space

    lowerLimit, upperLimit = get_limits(color=skinTone)

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)  #mask for all the pixels that belong to the color desired
                        #hsvImage calls the function that has been defined within the util colorLimit.py file

    mask_ = Image.fromarray(mask) #Gets mask then calls image.fromarray, converting an image from numpy to pillow

    bbox = mask_.getbbox() #Creates the box around the image

    if bbox is not None:
        x1, y1, x2, y2 = bbox

        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

    cv2.imshow('frame', frame) #Displays the frames

    if cv2.waitKey(1) & 0xff == ord('q'): 
        break
        #Upon pressing 'q' stop the capture

cap.release() #Release Memory

cv2.destroyAllWindows()

#Basic structure to display webcam stream