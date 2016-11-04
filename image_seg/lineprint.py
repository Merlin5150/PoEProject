import numpy as np
import cv2

# class PictureManager(object):
#     # Displays image 
#     def __init__(self):
#     	blackcolor = (0,0,0)

    # def findcenter(self):

flag = True
image = cv2.imread('line.jpg')

while True:

	if flag == True:
		size = image.shape
		imagepixels = np.reshape(image, (-1,1))
		# print imagepixels
		current_pixel = 0
		color = []

		while current_pixel < len(imagepixels):
			# print current_pixel
			# print len(imagepixels)
			current_pixel = current_pixel + 900
			color.append(imagepixels[current_pixel-1])
			
		for value in color:
			print value

		flag = False

	# cv2.imshow('Line', image)

	key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break