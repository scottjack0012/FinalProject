### example of face detection with opencv cascade classifier
##from cv2 import imread
##from cv2 import CascadeClassifier   
### load the photograph
##pixels = imread('test1.jpg')
### load the pre-trained model
##classifier = CascadeClassifier('haarcascade_frontalface_default.xml')
### perform face detection
##bboxes = classifier.detectMultiScale(pixels)
### print bounding box for each detected face
##for box in bboxes:
## print(box)



# plot photo with detected faces using opencv cascade classifier
import cv2
from cv2 import imread
from cv2 import imshow
from cv2 import waitKey
from cv2 import destroyAllWindows
from cv2 import CascadeClassifier
from cv2 import rectangle


def check_posy(cy):
##    print(cy)
    if cy > 370:
        print("Below drone level")
    elif cy < 75:
        print("Above drone level")
    


def check_posx(cx):
##    print(cx)
    if cx > 550:
        print("Turn Right")
    elif cx < 250:
        print("Turn Left")


if __name__ == '__main__':
    # load the photograph
    img = imread('mytest13.jpg')
    
    ##print(dimensions)
    ##print('Original Dimensions : ',img.shape)
    scale_percent = 20 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    print(width, height)
      
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
     
    ##print('Resized Dimensions : ',resized.shape)
     
    ##cv2.imshow("Resized image", resized)

    ##input("Press Enter to continue...")

    # load the pre-trained model
    classifier = CascadeClassifier('haarcascade_frontalface_default.xml')
    # perform face detection
    bboxes = classifier.detectMultiScale(resized)

    #Left box
    rectangle(resized, (0,0), (250,450), (0, 0, 255), 1)
    #Right box
    rectangle(resized, (550,0), (800,450), (0, 0, 255), 1)
    #Centre box
    rectangle(resized, (250,75), (550,370), (0, 255, 0), 1)

    # print bounding box for each detected face
    ####################################ONLY FOR ONE FACE ATM
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
     yPos = check_posy(cy)
     xPos = check_posx(cx)


    # show the image
    imshow('face detection', resized)
    # keep the window open until we press a key
    waitKey(0)
    # close the window
    destroyAllWindows()
