import os
import cv2
import cv2.cv as cv
import math
import numpy as np
import numpy.linalg as la

os.chdir('C:\Users\Mufiz\Desktop\CS4243')

VIDEO_TITLE  = 'football_stitched'
VIDEO_FORMAT = "mp4"
IMG_FORMAT	 = "png"


def background_extraction(videoTitle, videoFormat, imgFormat):
	cap = cv2.VideoCapture(videoTitle+'.'+videoFormat)
	
	videoWidth      = int(cap.get(cv.CV_CAP_PROP_FRAME_WIDTH))
	videoHeight     = int(cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
	videoFps        = int(cap.get(cv.CV_CAP_PROP_FPS))
	videoFrameCount = int(cap.get(cv.CV_CAP_PROP_FRAME_COUNT))

	ret, img = cap.read()
	avgImg = np.float32(img)

	for frameIndex in range(1, videoFrameCount):
		print "--EXTRACTING : frame "+str(frameIndex)
		ret, img = cap.read()
		
		#code for average img - running average
		newImg = np.float32(img)
		avgImg = ((frameIndex)*(avgImg) + newImg) / (frameIndex+1)
		#End of code 

		normImg = cv2.convertScaleAbs(avgImg) # convert into uint8 image

	cv2.destroyAllWindows()
	cap.release()

	cv2.imwrite(videoTitle+"_background."+imgFormat, avgImg)


def main():
	background_extraction(VIDEO_TITLE, VIDEO_FORMAT, IMG_FORMAT)

if __name__ == "__main__":
	main()