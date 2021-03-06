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

index = 0
while(index < 300):
	print index
	index+=1
	#we need to continuously find good params to track
	p_old = cv2.goodFeaturesToTrack(old_gray, mask = None, **shi_params)
	
	'''p_old = []
	temp = []
	temp2 = []
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
		p_old.append(temp)
		
	p_old = np.array(p_old, np.float32)'''	

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

#clean up
writer.release()
cap.release()