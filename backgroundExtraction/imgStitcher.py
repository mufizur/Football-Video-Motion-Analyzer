import os
import cv2
import math
import numpy as np
import numpy.linalg as la
from matplotlib import pyplot as plt

FLANN_INDEX_KDTREE = 1
IMG_CROP_MIN_HEIGHT = 350
IMG_CROP_MAX_HEIGHT = 1550
IMG_CROP_MIN_WIDTH  = 600
IMG_CROP_MAX_WIDTH  = 10300

IMG_APPEND_LEFT  = "left"
IMG_APPEND_RIGHT = "right"

LEFT_CROP_OFFSET_UPPER  = 4950
LEFT_CROP_OFFSET_LOWER  = 4393
RIGHT_CROP_OFFSET_UPPER = 6312
RIGHT_CROP_OFFSET_LOWER = 5500


def filter_matches(matches):
    goodMatches = []
    ratio=0.7

    for m in matches:
        if len(m) == 2 and m[0].distance < m[1].distance * ratio:
            goodMatches.append(m[0])

    return goodMatches


def get_transformed_img_dimensions(img, invH):
	imgRows    	 = len(img)
	imgColumns 	 = len(img[0]) if len(img) > 0 else 0

	imgDimensions = {
		"Umax" : None, 
		"Vmax" : None,
		"Umin" : None,
		"Vmin" : None 
	}

	top_left 	 =  [0, 0] 
	top_right    =  [imgColumns, 0]
	bottom_left  =  [0, imgRows]
	bottom_right =  [imgColumns, imgRows]
	img_corners  =  [top_left, top_right, bottom_left, bottom_right]

	for corner_pt in img_corners:
		U_coordinate = corner_pt[0]
		V_coordinate = corner_pt[1]
		normalizer   = U_coordinate*invH[2][0] + V_coordinate*invH[2][1] + invH[2][2]

		U_coordinate_remapped = (U_coordinate*invH[0][0] + V_coordinate*invH[0][1] + invH[0][2]) / normalizer
		V_coordinate_remapped = (U_coordinate*invH[1][0] + V_coordinate*invH[1][1] + invH[1][2]) / normalizer

		imgDimensions['Umax'] = U_coordinate_remapped if ((imgDimensions['Umax'] is None) or (imgDimensions['Umax'] < U_coordinate_remapped)) else imgDimensions['Umax']
		imgDimensions['Vmax'] = V_coordinate_remapped if ((imgDimensions['Vmax'] is None) or (imgDimensions['Vmax'] < V_coordinate_remapped)) else imgDimensions['Vmax']
		imgDimensions['Umin'] = U_coordinate_remapped if ((imgDimensions['Umin'] is None) or (imgDimensions['Umin'] > U_coordinate_remapped)) else imgDimensions['Umin']
		imgDimensions['Vmin'] = V_coordinate_remapped if ((imgDimensions['Vmin'] is None) or (imgDimensions['Vmin'] > V_coordinate_remapped)) else imgDimensions['Vmin']

	imgDimensions['Umin'] = min(0, imgDimensions['Umin'])
	imgDimensions['Vmin'] = min(0, imgDimensions['Vmin'])

	return imgDimensions


def get_img_homography(mainImg, appendImg):

	# Extracting img features using surf
	surf = cv2.SURF()
	mainImgFeatures,   mainImgDestination   = surf.detectAndCompute(mainImg,   None)
	appendImgFeatures, appendImgDestination = surf.detectAndCompute(appendImg, None)

	# Extracting good feature points
	indexParameters  = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
	searchParameters = dict(checks=50)
	flannMatcher 	 = cv2.FlannBasedMatcher(indexParameters, searchParameters)
	imgMatches   	 = flannMatcher.knnMatch(appendImgDestination, trainDescriptors=mainImgDestination, k=2)
	goodMatches 	 = filter_matches(imgMatches)

	# Saving image keypoints
	mainImg_keyPoints   = []
	appendImg_keyPoints = []
	for match in goodMatches:
	    mainImg_keyPoints.append(mainImgFeatures[match.trainIdx])
	    appendImg_keyPoints.append(appendImgFeatures[match.queryIdx])

	mainImgPoints   = np.array([keyPoint.pt for keyPoint in mainImg_keyPoints])
	appendImgPoints = np.array([keyPoint.pt for keyPoint in appendImg_keyPoints])

	#Finding Img homography
	homographyMatrix,_ = cv2.findHomography(appendImgPoints, mainImgPoints, cv2.RANSAC, 5.0)
	return homographyMatrix

def img_crop_append(appendImg, positionAppend):
	crop_appendImg  = appendImg
	cropAppendLower = 0 
	cropAppendUpper = 0

	if positionAppend == IMG_APPEND_LEFT:
		cropAppendLower = LEFT_CROP_OFFSET_LOWER
		cropAppendUpper = LEFT_CROP_OFFSET_UPPER

	elif positionAppend == IMG_APPEND_RIGHT:
		cropAppendLower = RIGHT_CROP_OFFSET_LOWER
		cropAppendUpper = RIGHT_CROP_OFFSET_UPPER

	crop_appendImg[0:len(appendImg),cropAppendLower:cropAppendUpper] = [0, 0, 0]
	return crop_appendImg

def get_img_warp_perspective(mainImg, appendImg, finalImgWidth, finalImgHeight, imgHomography, imgShift, positionAppend):

	imgHomography_shift = imgShift * imgHomography
	main_img_project    = cv2.warpPerspective(mainImg,   imgShift, (finalImgWidth, finalImgHeight))
	append_img_project  = cv2.warpPerspective(appendImg, imgHomography_shift, (finalImgWidth, finalImgHeight))
	
	img_crop_append(append_img_project, positionAppend)
	finalImg = cv2.add(main_img_project,  append_img_project, dtype=cv2.CV_8U)
	return finalImg


def imgStitch(mainImg, appendImg, positionAppend, imgHomography):
	
	imgDimensions = get_transformed_img_dimensions(appendImg, imgHomography)
	imgDimensions['Umax'] = max(imgDimensions['Umax'], len(mainImg[0]))
	imgDimensions['Vmax'] = max(imgDimensions['Vmax'], len(mainImg))

	imgShift = np.matrix(np.identity(3), np.float32)
	if imgDimensions['Umin'] < 0:
		imgShift[0,2] = imgShift[0,2] - imgDimensions['Umin']
		imgDimensions['Umax'] = imgDimensions['Umax'] - imgDimensions['Umin']
	
	if imgDimensions['Vmin'] < 0:
		imgShift[1,2] = imgShift[1,2] - imgDimensions['Vmin']
		imgDimensions['Vmax'] = imgDimensions['Vmax'] - imgDimensions['Vmin']

	finalImgWidth   = int(imgDimensions['Umax'])
	finalImgHeight  = int(imgDimensions['Vmax']) 

	finalImg = get_img_warp_perspective(mainImg, appendImg, finalImgWidth, finalImgHeight, imgHomography, imgShift, positionAppend)
	return finalImg


def img_crop_out_spaces(img):
	crop_img = img[IMG_CROP_MIN_HEIGHT:IMG_CROP_MAX_HEIGHT, IMG_CROP_MIN_WIDTH:IMG_CROP_MAX_WIDTH]
	return crop_img

def stitcher_firstFrame(leftImg, centreImg, rightImg):
	videoHomographyLeft    = get_img_homography(centreImg, leftImg)
	stitch_intermediateImg = imgStitch(centreImg, leftImg, IMG_APPEND_LEFT, videoHomographyLeft)
	videoHomographyRight   = get_img_homography(stitch_intermediateImg, rightImg)
	stitch_finalImg        = imgStitch(stitch_intermediateImg, rightImg, IMG_APPEND_RIGHT, videoHomographyRight)
	crop_finalImg 		   = img_crop_out_spaces(stitch_finalImg)
	return crop_finalImg, videoHomographyLeft, videoHomographyRight



def stitcher(leftImg, centreImg, rightImg, videoHomographyLeft, videoHomographyRight):	
	stitch_intermediateImg = imgStitch(centreImg, leftImg, IMG_APPEND_LEFT, videoHomographyLeft)
	stitch_finalImg        = imgStitch(stitch_intermediateImg, rightImg, IMG_APPEND_RIGHT, videoHomographyRight)
	crop_finalImg 		   = img_crop_out_spaces(stitch_finalImg)
	return crop_finalImg