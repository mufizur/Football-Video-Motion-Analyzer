import os
import cv2
import cv2.cv as cv
import math
import numpy as np
import numpy.linalg as la
 
os.chdir('C:/Users/Mufiz/Desktop/CS4243 Project/Football-Video-Motion-Analyzer/videoTracking')

VIDEO_TITLE_OUTPUT   = "video.avi"
VIDEO_HEIGHT = 600
VIDEO_WIDTH  = 4850

index = 0
term_crit = 0
roi_hist = 0
track_window = 0


bgFrameCap = cv2.VideoCapture('background.mp4')
frameCap   = cv2.VideoCapture('football_stitched.mp4')
_, frame   = frameCap.read()

# setup initial location of window
r,h,c,w = 475,120,4033, 100  # Refree linesman
#r,h,c,w = 225,60,3145, 50  # simply hardcoded the values
track_window = (c,r,w,h)
cv2.rectangle(frame, (c,r), (c+w,r+h), 255,2)
cv2.imwrite('img.png',frame)

# set up the ROI for tracking
roi = frame[r:r+h, c:c+w]
hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
videoOutput = cv2.VideoWriter()
videoOutput.open(VIDEO_TITLE_OUTPUT, cv.CV_FOURCC(*'XVID'), 23, (VIDEO_WIDTH, VIDEO_HEIGHT), True)

while(1):
	_, bgFrame = bgFrameCap.read()
	_, frame   = frameCap.read()
	hsv = cv2.cvtColor(bgFrame, cv2.COLOR_BGR2HSV)
	dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)

		
	_, track_window = cv2.meanShift(dst, track_window, term_crit)

	# Draw it on image
	x,y,w,h = track_window
	cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
	cv2.rectangle(bgFrame, (x,y), (x+w,y+h), 255,2)
	videoOutput.write(frame)
	#cv2.imwrite('img'+str(index)+'.png',frame)
	print index
	index = index + 1
	#break

videoOutput.release()