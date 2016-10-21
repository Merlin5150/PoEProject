import numpy as np
import cv2

# Displays image 

img = cv2.imread('frisk.jpg')
cv2.imshow('image',img)
k = cv2.waitKey(0) & 0xFF
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()


# Chunk of old code from here on- working on modifying it

class WebCam(object):
    """Runs the webcam and identifies green objects.
        return: center coordinates"""

    def __init__(self, bufsize = 100, counter = 0):
        self.camera = cv2.VideoCapture(0)
        self.ap = argparse.ArgumentParser()
        self.ap.add_argument("-v","--video",
            help="path to the(optional) video file")
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

# if __name__ == '__main__':

# # ****************** INITIALIZING STUFF ****************** #

#     # Initialize pygame
#     pygame.init()

#     # Define some colors
#     redColor = pygame.Color(0,0,255)
#     greenColor = pygame.Color(0,255,0)
#     blueColor = pygame.Color(255,0,0)
#     whiteColor = pygame.Color(255,255,255)
#     blackColor = pygame.Color(0,0,0)

#     # Set pygame fake desktop size
#     screenwidth = 600
#     screenheight = 450

#     size = (screenwidth, screenheight)
#     screen = pygame.display.set_mode(size)

#     greenLower = (29,86,6)
#     greenUpper = (64,255,255)

#     check = 0
#     frame = 0
#     spell_frame = 0
#     eventcount = 0
#     center = 0

#     webcam = WebCam()

#     # running = False
#     # running = True

#     BUTTON = pygame.USEREVENT+3
#     button_event = pygame.event.Event(BUTTON)

#     # Makes sure only the events we want are on the event queue
#     allowed_events = [QUIT,GRID,BUTTON]
#     pygame.event.set_allowed(allowed_events)

    
# # ****************** RUNTIME LOOP ****************** #
#     # This is the main loop of the program. 

#     while True:

#         if menu.gamerunning == True:
#             break
#         elif menu.tutorielrunning == True:
#             break

#         gotcenter = webcam.getcenter(greenLower, greenUpper)

#         if gotcenter == None:
#             master.selected = False
#         else:
#             center = gotcenter[0]
#             radius = gotcenter[1]

#             (x,y) = center

#             pygame.draw.circle(screen,menu.cursorcolor,(600-x,y),3,0)

#             if radius >= calradi + 15:
#                 pygame.event.post(button_event)
#                 menu.cursorcolor = redColor
#             else:
#                 menu.cursorcolor = blueColor

#         if key == ord("q"):
#             # Release the camera, close open windows
#             webcam.camera.release()
#             cv2.destroyAllWindows()
#             master.close()
#             pygame.quit()

#         time.sleep(.001)

#         # Find the center of any green objects' contours
#         gotcenter = webcam.getcenter(greenLower, greenUpper)
#         if gotcenter == None:
#             webcam.update_webcam((300, 225))
#         else:
#             center = gotcenter[0]
#             radius = gotcenter[1]
#             webcam.update_webcam(center)
#             if radius > 20:
#                 # If the radius is above a certain size we count it
#                 webcam.pts.append(center)
#                 webcam.rad.append(radius)
#                 webcam.counter = webcam.counter + 1
#                 (x,y) = center

#             master.process_events()

#         # Update the frames of the webcam video
#         webcam.frame = cv2.flip(webcam.frame, 1)
#         cv2.imshow("Frame",webcam.frame)
#         key = cv2.waitKey(1) & 0xFF
#         frame = frame + 1
#         time.sleep(.001)
#         if key == ord("q"):
#             # Release the camera, close open windows
#             webcam.camera.release()
#             cv2.destroyAllWindows()
#             master.close()
#             pygame.quit()
#         if key == ord("c"):
#             # Clear spell chain
#             model.spell_clear()
#         if key == ord("r"):
#             # Reset game
#             check = 0
#             enemy.x = 25
#             enemy.y = 100
#             enemy.hp = 100
#             player.hp = 500


#             if menu.tutorielrunning == True:
#                 directions = menu.font.render("Press q to quit", 40, blackColor)
#                 screen.blit(directions, (300, 15))

#                 directions = menu.font.render("Press c to start casting again", 40, blackColor)
#                 screen.blit(directions, (300, 35))

#             pygame.display.update()