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

#Changing the directory so that the result files are stored in a convenient place
import os

path = "/home/arianaolson/PoEProject/image_seg"

# Check current working directory.
retval = os.getcwd()
print "Current working directory %s" % retval

# Now change the directory
os.chdir( path )

# Check current working directory.
retval = os.getcwd()

print "Directory changed successfully to %s" % retval

image = cv2.imread('line.png')

#Checking to make sure image exists
if image is None:
	flag = False
	print "Image failed to load. Please check image and/or try again."
else:
	flag = True
	print "image loaded!"

#Making sure the image is the right size for later calculations
image = image[0:30,0:300]

if flag == True:
	size = image.shape
	# print size # Original size of picture
	imagepixels = np.reshape(image, (-1,1))

	##### Uncomment to view pixel values for image 'image'#####
	# for value in image:
	# 	print value

	current_pixel = 0

	# List of color values being sent to the printer
	color = []

	while current_pixel < 900:
		# if imagepixels[current_pixel] == 0:
		# 	print "black"
		# if imagepixels[current_pixel] == 255:
		# 	print 'white'
		current_pixel = current_pixel + 90
	
		color.append(imagepixels[current_pixel-1])


	##### Uncomment to visualize image and resized 1x? image. #####

	# key = cv2.waitKey(1) & 0xFF
	# cv2.imshow('original', image)
	# cv2.imshow('resized',imagepixels[0:900])
	# cv2.waitKey()
	# if key == ord("q"):
	# 	# Release the camera, close open windows
	# 	flag = False
	# 	cv2.destroyAllWindows()
	# flag = False

#####################################################


import serial, struct, threading
from time import sleep

#instance variables
connected = False
port = '/dev/ttyACM0'
baud = 9600
serial_port = serial.Serial(port, baud, timeout=0) 


a_list = []
# color codes: white = 0, black = 1
for value in color:
	if value == 255:
		print "white"
		a_list.append(chr(40))
		a_list.append(chr(20))
		a_list.append(chr(0))
		# a_list.append('40w')

	else:
		print "black"
		a_list.append(chr(10))
		a_list.append(chr(20))
		a_list.append(chr(1))
		# a_list.append('10b')
		sleep(1)

# a_list = ['90', '90', '90'] #A list of rotation values. Once we get rotation values for our image we should put them in this format.
# 							#Only rotates two times.
# >>>>>>> c85d7475afd6b9f8cc078e016aa430554c757913
# serial_port = serial.Serial(port, baud, timeout=0) 



#Running this function will be confusing at first. The motor will run even after the terminal seems finished
def rotate(rotatingValuesList):
	i = 0
	# for i in range(len(rotatingValuesList)):

	for i in range(len(rotatingValuesList)):
		
		s = a_list[i]
		print s
		serial_port.write(s.encode())
		sleep(2) # this sleep(2) NEEDS to be in this loop! The stepper motor needs time to process.
		i += 1

	rotate(a_list)
	# serial_port.close()

#Old attempt, because this worked for inputting stuff into terminal
# while(serial_port.isOpen()):
# 	##If you want to use
# 	# s = raw_input("INPUT : ")
# 	s = raw_input("INPUT IN DEGREES: ") #This should be here because this script mostly relies on an input.
# 	s = '15'; # Hopefully we can modify this to take in some data later. 
# 	serial_port.write(s.encode())