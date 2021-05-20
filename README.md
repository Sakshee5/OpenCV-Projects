# Overview of all files

## Image/ Webcam Color Detection
Detecting HSV color values in real time using Trackbars. Color Detection of a particular object from a static image and Webcam has been implemented seperately.

## Coin Detection and Counting
Takes in an image with scattered coins on a table. The aim is to identify the value of each coin and print the sum of all coins detected in the image. A bounding box is drawn around each detected coin with the value of coin printed beside it. The image (contains canadian coins) used is provided in the Images folder.

### Approach and concepts used
1. Coin Detection in the image is done using Contour Detection Techniques. 
2. The different types of coins are then segregated by calculating areas of the detected contours.
3. Since there is a lot of noise in the background of the original image, simply trying to detect contours by using edge detection techniques show poor results. 
   Thus color detection is used to mask the coins so as to seperate them from the noisy background. Contour Detection can be easily implemented on the masked image with high    efficiency and ease.   
4. The color values corresponding to masking of coins have been obtained by Image Color Detection.py

## Document Scannner Project
Scans document in real time using computer Webcam outputting the actual webcam footage, footage detecting the contours of the document to be scanned as well as the final cropped image of the scanned document. In absence of any document to be detected, the program simply outputs the original image.

### Concepts used
Simple image pre-processing techniques, Contour Detection, Warping, Image Stacking

## Invisibility Cloak Project
Harry Potter Fan? Definitely check this one out!!! By just using a few simple image processing techniques, I made my childhood fantasy come true and so can you:)

### Approach:
1. Capture and store the background frame for a couple seconds. (Drawback here is that this implementation only works with a static background:( )
2. Detect the color of the cloth you want to turn into as invisibility cloak using color detection. (Refer WebCam color Detection.py)
3. Segment out the cloth by generating a mask. 
4. Generate the final augmented output by replacing the cloth mask pixels by pixels of the background to create a magical effect. 

## Virtual Paint Project
Uses various techniques and basic functions in OpenCV such as importing WebCam video, color detection, contour detection etc. to build a live project wherein you can draw/paint virtually on your Webcam footage. You can draw using multiple pens/markers at the same time.

### Approach:
1. For this code implementation, get a marker pen with a unique cap color (the cap color should be different from the body of the marker)
2. This is so because we will detect the color of the marker cap using color detection techniques.
3. The cap will be segmented out using masking operations and contours will be detected. The topmost tip of the contour (marker cap) will be singled out so that we can use    OpenCV's cv2.circle (filled) function to draw lines with the same color as that of the marker wherever we drag the marker on the screen.
