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
paint_dir=os.listdir('Painting')

detector=hdm.handDetector()
paint_lst=[]


for id in paint_dir:
    img=cv.imread(f'Painting/{id}')
    img=cv.resize(img,(1080,700),cv.INTER_AREA)
    img=img[0:130,0:1080]
    paint_lst.append(img)

blank=np.zeros((720, 1280, 3),dtype='uint8')

mode='Selection'
color=(0,0,255)
xp,yp=0,0
paint_thickness=3
eraser_thickness=22
curr_select=paint_lst[0]
m=1
while True:
    isTrue,frame=cap.read()
    if(isTrue):
        frame=cv.flip(frame,1)
        detector.find_Hands(frame)
        lm=detector.find_Pos(frame)
        
        frame[0:130,0:1080]=curr_select
        curr_time=time.time()
        fps=1/(curr_time-prev_time)
        prev_time=curr_time
        #Painting
        if(len(lm)!=0):
            if(lm[8][2]<lm[6][2] and lm[12][2]<lm[10][2]):
                xp,yp=0,0
                mode='Selection'
                if lm[8][2]<130:
                    if lm[8][1]>240 and lm[8][1]<450:
                        color=(0,0,255)
                        curr_select=paint_lst[0]
                    elif lm[8][1]>=450 and lm[8][1]<650:
                        color=(255,0,0)
                        curr_select=paint_lst[1]
                    elif lm[8][1]>=650 and lm[8][1]<830:
                        color=(0,255,0)
                        curr_select=paint_lst[2]
                    elif lm[8][1]>=830 and lm[8][1]<1040:
                        color=(0,0,0)
                        curr_select=paint_lst[3]
                        

            elif(lm[8][2]<lm[6][2]):
                mode='Drawing'
                if(xp==0 and yp==0):
                    xp,yp=lm[8][1],lm[8][2]
                else:
                    if(m==1):
                        cv.line(blank,(xp,yp),(lm[8][1],lm[8][2]),color,paint_thickness)
                    else:
                        cv.line(blank,(xp,yp),(lm[8][1],lm[8][2]),color,eraser_thickness)
                       
                    xp,yp=lm[8][1],lm[8][2]

        
        cv.putText(frame,f'FPS: {int(fps)}',(10,50),cv.FONT_HERSHEY_COMPLEX,1,(255,255,0),2)
        cv.rectangle(frame,(1080,0),(2000,130),(255,255,255),-1)
        cv.putText(frame,f'{mode}',(1080,50),cv.FONT_HERSHEY_COMPLEX,1,(255,255,0),2)    
        cv.putText(frame,f'Mode',(1080,100),cv.FONT_HERSHEY_COMPLEX,1,(255,255,0),2)  
        imgGray=cv.cvtColor(blank,cv.COLOR_BGR2GRAY)         
        _,imgInv=cv.threshold(imgGray,25,255,cv.THRESH_BINARY_INV)
        imgInv=cv.cvtColor(imgInv,cv.COLOR_GRAY2BGR)
        frame=cv.bitwise_and(frame,imgInv)
        frame=cv.bitwise_or(frame,blank)
        cv.imshow("Cam",frame)  
        
        if(cv.waitKey(1) & 0xFF==ord('q')):
            break
    else:
        break
    
cap.release()