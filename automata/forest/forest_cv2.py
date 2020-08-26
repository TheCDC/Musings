import cv2
import numpy as np
img = np.zeros([500,500,3])

img[:,:,0] = np.ones([500,500]) * 64 / 255.0
img[:,:,1] = np.ones([500,500]) * 128 / 255.0
img[:,:,2] = np.ones([500,500]) * 192 / 255.0

while True:
    img = np.random.random_sample(img.shape)
    cv2.imshow("image", img)
cv2.waitKey()