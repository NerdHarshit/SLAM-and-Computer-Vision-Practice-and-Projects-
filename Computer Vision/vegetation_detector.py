'''
objective - to detect the vegetation in 2 images using the help of color based segmentation + the contour methods to draw a proper outline on that
Image
 ↓
HSV
 ↓
Color mask
 ↓
Morphological cleanup
 ↓
Contours
 ↓
Largest reasonable contour
 ↓
Bounding box
'''

'''
as of 17-9-26 the code works well on nsc1 image but fails fully on other vegetation images we have meaning it is still not generalised ! fix that to make 
a general purpose pipeline !!
try explorng the use of connected components!!
'''

import numpy as np
import cv2

img_path  = "../input_images/grchpt.png" #image of a road with trees on the side 

image = cv2.imread(img_path)
print(image.shape)

hsv_img = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

lower_thresh = (0,108,0)#0 110 0
upper_thresh = (69,120,94)# 35 235 100
raw_mask = cv2.inRange(
    hsv_img,
    lower_thresh,
    upper_thresh
)

kernel = cv2.getStructuringElement(
    cv2.MORPH_ELLIPSE,
    (5, 5)
)

'''opening = cv2.morphologyEx( #expand -> shring white
    raw_mask,
    cv2.MORPH_OPEN,
    kernel
)'''

closing = cv2.morphologyEx( #shring -> expand white better for vegetation
    raw_mask,
    cv2.MORPH_CLOSE,
    kernel
)

clean_mask = cv2.morphologyEx(
    closing,
    cv2.MORPH_CLOSE,
    kernel
)

cv2.imshow("Raw", raw_mask)
#cv2.imshow("Opening", opening)
cv2.imshow("Closing", closing)
cv2.imshow("Clean", clean_mask)

contours ,_ = cv2.findContours(
    clean_mask,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

for cont in contours:
    area = cv2.contourArea(cont)
    if area > 1500: #raise area so as to exclude false positives
        x,y,w,h = cv2.boundingRect(cont)
        cv2.rectangle(
            image,
            (x,y),
            (x+w,y+h),
            (255,0,0),
            3
        )

#cv2.imshow("mask",mask)
cv2.imshow("detection",image)
cv2.waitKey(0)
cv2.destroyAllWindows()