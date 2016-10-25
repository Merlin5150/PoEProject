import numpy as np
import cv2
 
im = cv2.imread('frisk.jpg')
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
# How do I get the image?
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# http://docs.opencv.org/master/d4/d73/tutorial_py_contours_begin.html
cv2.drawContours(img, contours, -1, (0,255,0), 3)