import cv2
import os
import numpy as np
import mapper 

def scanit(imgfile):

	image=cv2.imread(imgfile)
	image=cv2.resize(image,(900,1100))
	orig=image.copy()

	gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	#cv2.imshow("Title",gray)
	#cv2.waitKey(0)

	blurred=cv2.GaussianBlur(gray,(5,5),0)
	#first 2 is matrix muliplication. 3rd afrument is sigma. if not sure put 0
	#cv2.imshow("Blur",blurred)
	#cv2.waitKey(0)

	edged=cv2.Canny(blurred,30,50)
	#cv2.imshow("Canny",edged)
	#cv2.waitKey(0)

	contours,hierarchy = cv2.findContours(edged,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	contours=sorted(contours,key=cv2.contourArea,reverse=True)

	for c in contours:
		p=cv2.arcLength(c,True)
		approx=cv2.approxPolyDP(c,0.02*p,True)

		if len(approx)==4:
			target=approx
			break
	approx=mapper.mapp(target)

	pts = np.float32([[0,0],[900,0],[900,900],[0,900]])
	#faceCascade = cv2.CascadeClassifier( os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml") )
	op=cv2.getPerspectiveTransform(approx,pts)
	dst=cv2.warpPerspective(orig,op,(900,900))

	#cv2.imshow("Scanned",dst)
	#cv2.waitKey(0)
	return cv2.imshow("Scanned",dst), cv2.waitKey(0)

