import cv2

image_path ="../input_images/saturn.png" # "../input_images/saturn.png"

image = cv2.imread(image_path)
#print("IMage shape",image.shape)

#cv2.imshow("Imgae show ho jayega",image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

#img_crp = image[0:1000,0:1000]
#img_grey = cv2.cvtColor(img_crp,cv2.COLOR_BGR2GRAY)

#img_shrinked = cv2.resize(cv2.cvtColor(image,cv2.COLOR_BGR2GRAY),(1920,1080))
#cv2.imshow("cropped 0->1000px for both xy",img_shrinked)

#img_blurred = cv2.GaussianBlur(cv2.resize(image,(1920,1080)),(7,7),0)
'''edges = cv2.Canny(cv2.resize(image,(1920,1080)),
                  threshold1=100,
                  threshold2=200,
                  apertureSize=3,
                  L2gradient=False)

contours , hirerchy  = cv2.findContours(
    edges,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)
print("no of contours(closed loops) ",len(contours))
output = image.copy()

cv2.drawContours(
    output,
    contours,
    -1,
    (0, 255, 0),
    2
)


grey = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(grey,50,255,cv2.THRESH_BINARY)
_, threshinv = cv2.threshold(grey,50,255,cv2.THRESH_BINARY_INV)
_, otsuthresh = cv2.threshold(grey,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

adapthresh = cv2.adaptiveThreshold(grey,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

cv2.imshow("thresh", thresh)
cv2.imshow("thresh inv", threshinv)
cv2.imshow("otsu",otsuthresh)
cv2.imshow("adaptive",adapthresh)'''

hsvimg = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
lower_thresh = (35, 80, 50)
upper_thresh = (85, 255, 255)

mask = cv2.inRange(hsvimg,lower_thresh,upper_thresh)

cv2.imshow("original",image)
cv2.imshow("masked",mask)
cv2.waitKey(0)
cv2.destroyAllWindows()