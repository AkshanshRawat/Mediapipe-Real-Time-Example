from pickle import NONE
import cv2 as cv
import mediapipe as mp
import time

cap=cv.VideoCapture(0)
mphand=mp.solutions.hands
hands=mphand.Hands()
mpDraw=mp.solutions.drawing_utils

prev_time=0
curr_time=0

# x0,y0,x1,y1=0,0,1,1
while True:
    isTrue,frame=cap.read()
    if(isTrue):
        frame=cv.flip(frame,1)
        frameRGB=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        result=hands.process(frameRGB)
        # print(result.multi_hand_landmarks)
        if(result.multi_hand_landmarks):
            for Handlandmark in result.multi_hand_landmarks:
                for id,handmark in enumerate(Handlandmark.landmark):
                    # print(id,handmark)
                    print(id,end=": ")
                    # print(type(handmark))
                    h,w,c=frame.shape
                    cx,cy=int(handmark.x*w),int(handmark.y*h)
                    print(cx,cy)
                    if(id==0):
                        cv.circle(frame,(cx,cy),10,(0,0,255),-1)
                    # if(id==8):
                    #     x0=cx
                    #     y0=cy
                    # if(id==12):
                    #     x1=cx
                    #     y1=cy
                
                mpDraw.draw_landmarks(frame,Handlandmark,mphand.HAND_CONNECTIONS)
        # if(x0==x1 or y0==y1):
        #     break
        curr_time=time.time()
        fps=1/(curr_time-prev_time)
        prev_time=curr_time
        cv.putText(frame,f'FPS: {int(fps)}',(10,50),cv.FONT_HERSHEY_COMPLEX,1,(255,255,0),2)     
        cv.imshow("Cam",frame)

    if(cv.waitKey(1) & 0xFF==ord('q')):
        break

cap.release()