/* 
Poe Project 2016: Sprinkle Placer

Control the steppers that move the gantry using the Adafruit Motor Shield
*/

// TODO: implement calibration function to zero the stepper
// create classes/functions for stuff

#include <Wire.h>
#include <Adafruit_MotorShield.h>

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

// Connect a stepper motor with 200 steps per revolution (1.8 degree)
// to motor port #2 (M3 and M4)
Adafruit_StepperMotor *myStepper = AFMS.getStepper(200, 2);

int stepCommand;
int maxPosition = 90;
int minPosition = 0;
int stepperPosition = 0; // assumes callibration done and stepper starting at x=0

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps

  AFMS.begin();  // create with the default frequency 1.6KHz

  // setup the stepper
  myStepper->setSpeed(10);  // 10 rpm   
}


void loop() {
  // Check if the is incomming data in Serial
  if (Serial.available() > 0){
    stepCommand = Serial.parseInt();  // converts incoming data to integer
    // update the position of the stepper relative to initial calibration
    stepperPosition += stepCommand;

    Serial.print("I received the command: ");
    Serial.println(stepCommand);
    Serial.print("The motor position is: ");
    Serial.println(stepperPosition);

      if(stepperPosition < minPosition) { //Before minPosition was 0
        // limits number of steps to above the minimum position (defined as 0)
        Serial.print("below minimum limit. Moving this many steps instead: ");
        Serial.println(stepperPosition - stepCommand);
        myStepper->step(stepperPosition - stepCommand, BACKWARD, INTERLEAVE);
        stepperPosition = 0;
      }

      else if(stepperPosition > maxPosition) {
        // limits number of steps to below the maximum position
        Serial.print("above maximum limit. Moving this many steps instead: ");
        Serial.println(stepperPosition - maxPosition);
        myStepper->step(stepperPosition - maxPosition, FORWARD, INTERLEAVE);
        stepperPosition = maxPosition;
      }
      
      else {
        // if the stepper is within the upper and lower limits
        if (stepCommand > 0){
          // move the stepper in the positive direction
          myStepper->step(stepCommand, FORWARD, INTERLEAVE);
          delay(3);
        }
        
        else {
          // move the stepper in the positive direction
          myStepper->step(-stepCommand, BACKWARD, INTERLEAVE);
          delay(3);
        }
      }

    // "zeros" the motor on command
    if (stepperPosition != 0 && stepCommand == 0) {
      Serial.print("Position before returning home: ");
      Serial.println(stepperPosition);
      returnHome();
    }
  }

}

void returnHome() {
  // Returns the stepper back to its initial position
  myStepper->step(stepperPosition, BACKWARD, INTERLEAVE);
  stepperPosition = 0;
}

