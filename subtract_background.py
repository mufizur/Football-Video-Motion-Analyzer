import cv2
import cv2.cv as cv
import numpy as np
import os

### preparation for perform_homography
field = np.zeros([1112,745])

fieldCoordsArray = [(float(0), float(0)),(float(1112), float(0)),(float(1112), float(745)),(float(0), float(745))]
fieldCoords = [fieldCoordsArray[0], fieldCoordsArray[1], fieldCoordsArray[2], fieldCoordsArray[3]]

cornersArray = [(float(1930),float(156)),(float(3418), float(146)),(float(5770),float(690)),(float(0), float(690))]
corners = [cornersArray[0], cornersArray[1], cornersArray[2], cornersArray[3]]

#fullImageCoordsArray = [(float(0),float(0)),(float(3418), float(146)),(float(5770),float(690)),(float(0), float(690))]
Hmatrix, status = cv2.findHomography(np.array(corners), np.array(fieldCoords), 0)
HmatrixInverse, status = cv2.findHomography(np.array(fieldCoords), np.array(corners), 0)

def perform_homography(inputImage):
    return cv2.warpPerspective(inputImage, Hmatrix, field.shape)
def perform_inv_homography(inputImage):
    return cv2.warpPerspective(inputImage, HmatrixInverse, field.shape)

# Performs closest pair matching between two sets of coordinates
# Returns a list of coordinates with length = len(pts1)
def estimate_points(pts1, pts2, max_distance=50):
    #if len(pts1) == len(pts2): return pts2
    candidates = [[] for i in pts1]
    picked = [False for i in pts2]
    result = [None for i in pts1]

    for i,p1 in enumerate(pts1):
        for j,p2 in enumerate(pts2):
            d = np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
            if d < max_distance:
                candidates[i].append((d, j))
    for i,point in enumerate(pts1):
        i = int(i)
        candidates[i].sort()
        for candidate in candidates[i]:
            j = candidate[1]
            #if j >= len(pts1): continue
            if picked[j]:
                continue
            else:
                picked[j] = True
                result[i] = pts2[j]
                break
        if result[i] == None:
            if len(candidates[i]) > 0:
                result[i] = pts2[candidates[i][0][1]]
            else:
                result[i] = pts1[i]
    return result

# Given an image (frame), find the centroid of contours within a certain color range
# returns the resulting list of coordinates and the mask of the selected range
def extract_points(frame, points, color_range, max_distance=50, size=150):
    mask = cv2.inRange(frame, color_range[0], color_range[1])
    masked = cv2.bitwise_and(frame, frame, mask=mask)
    h,s,v = cv2.split(masked)

    blurred = cv2.GaussianBlur(h, (33,33), 1)
    kernel = np.ones([5,3], np.uint8)
    dilated = cv2.dilate(blurred, kernel, iterations=3)

    result = []
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if cv2.contourArea(c) < size:
            continue
        moment = cv2.moments(c)
        if moment['m00'] == 0:
            continue
        x = int(moment['m10'] / moment['m00'])
        y = int(moment['m01'] / moment['m00'])
        result.append((x,y))

    result = result if len(points) == 0 else estimate_points(points[-1], result, max_distance)
    points.append(result)
    return result

def draw(frame, coord, color):
    for points in coord:
        cv2.circle(frame, points, 20, color, 2)
        #rx, ry, rw, rh, a = points
        #cv2.putText(frame, str(a), (rx,ry+rh), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
        #cv2.rectangle(frame, (rx,ry), (rx+rw, ry+rh), color, 2)
    return frame

def track(video, bg):
    # mask to remove everything outside the field
	mask = np.zeros(bg.shape, np.uint8)
	corners = np.array([[1833, 129], [3050, 122],[5060, 600], [220, 600]])
	cv2.fillPoly(mask, [corners.reshape((-1,1,2))], (255, 255, 255))

	reader = cv2.VideoCapture(video)
	height, width, _ = bg.shape
	codec = cv.CV_FOURCC('M', 'P', '4', '2')
	writer = cv2.VideoWriter("subtracted.avi", codec, 24, (width, height), True)

	'''red_range = np.array([[0, 80, 80],[15,255,255]])
	blue_range = np.array([[95, 30, 30],[145,255,255]])
	yellow_range = np.array([[35, 130, 130],[40,255,255]])
	green_range = np.array([[45, 100, 100],[50,255,255]])
	white_range = np.array([[30, 15, 200],[40,25,220]])
	ball_range = np.array([[30, 30, 150],[40,90,185]])

	blue = []
	red = []
	yellow = []
	green = []
	white = []
	ball = [[(3174,213)]]'''

	fc = 7200
	for i in range(0, fc):
		print "Processing frame ", i, " of ", fc
		_, frame = reader.read()
		#cv2.imwrite("testing.png", frame)
		#remove background and everything outside the field
		#diff = cv2.bitwise_and(diff, diff, mask=mask)
		field = cv2.bitwise_and(mask, frame)

		subtracted = cv2.absdiff(frame, bg)
		subtracted_hsv = cv2.cvtColor(subtracted, cv2.COLOR_BGR2HSV)
		h,s,v = cv2.split(subtracted_hsv)
		_, v = cv2.threshold(v, 50, 255, cv2.THRESH_BINARY)

		field = cv2.bitwise_and(field, field, mask=v)
		hsv = cv2.cvtColor(field, cv2.COLOR_BGR2HSV)
		'''bpoints = extract_points(hsv, blue, blue_range)
		rpoints = extract_points(hsv, red, red_range)
		gpoints = extract_points(hsv, green, green_range)
		ypoints = extract_points(hsv, yellow, yellow_range)
		wpoints = extract_points(hsv, white, white_range)
		#ball_points = [(3174,213)] if i==0 else extract_points(hsv, ball, ball_range, size=100)
		#draw(frame, ball_points, (255,0,255))
		draw(frame, bpoints, (255,0,0))
		draw(frame, rpoints, (0,0,255))
		draw(frame, gpoints, (0,255,0))
		draw(frame, ypoints, (150,255,150))
		draw(frame, wpoints, (255,255,255))'''

		#if i > 155:
		#    cv2.imwrite("testing.png", field)
		writer.write(hsv)
	reader.release()
	writer.release()

def main():
    video = "football.mp4"
    bg = cv2.imread("bg.png")
    track(video, bg)

if __name__ == "__main__":
    main()