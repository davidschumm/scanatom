import cv2 as cv
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

img = cv.imread('walmart.jpg')

cv.imshow("Img ", img)
cv.waitKey(0)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

ret, thresh1 = cv.threshold(gray, 0, 255, cv.THRESH_OTSU | cv.THRESH_BINARY_INV)


# Specify structure shape and kernel size. 
# Kernel size increases or decreases the area 
# of the rectangle to be detected.
# A smaller value like (10, 10) will detect 
# each word instead of a sentence.
rect_kernel = cv.getStructuringElement(cv.MORPH_RECT, (10, 10))

dilation = cv.dilate(thresh1, rect_kernel, iterations = 1)

contours, hierarchy = cv.findContours(dilation, cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)

im2 = img.copy()

file = open("recognized.txt", "w+")
file.write("")
file.close()

for cnt in contours:
    x, y, w, h = cv.boundingRect(cnt)

    rect = cv.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cropped = im2[y:y + h, x:x + w]

    file = open("recognized.txt", "a")

    text = pytesseract.image_to_string(cropped)

    file.write(text)
    file.write("\n")
    file.close
