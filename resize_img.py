import cv2 as cv

img = cv.imread('walmart.jpg')


def rescaleFrame(frame, scale=0.2):
	width = int(frame.shape[1] * scale)
	height = int(frame.shape[0] * scale)

	dimensions = (width, height)

	return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

img_resized = rescaleFrame(img)

cv.imshow("Img resized", img_resized)
cv.waitKey(0)