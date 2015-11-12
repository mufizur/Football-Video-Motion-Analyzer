import os
import cv2
import cv2.cv as cv
import math
import numpy as np
import numpy.linalg as la
import copy 

os.chdir('C:/Users/Mufiz/Desktop/CS4243 Project/Football-Video-Motion-Analyzer/videoTracking')

VIDEO_TITLE_OUTPUT  = "video.avi"
VIDEO_HEIGHT 		= 600
VIDEO_WIDTH  		= 4850

#playerTracking points
PLAYER_POINTS = {
	"TEAM1"  : { # Blue team
		"1"  : (100, 100),
		"2"  : (200, 200),
		"3"  : (300, 300),
		"4"  : (400, 400),
		"5"  : (500, 500),
		"6"  : (600, 500),
		"7"  : (700, 500),
		"8"  : (800, 500),
		"9"  : (900, 500),
		"10" : (1000, 500),
		"11" : (1100, 500)
	}, 

	"TEAM2"  : { # Red team
		"1"  : (100, 100),
		"2"  : (200, 200),
		"3"  : (300, 300),
		"4"  : (400, 400),
		"5"  : (500, 500),
		"6"  : (600, 500),
		"7"  : (700, 500),
		"8"  : (800, 500),
		"9"  : (900, 500),
		"10" : (1000, 500),
		"11" : (1100, 500)
	}, 

	"REFREE" : (2748, 165)
}

topHomography = []


if __name__ == "__main__":

	camera  = cv2.VideoCapture("video.mp4")
	camera2 = cv2.VideoCapture("football.mp4") 

	#get the previous image from which the good features are taken
	prevImg = camera.read()[1]
	prevImg = cv2.cvtColor(prevImg,cv2.cv.CV_RGB2GRAY)

	#get the previous good features
	prevVect1   = cv2.goodFeaturesToTrack(prevImg, 50, 0.001, 100)
	prevVect    = prevVect1[0:21]

	prevVect[0] = np.array([2750, 165]) # Refree 

	prevVect[1]  = np.array([2715, 195]) # Red Player 1
	prevVect[2]  = np.array([2675, 150]) # Red Player 2
	prevVect[3]  = np.array([2805, 150]) # Red Player 3
	prevVect[4]  = np.array([2840, 135]) # Red Player 4
	prevVect[5]  = np.array([2750, 280]) # Red Player 5
	prevVect[6]  = np.array([2540, 130]) # Red Player 6
	prevVect[7]  = np.array([2475, 180]) # Red Player 7
	prevVect[8]  = np.array([3160, 240]) # Red Player 8
	prevVect[9]  = np.array([1955, 190]) # Red Player 9 [Keeper]

	prevVect[10]  = np.array([3140, 220]) # Blue Player 1
	prevVect[11]  = np.array([3010, 180]) # Blue Player 2
	prevVect[12]  = np.array([2955, 170]) # Blue Player 3
	prevVect[13]  = np.array([2880, 145]) # Blue Player 4
	prevVect[14]  = np.array([2690, 220]) # Blue Player 5
	prevVect[15]  = np.array([2850, 160]) # Blue Player 6
	prevVect[16]  = np.array([2810, 165]) # Blue Player 7
	prevVect[17]  = np.array([2875, 175]) # Blue Player 8
	prevVect[18]  = np.array([2755, 145]) # Blue Player 9 
	prevVect[19]  = np.array([2510, 190]) # Blue Player 10 
	prevVect[20]  = np.array([3270, 190]) # Blue Player 11 [Keeper]

	#prevVect[18] = np.array([3270, 180]) # Blue Keeper


	#prevVect[0] = np.array([500, 500])

	#print prevVect
	#print prevVect1
	videoOutput = cv2.VideoWriter()
	codec = cv.CV_FOURCC('M', 'P', '4', '2')
	videoOutput.open(VIDEO_TITLE_OUTPUT, codec, 23, (VIDEO_WIDTH, VIDEO_HEIGHT), True)
	frameIndex = 0

	
	while True:
	#while False:
		original = camera.read()[1]
		frame    = camera2.read()[1]
		#get the next image or calcOpticalFlowPyrLK
		nextImg = cv2.cvtColor(original,cv2.cv.CV_RGB2GRAY)
		#compute calcOpticalFlowPyrLK
		nextVect = np.copy(prevVect)
		nextVect , status , err = cv2.calcOpticalFlowPyrLK(prevImg,nextImg,prevVect,nextVect)
		print "--START FOR INDEX : "+str(frameIndex)+"--"
		#for every good feature we paint it
		for i in range(prevVect.shape[0]):
			p1 = (int(prevVect[i][0][0]),int(prevVect[i][0][1]))
			if i == 0: #Yellow reffree
				cv2.circle(frame, p1 ,10 , (0,255,255))
			
			elif i >= 1 and i <= 9: #Red Team 
				cv2.circle(frame, p1 ,10 , (0,0,255))

			elif i >= 10 and i <= 20: #Blue Team 
				cv2.circle(frame, p1 ,10 , (255,255,255))


		prevImg = nextImg.copy()
		prevVect = nextVect
		#frame = cv2.resize(frame, (0,0), fx=0.3, fy=0.3)
		#frame = cv2.cvtColor(frame, cv.CV_GRAY2RGB) 
		videoOutput.write(frame)
		frameIndex = frameIndex + 1
		#original = cv2.resize(original, (0,0), fx=0.3, fy=0.3)
		#cv2.imwrite('image'+str(frameIndex)+'.png', frame)
		#break
	
	videoOutput.release()
