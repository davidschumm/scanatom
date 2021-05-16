import cv2
import numpy as np 

image=cv2.imread("test_img.jpg")
image=cv2.resize(image,(800,1000))
orig=image.copy()

gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
cv2.imshow("Title",gray)
cv2.waitKey(0)

blurred=cv2.GaussianBlur(gray,(5,5),0)
#first 2 is matrix muliplication. 3rd afrument is sigma. if not sure put 0
cv2.imshow("Blur",blurred)
cv2.waitKey(0)

edged=cv2.Canny(blurred,30,50)
cv2.imshow("Canny",edged)
cv2.waitKey(0)

