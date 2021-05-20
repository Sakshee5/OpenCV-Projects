import cv2
import numpy as np

img = cv2.imread("C:/Users/Sakshee/Downloads/original image.jpg")
img = cv2.resize(img, (520, 480))
originalImg = img.copy()
imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

"""
Since there is a lot of noise in the background of original image, contour detection directly does not work. Thus we will create a mask of the coins using a color detector to seperate them from the background. Contour Detection on a masked image will be highly efficient and easy.
The values corresponding for masking of coins have been obtained by Image Color Detection.py
"""
lower = np.array([0, 36, 21])
upper = np.array([43, 157, 255])
mask = cv2.inRange(imgHSV, lower, upper)

contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
x, y, w, h = 0, 0, 0, 0

# so as eliminate unnecessary contours and make a list of coin contours
contour_list = []

for cnt in contours:
    peri = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.01*peri, True)
    area = cv2.contourArea(cnt)                                  # to eliminate very small areas

    if ((len(approx) > 8) & (area > 100)):
        contour_list.append(cnt)
        # print(cv2.contourArea(cnt))                             # printing to diffrentiate between areas of different coins later

# to count the number of coins of each class present in the image so as to able to count the total sum.
five = 0
ten = 0
twoFive = 0

for contour in contour_list:
    peri1 = cv2.arcLength(contour, True)
    approx1 = cv2.approxPolyDP(contour, 0.01 * peri1, True)
    area = cv2.contourArea(contour)
    x, y, w, h = cv2.boundingRect(approx1)

    # these exact number are derived after printing out the contour areas previously
    if area < 2000:
        ten = ten + 1
        cv2.putText(img, '10', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

    elif 2000 < area < 2500:
        five = five + 1
        cv2.putText(img, '5', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

    elif area > 2500:
        twoFive = twoFive + 1
        cv2.putText(img, '25', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

totalValue = 10*ten + 5*five + 25*twoFive
print(totalValue)

cv2.imshow('Coin Detection', img)
cv2.imshow('Original Image', originalImg)
cv2.waitKey(0)