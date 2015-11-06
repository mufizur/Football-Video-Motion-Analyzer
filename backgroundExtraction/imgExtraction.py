import os
import cv2
import cv2.cv as cv
import math
import numpy as np
import numpy.linalg as la
import copy 
from imgStitcher import stitcher, stitcher_firstFrame

os.chdir('C:/Users/Mufiz/Desktop/CS4243 Project/videoStitch')

TOTAL_IMAGES = 1 #7200
VIDEO_FORMAT = "mp4"
IMG_FORMAT	 = "png"
FINAL_IMG    = "frame_"

RESIZE_FACTOR	   = 0.5
VIDEO_TITLE        = "football_stitched"
BACKGROUND_IMG_TITLE = "football_stitched_background.png"
VIDEO_TITLE_OUTPUT   = "video.avi"
VIDEO_HEIGHT = 600
VIDEO_WIDTH  = 4850


def saveBackgroundVideo(videoStr, backgroundImg):
	video  = cv2.VideoCapture(videoStr  +'.'+ VIDEO_FORMAT)
	
	videoOutput = cv2.VideoWriter()
	#videoOutput.open(VIDEO_TITLE_OUTPUT, cv.CV_FOURCC(*'XVID'), 23, (VIDEO_WIDTH, VIDEO_HEIGHT), True)
	final_size = 0

	videoWidth      = int(video.get(cv.CV_CAP_PROP_FRAME_WIDTH))
	videoHeight     = int(video.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
	videoFps        = int(video.get(cv.CV_CAP_PROP_FPS))
	videoFrameCount = int(video.get(cv.CV_CAP_PROP_FRAME_COUNT))


	for frameIndex in range(0, videoFrameCount):
		if frameIndex == TOTAL_IMAGES:
			break

		_, frameImg  = video.read()
		frameSubtractedImg = copy.deepcopy(frameImg)

		print "--START FOR INDEX : "+str(frameIndex)+"--"

		rows = len(frameImg)
		columns = len(frameImg[0])

		for i in range(0, rows):
			for j in range(0, columns):
				frameSubtractedImg[i][j][0] = frameImg[i][j][0] - backgroundImg[i][j][0] if frameImg[i][j][0] > backgroundImg[i][j][0] else 0
				frameSubtractedImg[i][j][1] = frameImg[i][j][1] - backgroundImg[i][j][1] if frameImg[i][j][1] > backgroundImg[i][j][1] else 0
				frameSubtractedImg[i][j][2] = frameImg[i][j][2] - backgroundImg[i][j][2] if frameImg[i][j][2] > backgroundImg[i][j][2] else 0

		frameSubtractedImg = cv2.medianBlur(frameSubtractedImg, 5)
		cv2.imwrite("players4.jpg", frameSubtractedImg)
		#reSize = tuple((np.array(frameSubtractedImg.shape)[:2] * RESIZE_FACTOR).astype(int)[::-1])
		#frameSubtractedImg  = cv2.resize(frameSubtractedImg, reSize)
		#videoOutput.write(frameSubtractedImg) 
		
	#videoOutput.release()
	

def getImgsAll():
	bacgrkoundImg = cv2.imread(BACKGROUND_IMG_TITLE)
	saveBackgroundVideo(VIDEO_TITLE, bacgrkoundImg)


def main():
	getImgsAll()

if __name__ == "__main__":
	main()