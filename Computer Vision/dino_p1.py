import cv2
import numpy as np

image_path = "../input_images/dino.jpeg"

def autoThresh(arr, sigma=0.33):
    median_val = np.median(arr)
    lowerThresh = int(max(0, (1.0 - sigma) * median_val))
    upperThresh = int(min(255, (1.0 + sigma) * median_val))
    return lowerThresh, upperThresh

image = cv2.imread(image_path)
smaller = cv2.resize(image, (1008, 1526)) 
output_img = smaller.copy()

gray = cv2.cvtColor(smaller, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 1)

thl, thu = autoThresh(blur)
edges = cv2.Canny(blur, threshold1=thl, threshold2=thu)

# Connect edge gaps
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
dilated_edges = cv2.dilate(edges, kernel, iterations=2)

contours, _ = cv2.findContours(
    dilated_edges,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

# FIX 1: Filter out the table edge at the very bottom (e.g. y > 1100)
dino_contours = []
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    # Ignore small noise AND ignore huge contours touching the very bottom edge
    if cv2.contourArea(c) > 200 and y < 1000:
        dino_contours.append(c)

if dino_contours:
    # Get the largest contour excluding the table bottom
    largest_dino_contour = max(dino_contours, key=cv2.contourArea)

    # Draw all contours in purple
    cv2.drawContours(output_img, dino_contours, -1, (160, 32, 240), 2)

    # Calculate and draw bounding box for dinosaur
    x, y, w, h = cv2.boundingRect(largest_dino_contour)
    cv2.rectangle(output_img, (x, y), (x + w, y + h), (0, 255, 0), 3)

    print(f"Dinosaur Bounding Box at: x={x}, y={y}, w={w}, h={h}")

# FIX 2: Make the window resizable so it fits on your screen
cv2.namedWindow("Dinosaur Bounding Box", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Dinosaur Bounding Box", 600, 900)  # Scale window to fit screen

cv2.imshow("Dinosaur Binosaur", output_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
#this isnt the final outcome code pls do it on your own again to get the bounding box around the dino latr on your own as a practice
