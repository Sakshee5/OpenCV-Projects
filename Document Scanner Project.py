import cv2
import numpy as np

video = cv2.VideoCapture(0)

widthImg = 640
heightImg = 480
brightness = 150

video.set(3, widthImg)
video.set(4, heightImg)
video.set(10, brightness)

"""
Erosion:
It is useful for removing small white noises. Used to detach two connected objects etc.

Dilation:
In cases like noise removal, erosion is followed by dilation. Because, erosion removes white noises, but it also shrinks our object.
So we dilate it. Since noise is gone, they won’t come back, but our object area increases. It is also useful in joining broken parts of an object.
"""

def preProcessing(img):
    """
    Image preprocessing function to detect edges accurately. Edge detection is important here since we aim to scan documents.
    """
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5,5), 1)
    imgCanny = cv2.Canny(imgBlur,200,200)

    kernel = np.ones((5,5))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=2)
    imgThres = cv2.erode(imgDial, kernel, iterations=1)

    return imgThres

def getContours (img):
    biggest = np.array([])
    maxArea = 0                            # assuming that the document to be scanned is the largest contour
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        if area>5000:
            #cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            if area > maxArea and len(approx) == 4:          #assuming that the document is a rectangle (has 4 corners)
                biggest = approx
                maxArea = area
    cv2.drawContours(imgContour, biggest, -1, (255, 0, 0), 3)
    return biggest


def reorder (myPoints):
    """
    The biggest array returned by the contour function will be all jumbled up but we want a certain order of the points so as to feed it to
    pts2 in the getWarp function.
    """
    myPoints = myPoints.reshape((4, 2))                 # since we find an array of (4,1,2) wherein the 1 value is redundant
    myPointsNew = np.zeros((4, 1, 2), np.int32)
    add = myPoints.sum(1)
    #print("add", add)
    myPointsNew[0] = myPoints[np.argmin(add)]            # since the lowest sum will be closest to origin
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1]= myPoints[np.argmin(diff)]            # the point with positive difference (x-y) is the second point
    myPointsNew[2] = myPoints[np.argmax(diff)]
    #print("NewPoints",myPointsNew)
    return myPointsNew


def getWarp(img, biggest):

    biggest = reorder(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

    imgCropped = imgOutput[20:imgOutput.shape[0]-20, 20:imgOutput.shape[1]-20]
    imgCropped = cv2.resize(imgCropped, (widthImg, heightImg))

    return imgOutput

def stackImages (scale, imgArray):
     """
    Function to stack images togther in the form of an array so that only one output window contains all the results
    ARGUMENTS:
    imgArray - example [[img1, img2, ...imgn],[img1, img2, ...imgn], ...]
    scale - to scale the output window
    labels - label for each image to be displayed in the same format as imgArray
    RETURNS: stacked image
    """
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

while True:
    success, img = video.read()
    cv2.resize(img, (widthImg, heightImg))
    imgContour = img.copy()

    imgThres = preProcessing(img)
    biggest = getContours(imgThres)
    print(biggest)

    if biggest.size !=0:
        imgWarp = getWarp(img, biggest)

        imgArray = ([img, imgThres],
                    [imgContour, imgWarp])
    else:                                    # if a relevant contour isn't found
        imgArray = ([img, imgThres],
                    [img, img])

    stackedImages = stackImages(0.6, imgArray)

    cv2.imshow("Result", stackedImages)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break