#results un satisfactory may want to switch to a hybrid canny + segmentation method or segmentation only method 
'''
updated pipeline ->
segmentation provides better results compared to canny edge detection 
load image
convert to hsv
apply segmentation for page ka color (mostly white and grey)
apply opening type morphology as image is big enough to not get removed while noise gets removed
draw contour and pick the largest one 
apply approximation on the contour
pick the 4 edges 
apply perspective transform 

'''

import numpy as np
import cv2
from pathlib import Path

#input the images 
input_folder_path = Path("C:\\Users\\HARSHIT\\Desktop\\Computer Vision and LIDAR\\P2_doc_scanner\\input_pages")

extensions = {".jpg",".png",".jpeg"}

image_paths = []
images = []

cv2.namedWindow("Scanner",cv2.WINDOW_NORMAL)

for file in input_folder_path.iterdir():
    if file.suffix.lower() in extensions:
        image_paths.append(str(file))

for path in image_paths:
    images.append(cv2.imread(path))

cv2.resizeWindow("Scanner", 600, 900)

print("Numeber of images :",len(images))

#filter the images with blurring and conversion to hsv
filtered =[] # converting to hsv and blurring 
target_width = 1000 
for image in images:
   image = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
   image = cv2.GaussianBlur(
        image,
        (7,7),
        0
      )
   #h,w = image.shape[:2]
   #aspect_ratio = w/h
   #target_height = int(target_width/aspect_ratio)
   #image = cv2.resize(image,(target_width,target_height))
   filtered.append(image)
print("converted images to gray and blurred them too !")

#apply segmentation to detect the paper
lower_hsv = (0,0,71)
upper_hsvc = (179,58,210) #got from  hsv tuner script and manually adjusting till get proper segmentation on the paper

raw_segment_masks = []

for img in filtered:
    mask = cv2.inRange(
        img,
        lower_hsv,
        upper_hsvc
    )
    raw_segment_masks.append(mask)

print("applied segmentation on the images!")

#apply morphology to remove noise 
morphed = []
kernel = cv2.getStructuringElement(
    cv2.MORPH_RECT,
    (7,7)
)
for mask in raw_segment_masks:
    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
    )
    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel
    )
    morphed.append(mask)

print("applied opening morphology")

#the paper will most likely be the largest contour so detect that 
contours = []
for mask in morphed:
    conts , _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_NONE
    )
    largest = max(conts,key=cv2.contourArea)
    contours.append(largest)

print("found all the largest contours! in each image ..most likely to be the paper!!")

#approximate the contour to a rectangle 
factor = 0.02
approximates = []
for i, contour in enumerate(contours):
    perim = cv2.arcLength(
        contour,
        True   
    )
    epsilon = perim*factor
    approx = cv2.approxPolyDP(
        contour,
        epsilon,
        True
    )
    if len(approx) ==4:
      approximates.append((i,approx))

print("approximation to rectangle ish done!!")

#apply perspective transform 
def order_points(points):

    ordered = np.zeros((4, 2), dtype=np.float32)

    s = points.sum(axis=1)
    diff = np.diff(points, axis=1)

    ordered[0] = points[np.argmin(s)]      # top-left
    ordered[2] = points[np.argmax(s)]      # bottom-right

    ordered[1] = points[np.argmin(diff)]   # top-right
    ordered[3] = points[np.argmax(diff)]   # bottom-left

    return ordered

def four_point_transform(image, points):

    rect = order_points(points)

    (tl, tr, br, bl) = rect

    width_top = np.linalg.norm(tr - tl)
    width_bottom = np.linalg.norm(br - bl)

    max_width = int(max(width_top, width_bottom))

    height_left = np.linalg.norm(bl - tl)
    height_right = np.linalg.norm(br - tr)

    max_height = int(max(height_left, height_right))

    dst = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]
    ], dtype=np.float32)

    matrix = cv2.getPerspectiveTransform(
        rect,
        dst
    )

    warped = cv2.warpPerspective(
        image,
        matrix,
        (max_width, max_height)
    )

    return warped

scanned_pages = []
destination_path = str("C:\\Users\\HARSHIT\\Desktop\\Computer Vision and LIDAR\\P2_doc_scanner\\output_pages\\o_page")
for i, approx in approximates:

    points = approx.reshape(4, 2).astype(np.float32)

    scanned = four_point_transform(
        images[i],
        points
    )

    scanned_pages.append(scanned)

    success = cv2.imwrite(
        f"{destination_path}{i}.jpeg",
        scanned
    )
    if(success):
        print(f"Saved image : {i}")

    '''cv2.imshow(
        f"Scanned {i}",
        scanned
    )
    cv2.imshow(f"original{i}",images[i])'''

cv2.waitKey(0)
cv2.destroyAllWindows()
# draw the rectangle over the page 
#store the image






'''
older pipeline -----


This is the first major project (second technicallly if u consider vegetation detector too) for the roadmap given in roadmap.md
The goal is to build a document scanner pipeline using opencv2
load input image(s)
detect the papaer
find outline
find corners
fix the perspective transform 
present the scanned document in output folder 

proposed preliminary pipeline is 
Photograph
   ↓
Grayscale
   ↓
Blur
   ↓
Canny
   ↓
Contour detection
   ↓
Find document contour
   ↓
approxPolyDP()
   ↓
4 corners
   ↓
Perspective transform
   ↓
Scanned document
'''
'''
import numpy as np
import cv2
from pathlib import Path

input_folder_path = Path("C:\\Users\\HARSHIT\\Desktop\\Computer Vision and LIDAR\\P2_doc_scanner\\input_pages")

extensions = {".jpg",".png",".jpeg"}

image_paths = []
images = []

cv2.namedWindow("Scanner",cv2.WINDOW_NORMAL)

for file in input_folder_path.iterdir():
    if file.suffix.lower() in extensions:
        image_paths.append(str(file))

for path in image_paths:
    images.append(cv2.imread(path))

cv2.resizeWindow("Scanner", 600, 900)

print("Numeber of images :",len(images))

filtered =[] # resized and grey and burred 
target_width = 1000 
for image in images:
   image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
   image = cv2.GaussianBlur(
        image,
        (7,7),
        0
      )
   #h,w = image.shape[:2]
   #aspect_ratio = w/h
   #target_height = int(target_width/aspect_ratio)
   #image = cv2.resize(image,(target_width,target_height))
   filtered.append(image)
print("converted images to gray and blurred them too !")

edges = []
sigma = 0.33

for img in filtered:
    pix_intensity = np.median(img)
    lower = int(max(0,(1.0-sigma)*pix_intensity))
    upper = int(min(255,(1.0+sigma)*pix_intensity))
    img = cv2.Canny(
        img,
        lower,
        upper
      )
    edges.append(img)

print("applied edge detection to all")

kernel = cv2.getStructuringElement(
    cv2.MORPH_RECT,
    (7,7)
)

morphs = []

for edge in edges:
    edge = cv2.morphologyEx(
        edge,
        cv2.MORPH_CLOSE,
        kernel
    )

    morphs.append(edge)

print("applied morphology!")
cv2.imshow("Scanner",morphs[6])
cv2.waitKey(0)
cv2.destroyAllWindows()

'''







