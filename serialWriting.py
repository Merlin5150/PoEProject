#!/usr/bin/python
# NOTE: Make sure you run this via terminal! 
# DO NOT press ctrl + B in sublime
# Steps
# 1. Run the arduino file: StepperControl.ino
# 2. go to the directory of this file
# 3. type this in the command line: python serialWriting.py
# If you run this the old way (look in the last group of comments
# The "INPUT: " takes in a number of degrees to rotate by. Enter a number between 0 and 90

##############################################################
#Is jank, sorry
#I will fix it so it can run from it's own file. -L

import numpy as np
import cv2
# import scipy as sk

# class PictureManager(object):
#     # Displays image 
#     def __init__(self):
#     	blackcolor = (0,0,0)

    # def findcenter(self):

flag = True
image = cv2.imread('line.jpg')

if flag == True:
	# size = image.shape
	imagepixels = np.reshape(image, (-1,1))
	# print imagepixels
	current_pixel = 0
	color = []

	while current_pixel < len(imagepixels):
		# print current_pixel
		# print len(imagepixels)
		current_pixel = current_pixel + 900
		color.append(imagepixels[current_pixel-1])
		
	# for value in color:
	# 	print value

	flag = False

#####################################################


import serial, struct, threading
from time import sleep

#instance variables
connected = False
port = '/dev/ttyACM0'
baud = 9600

a_list = []

for value in color:
	if value == 255:
		a_list.append('40')
	else:
		pass

# a_list = ['90', '90', '90'] #A list of rotation values. Once we get rotation values for our image we should put them in this format.
# 							#Only rotates two times.
serial_port = serial.Serial(port, baud, timeout=0) 



#Running this function will be confusing at first. The motor will run even after the terminal seems finished
def rotate(rotatingValuesList):
	for i in range(len(rotatingValuesList)):
		s = a_list[i] 
		serial_port.write(s.encode())
		sleep(2) # this sleep(2) NEEDS to be in this loop! The stepper motor needs time to process.

rotate(a_list)


#Old attempt, because this worked for inputting stuff into terminal
# while(serial_port.isOpen()):
# 	##If you want to use
# 	# s = raw_input("INPUT : ")
# 	s = raw_input("INPUT IN DEGREES: ") #This should be here because this script mostly relies on an input.
# 	s = '15'; # Hopefully we can modify this to take in some data later. 
# 	serial_port.write(s.encode())