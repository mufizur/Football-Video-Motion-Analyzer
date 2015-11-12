import cv2
import numpy

MAX_POINTS = 100

def harris(image):
    return cv2.goodFeaturesToTrack(image,
								   mask = None,
								   useHarrisDetector = True,
								   maxCorners = 100,
								   qualityLevel = 0.3,
								   minDistance = 7,
								   blockSize = 7)

def fast(image):
    features = list(sorted(cv2.FastFeatureDetector().detect(image, None), key = lambda k: k.response, reverse = True))[:MAX_POINTS]
    return numpy.array([[k.pt] for k in features], numpy.float32)

def optical_flow(detector, name):
	cap = cv2.VideoCapture('video.mp4')
	writer = cv2.VideoWriter('%s.avi' % name,
							 int(cap.get(cv2.cv.CV_CAP_PROP_FOURCC)),
							 int(cap.get(cv2.cv.CV_CAP_PROP_FPS)),
							 (int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
							 int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))))
	
	ret, previous_frame = cap.read()
	if not ret:
		exit(1)
	previous_frame = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
	previous_features = detector(previous_frame)
	
	lukas_kanade = {'winSize': (15, 15),
                    'maxLevel': 2,
                    'criteria': (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)}
	
	while True:
		ret, frame = cap.read()
		if not ret:
			break
		
		gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		new_features, st, err = cv2.calcOpticalFlowPyrLK(previous_frame, gray_frame, previous_features, None, **lukas_kanade)
		
		good_new = new_features[st == 1]
		good_previous = previous_features[st == 1]
		
		for i, (new, previous) in enumerate(zip(good_new, good_previous)):
			a, b = new.ravel()
			c, d = previous.ravel()
			cv2.circle(frame, (a, b), 4, (255, 0, 0), -1)
		
		writer.write(frame)
		previous_frame = gray_frame
		previous_features = good_new.reshape(-1, 1, 2)
	
	cap.release()
	writer.release()

if __name__ == "__main__":
    optical_flow(harris, "harris.avi")
    optical_flow(fast, "fast.avi")