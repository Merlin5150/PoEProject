import numpy as np
import cv2

#Changing the directory so that the result files are stored in a convenient place
import os

path = "/home/anne/PoEProject/UPDATED_image_seg"

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

	current_pixel = 0

	# List of color values being sent to the printer
	color = []

	while current_pixel < 900:
		current_pixel = current_pixel + 90
		color.append(imagepixels[current_pixel-1])


import serial, struct, threading
from time import sleep

#instance variables
connected = False
port = '/dev/ttyACM0'
baud = 9600
serial_port = serial.Serial(port, baud, timeout=0) 


a_list = []
for value in color:
	if value == 255:
		print "white"
		a_list.append(chr(40)) # the x motor
		a_list.append(chr(40)) # the y motor
		a_list.append(chr(0)) # the color code
		# a_list.append('40w')

	else:
		print "black"
		a_list.append(chr(40)) # the x motor
		a_list.append(chr(40)) # the y motor
		a_list.append(chr(1)) #the color code
		# a_list.append('10b')
		sleep(1)

def rotate(rotatingValuesList):
	i = 0

	for i in range(len(rotatingValuesList)):
		
		s = rotatingValuesList[i]
		print ord(s)
		serial_port.write(s.encode())
		i += 1

rotate(a_list)

serial_port.close()