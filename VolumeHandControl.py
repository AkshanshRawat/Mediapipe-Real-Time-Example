from pickle import FALSE
import cv2 as cv
import mediapipe as mp
import numpy as np
import time
import math
import HandDetectingModule as hdm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
width_cam,hight_cam=640,480
cap=cv.VideoCapture(0)
cap.set(3,width_cam)
cap.set(4,hight_cam)


prev_time=0
curr_time=0

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volumeRange=volume.GetVolumeRange()
minVolume=volumeRange[0]
maxVolume=volumeRange[1]
vol=0
detector=hdm.handDetector(det_confidence=0.75)
while True:
    isTrue,frame=cap.read()
    if(isTrue):
        frame=cv.flip(frame,1)
        frame=detector.find_Hands(frame,draw=True)
        handlm=detector.find_Pos(frame)
        if(len(handlm)!=0):
            # print(handlm[4],handlm[8])

            cv.circle(frame,handlm[4][1:],5,(255,255,0),-1)
            cv.circle(frame,handlm[8][1:],5,(255,255,0),-1)
            cv.line(frame,handlm[4][1:],handlm[8][1:],(255,255,0),2)
            x1,y1,x2,y2=handlm[4][1],handlm[4][2],handlm[8][1],handlm[8][2]
            cv.circle(frame,((x1+x2)//2,(y1+y2)//2),5,(255,255,0),-1)
            length_line=math.hypot(x2-x1,y2-y1)
            # print(length_line)
            if length_line<=30:
                length_line=30
                cv.circle(frame,((x1+x2)//2,(y1+y2)//2),7,(0,0,255),-1)
            elif length_line>=120:
                length_line=120
                cv.circle(frame,((x1+x2)//2,(y1+y2)//2),7,(255,0,255),-1)
        # *** USING pycaw ***
            vol=np.interp(length_line,(30,120),(minVolume,maxVolume))
        volume.SetMasterVolumeLevel(vol, None)
        cv.rectangle(frame,(50,150),(85,400),(0,255,0),3)
        Readable_volume=int( np.interp(vol,(-62.5,0),(0,100)))
        cv.putText(frame,f'Volume: {Readable_volume }',(30,120),cv.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        
        cv.rectangle(frame,(50,int(np.interp(vol,(-62.5,0),(400,150)))),(85,400),(0,255,0),-1)
            

      
        
        
        curr_time=time.time()
        fps=1/(curr_time-prev_time)
        prev_time=curr_time
        cv.putText(frame,f'FPS: {int(fps)}',(10,50),cv.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)     
        cv.imshow("Cam",frame)
        

    if(cv.waitKey(1) & 0xFF==ord('q')):
        break
        
cap.release()