import numpy as np
import cv2

img = cv2.imread('media/line.jpeg')
type(img)
print(img.shape)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("gray", gray)
print(type(img))
print(gray.shape)
cv2.waitKey(0)
cv2.destroyAllWindows()