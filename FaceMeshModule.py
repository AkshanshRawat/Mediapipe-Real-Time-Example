import cv2 as cv
import mediapipe as mp
import time



class FaceMeshDetection():
    def __init__(self,image_mode=False,num_faces=1,refined_landmarks=False,detection_confidence=0.5,tracking_confidence=0.5):
        self.image_mode=image_mode
        self.num_faces=num_faces
        self.refined_landmarks=refined_landmarks
        self.detection_confidence=detection_confidence
        self.tracking_confidence=tracking_confidence
        self.mpDraw=mp.solutions.drawing_utils
        self.drawSpec=self.mpDraw.DrawingSpec(color=(255,255,0),thickness=1, circle_radius=1)
        self.mpFaceMesh=mp.solutions.face_mesh
        self.facemesh=self.mpFaceMesh.FaceMesh(self.image_mode,self.num_faces,self.refined_landmarks,self.detection_confidence,self.tracking_confidence)
    def detectfacemesh(self,img):
        imgRGB=cv.cvtColor(img,cv.COLOR_BGR2RGB)
        results=self.facemesh.process(imgRGB)
        if results.multi_face_landmarks:
            faces_list=[]
            for face in results.multi_face_landmarks:
                self.mpDraw.draw_landmarks(img,face,self.mpFaceMesh.FACEMESH_TESSELATION,self.drawSpec,self.drawSpec)
                # mpDraw.draw_landmarks(frame,face,mpFaceMesh.FACEMESH_IRISES)
                # mpDraw.draw_landmarks(frame,face,mpFaceMesh.FACEMESH_CONTOURS,drawSpec,drawSpec)
                face_list=[]
                for id,lm in enumerate(face.landmark):
                    # print(lm)
                    ih,iw=frame.shape[:2]
                    x,y=int(iw*lm.x),int(lm.y*ih)
                    face_list.append((id,x,y))
                faces_list.append(face_list)
        return img,faces_list
if __name__=='__main__':
    cap=cv.VideoCapture(0)
    prev_time=0
    curr_time=0
    detector=FaceMeshDetection(num_faces=2)
    while True:
        isTrue,frame=cap.read()
        if(isTrue):
            frame=cv.flip(frame,1)
            # frame=cv.resize(frame,(900,600))
            frame,face=detector.detectfacemesh(frame)

            if(len(face)!=0):
                print(face[0][4])      
            curr_time=time.time()
            fps=1/(curr_time-prev_time)
            prev_time=curr_time
            cv.putText(frame,f'FPS: {int(fps)}',(10,50),cv.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)     
            cv.imshow("Cam",frame)
                

        if(cv.waitKey(1) & 0xFF==ord('q')):
            break
        
    cap.release()