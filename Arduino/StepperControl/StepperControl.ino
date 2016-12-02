/*
  Poe Project 2016: CNC Sprinkle Printer

  Receives commands via serial
  Controls the steppers that move the gantry using the Adafruit Motor 
  Controsl the dispensing system
  For use with 2 axis gantry

  Instructions are written to serial in the form "<number of steps X><number of steps Y><color code>"
  in which steps can be positive or negative to denote direction
  and color code is either 1 for black (point at which pixel is dropped) or
  0 for white (point at which no pixel is dropped)

  by Team SprinkOlin
*/

// TODO could be really cool to have a controller to manually move the steppers on top of the print surface (buttons)

#include <Adafruit_MotorShield.h>
#include <Servo.h>
#include "StepperHeader.h"

// Create the motor shield objects. Because we are using 3 stepper motors, it
// was necessary to stack motor shields. The bottom shield
// has the default I2C address (no jumpers soldered shut)
// the top shield has the next hex address (rightmost jumper soldered closed)
// reference: https://learn.adafruit.com/adafruit-motor-shield-v2-for-arduino/stacking-shields

Adafruit_MotorShield AFMSbot(0x60); // Bottom shield
Adafruit_MotorShield AFMStop(0x61); // Top shield

// Connect stepper motors with 200 steps per revolution (1.8 degrees per step)
// to the motorports on the shield

// the gantry steppers:
Adafruit_StepperMotor *xStepper = AFMSbot.getStepper(200, 1); // M1 and M2 bottom board
Adafruit_StepperMotor *yStepper = AFMSbot.getStepper(200, 2); // M3 and M4 bottom board

// the dispenser stepper:
Adafruit_StepperMotor *dispenser = AFMStop.getStepper(200, 1);  //M1 and M2 top board

// initialize Servo Motor objects (may not need both of these anymore)
Servo sprinkleServo;  // for the agitator in the hopper
Servo beltServo;  // for the conveyor belt

// limit switch pins
const int switch1 = 8;
const int switch2 = 2; 

const int hopperPin = 9;  // the agitator servo pin
const int beltPin = 6;  // the conveyor belt servo pin

// flags to determine callibration status
// these are passed as arguments into the callibration function (defined below)
int stop1 = false;  
int stop2 = false;

// initialize command variables. These will be used to store the desired number of steps
// that the motors are commanded to go (command obtained via Serial)
int stepCommandX;
int stepCommandY;

//  setting min and max positions ensures that the steppers do not rotate past the limits of the gantry
int maxPositionX = 180;  // TODO find actual max number of steps to go from one side to other
int minPositionX = 0;  // TODO implement code to take into account dimensions and position of print surface
int maxPositionY = 180;
int minPositionY = 0;

// Because steppers, unlike servos, cannot keep track of their position, we need
// to keep track of the positions relative to the zero position (obtained by calibration)
// The initial positions are set to zero and are updated as the motors get commands 
// from Serial 
int stepperPositionX = 0;
int stepperPositionY = 0;

void returnHome(Adafruit_StepperMotor* motor) {
  // Returns the stepper back to its starting position
  motor->step(stepperPositionX, BACKWARD, INTERLEAVE);
  stepperPositionX = 0;
}

void calibrate(Adafruit_StepperMotor* motor, int switchPin, bool flag) {
  // Runs the motor towards the home position, until it hits a limit switch, indicating that the
  //motor should stop running.
  while (flag == false) {
    // run the motor towards the home position until the button is pressed
    int buttonState = digitalRead(switchPin);
    if (buttonState == LOW) {
      flag = true;
      Serial.println("pressed!");
      break;
    }
    motor->step(1, BACKWARD, INTERLEAVE);
    delay(3);
  }
  Serial.println("GO!");
  motor->step(5, FORWARD, INTERLEAVE); // steps a tiny bit away from the limit switch
}

void moveMotor(Adafruit_StepperMotor* motor, int stepCommand, int stepperPosition, int minPosition, int maxPosition) {
      // handles positions outside of the limits of the gantry geometry
    if (stepperPosition < minPosition) { //Before minPositionX was 0
      // limits number of steps to above the minimum position (defined as 0)
      // only goes as many steps as possibe before minimum position is reached
      Serial.print("below minimum limit. Moving this many steps instead: ");
      Serial.println(stepperPosition - stepCommand);
      motor->step(stepperPosition - stepCommand, BACKWARD, INTERLEAVE);
      stepperPosition = 0;
    }

    else if (stepperPosition > maxPosition) {
      // limits number of steps to below the maximum position
      // only goes as many steps as possible before maximum is reached
      Serial.print("above maximum limit. Moving this many steps instead: ");
      Serial.println(stepperPosition - maxPosition);
      motor->step(stepperPosition - maxPosition, FORWARD, INTERLEAVE);
      stepperPosition = maxPosition;
    }

    else {
      // if the stepper is within the upper and lower limits, it can move noramlly
      if (stepCommand > 0) {
        // move the stepper in the positive direction
        motor->step(stepCommand, FORWARD, INTERLEAVE);
        delay(3);
      }

      else {
        // move the stepper in the negative direction
        motor->step(-stepCommand, BACKWARD, INTERLEAVE);
        delay(3);
      }
    }
}

void setup() {
  // initialize the button pin as an input:
  pinMode(switch1, INPUT);

  // attach servo objects to their pins and set to starting position
  sprinkleServo.attach(hopperPin);
  sprinkleServo.write(0);
  beltServo.attach(beltPin);
  beltServo.write(0);

  // start Serial so that we can receive commands
  Serial.begin(9600);

  // allows us to communicate with the motor shields
  AFMStop.begin(); // create with the default frequency 1.6KHz
  AFMSbot.begin();

  // setup the steppers
  xStepper->setSpeed(10);  // 10 rpm
  yStepper->setSpeed(10);

  // run the calibration sequence on the motors
//  calibrate(xStepper, switch1, stop1);
//  delay(100);
//  calibrate(yStepper, switch2, stop2);
//  delay(100);
}

void loop() {
  // Check if the is incoming data in Serial and that callibration has occured
  if (Serial.available() >= 3 and Serial.available() % 3 == 0) {
    // looks for a line of the form '<number of steps><color code>'
    int stepCommandX = Serial.read();  // first character in sequence corresponds to X position
    int stepCommandY = Serial.read(); // second corresponds to Y position
    int colorCode = Serial.read(); // third corresponds to the color code
    Serial.print("Color: ");
    Serial.println(colorCode);

    // update the position of the stepper relative to initial calibration
    // at this point, it is OK if the position is outside of the limits,
    // we handle this a little later!
    stepperPositionX += stepCommandX;

    Serial.print("I received the commands: ");
    Serial.print(stepCommandX);
    Serial.print(" ");
    Serial.println(stepCommandY);
    Serial.print("The motor position is: ");
    Serial.print(stepperPositionX);
    Serial.print(" ");
    Serial.println(stepperPositionY);

    moveMotor(xStepper, stepCommandX, stepperPositionX, minPositionX, maxPositionX);
    delay(3);  
    moveMotor(yStepper, stepCommandY, stepperPositionY, minPositionY, maxPositionY); 
    delay(3);
    
    if (colorCode == 1) {
      // activates dispenser when a black sprixel is needed
      if (colorCode == 1) {
        // agitate sprinkles so they can fall into chute
        sprinkleServo.write(30);
        delay(10);
        sprinkleServo.write(0);
        // rotate dispenser to drop a sprinkle
        dispenser->step(100, BACKWARD, INTERLEAVE);
        delay(3);
      }

    }
  }
}

