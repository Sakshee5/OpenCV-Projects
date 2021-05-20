import cv2
import numpy as np

cap = cv2.VideoCapture(0)
background = 0

# we are using static background which we capture using a loop since the camera might take a few miliseconds to adjust
for i in range(30):
    _, background = cap.read()

# flipping depends on if your webcam / camera flips the original image. If it doesn't flipping is not required
# background = np.flip(background, axis=1)

while True:
    success, img = cap.read()
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # HSV values of the coloured cloak determined using  WebCam color detector.py
    h_min = 32
    h_max = 150
    s_min = 165
    s_max = 255
    v_min = 46
    v_max = 255

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    # Black and white mask. Cloak = white (255), Rest of the image = Black (0)
    mask = cv2.inRange(imgHSV, lower, upper)

    # removes small regions of false detection which will avoid random glitches in the final output.
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

    # replace the white region in the detected mask with the background pixels
    img[np.where(mask == 255)] = background[np.where(mask == 255)]

    cv2.imshow('Display', img)
    k = cv2.waitKey(10)
    if k == 27:
        break
