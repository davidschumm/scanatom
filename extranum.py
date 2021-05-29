import cv2 as cv
import pytesseract
from PIL import Image
import PIL.Image

from pytesseract import image_to_string

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

img = cv.imread('walmart.jpg')



def rescaleFrame(frame, scale=0.2):
	width = int(frame.shape[1] * scale)
	height = int(frame.shape[0] * scale)

	dimensions = (width, height)

	return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

img_resized = rescaleFrame(img)

cv.imshow("output ", img_resized)
cv.imwrite('Output Image.PNG', img_resized)
cv.waitKey(0)


output = pytesseract.image_to_string(PIL.Image.open('Output Image.PNG').convert("RGB"), lang='eng')
print(output)

ret, thresh = cv.threshold(img, 10, 255, cv.THRESH_OTSU)
print ("Threshold selected : ", ret)
cv.imwrite("./output_image.png", thresh)