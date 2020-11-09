import cv2
import numpy as np

frameWidth = 1920 #640
frameHeight = 1080 #480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)

myColors = [[17,64,191,37,245,245]]    ## HSV [Hmin,Smin,Vmin,Hmax,Smax,Vmax]
myColorValues = [[51,153,255]]         ## BGR

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x_c_s,y_c_s = [],[]
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>1000:
            cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)
            x_c_s.append(x+(w//2))
            y_c_s.append(y+(h//2))
        
    if len(y_c_s)!=0 & len(x_c_s)!=0:
        x_c = sum(x_c_s) // len(x_c_s)
        y_c = sum(y_c_s) // len(y_c_s)
    else
        x_c,y_c = 0,0
        
    return x_c,y_c

def findColor(img,myColors,myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        x,y=getContours(mask)
        cv2.circle(imgResult,(x,y),15,myColorValues[count],cv2.FILLED)
        count +=1
    return x,y

def empty(a):
    pass
cv2.namedWindow("HSV")
cv2.resizeWindow("HSV",640,240)
cv2.createTrackbar("Hue Min","HSV",17,179,empty)
while True:
    h_min = cv2.getTrackbarPos("Hue Min","HSV")
    success, img = cap.read()
    imgResult = img.copy()
    x,y = findColor(img, myColors,myColorValues)
    print(x,y)
 
    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) & h_min>170:
        break
        
cap.release()
cv2.destroyAllWindows()


