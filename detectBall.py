import cv2
import numpy as np
import imutils
from collections import deque
import serial
import time
import struct

# define the lower and upper boundaries of the "green"
# ball in the HSV color space
colorLower = (15*180/240, 140 , 150)
colorUpper = (40*180/240, 255 , 255)

ser = serial.Serial("com9", 9600)
time.sleep(2)

camera = cv2.VideoCapture(0)

while(True):
    ##s= time.time()
    # Capture frame-by-frame
    ret, frame = camera.read()
    #frame = cv2.flip( frame, 1 )
    # resize the frame, blur it, and convert it to the HSV
    frame = imutils.resize(frame, width=600)
    ##height, width = frame.shape[:2]
    #filters
    frame = cv2.GaussianBlur(frame, (11, 11), 0)
    frame = cv2.medianBlur(frame,5)
    #from RGB to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    #center = None
    # only proceed if at least one contour was found
    if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # only proceed if the radius meets a minimum size
            if radius > 10:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)
                    ##print ("x=",int(x),"y=",int(y))
                    #the frame width=600 and height=450
                    #mapping to 0-180
                    dx=int(x/600*180)
                    dy=int(y/450*180)
                    print ("x=",int(dx),"y=",int(dy))
                    ser.write(struct.pack('>BB',dx,dy));
    # Display the resulting frame
    cv2.imshow('frame1',hsv)
    cv2.imshow('frame2',mask)
    cv2.imshow('Result',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    ##e= time.time()
    ##print (s-e)
    
# When everything done, release the capture
ser.close()
camera.release()
cv2.destroyAllWindows()
