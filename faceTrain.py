import numpy as np
import cv2
import os
import time

class faceTrain():
    def __init__(self):
        pass

    def run(self):
        people = os.listdir('pictures')

        f = open("people.txt", "w")
        for person in people:
            f.write(person + '\n')
        f.close()

        DIR = "pictures"

        face_cascade = cv2.CascadeClassifier('../haarcascade_frontalface_default.xml')

        features = []
        labels = []
        def createTrain():
            for person in people:
                if person == '.DS_Store':
                    continue
                path = os.path.join(DIR, person)
                label = people.index(person)

                for img in os.listdir(path):
                    img_path = os.path.join(path, img)
                    img_array = cv2.imread(img_path)
                    gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)


                    features.append(gray)
                    labels.append(label)

        createTrain()
        features = np.array(features, dtype='object')
        labels = np.array(labels)

        face_recongnizer = cv2.face.LBPHFaceRecognizer_create()
        face_recongnizer.train(features, labels)

        face_recongnizer.save('face_trained.yml')
        np.save('features.npy', features)
        np.save('labels.npy', labels)

