import pyautogui
import os
import cv2 as cv
import time
import HandDetectingModule as hdm
import numpy as np


width_cam,hight_cam=1080,1080
cap=cv.VideoCapture(0)
cap.set(3,width_cam)
cap.set(4,hight_cam)
prev_time=0
curr_time=0
screenWidth,screenHeight=pyautogui.size()
print(screenWidth,screenHeight)
detector=hdm.handDetector()
mode=''

smooth=5
xprev,yprev=0,0
xmove,ymove=0,0
while True:
    isTrue,frame=cap.read()
    if(isTrue):
        frame=cv.flip(frame,1)
        detector.find_Hands(frame)
        lm=detector.find_Pos(frame)
        onscreenHeight,onscreenWidth=550,1120
        height,width=frame.shape[:2]
        curr_time=time.time()
        fps=1/(curr_time-prev_time)
        prev_time=curr_time
        
        if(len(lm)!=0):
            x1,y1=lm[8][1],lm[8][2]
            x2,y2=lm[12][1],lm[12][2]
            if x1>=100 and x1<=onscreenWidth and y1>=100 and y1<=onscreenHeight:
                if(lm[8][2]<lm[6][2] and lm[12][2]<lm[10][2]):
                    length=np.hypot(x1-x2,y1-y2)
                    xm=(x1+x2)//2
                    ym=(y1+y2)//2
                    cv.circle(frame,(xm,ym),3,(255,0,0),-1)
                    if(int(length)<40):
                        cv.circle(frame,(xm,ym),5,(0,0,255),-1)
                        pyautogui.click()

                        

                elif(lm[8][2]<lm[6][2]):


                    x3=np.interp(x1,(100,onscreenWidth),(0,screenWidth))
                    y3=np.interp(y1,(100,onscreenHeight),(0,screenHeight))
                    xmove=xprev+(x3-xprev)/smooth
                    ymove=yprev+(y3-yprev)/smooth
                    
                    pyautogui.moveTo(xmove, ymove, tween=pyautogui.easeInOutQuad)
                    xprev=xmove
                    yprev=ymove

        
        cv.putText(frame,f'FPS: {int(fps)}',(10,50),cv.FONT_HERSHEY_COMPLEX,1,(255,255,0),2)
        cv.rectangle(frame,(100,100),(onscreenWidth,onscreenHeight),(0,255,0),3)
        cv.imshow("Cam",frame)  
        # print(mode)
        if(cv.waitKey(1) & 0xFF==ord('q')):
            break
    else:
        break
    
cap.release()