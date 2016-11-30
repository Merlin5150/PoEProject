import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('test.png',0)
edges = cv2.Canny(img,100,200)

print "img[1]: " 
print img[1]
print "img[2]: " 
print img[2]
print "img[3]: " 
print img[3]
print "width of image: " + str(len(img[1])) 
print "height of image: " + str(len(img))
print "one element of image: "  + str(img[0][502])

#SO, I think this array has 208 elements, each element is an array that has 508 elements

#MAYBE, we can use 

# # Code to show the edge image, which is the negation 
plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()