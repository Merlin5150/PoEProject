# CNC M&M printer
## Team SprinkOlin | Principles of Engineering Fall 2016
Behold! The machine that takes an image and a pastry and faithfully recreates said image on said pastry with the aid of a computer program, a two-axis gantry, and a dispenser system. The result? A tasty-looking, creative picture.

In more words: the CNC M&M printer is a 2-axis gantry attached to a dispenser that interprets image-processing and movement code from an arduino to replicate a user inputted picture. First, the image processing code interprets the user's image makes it into "mixels" or MnM-sized pixels. Then the movement-related code translates the sprixel pattern into a series of movements and communicates them to the gantry. The dispenser on the rods of the gantry is moved by a series of belts along rods, pausing occasionally to release an M&M onto the icing-coated surface beneath it. This icing-coated surface's height can be adjusted by moving the build plate up and down teeth on the comb-like structures on which it rests.

This repo contains code for image processsing and serial transmission of insructions over serial to an Ardunio in Python, [serialWriting.py](https://github.com/kuannie1/PoEProject/blob/master/serialWriting.py), and code in Arduino C to recieve instructions and move the gantry accordingly, [StepperControl.ino](https://github.com/kuannie1/PoEProject/blob/master/Arduino/StepperControl/StepperControl.ino). 

This project was created as a final project for the Principles of Engineering course at [Olin College of Engineering](olin.edu). 
### Subsystems
#### Mechanical System

The gantry is a 2-axis gantry composed of rods held up by rail-shaft guide supports screwed into the a lasercut hardboard structure. Stepper-motor controlled gears across from pulleys are aligned with both axes. The gears and pulleys hold thin rubber belts that are moved by the stepper-controlled gears. The stepper motors themselves sit on tiny platforms in the corners of the gantry. The belt on the on the front-back axis attaches to a hardboard structure encasing the gear on the end of the left-right pair of rods. The belt on the left-right axis attaches to the dispenser structure. The entire left-right axis including the dispenser moves along the front-back axis with the help of linear bearings embedded in the hardboard structures at the end of the left-right axis. Similarly, the dispenser uses two linear bearings in its hardboard structure to move along the left-right axis. The build plate beneath the entire structure moves up and down depending on what notches on four comb-like devices the build plate is placed on.

The dispenser itself is entirely 3D printed. It consists of two tubes attached to the dispenser itself, which then attaches to the hardboard piece that moves along the left-right axis. The top tube is wide enough to loosely fit an MnM, which was established to help prevent jamming, and is tall enough to hold many vertically stacked MnMs at a time. The dispenser itself includes a cylinder with a circular cup-shaped divot spun by a mini servo motor inside of a structure that holds it between the top tube. The bottom tube, which is the same diameter as the top, but reaches down about half an inch above the build plate. The bottom tube also attaches to the hardboard piece moving along the left-right axis via a small rectangle that fits around the structure. The structure that holds the tubes above and below the dispenser also includes a small shield to prevent MnMs from falling forward while the cylinder is turning. The MnM drops down the top tube into the cup on the cylinder, which is then turned in such a way that it drops down into the bottom tube and lands on the build plate.

#### Software System

The image processing software as written in Python. It utilizes the OpenCV packages to process user-inputted images and convert them to stepper motor commands. The software takes in some black and white image, and resizes it to a 30 by 30 pixel matrix before identifying each pixel’s color. It then converts the color information into a series of motor commands, telling the gantry motors when and how far to move the dispenser. This information is sent through the serial stream to provide commands to the firmware.

#### Firmware System

Using the signals from the software's input from serial, the Arduino Uno and Sparkfun Motor Sheild uses Arduino C to convert those commands to determine which coils within the stepper motor should be magnetized. Those commands also indicate when to turn the servo motor in the dispenser. When the gantry stepper motors translate the dispenser to the next destination, the servo motor on the dispenser receives the command to turn and dispense an M&M.

#### Electrical System

The electrical system ensures that everything in the system is working smoothly. The limit switches mounted on the gantry help the steppers keep track of the dispenser's location and calibrates the motors if needed. In addition to the limit switches, the stepper motors and servos are connected to the firmware through jumper wires for secure connections.

### Build it Yourself!
1. The list of materials that we used for prototyping and our final build can be found [here](https://docs.google.com/spreadsheets/d/1XF6dD36GEhaLRRnJzzlNKo4jniRV8MezCQr9N6U7E4w/edit?usp=sharing.
2. Download the full CAD from [GrabCAD](https://grabcad.com/library/cnc-m-m-placer-2).
3. Laser cut the part files found in "_to_cut_.zip". For our project, we used the [Epilog Helix Laser Cutter](https://www.epiloglaser.com/index.htm). Most of these parts can also be cut by hand, although more labor may be needed to achieve the same quality.
4. Assemble the frame of the gantry based on the CAD and included drawings.
5. Put the build plate on a level uniform across the four comb structures.
6. Attach the rail-shaft guide supports with screws to the tops of each corner of the frame on the outside.
7. Assemble the hard board pieces associated with the left-right axis. Put linear bearings in the large holes on the outsides of these structures.
8. Run the forward-backward rods through these linear bearings.
9. Then run the rods through the rail-shaft guide supports and screw screws into the top holes of each rail shaft guide support to secure the rods.
10. Attach rail-shaft guide supports on the outsides of the bottom pieces of the hardboard pieces that are now sitting on the forward-backward axes. Screw them in as shown.
11. Assemble the middle hardboard piece shown to be attached to the left-right axis. Put linear bearings in the larger holes toward the bottom of this piece.
12. Run the lef-right rods through the rail-shaft guide supports through the outside hardboard component on one side of the left-right axis, then through the linear bearings on the center piece, and then through the linear bearings on the hardboard component on the other side of the left-right axis. Tighten screws on the ends of the rail-shaft guide supports to secure the rods.
13. 3D print the dispenser and file as needed. Carefully hot-glue the top tube to the tube-shaped part of the dispenser. Then fit the bottom of the dispenser piece onto the bottom tube. Place the square-shaped attachment piece along the center part of the hardboard on the lef-right axis. Glue this piece down as needed. Attach the mini servo to the small bead-shaped attachment poking out to the left side.
14. Secure the belts along the pulleys and gears by cutting them and attaching them around these components and to small slots on the end of the corresponding hardboard pieces. Small zipties are very useful in case the holes are too big or the belt is long enough to fit through both holes and meet in the middle.
15. Re-create the electrical systems as demonstrated by the electrical diagrams. Attach the limit switches on the front-right side of the forward-back axis and on the side of the center hardboard piece of the left-right axis facing the axis with the other limit switch on it.
16. The circuit can be recreated from the diagram [circuitDiagram_schem](https://github.com/kuannie1/PoEProject/blob/master/circuitdiagram/circuitDiagram_schem.pdf). We soldered our wires to a protoboard and added jumper connections for easy customizability, but a simple breadboard and jumper set up will work just fine!
17. Solder wires to the limit switches according to the diagram
18. Screw wires into the barrel jack connectors to make the adaptor cable. This will plug into the motor shield
19. Assemble circuit on a breadboard or protoboard and plug jumpers into appropriate Arduino pins.
20. Download the Arduino code and Python code, adjust parmeters for your gantry geometry, and you are ready to go!
21. To run, first upload the Arduino code, and then run the python script from the terminal.






















