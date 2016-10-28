import numpy as np
import cv2
import imutils
import argparse
from sklearn.cluster import KMeans

ap = argparse.ArgumentParser()

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
        self.greenLower = (29,30,6)
        self.greenUpper = (64,255,255)

        self.Lower = [self.yellowLower,self.greenLower]
        self.Upper =[self.yellowUpper,self.greenUpper]

    # def squareseg(self, img):
    #         image = img
    #         image = image.reshape((image.shape[0] * image.shape[1], 3))

    #         args = vars(ap.parse_args())

    #         # cluster the pixel intensities
    #         clt = KMeans(n_clusters = args["clusters"])
    #         clt.fit(image)


    def getcontours(self, Lower, Upper):
        image = self.pixpic
        # Resizes the frame, blurs the frame, converts to HSV color space
        img = imutils.resize(image, width=600)
        self.resize_img = image
        blurredinit = cv2.GaussianBlur(image,(5,5),0)
        blurred = cv2.medianBlur(blurredinit,29) 
        hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)


        for iterator in range(0,2):
            # Constructs a mask for "green" objects, performs dilations and erosions to remove erroneous parts of the mask
            mask = cv2.inRange(hsv, Lower[iterator], Upper[iterator])
            mask = cv2.erode(mask,None,iterations=1)

            # Finds contours in the mask, initializes the current (x,y) center
            self.cnts = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]

            #Draws all contours.
            if len(self.cnts) > 0:
                cv2.drawContours(blurred, self.cnts, -1, (0,255,0), 3)
                cv2.drawContours(self.pixpic, self.cnts, -1, (0,255,0), 3)
        return

    # def findcenter(self):
    #         #Finds center of largest contour area
    #         # Find the largest contour in the mask, use it to compute the minimum enclosing circle and centroid for that contour
    #         c = max(self.cnts,key=cv2.contourArea)
    #         M = cv2.moments(c)
    #         (center,radius) = cv2.minEnclosingCircle(c)
    #         Mlist= [M["m10"], M["m00"],M["m01"],M["m00"]]

    #         if any(Mlist) == 0:
    #             return None
    #         else:
    #             center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
    #             return [center,radius]

    def pixellate(self, img):

        #Pixellates image via color quantization and K-means clustering
        Z = img.reshape((-1,30))

        # convert to np.float32
        Z = np.float32(Z)

        # define criteria, number of clusters(K) and apply kmeans()
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 5
        ret,label,center=cv2.kmeans(Z,K,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

        # Now convert back into uint8, and make original image
        center = np.uint8(center)
        res = center[label.flatten()]
        self.pixpic = res.reshape((img.shape))
        return

    def imshow(self, pic, pixpic):
        # cv2.circle(picture.img,center[0],int(center[1]),(255,255,255))
        cv2.imshow('image',picture.img)
        cv2.imshow('Pixellated image',pixpic)
        k = cv2.waitKey(0) & 0xFF
        if k == 27:         # wait for ESC key to exit
            cv2.destroyAllWindows()

if __name__ == '__main__':

# ****************** INITIALIZING STUFF ****************** #
    picture = PictureManager()
    # picture.squareseg(picture.img)
    picture.pixellate(picture.img)
    picture.getcontours(picture.Lower, picture.Upper)
    picture.imshow(picture.img, picture.pixpic)