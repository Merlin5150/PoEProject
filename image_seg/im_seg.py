import numpy as np
import cv2


class PictureManager(object):
    # Displays image 
    def __init__(self):
        self.img = cv2.imread('frisk.jpg')

        # Define some colors
        redColor = (0,0,255)
        greenColor = (0,255,0)
        blueColor = (255,0,0)
        whiteColor = (255,255,255)
        blackColor = (0,0,0)

        # Set pygame fake desktop size
        screenwidth = 600
        screenheight = 450

        greenLower = (29,86,6)
        greenUpper = (64,255,255)

    def imseg(self):
        cv2.imshow('image',self.img)
        k = cv2.waitKey(0) & 0xFF
        if k == 27:         # wait for ESC key to exit
            cv2.destroyAllWindows()

# Chunk of old code from here on- working on modifying it

class WebCam(object):
    """Runs the webcam and identifies green objects.
        return: center coordinates"""

    def __init__(self, bufsize = 100, counter = 0):
        self.camera = cv2.imread('frisk.jpg')

        self.bufsize = bufsize
        self.ap.add_argument("-b", "--buffer", type=int, default = 100,
            help="max buffer size")
        self.pts = deque(maxlen=bufsize)
        self.rad = []
        self.counter = counter

        self.calpts = deque(maxlen=bufsize)
        self.calrad = []
        self.calcounter = counter

    def getcenter(self, greenLower, greenUpper):
        self.args = vars(self.ap.parse_args())
        (self.grabbed, self.frame) = self.camera.read() # Grabs the current frame
        
        # Resizes the frame, blurs the frame, converts to HSV color space
        self.frame = imutils.resize(self.frame, width=600)
        blurred = cv2.GaussianBlur(self.frame,(11,11),0)
        hsv = cv2.cvtColor(self.frame,cv2.COLOR_BGR2HSV)

        # Constructs a mask for "green" objects, performs dilations and erosions to remove erroneous parts of the mask
        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.erode(mask,None,iterations=1)

        # Finds contours in the mask, initializes the current (x,y) center
        self.cnts = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]

    def update_webcam(self, center):
        # Draw a dot to represent the wand's coordinates
        cv2.circle(webcam.frame, center, 5, redColor, -1)

if __name__ == '__main__':

# ****************** INITIALIZING STUFF ****************** #
    picture = PictureManager()
    picture.imseg()