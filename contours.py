import numpy as np
import cv2

#get from webcam
cap = cv2.VideoCapture("subtracted.avi")
cap2 = cv2.VideoCapture("football.mp4")
    
#find params for corner detection via Shi-Tomasi
shi_params = dict( maxCorners = 3000,
                       qualityLevel = 0.05, #determines amount of relevant points determined
                       minDistance = 7,
                       blockSize = 7 )

#random color gen!!! -- color[i].tolist()
#color = np.random.randint(0,255,(1000000,3))

#take first frame
ret, old_frame = cap.read()

#grayscale convert it
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_RGB2GRAY)

writer = cv2.VideoWriter('contours.avi',
							 int(cap.get(cv2.cv.CV_CAP_PROP_FOURCC)),
							 int(cap.get(cv2.cv.CV_CAP_PROP_FPS)),
							 (int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
							 int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))))

index = 0
while(index < 300):
	print index
	#we need to continuously find good params to track
	p_old = cv2.goodFeaturesToTrack(old_gray, mask = None, **shi_params)
	
	_, writeframe = cap2.read()
	centroids = []
	temp = []
	contours, hierarchy = cv2.findContours(old_gray, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
	for c in contours:
		if cv2.contourArea(c) < 150:
			continue
		moment = cv2.moments(c)
		if moment['m00'] == 0:
			continue
		x = int(moment['m10'] / moment['m00'])
		y = int(moment['m01'] / moment['m00'])
		temp = [[x,y]]
		cv2.circle(writeframe, (x, y), 10, (255,0,0), -1)
		centroids.append(temp)
		
	centroids = np.array(p_old, np.float32)

    #read curr frame and grayscale it
	ret,frame = cap.read()
	fgray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        
	mask = np.zeros_like(frame);
    
    #this is if we want to add lines into the tracking to follow the path
	img = cv2.add(writeframe,mask)
	writer.write(img)
    
    #update the previous frame and previous points
	old_gray = fgray.copy()
	index+=1

#clean up
writer.release()
cap.release()