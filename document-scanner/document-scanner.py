# This program scans a camera for any A4 size paper, rotate/warp it and show you the paper in A4 scale.
import cv2
import numpy as np

widthFrame = 480
heightFrame = 640

cap = cv2.VideoCapture(0)
cap.set(10, 100)       # brightness

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def preProcessing(frame):
    frameGrayed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frameBlurred = cv2.GaussianBlur(frameGrayed, (9, 9), 2)
    frameCanny = cv2.Canny(frameBlurred, 40, 50)
    kernel = np.ones((3, 3))
    frameDilated = cv2.dilate(frameCanny, kernel, iterations = 2)
    frameThreshold = cv2.erode(frameDilated, kernel, iterations = 1)
    return frameThreshold

def getContours(frame):
    biggest = np.array([])
    maxArea = 0
    contours, hieararchy = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1500:
            #cv2.drawContours(frameContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
    cv2.drawContours(frameContour, biggest, -1, (255, 0, 0), 20)
    return biggest

def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), np.int32)
    add = myPoints.sum(1)
    #print("add", add)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis = 1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    #print("New Points", myPointsNew)
    return myPointsNew

def getWarp(frame, biggest):
    biggest = reorder(biggest)
    pts1 = np.float32(biggest)                                                                          # corner points
    pts2 = np.float32([[0, 0], [widthFrame, 0], [0, heightFrame], [widthFrame, heightFrame]])           # top left, top right, bottom left, bottom right
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    frameOutput = cv2.warpPerspective(frame, matrix, (widthFrame, heightFrame))
    frameCropped = frameOutput[20:frameOutput.shape[0]-20, 20:frameOutput.shape[1]]
    frameCropped = cv2.resize(frameCropped, (widthFrame, heightFrame))
    return frameCropped

while(cap.isOpened()):
    success, frame = cap.read()
    cv2.resize(frame, (widthFrame, heightFrame))
    frameContour = frame.copy()
    frameThreshold = preProcessing(frame)
    biggest = getContours(frameThreshold)
    if biggest.size != 0:
        frameWarped = getWarp(frame, biggest)
        frameArray = ([frame, frameThreshold],
                      [frameContour, frameWarped])
        cv2.imshow("Result", frameWarped)
    else:
        frameArray = ([frame, frameThreshold],
                      [frame, np.zeros((512, 512, 3), np.uint8)])
    stackedFrames = stackImages(0.6, frameArray)
    cv2.imshow("Video", stackedFrames)
    if cv2.waitKey(15) & 0xFF == ord('q'):      # cv2.waitKey(x), x should be 1000/FPS. For example if FPS is 50, x should be 20.
        break

cap.release()
cv2.destroyAllWindows()
