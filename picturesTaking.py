import numpy as np
import cv2
import os
from getkey import getkey, keys
import time


class picturesTaking():
    def __init__(self):
        pass

    def run(self):
        
        cap = cv2.VideoCapture(0)
        print("Here take video")
        img_counter = 0
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
        target_path = os.getcwd() + "/pictures"
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Please press any key on keyboard to continue.")
        key = getkey()
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("Please type in your name.")
        name = input()
        if name == "exit":
            print("exiting add person\n\n")
            time.sleep(2)
            os.system('cls' if os.name == 'nt' else 'clear')
            return
        
        path = os.path.join(target_path, "{}".format(name))
        isExist = os.path.exists(path)

        if not isExist:
            os.makedirs(path)
            print("Your file is created!")

        print("Please take 20 pictures.")
        while img_counter < 20:
            ret, frame = cap.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces_rect = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1)
            
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
                
                print("Press [a] to add photo")
                print("Press [d] to delete photo")
                k = cv2.waitKey(0)
                key = k%256
                while(key != 27 and key != 97 and key != 100):
                    print("Wrong key. Try again.")
                    print("Press [a] to add photo")
                    print("Press [d] to delete photo")
                    k = cv2.waitKey(0)
                    key = k%256


                if k%256 == 27:
                    # ESC pressed
                    print("Escape hit, closing...")
                    break
                elif k%256 == 97:       # 32=space
                    # a pressed
                    img_name = os.getcwd() + "/pictures/{}/frame_{}.png".format(name, img_counter)
                    save_path = os.path.join(path, img_name)
                    cv2.imwrite(save_path, faces_roi)
                    print("{} written!".format(img_name))
                    img_counter += 1
                elif k%256 == 100:
                    # d pressed
                    pass
            else:
                cv2.imshow('ROI', frame)
                k = cv2.waitKey(1)
                if k%256 == 27:
                    # ESC pressed
                    print("Escape hit, closing...")
                    break
            
            
        cap.release()
        cv2.destroyAllWindows()
