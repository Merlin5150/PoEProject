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

#include <Adafruit_MotorShield.h>
#include <Servo.h>
#include "StepperHeader.h"

Adafruit_MotorShield AFMSbot(0x60); // Bottom shield

// Connect stepper motors with 200 steps per revolution (1.8 degrees per step)
// to the motorports on the shield

// the gantry steppers:
Adafruit_StepperMotor *xStepper = AFMSbot.getStepper(200, 1); // M1 and M2 bottom board
Adafruit_StepperMotor *yStepper = AFMSbot.getStepper(200, 2); // M3 and M4 bottom board


// initialize Servo Motor objects (may not need both of these anymore)
Servo sprinkleServo;  // for the agitator in the hopper

// limit switch pins
const int switch1 = 8;
const int switch2 = 2; 

const int hopperPin = 9;  // the agitator servo pin

// flags to determine callibration status
// these are passed as arguments into the callibration function (defined below)
int stop1 = false;  
int stop2 = false;

// initialize command variables. These will be used to store the desired number of steps
// that the motors are commanded to go (command obtained via Serial)
int stepCommandX = 0;
int stepCommandY = 0;

//  setting min and max positions ensures that the steppers do not rotate past the limits of the gantry
int maxPositionX = 710;
int minPositionX = 0; 
int maxPositionY = 2100;
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
    if (buttonState == HIGH) {
      flag = true;
      break;
    }
    motor->step(1, BACKWARD, INTERLEAVE);
    delay(3);
  }
//  Serial.println("GO!");
  motor->step(100, FORWARD, INTERLEAVE); // steps a tiny bit away from the limit switch
}

int moveMotor(Adafruit_StepperMotor* motor, int stepCommand, int stepperPosition, int minPosition, int maxPosition) {
      // handles positions outside of the limits of the gantry geometry
    if (stepperPosition + stepCommand < minPosition) { //Before minPositionX was 0
      // limits number of steps to above the minimum position (defined as 0)
      // only goes as many steps as possibe before minimum position is reached
      motor->step(abs(minPosition - stepperPosition), BACKWARD, INTERLEAVE);
      stepperPosition = 0;
    }

    else if (stepperPosition + stepCommand > maxPosition) {
      // limits number of steps to below the maximum position
      // only goes as many steps as possible before maximum is reached
      motor->step(maxPosition - stepperPosition, FORWARD, INTERLEAVE);
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
        motor->step(abs(stepCommand), BACKWARD, INTERLEAVE);
        delay(3);
      }
      stepperPosition += stepCommand;
    }
    return stepperPosition;
}

void setup() {
  // initialize the button pin as an input:
  pinMode(switch1, INPUT);

  // attach servo objects to their pins and set to starting position
  sprinkleServo.attach(hopperPin);
  sprinkleServo.write(179);

  // start Serial so that we can receive commands
  Serial.begin(9600);

  // allows us to communicate with the motor shields
  AFMSbot.begin();

  // setup the steppers
  xStepper->setSpeed(50);  // 50 rpm
  yStepper->setSpeed(50);

  // run the calibration sequence on the motors
  calibrate(xStepper, switch1, stop1);
  delay(100);
  calibrate(yStepper, switch2, stop2);
  delay(100);
  Serial.flush();
  Serial.println("Ready");
}

void loop() {
  // Check if the is incoming data in Serial and that callibration has occured
  if (Serial.available() >= 4) {
    // Because characters are 1 byte and ints are 2 bytes, we have to be careful to cast our Serial
    // readings to a character to ensure that the right information is being communicated!'
    char signX = (char)Serial.read();  // direction of motion in X
    int stepCommandX = 50 * (int)(char)(Serial.read());  // first character in sequence corresponds to X position
      if (signX == 0) {
        stepCommandX *= -1;
      }

    char signY = (char)Serial.read();  // direction of motion in Y
    int stepCommandY = 50 * (int)(char)Serial.read(); // second corresponds to Y position
    Serial.println(stepCommandY);
      if (signY == 0) {
        stepCommandY *= -1;
      }


    stepperPositionX = moveMotor(xStepper, stepCommandX, stepperPositionX, minPositionX, maxPositionX);  
    stepperPositionY = moveMotor(yStepper, stepCommandY * 2, stepperPositionY, minPositionY, maxPositionY); 
    delay(1000);
    

    // turn the dispenser to dump an m&m
    sprinkleServo.write(1);
    delay(500);
    sprinkleServo.write(179);
    delay(500);
//    Serial.flush();
  }
}

