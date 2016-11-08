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

path = "/home/lzuehsow/PoEProject/image_seg"

# Check current working directory.
retval = os.getcwd()
print "Current working directory %s" % retval

# Now change the directory
os.chdir( path )

# Check current working directory.
retval = os.getcwd()

print "Directory changed successfully %s" % retval


flag = True
image = cv2.imread('line.png')
image = image[0:30,0:300]

if flag == True:
	size = image.shape
	# print size
	imagepixels = np.reshape(image, (-1,1))
	# imagepixels = imagepixels[0:-1]

	# for value in image:
	# 	print value

	# print imagepixels[0:300]
	current_pixel = 0
	color = []

	while current_pixel < 900:
		# print current_pixel
		if imagepixels[current_pixel] == 0:
			print "black"
		if imagepixels[current_pixel] == 255:
			print 'white'
		current_pixel = current_pixel + 90
		# print imagepixels[current_pixel-1]
	
		color.append(imagepixels[current_pixel-1])

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


# import serial, struct, threading
# from time import sleep

# #instance variables
# connected = False
# port = '/dev/ttyACM0'
# baud = 9600


# a_list = []

# for value in color:
# 	if value == 255:
# 		print "black"
# 		a_list.append('10b')

# 	else:
# 		print "white"
# 		a_list.append('40w')
# 		sleep(1)

# # a_list = ['90', '90', '90'] #A list of rotation values. Once we get rotation values for our image we should put them in this format.
# # 							#Only rotates two times.
# # >>>>>>> c85d7475afd6b9f8cc078e016aa430554c757913
# # serial_port = serial.Serial(port, baud, timeout=0) 



# #Running this function will be confusing at first. The motor will run even after the terminal seems finished
# def rotate(rotatingValuesList):
# 	i = 0
# 	# for i in range(len(rotatingValuesList)):
# 	for i in range(len(rotatingValuesList)):
		
# 		s = a_list[i]
# 		print s
# 		serial_port.write(s.encode())
# 		sleep(2) # this sleep(2) NEEDS to be in this loop! The stepper motor needs time to process.
# 		i += 1

# rotate(a_list)


# #Old attempt, because this worked for inputting stuff into terminal
# # while(serial_port.isOpen()):
# # 	##If you want to use
# # 	# s = raw_input("INPUT : ")
# # 	s = raw_input("INPUT IN DEGREES: ") #This should be here because this script mostly relies on an input.
# # 	s = '15'; # Hopefully we can modify this to take in some data later. 
# # 	serial_port.write(s.encode())