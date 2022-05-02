import numpy as np
import cv2
import time
import os
import shutil
from getkey import getkey, keys
import faceTrain as ft
train = ft.faceTrain()

class faceDel():
	def __init__(self):
		pass
        
	def PrintMembers(self, filename):
		members = []
		with open(filename, "r") as f:
			lines = f.readlines()
		with open(filename, "w") as f:
			for line in lines:
				# DS_Store will generate in Mac only, can delete the 'if' when using other OS
				if line.strip("\n") != ".DS_Store":
					f.write(line)
				members.append(line.strip("\n"))
		return members
    
	def run(self):
		members = self.PrintMembers('people.txt')

		if len(members) == 0:
			print("No stored person.")
			return
		
		os.system('cls' if os.name == 'nt' else 'clear')
		print("Please press any key on keyboard to continue.")
		key = getkey()
		os.system('cls' if os.name == 'nt' else 'clear')
		
		print("Input the name of the person from the list that you want to delete:")

		# -------------------- #
		# Print exist member
		for i, member in enumerate(members):
			print("{}. {}".format(i+1, member))
		# -------------------- #

		people = os.listdir('pictures')

		print("Please type in your name.")
		name = input()
		if name == "exit":
			print("exiting delete person\n\n")
			time.sleep(2)
			os.system('cls' if os.name == 'nt' else 'clear')
			return

		path = os.path.join(os.getcwd(), "pictures", name)
		isExist = os.path.exists(path)
		if isExist:
			shutil.rmtree(path)
			people = os.listdir('pictures')

			f = open("people.txt", "w")
			for person in people:
				f.write(person + '\n')
			f.close()
			
			members = self.PrintMembers('people.txt')
			if len(members) > 0:
				train.run()
			print("Person deleted")
			time.sleep(2)
			os.system('cls' if os.name == 'nt' else 'clear')
		else:
			print(name, "is NOT a valid input! Try again")
