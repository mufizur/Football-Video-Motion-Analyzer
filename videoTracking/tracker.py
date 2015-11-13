import os
import cv2
import cv2.cv as cv
import math
import numpy as np
import numpy.linalg as la
import copy 
import json

os.chdir('C:/Users/Mufiz/Desktop/CS4243 Project/Football-Video-Motion-Analyzer/videoTracking')

VIDEO_TITLE_OUTPUT  = "video.avi"
VIDEO_HEIGHT 		= 600
VIDEO_WIDTH  		= 4850

#playerTracking points

FRAMEPOINTS = []

topHomography = [[  3.70795420e+01,   1.57907552e+02,  -8.32616546e+04],
				 [  1.64879407e+00,   2.61746691e+02,  -3.17123425e+04],
				 [  5.15248147e-04,   6.36123293e-02,   1.00000000e+00]]

def getProjectedPoints(point):
	prevX = point[0][0]
	prevY = point[0][1]

	newX = (topHomography[0][0]*prevX +  topHomography[0][1]*prevY + topHomography[0][2]) / (topHomography[2][0]*prevX +  topHomography[2][1]*prevY + topHomography[2][2])
	newY = (topHomography[1][0]*prevX +  topHomography[1][1]*prevY + topHomography[1][2]) / (topHomography[2][0]*prevX +  topHomography[2][1]*prevY + topHomography[2][2])
	return (newX, newY)


PLAYER_POINTS = {
	"RED"  : { # Red team
		"1"  : (3160, 240),
		"2"  : (2840, 140),
		"3"  : (2800, 160),
		"4"  : (2675, 155),
		"5"  : (2715, 185),
		"6"  : (2745, 275),
		"7"  : (2540, 130),
		"8"  : (2475, 180),
		"9"  : (1960, 195)  #Keeper
	}, 

	"BLUE"  : { # Blue team
		"1"  : (3145, 220),
		"2"  : (3010, 190),
		"3"  : (2950, 170),
		"4"  : (2875, 175),
		"5"  : (2875, 145),
		"6"  : (2845, 160),
		"7"  : (2755, 145),
		"8"  : (2695, 220),
		"9"  : (2505, 195),
		"10" : (2810, 165),
		"11" : (3270, 190)  #Keeper
	}, 

	"REFREE"  : (2748, 172),
	"LINESMEN": (4095, 525),
}

def getListPoints(points):
	newPoints = {
		"RED"  : { # Red team
			"1"  : getProjectedPoints(points[2].tolist()),
			"2"  : getProjectedPoints(points[3].tolist()),
			"3"  : getProjectedPoints(points[4].tolist()),
			"4"  : getProjectedPoints(points[5].tolist()),
			"5"  : getProjectedPoints(points[6].tolist()),
			"6"  : getProjectedPoints(points[7].tolist()),
			"7"  : getProjectedPoints(points[8].tolist()),
			"8"  : getProjectedPoints(points[9].tolist()),
			"9"  : getProjectedPoints(points[10].tolist())
		}, 

		"BLUE"  : { # Blue team
			"1"  : getProjectedPoints(points[11].tolist()),
			"2"  : getProjectedPoints(points[12].tolist()),
			"3"  : getProjectedPoints(points[13].tolist()),
			"4"  : getProjectedPoints(points[14].tolist()),
			"5"  : getProjectedPoints(points[15].tolist()),
			"6"  : getProjectedPoints(points[16].tolist()),
			"7"  : getProjectedPoints(points[17].tolist()),
			"8"  : getProjectedPoints(points[18].tolist()),
			"9"  : getProjectedPoints(points[19].tolist()),
			"10" : getProjectedPoints(points[20].tolist()),
			"11" : getProjectedPoints(points[21].tolist())
		}, 

		"REFREE"  : getProjectedPoints(points[1].tolist()),
		"LINESMEN": getProjectedPoints(points[0].tolist()),
	}

	return newPoints


def setInitialPreVect(points, prevVect):
	prevVect[0] = points["LINESMEN"] # Linesmen 
	prevVect[1] = points["REFREE"]   # refree

	prevVect[2]   = points["RED"]["1"]  # Red Player 1
	prevVect[3]   = points["RED"]["2"]  # Red Player 2
	prevVect[4]   = points["RED"]["3"]  # Red Player 3
	prevVect[5]   = points["RED"]["4"]  # Red Player 4
	prevVect[6]   = points["RED"]["5"]  # Red Player 5
	prevVect[7]   = points["RED"]["6"]  # Red Player 6
	prevVect[8]   = points["RED"]["7"]  # Red Player 7
	prevVect[9]   = points["RED"]["8"]  # Red Player 8
	prevVect[10]  = points["RED"]["9"]  # Red Player 9 [Keeper]

	prevVect[11]  = points["BLUE"]["1"]  # Blue Player 1
	prevVect[12]  = points["BLUE"]["2"]  # Blue Player 2
	prevVect[13]  = points["BLUE"]["3"]  # Blue Player 3
	prevVect[14]  = points["BLUE"]["4"]  # Blue Player 4
	prevVect[15]  = points["BLUE"]["5"]  # Blue Player 5
	prevVect[16]  = points["BLUE"]["6"]  # Blue Player 6
	prevVect[17]  = points["BLUE"]["7"]  # Blue Player 7
	prevVect[18]  = points["BLUE"]["8"]  # Blue Player 8
	prevVect[19]  = points["BLUE"]["9"]  # Blue Player 9 
	prevVect[20]  = points["BLUE"]["10"] # Blue Player 10 
	prevVect[21]  = points["BLUE"]["11"] # Blue Player 11 [Keeper]

	return prevVect

def getTopPoint(linesmenPt):
	topMaximum = 3000
	topMinimum = 1850
	topMiddle  = 2400

	bottomMaximum = 4800
	bottomMinimum = 200
	bottomMiddle  = 2500

	topRange    = topMaximum - topMinimum
	bottomRange = bottomMaximum - bottomMinimum
	ratioRange  = 8#bottomRange / topRange

	bottomX = int(linesmenPt[0])
	bottomY = int(linesmenPt[1])

	topX    = topMiddle
	topY    = 120

	if bottomX <= bottomMiddle:
		topX = topMiddle - (bottomX / ratioRange)
		if topX < topMinimum:
			topX = topMinimum
	else:
		topX = topMiddle + (bottomX / ratioRange)
		if topX > topMaximum:
			topX = topMaximum

	return (topX, topY)

	

def projectOffside(linesmenPt, frame):
	topPoint = getTopPoint(linesmenPt)
	cv2.line(frame, (int(linesmenPt[0]), int(linesmenPt[1])), topPoint, (255,255,255))
	#cv2.line(frame, (1850,120), (2400,120), (255,255,255))
	#cv2.line(frame, (200,500), (2500,500), (255,255,255))
	return frame


#def errorCorrection(prevVect, nextVect):

if __name__ == "__main__":
	#f = open('points.txt', 'w')
	camera  = cv2.VideoCapture("background.mp4")
	camera2 = cv2.VideoCapture("football_stitched.mp4") 

	#get the previous image from which the good features are taken
	prevImg = camera.read()[1]
	prevImg = cv2.cvtColor(prevImg,cv2.cv.CV_RGB2GRAY)

	#get the previous good features
	prevVect1   = cv2.goodFeaturesToTrack(prevImg, 50, 0.001, 100)
	prevVect    = prevVect1[0:22]
	prevVect    = setInitialPreVect(PLAYER_POINTS, prevVect)

	videoOutput = cv2.VideoWriter()
	codec = cv.CV_FOURCC('M', 'P', '4', '2')
	videoOutput.open(VIDEO_TITLE_OUTPUT, codec, 23, (VIDEO_WIDTH, VIDEO_HEIGHT), True)
	frameIndex = 0

	while True:
	#while False:
		original = camera.read()[1]
		frame    = camera2.read()[1]

		nextImg = cv2.cvtColor(original,cv2.cv.CV_RGB2GRAY)
		nextVect = np.copy(prevVect)
		nextVect , status , err = cv2.calcOpticalFlowPyrLK(prevImg,nextImg,prevVect,nextVect)
		print "--START FOR INDEX : "+str(frameIndex)+"--"

		for i in range(prevVect.shape[0]):
			p1 = (int(prevVect[i][0][0]),int(prevVect[i][0][1]))
			if i == 0 or i == 1: #Yellow reffree
				cv2.circle(frame, p1 ,10 , (0,255,255), 10)
			
			elif i >= 2 and i <= 10: #Red Team 
				cv2.circle(frame, p1 ,10 , (0,0,255), 10)

			elif i >= 11 and i <= 21: #Blue Team 
				cv2.circle(frame, p1 ,10 , (255,255,255), 10)

		listPts = getListPoints(prevVect)
		FRAMEPOINTS.append(listPts)
		prevImg = nextImg.copy()
		#nextVect = errorCorrection(prevVect, nextVect)
		prevVect = nextVect
		frame = projectOffside(prevVect[0][0], frame)
		videoOutput.write(frame)
		frameIndex = frameIndex + 1

		if (frameIndex % 50) == 0:
			cv2.imwrite('image'+str(frameIndex)+'.png', frame)

		#cv2.imwrite('image'+str(frameIndex)+'.png', frame)
		if frameIndex == 220:
			break
		#break
	
	#f.write(json.dumps(FRAMEPOINTS))
	#f.close()
	#print len(FRAMEPOINTS)
	videoOutput.release()
