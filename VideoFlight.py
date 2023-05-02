
# plot photo with detected faces using opencv cascade classifier
import cv2
import logging
import time
import numpy as np
from cv2 import imread
from cv2 import imshow
from cv2 import waitKey
from cv2 import destroyAllWindows
from cv2 import CascadeClassifier
from cv2 import rectangle

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
    ##    print(cx)
        if cx > 550:
            print("Turn Right")
            mc.start_turn_right(20)
        elif cx < 250:
            print("Turn Left")
            mc.start_turn_left(20)
        else:
            print("Detected in Centre")
            mc.stop()
            

def get_frame(startTime):
    currentTime = time.time()
    timePassed = currentTime - startTime
    currentFrame = round(timePassed * 29)
    print(currentFrame)
    return currentFrame
    
    

if __name__ == '__main__':
    cflib.crtp.init_drivers()
    with SyncCrazyflie(URI) as scf:
        with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
            time.sleep(1)
            vid = cv2.VideoCapture('/home/jackscott/MyFiles/openCV/mytestvid1.mp4')
            #print(seconds)
            total = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
            count = 0
            #print(total)
            classifier = CascadeClassifier('/home/jackscott/MyFiles/openCV/haarcascade_frontalface_default.xml')
            dim = (800, 450)
            startTime = time.time()
            if (vid.isOpened()== False):
                print("Error setting up video")
            else:
                while (vid.isOpened()):
                    frameNo = get_frame(startTime)
                    vid.set(cv2.CAP_PROP_POS_FRAMES,frameNo)
                    ret, frame = vid.read()
                    if ret == True:
                        
                        resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
                        #cv2.imshow('Frame', resized)
                        
                        bboxes = classifier.detectMultiScale(resized)
                        for box in bboxes:
                         print(box)

                        #Left box
                        rectangle(resized, (0,0), (250,450), (0, 0, 255), 1)
                        #Right box
                        rectangle(resized, (550,0), (800,450), (0, 0, 255), 1)
                        #Centre box
                        rectangle(resized, (250,75), (550,370), (0, 255, 0), 1)

                        for box in bboxes:
                            # extract
                            x, y, width, height = box
                            x2, y2 = x + width, y + height
                            cx, cy = round(x + (width/2)), round(y + (height/2))
                            
                            # draw a rectangle over the pixels
                            rectangle(resized, (x, y), (x2, y2), (0,0,255), 1)
                            rectangle(resized, (cx-5, cy-5), (cx+5, cy+5), (255, 0, 0), 1)
                            yPos = check_posy(cy, scf)
                            xPos = check_posx(cx, scf)

                        if cv2.waitKey(25) & 0xFF == ord('q'):
                            break
                    else:
                        break
                    imshow('face detection', resized)
            
    vid.release()

    cv2.destroyAllWindows()
