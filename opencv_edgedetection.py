import cv2
import numpy as np
from matplotlib import pyplot as plt

# img = cv2.imread('testpictures/flower.jpg',0)
img = cv2.imread('testpictures/flower.jpg',0)

# edges = cv2.Canny(img,100,200)
# print img
# print "img[1]: " 
# print img[1]
# print "img[2]: " 
# print img[2]
# print "img[3]: " 
# print img[3]
# print "width of image: " + str(len(img[1])) 
# print "height of image: " + str(len(img))
# print "one element of image: "  + str(img[0][502])

#SO, I think this array has 208 elements, each element is an array that has 508 elements

#try resizing, help here: http://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html#void%20resize(InputArray%20src,%20OutputArray%20dst,%20Size%20dsize,%20double%20fx,%20double%20fy,%20int%20interpolation)
# Make fx & fy equal to the general scale of the cupcakes we use.
# res = cv2.resize(img,None,fx=.03, fy=.03, interpolation = cv2.INTER_AREA)

res = cv2.resize(img,(30,30), interpolation = cv2.INTER_AREA) # Resize image to 30x30 pixels
print "width of new image: " + str(len(res[1])) 
print "height of new image: " + str(len(res))
print "original image matrix: "
print res

x_motor = []
y_motor = []
for i in range(len(res)):
	for j in range(len(res[i])):
		if res[i][j] < 200:
			x_motor.append(i)
			y_motor.append(j)
			res[i][j] = 0
		else:
			res[i][j] = 255

print "new image matrix: "
print res

print "length of xmotor coordinates:" 
print len(x_motor)
print "length of ymotor coordinates:" 
print len(y_motor)

print "x-coordinates: "
print x_motor
print "y-coordinates: "
print y_motor


color = np.reshape(res, (-1,1))

# print "one element of new image: "  + str(res[0][502])
q = False

while q == False:
	cv2.imshow('BW',res)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break



# # # Code to show the edge image, which is the negation 
# plt.subplot(121),plt.imshow(img,cmap = 'gray')
# plt.title('original'), plt.xticks([]), plt.yticks([])
# # plt.subplot(122),plt.imshow(res,cmap = 'gray')
# # plt.title('modified'), plt.xticks([]), plt.yticks([])

# plt.subplot(122),plt.imshow(res,cmap = 'gray')
# plt.title('modified'), plt.xticks([]), plt.yticks([])


# plt.show()