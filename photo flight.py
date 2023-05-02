
# plot photo with detected faces using opencv cascade classifier
import cv2
from cv2 import imread
from cv2 import imshow
from cv2 import waitKey
from cv2 import destroyAllWindows
from cv2 import CascadeClassifier
from cv2 import rectangle

import logging
import time

import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

URI = 'radio://0/80/2M/E7E7E7E7E7'
DEFAULT_HEIGHT = 0.5


def check_posy(cy, scf):
##    print(cy)
    if cy > 370:
        print("Below drone level")
    elif cy < 75:
        print("Above drone level")
    


def check_posx(cx, scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
    ##    print(cx)
        if cx > 550:
            print("Turn Right")
            mc.turn_right(90)
        elif cx < 250:
            print("Turn Left")
            mc.turn_left(90)


if __name__ == '__main__':
    cflib.crtp.init_drivers()
    with SyncCrazyflie(URI) as scf:

        # load the photograph
        img = imread('/home/jackscott/MyFiles/openCV/mytest21.jpg')
        
        
        scale_percent = 20 
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
         
        
        classifier = CascadeClassifier('/home/jackscott/MyFiles/openCV/haarcascade_frontalface_default.xml')
        bboxes = classifier.detectMultiScale(resized)

        #Left box
        rectangle(resized, (0,0), (250,450), (0, 0, 255), 1)
        #Right box
        rectangle(resized, (550,0), (800,450), (0, 0, 255), 1)
        #Centre box
        rectangle(resized, (250,75), (550,370), (0, 255, 0), 1)

        for box in bboxes: 
         # extract
         x, y, width, height = box
         print(x, y, width, height)
         x2, y2 = x + width, y + height
         cx, cy = round(x + (width/2)), round(y + (height/2))
         print(cx, cy)
         
         # draw a rectangle over the pixels
         rectangle(resized, (x, y), (x2, y2), (255, 0, 0), 1)
         # draw centre point 
         rectangle(resized, (cx-5, cy-5), (cx+5, cy+5), (255, 0, 0), 1)
         yPos = check_posy(cy, scf)
         xPos = check_posx(cx, scf)


        # show the image
        imshow('face detection', resized)
        # keep the window open until we press a key
        waitKey(0)
        # close the window
        destroyAllWindows()
