import numpy as np
import cv2
import time


class faceReco():
    def __init__(self):
        pass

    def run(self):
        people = []

        f = open("people.txt", "r")
        names = f.readlines()

        for person in names:
            people.append(person[:-1])
        f.close()
        
        cap = cv2.VideoCapture(0)
        cTime = 0
        pTime = 0
        cv2.startWindowThread()
        
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


        face_recongnizer = cv2.face.LBPHFaceRecognizer_create()
        face_recongnizer.read('face_trained.yml')
        
        
        while True:
            detected = []
            success, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces_rect = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1)
            vaildcon = False
            notDetected = True

            maxX = 0
            maxY = 0
            maxW = 0
            maxH = 0
            for (x,y,w,h) in faces_rect:
                if w > maxW and h > maxH:
                    maxX = x
                    maxY = y
                    maxW = w
                    maxH = h

            if(maxH > 200 and maxW > 100 and maxX > 0 and maxY > 0):
                faces_roi = gray[maxY:y+maxH, maxX:maxX+maxW]
                cv2.imshow('ROI', faces_roi)
                #cv2.waitKey(0)

                #cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), thickness=2)
                
                label, confidence = face_recongnizer.predict(faces_roi)
                if confidence > 0.0 and confidence < 100.0:
                    confidence = 100.0 - confidence
                    vaildcon = True
                
                if len(people) > 0:
                    if people[label] not in detected and vaildcon and confidence >= 50.0:
                        detected.append(people[label])
                        print(f'Label = {people[label]} with a condifence of {"%.2f" %confidence}%')
                        labelPresent = str(people[label]) + ": " + str(int(confidence)) + "%"
                        notDetected = False
                        cv2.putText(img, str(labelPresent), (maxX,maxY-15), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0,255,0), 1)
                        cv2.rectangle(img, (maxX,maxY), (maxX+maxW,y+maxH), (0,255,0), thickness=2)
                
                if (vaildcon and confidence < 50.0) or len(people) == 0:
                    labelPresent = "Unknow"
                    
                    cv2.putText(img, str(labelPresent), (maxX,maxY-15), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0,0,255), 1)
                    cv2.rectangle(img, (maxX,maxY), (maxX+maxW,y+maxH), (0,0,255), thickness=2)

            '''
            for (x,y,w,h) in faces_rect:
                faces_roi = gray[y:y+h, x:x+w]
                #cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), thickness=2)
                label, confidence = face_recongnizer.predict(faces_roi)
                if people[label] not in detected and confidence > 50.0 and confidence < 100.0:
                    detected.append(people[label])
                    print(f'Label = {people[label]} with a condifence of {confidence}')
                    labelPresent = str(people[label]) + ": " + str(int(confidence)) + "%"

                    cv2.putText(img, str(labelPresent), (x-20,y-20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 0, 0), 1)
                    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), thickness=2)
            '''
            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
            fpsPresent = "FPS: " + str(int(fps))
            cv2.putText(img, str(fpsPresent), (20,20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 255, 0), 1)

            cv2.imshow('Facial Recognition', img)
            k = cv2.waitKey(1)
            if k%256 == 27:
                # ESC pressed
                cap.release()
                cv2.destroyAllWindows()
                print("Escape hit, closing...")
                return
