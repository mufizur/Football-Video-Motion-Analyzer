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


	for frameIndex in range(0, videoFrameCount):
		if frameIndex == TOTAL_IMAGES:
			break

		_, frame  = video.read()
		#frameSubtractedImg     = cv2.cvtColor(frameSubtractedImg,cv2.cv.CV_RGB2GRAY)
		rows = len(backgroundImg)
		columns = len(backgroundImg[0])

		frameSubtractedImg = copy.deepcopy(frame)
		frameSubtractedImg = frameSubtractedImg.astype(np.int16)
		frame = frame.astype(np.int16)
		backgroundImg = backgroundImg.astype(np.int16)
		print "--START FOR INDEX : "+str(frameIndex)+"--"

		frameSubtractedImg = frame - backgroundImg
		frameSubtractedImg = frameSubtractedImg.clip(0)
		frameSubtractedImg = frameSubtractedImg.astype(np.uint8)

		#frameSubtractedImg = cv2.cvtColor(frameSubtractedImg, cv.CV_GRAY2RGB) 
		frameSubtractedImg = cv2.medianBlur(frameSubtractedImg, 5)
		videoOutput.write(frameSubtractedImg)
		cv2.imwrite("new.png", frameSubtractedImg)
		break;
		
	videoOutput.release()
	

def getImgsAll():
	backgroundImg = cv2.imread(BACKGROUND_IMG_TITLE)
	print backgroundImg
	saveBackgroundVideo(VIDEO_TITLE, backgroundImg)


def main():
	getImgsAll()

if __name__ == "__main__":
	main()