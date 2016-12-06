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

path = "/home/arianaolson/PoEProject/UPDATED_image_seg"


# Check current working directory.
retval = os.getcwd()
print "Current working directory %s" % retval

# Now change the directory
os.chdir( path )

# Check current working directory.
retval = os.getcwd()

print "Directory changed successfully to %s" % retval

img = cv2.imread('smiley.png')

#Checking to make sure image exists
if img is None:
	flag = False
	print "Image failed to load. Please check image and/or try again."
else:
	flag = True
	print "image loaded!"

if flag == True:
# <<<<<<< HEAD
# 	size = image.shape
# 	# print size # Original size of picture
# 	imagepixels = np.reshape(image, (-1,1))

# 	##### Uncomment to view pixel values for image 'image'#####
# 	# for value in image:
# 	# 	print value

# 	current_pixel = 0

# 	# List of color values being sent to the printer
# 	color = []

# 	while current_pixel < 900:
# 		# if imagepixels[current_pixel] == 0:
# 		# 	print "black"
# 		# if imagepixels[current_pixel] == 255:
# 		# 	print 'white'
# 		current_pixel = current_pixel + 90
	
# 		color.append(imagepixels[current_pixel-1])


# 	##### Uncomment to visualize image and resized 1x? image. #####

# 	# key = cv2.waitKey(1) & 0xFF
# 	# cv2.imshow('original', image)
# 	# cv2.imshow('resized',imagepixels[0:900])
# 	# cv2.waitKey()
# 	# if key == ord("q"):
# 	# 	# Release the camera, close open windows
# 	# 	flag = False
# 	# 	cv2.destroyAllWindows()
# 	# flag = False

# #####################################################


# import serial, struct, threading
# from time import sleep

# #instance variables
# connected = False
# port = '/dev/ttyACM0'
# baud = 9600
# serial_port = serial.Serial(port, baud, timeout=0) 


# a_list = []
# # color codes: white = 0, black = 1
# for value in color:
# 	if value == 255:
# 		print "white"
# 		a_list.append(chr(40))
# 		a_list.append(chr(20))
# 		a_list.append(chr(0))
# 		# a_list.append('40w')

# 	else:
# 		print "black"
# 		a_list.append(chr(10))
# 		a_list.append(chr(10))
# 		# a_list.append(chr(1))
# 		# a_list.append('10b')
# 		sleep(1)

# # a_list = ['90', '90', '90'] #A list of rotation values. Once we get rotation values for our image we should put them in this format.
# # 							#Only rotates two times.
# # >>>>>>> c85d7475afd6b9f8cc078e016aa430554c757913
# =======
# 	res = cv2.resize(img,(30,30), interpolation = cv2.INTER_AREA) # Resize image to 30x30 pixels
# 	print "width of new image: " + str(len(res[1])) 
# 	print "height of new image: " + str(len(res))
# 	print "original image matrix: "
# 	print res


# 	for i in range(len(res)):
# 		for j in range(len(res[i])):
# 			print res[i][j]
# 			if res[i][j] < 200:
# 				res[i][j] = 0
# 			else:
# 				res[i][j] = 255

# # 	print "new image matrix: "
# # 	print res

# # 	color = np.reshape(res, (-1,1))

# # while flag == True:
# # 	cv2.imshow('BW',res)
# # 	key = cv2.waitKey(1) & 0xFF

# # 	if key == ord("q"):
# # 		break

# # #####################################################


# # import serial, struct, threading
# # from time import sleep

# # #instance variables
# # connected = False
# # port = '/dev/ttyACM0'
# # baud = 9600
# >>>>>>> 7f3498ab42e45288da9def503161226943955f4c
# # serial_port = serial.Serial(port, baud, timeout=0) 


# # a_list = []
# # # color codes: white = 0, black = 1
# # for value in color:
# # 	if value == 255:
# # 		print "white"
# # 		a_list.append(chr(40))
# # 		a_list.append(chr(20))
# # 		a_list.append(chr(0))
# # 		# a_list.append('40w')

# # 	else:
# # 		print "black"
# # 		a_list.append(chr(10))
# # 		a_list.append(chr(10))
# # 		a_list.append(chr(1))
# # 		# a_list.append('10b')
# # 		sleep(1)

# # # a_list = ['90', '90', '90'] #A list of rotation values. Once we get rotation values for our image we should put them in this format.
# # # 							#Only rotates two times.
# # # >>>>>>> c85d7475afd6b9f8cc078e016aa430554c757913
# # # serial_port = serial.Serial(port, baud, timeout=0) 



# <<<<<<< HEAD
# #Running this function will be confusing at first. The motor will run even after the terminal seems finished
# =======
# # #Running this function will be confusing at first. The motor will run even after the terminal seems finished
# >>>>>>> 7f3498ab42e45288da9def503161226943955f4c
# # def rotate(rotatingValuesList):
# # 	i = 0
# # 	# for i in range(len(rotatingValuesList)):

# # 	for i in range(len(rotatingValuesList)):
		
# # 		s = rotatingValuesList[i]
# # 		print ord(s)
# # 		serial_port.write(s.encode())
# # 		i += 1

# # rotate(a_list)
# <<<<<<< HEAD
# serial_port.write(a_list)

# serial_port.close()

# #Old attempt, because this worked for inputting stuff into terminal
# # while(serial_port.isOpen()):
# # 	##If you want to use
# # 	# s = raw_input("INPUT : ")
# # 	s = raw_input("INPUT IN DEGREES: ") #This should be here because this script mostly relies on an input.
# # 	s = '15'; # Hopefully we can modify this to take in some data later. 
# # 	serial_port.write(s.encode())
# =======

# # serial_port.close()

# # #Old attempt, because this worked for inputting stuff into terminal
# # # while(serial_port.isOpen()):
# # # 	##If you want to use
# # # 	# s = raw_input("INPUT : ")
# # # 	s = raw_input("INPUT IN DEGREES: ") #This should be here because this script mostly relies on an input.
# # # 	s = '15'; # Hopefully we can modify this to take in some data later. 
# # # 	serial_port.write(s.encode())
# >>>>>>> 7f3498ab42e45288da9def503161226943955f4c
