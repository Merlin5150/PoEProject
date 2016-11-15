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

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

// Connect a stepper motor with 200 steps per revolution (1.8 degree)
// to motor port #2 (M3 and M4)
Adafruit_StepperMotor *xStepper = AFMS.getStepper(200, 1);
Adafruit_StepperMotor *yStepper = AFMS.getStepper(200, 1);

Servo sprinkleServo;
Servo beltServo;

const int buttonPin = 8;     // the number of the pushbutton pin
const int hopperPin = 9;
const int beltPin = 6;
boolean buttonPressed = false;  // flag determines if callibration has been completed
int stepCommand;
int maxPosition = 180;  // TODO find actual max number of steps to go from one side to other
int minPosition = 0;  // TODO implement code to take into account dimensions and position of print surface
int stepperPosition = 0; // assumes callibration done and stepper starting at x=0


void setup() {
  // initialize the button pin as an input:
  pinMode(buttonPin, INPUT);
  sprinkleServo.attach(hopperPin);
  sprinkleServo.write(0);

  beltServo.attach(beltPin);
  beltServo.write(0);
  Serial.begin(9600);

  AFMS.begin(); // create with the default frequency 1.6KHz

  // setup the stepper
  xStepper->setSpeed(10);  // 10 rpm  
  yStepper->setSpeed(10); 

  // run the callibration sequence on one motor
  calibrate(xStepper);
  calibrate(yStepper);

  Serial.println("Ready");
}

void loop() {
  // Check if the is incoming data in Serial and that callibration has occured
  if (Serial.available() && buttonPressed > 0){
    // looks for a line of the form '<number of steps><color code>'
    int stepCommand = Serial.read();  // looks for the step number in the incoming data
    int colorCode = Serial.read(); // reads the first non-integer character as the color code
    Serial.print("Color: ");
    Serial.println(colorCode);

    // update the position of the stepper relative to initial calibration
    stepperPosition += stepCommand;

    Serial.print("I received the command: ");
    Serial.println(stepCommand);
    Serial.print("The motor position is: ");
    Serial.println(stepperPosition);

      if(stepperPosition < minPosition) { //Before minPosition was 0
        // limits number of steps to above the minimum position (defined as 0)
        // only goes as many steps as possibe before minimum position is reached
        Serial.print("below minimum limit. Moving this many steps instead: ");
        Serial.println(stepperPosition - stepCommand);
        xStepper->step(stepperPosition - stepCommand, BACKWARD, INTERLEAVE);
        stepperPosition = 0;
      }

      else if(stepperPosition > maxPosition) {
        // limits number of steps to below the maximum position
        // only goes as many steps as possible before maximum is reached
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
          // move the stepper in the negative direction
          xStepper->step(-stepCommand, BACKWARD, INTERLEAVE);
          delay(3);
        }
      }

    // returns the motor to the zero home position on command
    if (stepperPosition != 0 && stepCommand == 0) {
      Serial.print("Position before returning home: ");
      Serial.println(stepperPosition);
      returnHome(xStepper);
    }
    if (colorCode == 1) {
      Serial.println("drop!");
      sprinkleServo.write(100);
      delay(100);
      sprinkleServo.write(0);
      delay(50);
      beltServo.write(180);
      delay(500);
      beltServo.write(0);
      delay(10);
      // TODO add code to drop a sprinkle
    }

  }
}

void returnHome(Adafruit_StepperMotor* motor) {
  // Returns the stepper back to its initial position
  motor->step(stepperPosition, BACKWARD, INTERLEAVE);
  stepperPosition = 0;
}

void calibrate(Adafruit_StepperMotor* motor) {
  // Runs the motor towards the home position, until it hits the button, indicating that the 
  //motor should stop running.
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

