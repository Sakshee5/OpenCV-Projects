import cv2
import numpy as np


def empty(a):
    pass


# trackbars help us to play around with color values in real-time

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)
cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)
cv2.createTrackbar("Hue Max", "TrackBars", 179, 179, empty)
cv2.createTrackbar("Sat Min", "TrackBars", 0, 255, empty)
cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
cv2.createTrackbar("Val Min", "TrackBars", 0, 255, empty)
cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

# cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)
# cv2.createTrackbar("Hue Max", "TrackBars", 43, 179, empty)
# cv2.createTrackbar("Sat Min", "TrackBars", 36, 255, empty)
# cv2.createTrackbar("Sat Max", "TrackBars", 157, 255, empty)
# cv2.createTrackbar("Val Min", "TrackBars", 21, 255, empty)
# cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

# minimum and maximum ranges have been determined after creating the mask and manipulating values in real time

while True:
    img = cv2.imread("C:/Users/Sakshee/Downloads/original image.jpg")
    img = cv2.resize(img, (520, 480))
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")

    print(h_min, h_max, s_min, s_max, v_min, v_max)

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHSV, lower, upper)  # creating mask for a particular colour on the HSV Image

    imgResult = cv2.bitwise_and(img, img, mask=mask)  # new image is just the original image with mask applied
    # adds images, basically checking both the images and wherever pixels in both images are present it takes that as a yes and stores that
    # in new image

    cv2.imshow("Original", img)
    cv2.imshow("HSV", imgHSV)
    cv2.imshow("mask",
               mask)  # we can change the trackbar values to get the mask of the colour we need (mask is black and white)
    cv2.imshow("Result", imgResult)
    # this will be same as the mask but additionally have the colour from the actual image instead of white as in the mask

    cv2.waitKey(1)
