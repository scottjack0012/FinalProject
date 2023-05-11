
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

from matplotlib import pyplot
from matplotlib.patches import Rectangle
from mtcnn.mtcnn import MTCNN

import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

#video4 shows turning and going to and from face
#video5 shows search function
#video6 shows variable turning

URI = 'radio://0/80/2M/E7E7E7E7E7'
DEFAULT_HEIGHT = 0.5
dimx = 800 #Dimentions of resized image
dimy = 450
centrewidth = 300      #width of centre box
centreleft = round((dimx / 2) - (centrewidth / 2))      #left side position of centre box
centreright = round((dimx / 2) + (centrewidth / 2))     #right side position of centre box
centretop = round((dimy / 2) - (centrewidth / 2))       #top side position of centre box
centrebottom = round((dimy / 2) + (centrewidth / 2))    #bottom side position of centre box
print(dimx, dimy, centrewidth, centreleft, centreright, centretop, centrebottom)



def check_posy(cy):
##    print(cy)
    if cy > centrebottom:
        print("Below drone level")
    elif cy < centretop:
        print("Above drone level")
    


def check_posx(cx):
    ##    print(cx)
    if (cx < centreright) and (cx > centreleft):
        print("Detected in the centre")
        mc.stop()
    elif cx > centreright:
        diff = cx - centreright
        print("diff", str(diff))
        turnvar = (diff / (dimx - centreright)) * 40
        print("turnvar:" + str(turnvar))
        print("Turn Right")
        mc.turn_right(turnvar, 90)
        return "Right"
    elif cx < centreleft:
        diff = centreleft - cx
        print("diff", str(diff))
        turnvar = (diff / centreleft) * 40
        print("turnvar:" + str(turnvar))
        print("Turn Left")
        mc.turn_left(turnvar, 90)
        return "Left"

def check_distance(area):
    if (area < 39000) and (area > 23000):
        print("Good distance")
        mc.start_forward(0)
        mc.start_back(0)
    elif (area < 23000):
        print("Too far, getting closer")
        mc.start_forward(0.2)
    elif (area > 39000):
        print("Too Close!")
        mc.start_back(0.1)

def search(direction):
    if direction == "Left":
        mc.start_turn_left(25)
        print("Searching left")
    elif direction == "Right":
        mc.start_turn_right(25)
        print("Searching right")
    else:
        mc.start_turn_left(0.2)
        print("Searching for face")


def get_frame(startTime):
    currentTime = time.time()
    timePassed = currentTime - startTime
    currentFrame = round(timePassed * 29)
    print(currentFrame)
    return currentFrame
    
    

if __name__ == '__main__':
    cflib.crtp.init_drivers()
    #with SyncCrazyflie(URI) as scf:
        #with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:

    detector = MTCNN()
    time.sleep(3)
    direction = "Right"
    vid = cv2.VideoCapture('/home/jackscott/MyFiles/testimages/mytestvid3.mp4')
    #print(seconds)
    total = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    count = 0
    #print(total)
    classifier = CascadeClassifier('/home/jackscott/MyFiles/openCV/haarcascade_frontalface_default.xml')
    startTime = time.time()
    if (vid.isOpened()== False):
        print("Error setting up video")
    else:
        while (vid.isOpened()):
            frameNo = get_frame(startTime)
            vid.set(cv2.CAP_PROP_POS_FRAMES,frameNo)
            ret, frame = vid.read()
            if ret == True:
                
                resized = cv2.resize(frame, (dimx, dimy), interpolation = cv2.INTER_AREA)
                #cv2.imshow('Frame', resized)
                
                bboxes = detector.detect_faces(resized)
                bboxes = np.array(bboxes)
                for box in bboxes:
                 print(box)

                #Left box
                rectangle(resized, (0,0), (centreleft,dimy), (0, 0, 255), 1)
                #Right box
                rectangle(resized, (centreright,0), (dimx,dimy), (0, 0, 255), 1)
                #Centre box
                rectangle(resized, (centreleft,centretop), (centreright,centrebottom), (0, 255, 0), 1)

                if not bboxes.any():
                    print("No face detected")
                    print(direction)
                    #search(direction)

                for box in bboxes:
                    # extract
                    x, y, width, height = box['box']
                    area = height * width
                    x2, y2 = x + width, y + height
                    cx, cy = round(x + (width/2)), round(y + (height/2))
                    
                    # draw a rectangle over the pixels
                    rectangle(resized, (x, y), (x2, y2), (255, 0, 0), 1)
                    rectangle(resized, (cx-5, cy-5), (cx+5, cy+5), (255, 255, 0), 1)
                              
                    for key, value in box['keypoints'].items():
                             cv2.circle(resized, value, 2, (0, 0, 255), 10)
                    print(area)
                    #check_posy(cy)
                    #direction = check_posx(cx)
                    print(direction)
                    #check_distance(area)

                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break
            imshow('face detection', resized)
            
    vid.release()

    cv2.destroyAllWindows()
