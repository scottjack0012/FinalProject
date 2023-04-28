import cv2
import time
import numpy as np
from cv2 import imread
from cv2 import imshow
from cv2 import waitKey
from cv2 import destroyAllWindows
from cv2 import CascadeClassifier
from cv2 import rectangle
#fps = 29


if __name__ == '__main__':
    vid = cv2.VideoCapture('mytestvid1.mp4')
    total = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    count = 0
    #print(total)
    classifier = CascadeClassifier('haarcascade_frontalface_default.xml')
    dim = (800, 450)

    if (vid.isOpened()== False):
        print("Error setting up video")
    else:
        while (vid.isOpened()):
            
            ret, frame = vid.read()
            if ret == True:
                count = count + 1
                
                resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
                cv2.imshow('Frame', resized)
                
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
                    # show the image
                    imshow('face detection', resized)

                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break
            

    vid.release()

    cv2.destroyAllWindows()
        
    
