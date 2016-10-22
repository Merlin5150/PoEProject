import numpy as np
import cv2
import imutils


class PictureManager(object):
    # Displays image 
    def __init__(self):
        self.img = cv2.imread('sprinkles.jpg')
        self.cnts = []

        # # Define some colors
        # redColor = (0,0,255)
        # greenColor = (0,255,0)
        # blueColor = (255,0,0)
        # whiteColor = (255,255,255)
        # blackColor = (0,0,0)

        self.yellowLower = (20,100,100)
        self.yellowUpper = (30,255,255)
        self.greenLower = (29,86,6)
        self.greenUpper = (64,255,255)

        self.Lower = [self.yellowLower,self.greenLower]
        self.Upper =[self.yellowUpper,self.greenUpper]

    def getcontours(self, Lower, Upper):
        
        # Resizes the frame, blurs the frame, converts to HSV color space
        img = imutils.resize(self.img, width=600)
        blurred = cv2.GaussianBlur(self.img,(11,11),0)
        hsv = cv2.cvtColor(self.img,cv2.COLOR_BGR2HSV)

        for iterator in range(0,2):
            # Constructs a mask for "green" objects, performs dilations and erosions to remove erroneous parts of the mask
            mask = cv2.inRange(hsv, Lower[iterator], Upper[iterator])
            mask = cv2.erode(mask,None,iterations=1)

            # Finds contours in the mask, initializes the current (x,y) center
            self.cnts = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]

            if len(self.cnts) > 0:
                #Draws all contours.
                cv2.drawContours(self.img, self.cnts, -1, (0,255,0), 3)

            # #Finds center of largest contour area
            # # Find the largest contour in the mask, use it to compute the minimum enclosing circle and centroid for that contour
            # c = max(self.cnts,key=cv2.contourArea)
            # M = cv2.moments(c)
            # (center,radius) = cv2.minEnclosingCircle(c)
            # Mlist= [M["m10"], M["m00"],M["m01"],M["m00"]]

            # if any(Mlist) == 0:
            #     return None
            # else:
            #     center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
            #     return [center,radius]
        return

    def imseg(self, pic):
        # cv2.circle(picture.img,center[0],int(center[1]),(255,255,255))
        cv2.imshow('image',picture.img)
        k = cv2.waitKey(0) & 0xFF
        if k == 27:         # wait for ESC key to exit
            cv2.destroyAllWindows()

if __name__ == '__main__':

# ****************** INITIALIZING STUFF ****************** #
    picture = PictureManager()
    picture.getcontours(picture.Lower, picture.Upper)
    picture.imseg(picture.img)