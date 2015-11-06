import os
import cv2
import cv2.cv as cv
import math
import numpy as np
import numpy.linalg as la

IMG_HEIGHT  = 600 
IMG_WIDTH   = 4850

CROP_RIGHT  = 400
CROP_LEFT   = 4780
CROP_TOP    = 420
CROP_BOTTOM = 3200

REMAP_SCALE_FACTOR = 30
FIELD_SCALE_FACTOR = 1.5
REMAPPED_HEIGHT    = 90 * REMAP_SCALE_FACTOR #Field is 90m
REMAPPED_WIDTH     = REMAPPED_HEIGHT * FIELD_SCALE_FACTOR
IMG_OFFSET = 500

IMG_POINTS = {
	"TOP_RIGHT"     : [2990, IMG_HEIGHT-478], #img[0:IMG_HEIGHT-478, 2990 :IMG_WIDTH]
	"TOP_LEFT"      : [1833, IMG_HEIGHT-471], #img[0:IMG_HEIGHT-471, 1833 :IMG_WIDTH]
	"BOTTOM_RIGHT"  : [4800, IMG_HEIGHT],  #img[0:IMG_HEIGHT-56,  4800 :IMG_WIDTH]
	"BOTTOM_LEFT"   : [220,  IMG_HEIGHT],  #img[0:IMG_HEIGHT-22,  220  :IMG_WIDTH] 
	"CENTRE"	    : [2430, IMG_HEIGHT-390], #img[0:IMG_HEIGHT-390, 0:IMG_WIDTH]
}

REMAPPED_POINTS = {
	"TOP_RIGHT"    : [REMAPPED_WIDTH+IMG_OFFSET, 0+IMG_OFFSET],
	"TOP_LEFT"     : [0+IMG_OFFSET, 0+IMG_OFFSET], 
	"BOTTOM_RIGHT" : [REMAPPED_WIDTH+IMG_OFFSET,   REMAPPED_HEIGHT+IMG_OFFSET], 
	"BOTTOM_LEFT"  : [0+IMG_OFFSET, REMAPPED_HEIGHT+IMG_OFFSET],   
	"CENTRE"	   : [REMAPPED_WIDTH/2+IMG_OFFSET, REMAPPED_HEIGHT/2+IMG_OFFSET] 
}

def convert_points_list_to_array(pointsList):
	pointsArray = []
	pointsArray = [pointsList['TOP_LEFT'], 
				   pointsList['TOP_RIGHT'], 
				   pointsList['BOTTOM_LEFT'], 
				   pointsList['BOTTOM_RIGHT'],
				   pointsList['CENTRE']]

	return pointsArray

def crop_img(finalImg):
	return finalImg[CROP_TOP:CROP_BOTTOM, CROP_RIGHT:CROP_LEFT]

def imgTopProjection(img):
	mainImgPts  = np.array(convert_points_list_to_array(IMG_POINTS), dtype=np.float32)
	remappedPts = np.array(convert_points_list_to_array(REMAPPED_POINTS), dtype=np.float32)
	
	homography, _  = cv2.findHomography(mainImgPts, remappedPts, cv2.RANSAC, 5.0) 
	finalImg = cv2.warpPerspective(img, homography, (int(REMAPPED_HEIGHT+(IMG_OFFSET*5)), int(REMAPPED_WIDTH)))
	finalImg = crop_img(finalImg)
	return finalImg

if __name__ == "__main__":
	main()