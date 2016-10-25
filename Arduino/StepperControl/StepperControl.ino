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

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps

  AFMS.begin();  // create with the default frequency 1.6KHz

  // setup the stepper
  myStepper->setSpeed(10);  // 10 rpm   
}

int i;
int stepCommand;
int stepSize;

int stepperPosition = 0; // assumes callibration done and stepper starting at x=0
void loop() {
  // Check if the is incomming data in Serial
  if (Serial.available() > 0){
      stepCommand = Serial.read() - '0';  // converts incoming data to integer
      stepperPosition += stepCommand;
      stepSize = abs(stepCommand);
      Serial.println(stepCommand);

      boolean negative = false;
      byte aChar = Serial.read();
      Serial.println(aChar);
      if(aChar == '-'){
        negative = true;
      }

      if (!negative){
        // move the stepper in the positive direction
        myStepper->step(stepSize, FORWARD, INTERLEAVE);
        delay(3);
      }
      
      else {
        // move the stepper in the positive direction
        myStepper->step(stepSize, BACKWARD, INTERLEAVE);
        delay(3);
      }
  }
}
