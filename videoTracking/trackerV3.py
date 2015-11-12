import cv2
import cv2.cv as cv
import numpy as np
import os

os.chdir('C:/Users/Mufiz/Desktop/CS4243 Project/Football-Video-Motion-Analyzer/videoTracking')

def estimate_points(pts1, pts2):
    #if len(pts1) == len(pts2): return pts2
    candidates = [[] for i in pts1]
    picked = [False for i in pts2]
    result = [None for i in pts1]

    for i,p1 in enumerate(pts1):
        for j,p2 in enumerate(pts2):
            d = np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
            if d < 50:
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

def extract(hsv, lower, upper):
    mask = cv2.inRange(hsv, lower, upper)
    masked = cv2.bitwise_and(hsv, hsv, mask=mask)
    h,_,_ = cv2.split(masked)
    h = cv2.GaussianBlur(h, (33,33), 1)
    kernel = np.ones([5,3], np.uint8)
    h = cv2.dilate(h, kernel, iterations=3)

    result = []
    contours, hierarchy = cv2.findContours(h, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if cv2.contourArea(c) < 150:
            continue
        moment = cv2.moments(c)
        if moment['m00'] == 0:
            continue
        x = int(moment['m10'] / moment['m00'])
        y = int(moment['m01'] / moment['m00'])
        result.append((x,y))
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
    corners = np.array([[1870, 159], [3495, 150],[5750, 650], [100, 650]])
    cv2.fillPoly(mask, [corners.reshape((-1,1,2))], (255, 255, 255))

    reader = cv2.VideoCapture(video)
    height, width, _ = bg.shape
    codec = cv.CV_FOURCC('M', 'P', '4', '2')
    writer = cv2.VideoWriter("test.avi", codec, 24, (width, height), True)

    red1 = np.array([0, 80, 80])
    red2 = np.array([15, 255, 255])
    blue1 = np.array([95, 30, 30])
    blue2 = np.array([145, 255, 255])
    yellow1 = np.array([30, 100, 210])
    yellow2 = np.array([50, 140, 255])

    blue = []
    red = []
    fc = 1200
    for i in range(0, fc):
        print "Processing frame ", i, " of ", fc
        _, frame = reader.read()

        # remove background and everything outside the field
        #diff = cv2.absdiff(frame, bg)
        #diff = cv2.bitwise_and(diff, diff, mask=mask)
        field = cv2.bitwise_and(mask, frame)

        hsv = cv2.cvtColor(field, cv2.COLOR_BGR2HSV)
        h,s,v = cv2.split(hsv)
        _, v = cv2.threshold(v, 50, 255, cv2.THRESH_BINARY)
        #v = cv2.GaussianBlur(v, (33, 33), 3)

        field = cv2.bitwise_and(field, field, mask=v)
        hsv = cv2.cvtColor(field, cv2.COLOR_BGR2HSV)

        bplayers = extract(hsv, blue1, blue2)
        bplayers = bplayers if len(blue) == 0 else estimate_points(blue[-1], bplayers)
        blue.append(bplayers)
        draw(frame, bplayers, (255,0,0))

        rplayers = extract(hsv, red1, red2)
        rplayers = rplayers if len(red) == 0 else estimate_points(red[-1], rplayers)
        red.append(rplayers)
        draw(frame, rplayers, (0,0,255))

        #draw(frame, red_players, (0,0,255))
        #red_players = extract(hsv, red1, red2)
        #draw(frame, yellow_players, (255,255,0))
        #yellow_players = extract(hsv, yellow1, yellow2)

        cv2.imwrite("testing.png", frame)
        writer.write(frame)
    reader.release()
    writer.release()

def main():
    video = "video.mp4"
    bg = cv2.imread("football_stitched_background.png")
    track(video, bg)

if __name__ == "__main__":
    main()
