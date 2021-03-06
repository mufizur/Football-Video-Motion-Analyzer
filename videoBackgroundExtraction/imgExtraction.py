import os
import cv2
import cv2.cv as cv
import math
import numpy as np
import numpy.linalg as la
import copy 
from imgStitcher import stitcher, stitcher_firstFrame

os.chdir('C:/Users/Mufiz/Desktop/CS4243 Project/Football-Video-Motion-Analyzer/videoBackgroundExtraction')

TOTAL_IMAGES = 7200 #7200
VIDEO_FORMAT = "mp4"
IMG_FORMAT	 = "png"
FINAL_IMG    = "frame_"

VIDEO_TITLE        = "football_stitched"
BACKGROUND_IMG_TITLE = "football_stitched_background.png"
VIDEO_TITLE_OUTPUT   = "video.avi"
VIDEO_HEIGHT = 600
VIDEO_WIDTH  = 4850


def saveBackgroundVideo(videoStr, backgroundImg):
	video  = cv2.VideoCapture(videoStr  +'.'+ VIDEO_FORMAT)
	
	videoOutput = cv2.VideoWriter()
	videoOutput.open(VIDEO_TITLE_OUTPUT, cv.CV_FOURCC(*'XVID'), 23, (VIDEO_WIDTH, VIDEO_HEIGHT), True)
	final_size = 0

	videoWidth      = int(video.get(cv.CV_CAP_PROP_FRAME_WIDTH))
	videoHeight     = int(video.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
	videoFps        = int(video.get(cv.CV_CAP_PROP_FPS))
	videoFrameCount = int(video.get(cv.CV_CAP_PROP_FRAME_COUNT))

	imgMask = np.zeros(backgroundImg.shape, np.uint8)
	imgCorners = np.array([[1833,129], [3050, 122], [5060, 600], [220, 600]])
	cv2.fillPoly(imgMask, [imgCorners.reshape((-1, 1, 2))], (255,255,255))

	for frameIndex in range(0, videoFrameCount):
		if frameIndex == TOTAL_IMAGES:
			break

		_, frame  = video.read()
		imgSelection = cv2.bitwise_and(imgMask, frame)
		imgSubstration = cv2.absdiff(frame, backgroundImg)
		imgSubstrationHSV = cv2.cvtColor(imgSubstration, cv2.COLOR_BGR2HSV)
		_, _, imgSubstrationV = cv2.split(imgSubstrationHSV)
		_, vThreshold = cv2.threshold(imgSubstrationV, 50, 255, cv2.THRESH_BINARY)

		imgSelection = cv2.bitwise_and(imgSelection, imgSelection, mask=vThreshold)
		imgFinal = cv2.cvtColor(imgSelection, cv2.COLOR_BGR2HSV)
		imgFinal = imgFinal.astype(np.uint8)
		print frameIndex
		if frameIndex == 230:
			break
		videoOutput.write(imgFinal)
		#imgSubstration = cv2.medianBlur(imgSubstration, 5)
		#break;
		
	videoOutput.release()
	

def getImgsAll():
	backgroundImg = cv2.imread(BACKGROUND_IMG_TITLE)
	print backgroundImg
	saveBackgroundVideo(VIDEO_TITLE, backgroundImg)


def main():
	getImgsAll()

if __name__ == "__main__":
	main()