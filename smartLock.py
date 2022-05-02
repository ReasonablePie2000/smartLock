from sense_hat import SenseHat
import numpy as np
import cv2
import time
import os
import shutil

import picturesTaking as pt
import faceTrain as ft
import faceDel as fd
import faceVaild as fvaild

sense = SenseHat()

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

green = (0, 255, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
white = (255,255,255)
nothing = (0,0,0)
pink = (255,105, 180)

G = green
R = red
O = nothing

pass_logo = [	O, O, O, O, O, O, O, G, 
				O, O, O, O, O, O, G, G,
				O, O, O, O, O, G, G, O, 
				G, O, O, O, G, G, O, O,
				G, G, O, G, G, O, O, O,
				G, G, G, G, O, O, O, O,
				G, G, G, O, O, O, O, O,
				G, G, O, O, O, O, O, O,]
	
	

denied_logo = [	R, R, O, O, O, O, R, R, 
				O, R, R, O, O, R, R, O,
				O, O, R, R, R, R, O, O, 
				O, O, O, R, R, O, O, O,
				O, O, O, R, R, O, O, O,
				O, O, R, R, R, R, O, O,
				O, R, R, O, O, R, R, O,
				R, R, O, O, O, O, R, R,]

nothing_logo = [O for i in range(64)]

sense.set_pixels(nothing_logo)


def joyStickMoved(events):
	for event in events:
		if event.direction == "middle" and event.action == "pressed":	#when middle is pressed, run faical recognition
			cap = cv2.VideoCapture(0)
			cv2.startWindowThread()
			continVaild = 0
			continInvaild = 0
			continNotdet = 0
			
			# if 3 continuous vaild face unlock door
			# if 3 continuous invalid face deny access
			# if 10 continuos no face detected deny access
			while continVaild < 3 and continInvaild < 3 and continNotdet < 10:				
				success, img = cap.read()
				cv2.imshow('ROI', img)
				k = cv2.waitKey(1)
				
				vaildFace, name = vaild.run(img)
				if vaildFace == 1:
					print("vaild")
					continVaild += 1
					continInvaild = 0
					continNotdet = 0
				elif vaildFace == 0:
					print("Invaild")
					continInvaild += 1
					continVaild = 0
					continNotdet = 0
					
				elif vaildFace == 10:
					print("No person in database")
					break
					
				else:
					print("Not detected")
					continInvaild = 0
					continVaild = 0
					continNotdet += 1
					
			cap.release()
			cv2.destroyAllWindows()
			
			if continVaild >= 3:			#if face matched unlock the door
				sense.set_pixels(pass_logo)
				time.sleep(0.5)
				sense.set_pixels(nothing_logo)
				p.ChangeDutyCycle(7.5)		#unlock
				sense.show_message("Welcome " + str(name) + "!")	#show welcome message
				time.sleep(3)
				p.ChangeDutyCycle(3.5)		#lock
				os.system('cls' if os.name == 'nt' else 'clear')
				
			else:	#if no matching face, display denied_logo
				sense.set_pixels(denied_logo)
				time.sleep(0.5)
				sense.set_pixels(nothing_logo)
				time.sleep(0.1)
				sense.set_pixels(denied_logo)
				time.sleep(0.5)
				sense.set_pixels(nothing_logo)
				os.system('cls' if os.name == 'nt' else 'clear')
				
		#when up is pressed, add person
		elif event.direction == "up" and event.action == "pressed":
			pic.run()
			train.run()	# Train the model with new person
			print("Person added and model trained successfully")
			time.sleep(2)
			os.system('cls' if os.name == 'nt' else 'clear')
		
		#when down is pressed, delete person
		elif event.direction == "down" and event.action == "pressed":
			delete.run()
			
		#when left is pressed, quit programe
		elif event.direction == "left" and event.action == "pressed":
			print("QUIT!")
			GPIO.cleanup()
			sense.set_pixels(nothing_logo)
			sense.show_message("Bye!", 0.06)
			os.system('cls' if os.name == 'nt' else 'clear')
			exit()

def main():
	
	#show welcome message
	sense.show_message("Welcome!", 0.06)
	
	#show temp and humi when no joystick action detected
	while True:
		events = sense.stick.get_events()
		if len(events) == 0:
			temp = sense.get_temperature()
			if temp > 30.0:
				backC = red
				TextC = yellow
			elif temp > 15.0:
				backC = nothing
				TextC = white
			else:
				backC = white
				TextC = blue
				
			tempPresent = str("Temp:") + str(int(temp)) + "C."
			sense.show_message(tempPresent, 0.06, text_colour=TextC, back_colour=backC)
		else:
			joyStickMoved(events)
			time.sleep(3)
		
		events = sense.stick.get_events()
		if len(events) == 0:
			humi = sense.get_humidity()
			if humi > 75.0:
				backC = red
				TextC = yellow
			else:
				backC = nothing
				TextC = white
				
			humiPresent = str("Humidity:") + str(int(humi)) + "%."
			sense.show_message(humiPresent, 0.06, text_colour=TextC, back_colour=backC)
		else:
			joyStickMoved(events)
			time.sleep(3)
		
		
if __name__ == "__main__":
	main()
