from sense_hat import SenseHat
import numpy as np
import cv2
import time
import os
import shutil

import picturesTaking as pt
import faceTrain as ft
import faceDel as fd
import faceReco as fr
import faceVaild as fvaild

sense = SenseHat()

recog = fr.faceReco()
pic = pt.picturesTaking()
train = ft.faceTrain()
delete = fd.faceDel()
vaild = fvaild.faceVaild()

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(3.5) # Initialization

def main():
    pic = pt.picturesTaking()
    train = ft.faceTrain()
    recog = fr.faceReco()
    delete = fd.faceDel()

    while True:
        print("1. Add a person")
        print("2. Delete a person")
        print("3. Run face recognition")
        print("4  Train model")
        print("5. Lock")
        print("6. Unlock")
        print("7. Quit")
        
        print("Please choose from [1], [2], [3] etc..")

        members = delete.PrintMembers('people.txt')
        userIn = input()
        if userIn == "1":
            pic.run()
            train.run()
        elif userIn == "2":
            delete.run()
        elif userIn == "3":
            recog.run()
        elif userIn == "4":
            train.run()
        elif userIn == "5":
            p.ChangeDutyCycle(3.5)
        elif userIn == "6":
            p.ChangeDutyCycle(7.5)	
        elif userIn == "7":
            print("Quit")
            return

main()
