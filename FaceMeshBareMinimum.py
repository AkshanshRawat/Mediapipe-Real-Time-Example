import cv2 as cv
import mediapipe as mp
import time

cap=cv.VideoCapture(0)
prev_time=0
curr_time=0
mpDraw=mp.solutions.drawing_utils
drawSpec=mpDraw.DrawingSpec(color=(255,255,0),thickness=1, circle_radius=1)
mpFaceMesh=mp.solutions.face_mesh
facemesh=mpFaceMesh.FaceMesh(max_num_faces=2)

while True:
    isTrue,frame=cap.read()
    if(isTrue):
        frame=cv.flip(frame,1)
        # frame=cv.resize(frame,(900,600))
        imgRGB=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        results=facemesh.process(imgRGB)
        if results.multi_face_landmarks:
            for face in results.multi_face_landmarks:
                mpDraw.draw_landmarks(frame,face,mpFaceMesh.FACEMESH_TESSELATION,drawSpec,drawSpec)
                # mpDraw.draw_landmarks(frame,face,mpFaceMesh.FACEMESH_IRISES)
                # mpDraw.draw_landmarks(frame,face,mpFaceMesh.FACEMESH_CONTOURS,drawSpec,drawSpec)
                for id,lm in enumerate(face.landmark):
                    # print(lm)
                    ih,iw=frame.shape[:2]
                    x,y=int(iw*lm.x),int(lm.y*ih)
                    print(id,x,y)

                
        curr_time=time.time()
        fps=1/(curr_time-prev_time)
        prev_time=curr_time
        cv.putText(frame,f'FPS: {int(fps)}',(10,50),cv.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)     
        cv.imshow("Cam",frame)
            

    if(cv.waitKey(1) & 0xFF==ord('q')):
        break
    
cap.release()