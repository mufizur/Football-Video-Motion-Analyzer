import os
import cv2
import cv2.cv as cv
import math
import numpy as np
import numpy.linalg as la
from imgStitcher import stitcher, stitcher_firstFrame

os.chdir('C:/Users/Mufiz/Desktop/CS4243 Project/videoStitch')

TOTAL_IMAGES = 230 #7200
VIDEO_FORMAT = "mp4"
IMG_FORMAT	 = "png"
FINAL_IMG    = "frame_"

RESIZE_FACTOR	   = 0.5
VIDEO_TITLE_LEFT   = "football_left"
VIDEO_TITLE_MIDDLE = "football_mid"
VIDEO_TITLE_RIGHT  = "football_right"
VIDEO_TITLE_OUTPUT = "video.avi"
VIDEO_HEIGHT = 600
VIDEO_WIDTH  = 4850


def saveSitchedVideo(videoRightStr, videoMiddleStr, videoLeftStr):
	videoRight  = cv2.VideoCapture(videoRightStr  +'.'+ VIDEO_FORMAT)
	videoMiddle = cv2.VideoCapture(videoMiddleStr +'.'+ VIDEO_FORMAT)
	videoLeft   = cv2.VideoCapture(videoLeftStr   +'.'+ VIDEO_FORMAT)
	
	videoOutput = cv2.VideoWriter()
	videoOutput.open(VIDEO_TITLE_OUTPUT, cv.CV_FOURCC(*'XVID'), 23, (VIDEO_WIDTH, VIDEO_HEIGHT), True)
	final_size = 0

	videoWidth      = int(videoRight.get(cv.CV_CAP_PROP_FRAME_WIDTH))
	videoHeight     = int(videoRight.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
	videoFps        = int(videoRight.get(cv.CV_CAP_PROP_FPS))
	videoFrameCount = int(videoRight.get(cv.CV_CAP_PROP_FRAME_COUNT))

	videoHomographyLeft   = "" 
	videoHomographyRight  = ""

	for frameIndex in range(0, videoFrameCount):
		if frameIndex == TOTAL_IMAGES:
			break

		_, frameRightImg  = videoRight.read()
		_, frameMiddleImg = videoMiddle.read()
		_, frameLeftImg   = videoLeft.read()
		print "--START STITCHING FOR INDEX : "+str(frameIndex)+"--"

		if frameIndex == 0:
			frameStitchImg, videoHomographyLeft, videoHomographyRight = stitcher_firstFrame(frameLeftImg, frameMiddleImg, frameRightImg)
			reSize = tuple((np.array(frameStitchImg.shape)[:2] * RESIZE_FACTOR).astype(int)[::-1])
			frameStitchImg  = cv2.resize(frameStitchImg, reSize)
			videoOutput.write(frameStitchImg) 
		else:
			frameStitchImg = stitcher(frameLeftImg, frameMiddleImg, frameRightImg, videoHomographyLeft, videoHomographyRight)	
			reSize = tuple((np.array(frameStitchImg.shape)[:2] * RESIZE_FACTOR).astype(int)[::-1])
			frameStitchImg  = cv2.resize(frameStitchImg, reSize)
			videoOutput.write(frameStitchImg) 
		
	videoOutput.release()
	

def getImgsAll():
	saveSitchedVideo(VIDEO_TITLE_RIGHT, VIDEO_TITLE_MIDDLE, VIDEO_TITLE_LEFT)


def main():
	getImgsAll()

if __name__ == "__main__":
	main()