import numpy as np
import cv2

mask = np.zeros((400,600),dtype=np.uint8)
range =  np.random.default_rng()
mat = range.integers(low=0,high=2,size=(400,600))
mask = mask +mat

cv2.rectangle(
    mask,
    (50,50),
    (150,150),
    255,
    -1
)
cv2.rectangle(
    mask,
    (250,80),
    (350,180),
    255,
    -1
)
cv2.circle(
    mask,
    (500,500),
    250,
    255,
    -1
)

num_labels , labels = cv2.connectedComponents(mask)
print("labels :",num_labels)
print("foreground components",num_labels-1)
cv2.imshow("mask",mask)
cv2.waitKey(0)
cv2.destroyAllWindows()
