import cv2 as cv
import mediapipe as mp
import time

class FaceDetecctor():
    def __init__(self, min_detect_confidence=0.5):
        self.min_detect_confidence=min_detect_confidence
        
        self.FacesD=mp.solutions.face_detection
        self.face_object=self.FacesD.FaceDetection(self.min_detect_confidence)
        
        # print(self.face_object.min_detection_confidence)
        self.drawing=mp.solutions.drawing_utils

    def detectFace(self,img):
        imgRGB=cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.result=self.face_object.process(imgRGB)
        if self.result.detections:
            for id,detect_it in enumerate(self.result.detections):
                boxC=detect_it.location_data.relative_bounding_box
                iy,ix=img.shape[:2]
                txt=detect_it.score[0]
                if(txt<self.min_detect_confidence):
                    print(txt)
                # if(txt>=self.min_detect_confidence):
                else:
                    box=int(boxC.xmin*ix),int(boxC.ymin*iy),int(boxC.width*ix),int(boxC.height*iy)
                    cv.rectangle(img,box,(255,0,255),2) 
                    cv.putText(img,f'{int(txt*100)}%',(box[0]-4,box[1]-4),cv.FONT_HERSHEY_COMPLEX,1,(255,0,255),1)
            
        return img

def main():
    cap=cv.VideoCapture(0)
    prev_time=0
    curr_time=0
    detector=FaceDetecctor(0.75)
    while True:
        isTrue,frame=cap.read()
        if(isTrue):
            frame=cv.flip(frame,1)
            # frame=cv.resize(frame,(900,600))
            frame=detector.detectFace(frame)
            
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