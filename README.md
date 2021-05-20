# Overview of all files

## Image/ Webcam Color Detection
Detecting HSV color values in real time using Trackbars. Color Detection of a particular object from a static image and Webcam has been implemented seperately.

## Coin Detection and Counting
Takes in an image with scattered coins on a table. The aim is to identify the value of each coin and print the sum of all coins detected in the image. A bounding box is drawn around each detected coin with the value of coin printed beside it. The image (contains canadian coins) used is provided in the Images folder.

### Approach and concepts used
1. Coin Detection using Contours and segregation using contour area.
2. Since there is a lot of noise in the background of original image, even after edge detection image processing techniques, contour detection directly shows poor results. 
   Thus color detection is used to mask the coins so as to seperate them from the noisy background. Contour Detection can be implemented on the masked image and will be highly    efficient and easy.
3. The color values corresponding to masking of coins have been obtained by Image Color Detection.py

### Document Scannner Project
Scans document in real time using computer Webcam outputting the actual webcam footage, footage detecting the contours of the document to be scanned as well as the final cropped image of the scanned document. In absence of any document to be detected, the program simply outputs the original image.

### Concepts used
Simple image pre-processing techniques, Contour Detection, Warping, Image Stacking

### Invisibility Cloak Project
Harry Potter Fan? Check it out!!! By just using a few simple image processing techniques, I made my childhood fantasy come true and so can you:)

Approach:
1. Capture and store the background frame for a couple seconds. (Drawback here is that this implementation only works with a static background:( )
2. Detect the color of the cloth you want to turn into as invisibility cloak using color detection. (Refer WebCam color Detection.py)
3. Segment out the cloth by generating a mask. 
4. Generate the final augmented output by replacing the cloth mask pixels by pixels of the background to create a magical effect. 

### Virtual Paint Project
Uses various techniques and basic functions in OpenCV such as importing WebCam video, color detection, contour detection etc. to build a live project wherein you can draw/paint virtually on your Webcam footage.
