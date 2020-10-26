# Blackboard Collaborate auto raise hands if raised hands detected in some parts of the screen
# It can act as a attendance bot if lecturer takes attendance by raised hands
# One of the downside is you have to keep Blackboard on top or don't obstruct the locations of the screen which the program needs
# I know that it can be wrote with less code but i didn't put too much effort on this and used some codes from my other projects and rearranged them
import time
import cv2
import mss
import numpy as np
from pynput.mouse import Button, Controller

def findColor(img, myColors):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
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
        if area > 0:
            cv2.drawContours(frameResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            #cv2.imshow("contour", frameResult)
    return x + (w//2), y + (h//2)

myColors = [[140, 86, 140, 179, 190, 218]]      # attendance purple, [h_min, s_min, v_min, h_max, s_max, v_max]
myPoints = []
mouse = Controller()
flag = 0                                        # for not spamming clicks if there are raised hands

with mss.mss() as sct:
    monitor = {"top": 860, "left": 1562, "width": 32, "height": 32}         # where to check for raised hands?

    while "Screen capturing":
        last_time = time.time()

        img = np.array(sct.grab(monitor))

        cv2.imshow("OpenCV/Numpy normal", img)

        frameResult = img.copy()
        newPoints = findColor(img, myColors)
        if len(newPoints) != 0:
            for newP in newPoints:
                myPoints.append(newP)
        if len(newPoints) != 0 and flag == 0:   # if there are raised hands and not clicked yet
            mouse.position = (848, 1010)        # where to click to raise hands?
            mouse.press(Button.left)
            mouse.release(Button.left)
            flag = 1
        elif len(newPoints) == 0 and flag == 1: # if there are no raised hands and not clicked yet
            mouse.position = (848, 1010)        # where to click to raise hands?
            mouse.press(Button.left)
            mouse.release(Button.left)
            flag = 0

        #cv2.imshow("Result", frameResult)
        print('The current pointer position is {0}'.format(mouse.position))
        print("fps: {}".format(1 / (time.time() - last_time)))

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break


