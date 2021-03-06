# virtual webcam paint
import cv2
import numpy as np

def findColor(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        cv2.circle(frameResult, (x, y), 15, myColorValues[count], cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1
        #cv2.imshow(str(color[0]), mask)
    return newPoints

def getContours(img):
    contours, hieararchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 100:
            #cv2.drawContours(frameResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.03*peri, True)             # If you don't get satisfying results with detection try to increase or decrease 0.03
            x, y, w, h = cv2.boundingRect(approx)
    return x + (w//2), y

def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(frameResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)

cap = cv2.VideoCapture(0)
cap.set(3, 640)                                 # width
cap.set(4, 480)                                 # height

# Hue, Saturation and Value of the colors that will detected
# These values are only for me under particular light conditions and particular camera
# You have to find your own HSV values. I added a color finder for you in the same repository.
# Also you can add many colors you want.
# [h_min, s_min_ v_min, h_max, s_max, v_max]
myColors = [[24, 49, 149, 37, 255, 255],        # yellow
            [118, 64, 54, 147, 255, 255],       # purple
            [154, 77, 134, 179, 255, 255]]      # pink

# The colors which will be painted on the screen.
# Remember to enter these color codes according to the myColors array. It will be painted respectively to that array.
# You can add many colors you want as long as there is a corresponding HSV value in myColors
myColorValues = [[0, 255, 255],                 # BGR Format
                 [213, 0, 128],
                 [178, 102, 255]]

myPoints = []                      # [x, y, colorID]

while(cap.isOpened()):
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)                  # You don't need this if your camera shows you mirrored.
    frameResult = frame.copy()
    newPoints = findColor(frame, myColors, myColorValues)
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(newPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)
    cv2.imshow("Video", frameResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):      # waitKey'in delayi x = 1000/FPS şeklinde ayarlamak lazım
        break

cap.release()
cv2.destroyAllWindows()
