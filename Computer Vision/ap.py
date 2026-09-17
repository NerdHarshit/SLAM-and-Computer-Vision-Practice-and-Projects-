import cv2
import numpy as np

img = np.zeros((500, 500), dtype=np.uint8)

# rectangle
cv2.rectangle(
    img,
    (100, 100),
    (400, 350),
    255,
    -1
)

contours, _ = cv2.findContours(
    img,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_NONE
)

contour = contours[0]

perimeter = cv2.arcLength(
    contour,
    True
)

for factor in [0.001, 0.01, 0.05, 0.1]:

    epsilon = factor * perimeter

    approx = cv2.approxPolyDP(
        contour,
        epsilon,
        True
    )

    print(
        "epsilon:",
        factor,
        "points:",
        len(approx)
    )