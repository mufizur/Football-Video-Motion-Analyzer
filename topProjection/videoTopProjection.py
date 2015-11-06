import os
import cv2
import cv2.cv as cv
import math
import numpy as np
import numpy.linalg as la
from topProjection import imgTopProjection

os.chdir('C:/Users/Mufiz/Desktop/CS4243/topProjection')

TOTAL_IMAGES = 5 #7200

RESIZE_FACTOR = 0.5
VIDEO_TITLE   = "football_stitched"
VIDEO_FORMAT  = "mp4"

VIDEO_TITLE_OUTPUT = "video.avi"
VIDEO_HEIGHT = 600
VIDEO_WIDTH  = 4850

def saveVideoTopProjection(videoStr, videoFormat):
	video = cv2.VideoCapture(videoStr  +'.'+ videoFormat)
	
	videoOutput = cv2.VideoWriter()
	videoOutput.open(VIDEO_TITLE_OUTPUT, cv.CV_FOURCC(*'XVID'), 23, (VIDEO_WIDTH, VIDEO_HEIGHT), True)

	videoWidth      = int(video.get(cv.CV_CAP_PROP_FRAME_WIDTH))
	videoHeight     = int(video.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
	videoFps        = int(video.get(cv.CV_CAP_PROP_FPS))
	videoFrameCount = int(video.get(cv.CV_CAP_PROP_FRAME_COUNT))

	for frameIndex in range(0, videoFrameCount):
		if frameIndex == TOTAL_IMAGES:
			break

		_, frameImg = video.read() 
		print "--START TOP VIEW FOR INDEX : "+str(frameIndex)+"--"

		finalImg = imgTopProjection(frameImg)
		reSize = tuple((np.array(finalImg.shape)[:2] * RESIZE_FACTOR).astype(int)[::-1])
		finalImgResize = cv2.resize(finalImg, reSize)
		#cv2.imwrite(str(frameIndex)+'.png', finalImgResize)
		videoOutput.write(finalImgResize) 

	videoOutput.release()

	
	
def main():
	saveVideoTopProjection(VIDEO_TITLE, VIDEO_FORMAT)


if __name__ == "__main__":
	main()