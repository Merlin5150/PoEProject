#!/usr/bin/python
# NOTE: Make sure you run this via terminal! 
# DO NOT press ctrl + B in sublime
# Steps
# 1. Run the arduino file: StepperControl.ino
# 2. go to the directory of this file
# 3. type this in the command line: python serialWriting.py
# If you run this the old way (look in the last group of comments
# The "INPUT: " takes in a number of degrees to rotate by. Enter a number between 0 and 90

import numpy as np
import cv2
from matplotlib import pyplot as plt
# import scipy as sk

imgsize = 40
x_motor = []
y_motor = []

# Resizing the image:
img = cv2.imread('testpictures/smiley.png')
#Checking to make sure image exists
if img is None:
	flag = False
	print "Image failed to load. Please check image and/or try again."
else:
	flag = True
	print "image loaded!"

if flag == True:
	res = cv2.resize(img,(imgsize,imgsize), interpolation = cv2.INTER_AREA) # Resize image to 30x30 pixels
	print "width of new image: " + str(len(res[1])) 
	print "height of new image: " + str(len(res))
	# print "original image matrix: "
	# print res

newres = np.zeros((imgsize, imgsize))
#Reformats the res matrix and stores the result in the newres matrix. Also, starts filling in values into x_motor and y_motor
for i in range(imgsize):
	for j in range(imgsize):
		newres[i][j] = res[i][j][0]
		if newres[i][j] < 200:
			x_motor.append(i)
			y_motor.append(j)
			newres[i][j] = 0
		else:
			newres[i][j] = 255

print "x coordinates go from " + str(x_motor[0]) + " to " + str(x_motor[-1])
print "y coordinates go from " + str(y_motor[0]) + " to " + str(y_motor[-1])

#INITIALIZING VALUES:
Xcoord = x_motor[-1]
Ycoord = y_motor[-1]
remaining_coordinates = imgsize
# Starting at 0, 0
previousX = 0
previousY = 0
#The values we'll feed to the rotating method
a_list = []
#The number of steps that constitute a "sprixel" or "M&M pixel"
stepper_factor = 10  #change after we redefine what a sprixel is

# color codes: white = 0, black = 1
while (remaining_coordinates > 1):
	displacementX = Xcoord - previousX
	displacementY = Ycoord - previousY
	print "new x displacement: "
	print displacementX
	print "new y displacement: "
	print displacementY
	a_list.append(displacementX)
	a_list.append(displacementY)
	# a_list.append(chr(1)) #Color code
	print "x coordinate: "
	print Xcoord
	print "y coordinate:"
	print Ycoord
	previousX = Xcoord
	previousY = Ycoord
	del x_motor[-1]
	del y_motor[-1]
	print "updating this x coordinate to: "
	print x_motor[-1]
	Xcoord = x_motor[-1]
	print "updating this y coordinate to: "
	print y_motor[-1]
	Ycoord = y_motor[-1]
	remaining_coordinates = len(x_motor)

# a_list = ['90', '90', '90'] #A list of rotation values. Once we get rotation values for our image we should put them in this format.
# 							#Only rotates two times.
# >>>>>>> c85d7475afd6b9f8cc078e016aa430554c757913
# serial_port = serial.Serial(port, baud, timeout=0) 

#Running this function will be confusing at first. The motor will run even after the terminal seems finished
# def rotate(rotatingValuesList):
# 	i = 0
# 	for i in range(len(rotatingValuesList)):
# 		s = rotatingValuesList[i]
# 		print ord(s)
# 		serial_port.write(s.encode())
# 		i += 1

# rotate(a_list)

# serial_port.close()

# #Old attempt, because this worked for inputting stuff into terminal
# # while(serial_port.isOpen()):
# # 	##If you want to use
# # 	# s = raw_input("INPUT : ")
# # 	s = raw_input("INPUT IN DEGREES: ") #This should be here because this script mostly relies on an input.
# # 	s = '15'; # Hopefully we can modify this to take in some data later. 
# # 	serial_port.write(s.encode())




# 	print "new image matrix: "
# 	print res

# 	color = np.reshape(res, (-1,1))

# while flag == True:
# 	cv2.imshow('BW',res)
# 	key = cv2.waitKey(1) & 0xFF

# 	if key == ord("q"):
# 		break