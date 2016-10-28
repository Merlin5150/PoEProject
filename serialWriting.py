#!/usr/bin/python
# NOTE: Make sure you run this via terminal! 
# DO NOT press ctrl + B in sublime
# Steps
# 1. Run the arduino file: StepperControl.ino
# 2. go to the directory of this file
# 3. type this in the command line: python serialWriting.py
# If you run this the old way (look in the last group of comments
# The "INPUT: " takes in a number of degrees to rotate by. Enter a number between 0 and 90


import serial, struct, threading
from time import sleep

#instance variables
connected = False
port = '/dev/ttyACM0'
baud = 9600
# a_list = ['25'] #A list of rotation values. Once we get rotation values for our image we should put them in this format.
							#Only rotates two times.
serial_port = serial.Serial(port, baud, timeout=0) 



#Running this function will be confusing at first. The motor will run even after the terminal seems finished
def rotate():
	i = 0
	# for i in range(len(rotatingValuesList)):
	while (2<3):
		print i
		s = '25'
		serial_port.write(s.encode())
		sleep(2) # this sleep(2) NEEDS to be in this loop! The stepper motor needs time to process.
		i += 1

rotate()







#Old attempt, because this worked for inputting stuff into terminal
# while(serial_port.isOpen()):
# 	##If you want to use
# 	# s = raw_input("INPUT : ")
# 	s = raw_input("INPUT IN DEGREES: ") #This should be here because this script mostly relies on an input.
# 	s = '15'; # Hopefully we can modify this to take in some data later. 
# 	serial_port.write(s.encode())