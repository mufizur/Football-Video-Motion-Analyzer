import numpy as np
import cv2

FRAMEPOINTS = []

topHomography = [[  3.70795420e+01,   1.57907552e+02,  -8.32616546e+04],
				 [  1.64879407e+00,   2.61746691e+02,  -3.17123425e+04],
				 [  5.15248147e-04,   6.36123293e-02,   1.00000000e+00]]

def getProjectedPoints(point):
	prevX = point[0][0]
	prevY = point[0][1]

	newX = (topHomography[0][0]*prevX +  topHomography[0][1]*prevY + topHomography[0][2]) / (topHomography[2][0]*prevX +  topHomography[2][1]*prevY + topHomography[2][2])
	newY = (topHomography[1][0]*prevX +  topHomography[1][1]*prevY + topHomography[1][2]) / (topHomography[2][0]*prevX +  topHomography[2][1]*prevY + topHomography[2][2])
	return (newX, newY)


PLAYER_POINTS = {
	"RED"  : { # Red team
		"1"  : (3160, 240),
		"2"  : (2840, 140),
		"3"  : (2800, 160),
		"4"  : (2675, 155),
		"5"  : (2715, 185),
		"6"  : (2745, 275),
		"7"  : (2540, 130),
		"8"  : (2475, 180),
		"9"  : (1960, 195)  #Keeper
	}, 

	"BLUE"  : { # Blue team
		"1"  : (3145, 220),
		"2"  : (3010, 190),
		"3"  : (2950, 170),
		"4"  : (2875, 175),
		"5"  : (2875, 145),
		"6"  : (2845, 160),
		"7"  : (2755, 145),
		"8"  : (2695, 220),
		"9"  : (2505, 195),
		"10" : (2810, 165),
		"11" : (3270, 190)  #Keeper
	}, 

	"REFREE"  : (2748, 172),
	"LINESMEN": (4095, 525),
}

def getListPoints(points):
	newPoints = {
		"RED"  : { # Red team
			"1"  : getProjectedPoints(points[2].tolist()),
			"2"  : getProjectedPoints(points[3].tolist()),
			"3"  : getProjectedPoints(points[4].tolist()),
			"4"  : getProjectedPoints(points[5].tolist()),
			"5"  : getProjectedPoints(points[6].tolist()),
			"6"  : getProjectedPoints(points[7].tolist()),
			"7"  : getProjectedPoints(points[8].tolist()),
			"8"  : getProjectedPoints(points[9].tolist()),
			"9"  : getProjectedPoints(points[10].tolist())
		}, 

		"BLUE"  : { # Blue team
			"1"  : getProjectedPoints(points[11].tolist()),
			"2"  : getProjectedPoints(points[12].tolist()),
			"3"  : getProjectedPoints(points[13].tolist()),
			"4"  : getProjectedPoints(points[14].tolist()),
			"5"  : getProjectedPoints(points[15].tolist()),
			"6"  : getProjectedPoints(points[16].tolist()),
			"7"  : getProjectedPoints(points[17].tolist()),
			"8"  : getProjectedPoints(points[18].tolist()),
			"9"  : getProjectedPoints(points[19].tolist()),
			"10" : getProjectedPoints(points[20].tolist()),
			"11" : getProjectedPoints(points[21].tolist())
		}, 

		"REFREE"  : getProjectedPoints(points[1].tolist()),
		"LINESMEN": getProjectedPoints(points[0].tolist()),
	}

	return newPoints


def setInitialPreVect(points, prevVect):
	prevVect[0] = points["LINESMEN"] # Linesmen 
	prevVect[1] = points["REFREE"]   # refree

	prevVect[2]   = points["RED"]["1"]  # Red Player 1
	prevVect[3]   = points["RED"]["2"]  # Red Player 2
	prevVect[4]   = points["RED"]["3"]  # Red Player 3
	prevVect[5]   = points["RED"]["4"]  # Red Player 4
	prevVect[6]   = points["RED"]["5"]  # Red Player 5
	prevVect[7]   = points["RED"]["6"]  # Red Player 6
	prevVect[8]   = points["RED"]["7"]  # Red Player 7
	prevVect[9]   = points["RED"]["8"]  # Red Player 8
	prevVect[10]  = points["RED"]["9"]  # Red Player 9 [Keeper]

	prevVect[11]  = points["BLUE"]["1"]  # Blue Player 1
	prevVect[12]  = points["BLUE"]["2"]  # Blue Player 2
	prevVect[13]  = points["BLUE"]["3"]  # Blue Player 3
	prevVect[14]  = points["BLUE"]["4"]  # Blue Player 4
	prevVect[15]  = points["BLUE"]["5"]  # Blue Player 5
	prevVect[16]  = points["BLUE"]["6"]  # Blue Player 6
	prevVect[17]  = points["BLUE"]["7"]  # Blue Player 7
	prevVect[18]  = points["BLUE"]["8"]  # Blue Player 8
	prevVect[19]  = points["BLUE"]["9"]  # Blue Player 9 
	prevVect[20]  = points["BLUE"]["10"] # Blue Player 10 
	prevVect[21]  = points["BLUE"]["11"] # Blue Player 11 [Keeper]

	return prevVect

#get from webcam
cap = cv2.VideoCapture("video.avi")
cap2 = cv2.VideoCapture("football.mp4")
    
#find params for corner detection via Shi-Tomasi
shi_params = dict( maxCorners = 3000,
                       qualityLevel = 0.05, #determines amount of relevant points determined
                       minDistance = 7,
                       blockSize = 7 )

#find params for Lucas-Kanade optical flow
lk_params = dict( winSize  = (12,12), #larger window means better tracking, but slower computation (more cost)
                  maxLevel = 0,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

#random color gen!!! -- color[i].tolist()
#color = np.random.randint(0,255,(1000000,3))

#take first frame
ret, old_frame = cap.read()

#grayscale convert it
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_RGB2GRAY)

writer = cv2.VideoWriter('result.avi',
							 int(cap.get(cv2.cv.CV_CAP_PROP_FOURCC)),
							 int(cap.get(cv2.cv.CV_CAP_PROP_FPS)),
							 (int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
							 int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))))

p_old1   = cv2.goodFeaturesToTrack(old_gray, mask = None, **shi_params)
#p_old1   = cv2.goodFeaturesToTrack(prevImg, 50, 0.001, 100)
p_old = p_old1[0:22]
p_old = setInitialPreVect(PLAYER_POINTS, p_old)

index = 0
while(index < 300):
	print index
	index+=1
	#we need to continuously find good params to track

    #read curr frame and grayscale it
	ret,frame = cap.read()
	_, writeframe = cap2.read()
	fgray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    
    #init p_new in case we wanted to use flags
	p_new = np.zeros_like(p_old)
    
    #use Lucas-Kanade algorithm to find optical flow
	p_new, status, error = cv2.calcOpticalFlowPyrLK(old_gray, fgray, p_old, p_new, **lk_params)
    
    #find the best matching points
	good_new = p_new[status == 1] #status is 1 for a match
	good_old = p_old[status == 1]
    
	mask = np.zeros_like(frame);
    
    #draw the overlaying tracking img
	for i,(new,old) in enumerate(zip(good_new,good_old)):
		a,b = new.ravel() #tmp new value
		c,d = old.ravel() #tmp old value -- necessary for drawing line tracking

		#draws a line connecting the old point with the new point
		cv2.line(mask,(a,b),(c,d),(0,255,0),2)

		#draws the new dot
		cv2.circle(writeframe,(int(a),int(b)),4,(255,0,0),-1)
		
		#cv2.circle(frame, (a,b) ,10 , (0,255,255))

    #this is if we want to add lines into the tracking to follow the path
	img = cv2.add(writeframe,mask)
	writer.write(img)
    
    #update the previous frame and previous points
	old_gray = fgray.copy()
	p_old = p_new

#clean up
writer.release()
cap.release()