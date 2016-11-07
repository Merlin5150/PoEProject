/* 
Poe Project 2016: Sprinkle Placer

Receives commands via serial
Controls the steppers that move the gantry using the Adafruit Motor Shield
For use with 1 axis gantry
*/

// TODO could be really cool to have a controller to manually move the steppers on top of the print surface (buttons)

#include <Adafruit_MotorShield.h>
#include <Servo.h>

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

// Connect a stepper motor with 200 steps per revolution (1.8 degree)
// to motor port #2 (M3 and M4)
Adafruit_StepperMotor *xStepper = AFMS.getStepper(200, 2);

const int buttonPin = 8;     // the number of the pushbutton pin
boolean buttonPressed = false;  // flag determines if callibration has been completed
int stepCommand;
int maxPosition = 180;  // TODO find actual max number of steps to go from one side to other
int minPosition = 0;  // TODO implement code to take into account dimensions and position of print surface
int stepperPosition = 0; // assumes callibration done and stepper starting at x=0


void setup() {
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT);
  Serial.begin(9600);           // set up Serial library at 9600 bps

  AFMS.begin();  // create with the default frequency 1.6KHz

  // setup the stepper
  xStepper->setSpeed(10);  // 10 rpm  

  // run the callibration sequence on one motor
  callibrate(xStepper);

  
}

void loop() {
  boolean dropSprinkle = false;
  // Check if the is incomming data in Serial
  if (Serial.available() && buttonPressed > 0){
    stepCommand = Serial.parseInt();  // converts incoming data to integer
    char colorCode = Serial.read();
    Serial.print("Color: ");
    Serial.println(colorCode);
    if (colorCode == 'b') {
      dropSprinkle = true;
    }
//    Serial.println(dropSprinkle);
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
        xStepper->step(stepperPosition - stepCommand, BACKWARD, INTERLEAVE);
        stepperPosition = 0;
      }

      else if(stepperPosition > maxPosition) {
        // limits number of steps to below the maximum position
        Serial.print("above maximum limit. Moving this many steps instead: ");
        Serial.println(stepperPosition - maxPosition);
        xStepper->step(stepperPosition - maxPosition, FORWARD, INTERLEAVE);
        stepperPosition = maxPosition;
      }
      
      else {
        // if the stepper is within the upper and lower limits
        if (stepCommand > 0){
          // move the stepper in the positive direction
          xStepper->step(stepCommand, FORWARD, INTERLEAVE);
          delay(3);
        }
        
        else {
          // move the stepper in the positive direction
          xStepper->step(-stepCommand, BACKWARD, INTERLEAVE);
          delay(3);
        }
      }

    // "zeros" the motor on command
    if (stepperPosition != 0 && stepCommand == 0) {
      Serial.print("Position before returning home: ");
      Serial.println(stepperPosition);
      returnHome(xStepper);
    }
  }

}

void returnHome(Adafruit_StepperMotor* motor) {
// ^^^ This is what I attempted ^^^
  // Returns the stepper back to its initial position
  motor->step(stepperPosition, BACKWARD, INTERLEAVE);
  stepperPosition = 0;
}

void callibrate(Adafruit_StepperMotor motor) {
// ^^^ A different attempt ^^^
  // Runs the motor towards the home position, until it hits the button, indicating tha the 
  // home position has been reached and that the motor should stop running.
  while (buttonPressed == false) {
    // run the motor towards the home position until the button is pressed
    int buttonState = digitalRead(buttonPin);
    if (buttonState == HIGH) {
        buttonPressed = true;
        Serial.println("pressed!");
        break;
      }
    motor->step(1, BACKWARD, INTERLEAVE);
    delay(3);     
  }
}

