import cv2
import numpy as np

video = cv2.VideoCapture(0)

frameWidth = 640
frameHeight = 480
brightness = 150

video.set(3, frameWidth)
video.set(4, frameHeight)
video.set(10, brightness)

#any number of colours can be added to the list
#colour detection from the web-cam can be done by using the project- WebCam Colour Detector
myColors = [[123, 53, 83, 160, 158, 255],    #purple
            [53, 118, 69, 90, 255, 255],     #green
            [84, 77, 123, 127, 255, 255]]    #blue

myColorValues = [[204, 0, 204],
                 [76, 153, 0],
                 [153 ,0 ,0]]      #BGR

myPoints = []     #[x, y, colorID]

def findColor(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []                 # list of points with [[x, y, colorID],[],[],...etc]

    for color in myColors:
        lower = np.array(color[0:3])      #[h_min, s_min, v_min]
        upper = np.array(color[3:6])      #[h_max, s_max, v_max]
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)          # gives us the upper center tip of the contour
        cv2.circle(imgResult, (x, y), 5, myColorValues[count], cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x, y, count])
        count +=1
        #cv2.imshow(str(color[0]), mask)
    return newPoints

def getContours (img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            #cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2, y            # center of tip

def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 5, myColorValues[point[2]], cv2.FILLED)


while True:
    success, img = video.read()
    imgResult = img.copy()
    newPoints = findColor(img, myColors, myColorValues)

    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)

    if len(myPoints)!=0:
        drawOnCanvas(myPoints, myColorValues)

    cv2.imshow("Result", imgResult)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break