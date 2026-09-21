'''
goal is to extract the road from the image..so first actually assume that road is in the lower half of the image so crop out the upper part
then apply segmentation on the cropped image that makes the road as the largest contour. get the largest contour and then use 2 new methods
cv2.fillPoly()
use this to properly fill the area of the road incase it wasnt properly filled . to do so get the 4 corners of the largest contour 4 or more points
this will get a clean and fully filled mask

cv2.bitwise_and() use this over the original cropped image and the mask to separate out only the road from the cropped part in the image 
'''

import cv2
import numpy as np

image_path = "C:\\Users\\HARSHIT\\Desktop\\Computer Vision and LIDAR\\Lane_detector\\input_roads\\city1.jpg"

image = cv2.imread(image_path)
print(image.shape)

#assumed that road in lower half of the image so crop out from image midpoint
ratio = 0.5 # to determine how much of image to crop..for now im assumig road only in the lower half of the image..can later change to 1/3 or 1/4 etc
h_mid = int(image.shape[0] * ratio )
print(h_mid)

roi_h = image.shape[0] - h_mid

roi_image = image[roi_h:,:,:]
print(roi_image.shape)

hsvImg = cv2.cvtColor(roi_image,cv2.COLOR_BGR2HSV)

lower_limit = (96,26,80)
upper_limit = (109,163,198)
mask = cv2.inRange(
    hsvImg,
    lower_limit,
    upper_limit
)

kernel = cv2.getStructuringElement(
    cv2.MORPH_RECT,
    (5,5)
)

mask = cv2.morphologyEx(
    mask,
    cv2.MORPH_OPEN,
    kernel
)

mask = cv2.morphologyEx(
    mask,
    cv2.MORPH_OPEN,
    kernel
)

#got a somewhat clean mask of the road now lets make the road as the largest contour
contours ,_ = cv2.findContours(
    mask,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_NONE
)

largest_contour = max(contours,key=cv2.contourArea)
print("len of largest contour" ,len( largest_contour))

cv2.drawContours(
    roi_image,
    largest_contour,
    -1,
    (0,255,0),
    2
)
#great results till here btw

x,y,w,h = cv2.boundingRect(largest_contour)
#print(x,y,w,h)
cv2.rectangle(
    roi_image,
    (x,y),
    (x+w,y+h),
    (255,0,0),
    2
)
factor = 0.005
approx_pts = cv2.approxPolyDP(
    largest_contour,
    epsilon= cv2.arcLength(largest_contour,True)*factor,
    closed=True
)
print("len after approximation",len(approx_pts))

#gives almost same result as without fill poly. thus make fill poly on a blank image !
blank_img = np.zeros((roi_image.shape[0],roi_image.shape[1]),dtype=np.uint8)

cv2.fillPoly(blank_img,[largest_contour],255)
#this now has the proper road area only as the white region and rest all black 

roi_img_cpy = cv2.cvtColor(roi_image.copy(),cv2.COLOR_BGR2GRAY)

result = cv2.bitwise_and(roi_img_cpy,roi_img_cpy,mask=blank_img)

cv2.imshow("image",roi_image)
cv2.imshow("mmask",mask)
cv2.imshow("polyfill",blank_img)
cv2.imshow("result",result)
cv2.waitKey(0)
cv2.destroyAllWindows()

