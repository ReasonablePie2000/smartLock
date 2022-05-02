import numpy as np
import cv2
import time


class faceVaild():
	def __init__(self):
		pass

	def run(self, img):
		people = []

		f = open("people.txt", "r")
		names = f.readlines()

		for person in names:
			people.append(person[:-1])
		f.close()
        
		if len(people) == 0:
			return 10, "none"
        
		face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

		face_recongnizer = cv2.face.LBPHFaceRecognizer_create()
		face_recongnizer.read('face_trained.yml')

		detected = []
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

			label, confidence = face_recongnizer.predict(faces_roi)
			if confidence > 0.0 and confidence < 100.0:
				confidence = 100.0 - confidence
				vaildcon = True
			
			if len(people) > 0:
				if people[label] not in detected and vaildcon and confidence >= 50.0:
					return 1, people[label]
				else:
					return 0, "none"
			
		return -1, "none"
			
