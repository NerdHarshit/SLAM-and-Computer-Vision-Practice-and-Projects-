'''import cv2

image = cv2.imread("../P2_doc_scanner\\input_pages\\page6.jpeg")

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

cv2.namedWindow("Trackbars")

cv2.resizeWindow("images", 600, 900)

def nothing(x):
    pass

def mouse_callback(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:

        pixel = hsv[y, x]

        print(
            f"HSV at ({x},{y}): {pixel}"
        )

# H
cv2.createTrackbar("H Min", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("H Max", "Trackbars", 179, 179, nothing)

# S
cv2.createTrackbar("S Min", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("S Max", "Trackbars", 255, 255, nothing)

# V
cv2.createTrackbar("V Min", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("V Max", "Trackbars", 255, 255, nothing)


while True:

    h_min = cv2.getTrackbarPos("H Min", "Trackbars")
    h_max = cv2.getTrackbarPos("H Max", "Trackbars")

    s_min = cv2.getTrackbarPos("S Min", "Trackbars")
    s_max = cv2.getTrackbarPos("S Max", "Trackbars")

    v_min = cv2.getTrackbarPos("V Min", "Trackbars")
    v_max = cv2.getTrackbarPos("V Max", "Trackbars")

    lower = (h_min, s_min, v_min)
    upper = (h_max, s_max, v_max)

    mask = cv2.inRange(
        hsv,
        lower,
        upper
    )
    cv2.imshow("images", image)
    cv2.imshow("images", mask)

    cv2.setMouseCallback(
    "Trackbars",
    mouse_callback
)
    
    key = cv2.waitKey(1)

    if key == ord("q"):
        print("Lower:", lower)
        print("Upper:", upper)
        break

cv2.destroyAllWindows()'''

import numpy as np
import cv2

# Load image
image = cv2.imread("../P2_doc_scanner/input_pages/page6.jpeg")

if image is None:
    print("Error: Could not load image. Check the file path.")
    exit()

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# cv2.WINDOW_NORMAL allows manual resizing with the mouse
cv2.namedWindow("Original Image", cv2.WINDOW_NORMAL)
cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)
cv2.namedWindow("Trackbars", cv2.WINDOW_NORMAL)

# Set default window dimensions (user can still resize manually)
cv2.resizeWindow("Original Image", 600, 900)
cv2.resizeWindow("Mask", 600, 900)
cv2.resizeWindow("Trackbars", 400, 300)


def nothing(x):
    pass


def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if y < hsv.shape[0] and x < hsv.shape[1]:
            pixel = hsv[y, x]
            print(f"HSV at ({x},{y}): {pixel}")


# Set mouse callback on the Original Image window once
cv2.setMouseCallback("Original Image", mouse_callback)

# H
cv2.createTrackbar("H Min", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("H Max", "Trackbars", 179, 179, nothing)

# S
cv2.createTrackbar("S Min", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("S Max", "Trackbars", 255, 255, nothing)

# V
cv2.createTrackbar("V Min", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("V Max", "Trackbars", 255, 255, nothing)

while True:
    h_min = cv2.getTrackbarPos("H Min", "Trackbars")
    h_max = cv2.getTrackbarPos("H Max", "Trackbars")

    s_min = cv2.getTrackbarPos("S Min", "Trackbars")
    s_max = cv2.getTrackbarPos("S Max", "Trackbars")

    v_min = cv2.getTrackbarPos("V Min", "Trackbars")
    v_max = cv2.getTrackbarPos("V Max", "Trackbars")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    mask = cv2.inRange(hsv, lower, upper)

    cv2.imshow("Original Image", image)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(1)
    if key == ord("q"):
        print("Lower:", lower)
        print("Upper:", upper)
        break

cv2.destroyAllWindows()