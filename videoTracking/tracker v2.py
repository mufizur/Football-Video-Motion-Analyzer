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
TOTAL_IMAGES = 7200

term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )


trackPoints = {
	"refree" : {
		"row" 	 : 475,
		"height" : 120,
		"column" : 4033,
		"width"  : 100
	},

	"RP1" : {
		"row" 	 : 225,
		"height" : 60,
		"column" : 3145,
		"width"  : 50
	}
}

def setUpMeanShift(points, frame):
	roi_hist_array = []

	for pointKey in points:
		dimension = points[pointKey]
		r, h, c, w = dimension['row'], dimension['height'], dimension['column'], dimension['width']
		track_window = (c, r, w, h)
		cv2.rectangle(frame, (c,r), (c+w,r+h), 255,2)

		roi = frame[r:r+h, c:c+w]
		hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
		roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
		cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
		roi_hist_array.append(roi_hist)

	return roi_hist_array

def meanShifter(roi_hist, bgFrame, frame):
	#_, bgFrame = bgFrameCap.read()
	#_, frame   = frameCap.read()
	hsv = cv2.cvtColor(bgFrame, cv2.COLOR_BGR2HSV)
	dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
	_, track_window = cv2.meanShift(dst, track_window, term_crit)

	# Draw it on image
	x,y,w,h = track_window
	cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
	cv2.rectangle(bgFrame, (x,y), (x+w,y+h), 255,2)

	return frame, newTrackWindow


def tracker():
	videoOutput = cv2.VideoWriter()
	videoOutput.open(VIDEO_TITLE_OUTPUT, cv.CV_FOURCC(*'XVID'), 23, (VIDEO_WIDTH, VIDEO_HEIGHT), True)
	videoOutput.release()

	bgFrameCap = cv2.VideoCapture('video.mp4')
	frameCap   = cv2.VideoCapture('football_stitched.mp4')
	videoFrameCount = int(bgFrameCap.get(cv.CV_CAP_PROP_FRAME_COUNT))
	roi_hist_array = setUpMeanShift(trackPoints, frameCap.read())

	for frameIndex in range(0, videoFrameCount):
		if frameIndex == TOTAL_IMAGES:
			break
		
		frame   = frameCap.read()
		bgFrame = bgFrameCap.read()

		pointIndex = 0
		for pointKey in trackPoints:
			roi_hist = roi_hist_array[pointIndex]
			frame, newTrackWindow = meanShifter(roi_hist, bgFrame, frame)

			pointIndex = pointIndex + 1
