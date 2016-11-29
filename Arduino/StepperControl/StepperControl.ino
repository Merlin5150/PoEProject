/*
  Poe Project 2016: CNC Sprinkle Printer

  Receives commands via serial
  Controls the steppers that move the gantry using the Adafruit Motor Shield
  For use with 1 axis gantry

  Instructions are written to serial in the form "<number of steps><color code>"
  in which <integer> can be positive or negative to denote direction
  and color code is either 'b' for black (point at which pixel is dropped) or
  'w' for white (point at which no pixel is dropped)

  by Team SprinkOlin
*/

// TODO could be really cool to have a controller to manually move the steppers on top of the print surface (buttons)

#include <Adafruit_MotorShield.h>
#include <Servo.h>
#include "StepperHeader.h"

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMSbot(0x60); // Bottom shield
Adafruit_MotorShield AFMStop(0x61); // Top shield

// Connect a stepper motor with 200 steps per revolution (1.8 degree)
// to motor port #2 (M3 and M4)
Adafruit_StepperMotor *xStepper = AFMSbot.getStepper(200, 1);
Adafruit_StepperMotor *yStepper = AFMSbot.getStepper(200, 2);
Adafruit_StepperMotor *dispenser = AFMStop.getStepper(200, 1);

Servo sprinkleServo;
Servo beltServo;

const int switch1 = 8;     // the number of the pushbutton pin
const int hopperPin = 9;
const int beltPin = 6;
int stop1 = false;  // flag determines if callibration has been completed
int stop2 = false;
int stepCommandX;
int stepCommandY;
int maxPositionX = 180;  // TODO find actual max number of steps to go from one side to other
int minPositionX = 0;  // TODO implement code to take into account dimensions and position of print surface
int stepperPositionX = 0; // assumes callibration done and stepper starting at x=0

void returnHome(Adafruit_StepperMotor* motor) {
  // Returns the stepper back to its initial position
  motor->step(stepperPositionX, BACKWARD, INTERLEAVE);
  stepperPositionX = 0;
}

void calibrate(Adafruit_StepperMotor* motor, int switchPin, bool flag) {
  // Runs the motor towards the home position, until it hits the button, indicating that the
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
//  buttonPressed == false;
  Serial.println("GO!");
  motor->step(5, FORWARD, INTERLEAVE); // steps a tiny bit away from the limit switch
}

void setup() {
  // initialize the button pin as an input:
  pinMode(switch1, INPUT);
  sprinkleServo.attach(hopperPin);
  sprinkleServo.write(0);

  beltServo.attach(beltPin);
  beltServo.write(0);
  Serial.begin(9600);

  AFMStop.begin(); // create with the default frequency 1.6KHz
  AFMSbot.begin();

  // setup the stepper
  xStepper->setSpeed(10);  // 10 rpm
  yStepper->setSpeed(10);

  // run the calibration sequence on one motor
    calibrate(xStepper, switch1, stop1);
    delay(100);
    Serial.println("next");
    calibrate(yStepper, 2, stop2);
    delay(100);

  Serial.println("Ready");
}

void loop() {
  // Check if the is incoming data in Serial and that callibration has occured
  if (Serial.available()) {
    // looks for a line of the form '<number of steps><color code>'
    int stepCommandX = Serial.read();  // looks for the step number in the incoming data
    int stepCommandY = Serial.read();  // uncomment to get 2-axis commands
    int colorCode = Serial.read(); // reads the first non-integer character as the color code
    Serial.print("Color: ");
    Serial.println(colorCode);

    // update the position of the stepper relative to initial calibration
    stepperPositionX += stepCommandX;

    Serial.print("I received the command: ");
    Serial.println(stepCommandX);
    Serial.print("The motor position is: ");
    Serial.println(stepperPositionX);

    if (stepperPositionX < minPositionX) { //Before minPositionX was 0
      // limits number of steps to above the minimum position (defined as 0)
      // only goes as many steps as possibe before minimum position is reached
      Serial.print("below minimum limit. Moving this many steps instead: ");
      Serial.println(stepperPositionX - stepCommandX);
      xStepper->step(stepperPositionX - stepCommandX, BACKWARD, INTERLEAVE);
      stepperPositionX = 0;
    }

    else if (stepperPositionX > maxPositionX) {
      // limits number of steps to below the maximum position
      // only goes as many steps as possible before maximum is reached
      Serial.print("above maximum limit. Moving this many steps instead: ");
      Serial.println(stepperPositionX - maxPositionX);
      xStepper->step(stepperPositionX - maxPositionX, FORWARD, INTERLEAVE);
      stepperPositionX = maxPositionX;
    }

    else {
      // if the stepper is within the upper and lower limits
      if (stepCommandX > 0) {
        // move the stepper in the positive direction
        xStepper->step(stepCommandX, FORWARD, INTERLEAVE);
        delay(3);
      }

      else {
        // move the stepper in the negative direction
        xStepper->step(-stepCommandX, BACKWARD, INTERLEAVE);
        delay(3);
      }
    }

    //    // returns the motor to the zero home position on command
    //    if (stepperPositionX != 0 && stepCommandX == 0) {
    //      Serial.print("Position before returning home: ");
    //      Serial.println(stepperPositionX);
    //      returnHome(xStepper);
    //    }

    if (colorCode == 1) {
      // activates dispenser when a black sprixel is needed
      // returns the motor to the zero home position on command
      if (stepperPositionX != 0 && stepCommandX == 0) {
        Serial.print("Position before returning home: ");
        Serial.println(stepperPositionX);
        returnHome(xStepper);
      }
      if (colorCode == 1) {
//        Serial.println("drop!");
//        sprinkleServo.write(100);
//        delay(100);
//        sprinkleServo.write(0);
//        delay(50);
//        beltServo.write(180);
//        delay(500);
//        beltServo.write(0);
//        delay(10);
          dispenser->step(20, FORWARD, SINGLE);
        // TODO add code to drop a sprinkle
      }

    }
  }
}

