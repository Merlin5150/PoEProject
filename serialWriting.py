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

imgsize = 10	# side length of square image
x_motor = []
y_motor = []

# Resizing the image:
img = cv2.imread('testpictures/1.png')
#Checking to make sure image exists
if img is None:
	flag = False
	print "Image failed to load. Please check image and/or try again."
else:
	flag = True
	print "image loaded!"

if flag == True:
	res = cv2.resize(img,(imgsize,imgsize), interpolation = cv2.INTER_AREA) # Resize image to 10x10 pixels
	print "width of new image: " + str(len(res[1])) 
	print "height of new image: " + str(len(res))

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

# direction codes: BACKWARDS = 0, FORWARDS = 1
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

	previousX = Xcoord
	previousY = Ycoord

	del x_motor[-1]
	del y_motor[-1]

	Xcoord = x_motor[-1]
	Ycoord = y_motor[-1]

	remaining_coordinates = len(x_motor)


port = '/dev/ttyACM0' # change to match current port Arduino is connected to
serial_port = serial.Serial(port, baudrate=9600, timeout=1, xonxoff=True)	# open the serial port 


def rotate(rotatingValuesList):
	'''
	Converts the list of directions to a bytearray for transmission
	packets of 4 bytes are written to serial at a time

	rotatingValuesList: a list of commands specifying the direction and displacement 
	for each motor
	'''

	# Handshakes with the Arduino. 
	# The Arduino sends "Ready" over serial once calibration is complete
	flag = True
	while flag:
		if serial_port.inWaiting() > 0:
			serial_port.flushInput()	#clear the serial input buffer
			print "flushed"
			flag = False


	barr = bytearray(rotatingValuesList)
	for b in barr:
		print b,
	print '\n'
	for i in range(0, len(barr), 4):
		print [c for c in barr[i:i+4]]	
		serial_port.write(barr[i:i+4])
		time.sleep(5)	# this delay keeps the serial buffer from overflowing

rotate(a_list)
serial_port.flushInput() # prevents false starts if running script multiple times
serial_port.close()	# close the serial port.