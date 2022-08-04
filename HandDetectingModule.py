
from pickle import FALSE, NONE, TRUE
import cv2 as cv
import mediapipe as mp
import time



class handDetector():
    def __init__(self,img_mode=FALSE,hand_no=2,complexity=1,det_confidence=0.5,track_confidence=0.5):
        self.img_mode=img_mode
        self.hand_no=hand_no
        self.complexity=complexity
        self.det_confidence=det_confidence
        self.track_confidence=track_confidence
        self.mphand=mp.solutions.hands
        self.hands=self.mphand.Hands(self.img_mode,self.hand_no,self.complexity,self.det_confidence,self.track_confidence)
        self.mpDraw=mp.solutions.drawing_utils


    def find_Hands(self,img,draw=True):
        BGRimg=cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.result=self.hands.process(BGRimg)
        if(self.result.multi_hand_landmarks):
            for Handlandmark in self.result.multi_hand_landmarks:           
                if(draw):
                   
                    self.mpDraw.draw_landmarks(img,Handlandmark,self.mphand.HAND_CONNECTIONS)
        return img

    def find_Pos(self,img,handNo=0):
        lmList=[]
        if(self.result.multi_hand_landmarks):
            Handlandmark=self.result.multi_hand_landmarks[handNo] 
            for id,handmark in enumerate(Handlandmark.landmark):
                h,w,c=img.shape
                cx,cy=int(handmark.x*w),int(handmark.y*h)
                lmList.append((id,cx,cy))

        return lmList  
def main():
    cap=cv.VideoCapture(0)
    prev_time=0
    curr_time=0
    hd=handDetector()
    while True:
        isTrue,frame=cap.read()
        if(isTrue):
            frame=cv.flip(frame,1)
            frame=hd.find_Hands(frame)
            lmlist=hd.find_Pos(frame)
            if(len(lmlist)!=0):
                print(lmlist[4]) 
            curr_time=time.time()
            fps=1/(curr_time-prev_time)
            prev_time=curr_time
            cv.putText(frame,f'FPS: {int(fps)}',(10,50),cv.FONT_HERSHEY_COMPLEX,1,(255,255,0),2)     
            cv.imshow("Cam",frame)
            

        if(cv.waitKey(1) & 0xFF==ord('q')):
            break
    
    cap.release()

if __name__=="__main__":
    main()