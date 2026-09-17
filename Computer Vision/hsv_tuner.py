import cv2

image = cv2.imread("../input_images/nsc1.png")

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

cv2.namedWindow("Trackbars")
#cv2.namedWindow("Original")


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

    cv2.imshow("Original", image)
    cv2.imshow("Mask", mask)

    cv2.setMouseCallback(
    "Trackbars",
    mouse_callback
)
    
    key = cv2.waitKey(1)

    if key == ord("q"):
        print("Lower:", lower)
        print("Upper:", upper)
        break

cv2.destroyAllWindows()