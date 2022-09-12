import numpy as np
import cv2

img=cv2.imread("IITRopar_Kasif_Ansari_15453556745.jpg") 
l,h,c=img.shape
# img.reshape(int(l/4),int(h/4),c)
img =cv2.resize(img, dsize=(int(l/4),int(h/4)))
margin = 50
depth=np.average(img[210:270, 280:360])
cv2.imshow("a",img[210:27000, 280:36000])
cv2.waitKey(0)
# print(img)
mask = cv2.inRange(img, (depth-margin, depth-margin, depth-margin), (depth+margin, depth+margin, depth+margin))
cv2.imshow("b",mask)
cv2.waitKey(0)
kernel = np.ones((3, 3), np.uint8)
mask = cv2.erode(mask, kernel, iterations=5)
contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.imshow("c",mask)
cv2.waitKey(0)
mask = np.zeros(img.shape, np.uint8)
cv2.drawContours(mask, [contours[0]], -1, 255, -1) 
cv2.imshow("d",mask)
cv2.waitKey(0)
img=cv2.mean(img,mask=mask)
cv2.imshow("e",img)
cv2.waitKey(0)