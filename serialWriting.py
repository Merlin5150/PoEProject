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
import serial 
from matplotlib import pyplot as plt
import time
# import scipy as sk

imgsize = 10
x_motor = []
y_motor = []

# Resizing the image:
img = cv2.imread('testpictures/line.png')
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

print "x coordinates go from " + str(x_motor[0]) + " to " + str(x_motor[-1]) + " and has this length: " + str(len(x_motor))
print "y coordinates go from " + str(y_motor[0]) + " to " + str(y_motor[-1]) + " and has this length: " + str(len(y_motor))

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
	if (displacementX > 0):
		a_list.append(chr(1))
	else:
		a_list.append(chr(0))
	a_list.append(chr(np.abs(displacementX)))

	if (displacementY > 0):
		a_list.append(chr(1))
	else:
		a_list.append(chr(0))
	a_list.append(chr(np.abs(displacementY)))
	# a_list.append(chr(1)) #Color code
	# print "x coordinate: "
	# print Xcoord
	# print "y coordinate:"
	# print Ycoord
	previousX = Xcoord
	previousY = Ycoord
	del x_motor[-1]
	del y_motor[-1]
	# print "updating this x coordinate to: "
	# print x_motor[-1]
	Xcoord = x_motor[-1]
	# print "updating this y coordinate to: "
	# print y_motor[-1]
	Ycoord = y_motor[-1]
	remaining_coordinates = len(x_motor)

# a_list = ['90', '90', '90'] #A list of rotation values. Once we get rotation values for our image we should put them in this format.
# 							#Only rotates two times.
# >>>>>>> c85d7475afd6b9f8cc078e016aa430554c757913
port = '/dev/ttyACM0'
serial_port = serial.Serial(port, baudrate=9600, timeout=1, xonxoff=True)
# serial_port = serial.Serial(port, baud, timeout=0) 

#Running this function will be confusing at first. The motor will run even after the terminal seems finished
def rotate(rotatingValuesList):
	flag = True
	while flag:
		if serial_port.inWaiting() > 0:
			serial_port.flushInput()
			print "flushed"
			flag = False


	barr = bytearray(rotatingValuesList)
	for b in barr:
		print b,
	print '\n'
	for i in range(0, len(barr), 4):
		print [c for c in barr[i:i+4]]
		serial_port.write(barr[i:i+4])
		time.sleep(5)
		# print barr, 'test'

	# 	print bytearray(rotatingValuesList)
	# serial_port.write(bytearray(rotatingValuesList))
rotate(a_list)
serial_port.flushInput()
serial_port.close()