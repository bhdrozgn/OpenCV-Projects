# It reads your camera and let you find HSV values for real objects.
import cv2
import numpy as np 
 
def empty(a):
    pass
 
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)
cv2.createTrackbar("Hue Min", "HSV", 0, 179, empty)              # Trackbar name, window name, min value, max value(hue max value is 179 in opencv), what function to call on change, 0 - 179
cv2.createTrackbar("Hue Max", "HSV", 179, 179, empty)            # 179 - 179
cv2.createTrackbar("Saturation Min", "HSV", 0, 255, empty)       # 0 - 255
cv2.createTrackbar("Saturation Max", "HSV", 255, 255, empty)     # 255 - 255
cv2.createTrackbar("Value Min", "HSV", 0, 255, empty)            # 0 - 255
cv2.createTrackbar("Value Max", "HSV", 255, 255, empty)          # 255 - 255
 
while True:
    success, frame = cap.read()
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    h_min = cv2.getTrackbarPos("Hue Min", "HSV")
    h_max = cv2.getTrackbarPos("Hue Max", "HSV")
    s_min = cv2.getTrackbarPos("Saturation Min", "HSV")
    s_max = cv2.getTrackbarPos("Saturation Max", "HSV")
    v_min = cv2.getTrackbarPos("Value Min", "HSV")
    v_max = cv2.getTrackbarPos("Value Max", "HSV")
    print(h_min)
 
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(frameHSV, lower, upper)
    result = cv2.bitwise_and(frame, frame, mask=mask)
 
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    hStack = np.hstack([frame, mask, result])
    cv2.imshow('Horizontal Stacking', hStack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
cap.release()
cv2.destroyAllWindows()
