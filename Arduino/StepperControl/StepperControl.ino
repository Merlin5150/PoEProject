/*
  Poe Project 2016: CNC M&M Printer

  Receives commands via serial
  Controls the steppers that move the gantry using the Adafruit Motor 
  Controls the dispensing system
  For use with 2 axis gantry

  Instructions are written to serial in the form: "<direction stepperX><displacement stepperX><direction stepperY><displacement stepperY>"
  in which 0 represents BACKWARDS and 1 represents FORWARDS

  by Team SprinkOlin
*/

#include <Adafruit_MotorShield.h>
#include <Servo.h>

Adafruit_MotorShield AFMSbot(0x60);

// Connect stepper motors with 200 steps per revolution (1.8 degrees per step)
// to the motorports on the shield

// the gantry steppers:
Adafruit_StepperMotor *xStepper = AFMSbot.getStepper(200, 1); // M1 and M2
Adafruit_StepperMotor *yStepper = AFMSbot.getStepper(200, 2); // M3 and M4


// initialize Servo Motor object
Servo sprinkleServo;  // for the agitator in the hopper

// limit switch pins
const int switch1 = 8;  // corresponds to xStepper
const int switch2 = 2;  // corresponds to yStepper 

const int servoPin = 9;  // the agitator servo pin

// flags to determine callibration status
// these are passed as arguments into the callibration function (defined below)
int stop1 = false;  // corresponds to xStepper  
int stop2 = false;  // corresponds to yStepper

// initialize command variables. These will be used to store the desired number of steps
// that the motors are commanded to go (command obtained via Serial)
int stepCommandX = 0;
int stepCommandY = 0;

// setting min and max positions ensures that the steppers do not rotate past the limits of the gantry
// these are experimentally determined and may vary greatly depending on gantry geometry
int maxPositionX = 710;
int minPositionX = 0; 
int maxPositionY = 2100;
int minPositionY = 0;

// Because steppers, unlike servos, cannot keep track of their position, we need
// to keep track of the positions relative to the zero position (obtained by calibration)
// The initial positions are set to zero and are updated as the motors read commands 
// from Serial 
int stepperPositionX = 0;
int stepperPositionY = 0;

void calibrate(Adafruit_StepperMotor* motor, int switchPin, bool flag) {
  // Runs the motor towards the home position, until it hits a limit switch, indicating that the
  // motor should stop running.
  // motor: a pointer to a motor object. Either xStepper or yStepper in this code.
  // switchPin: the pin of the limit switch corresponding to motor.
  // flag: indicator whether switch was press. Either stop1 or stop2 in this code.
  
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
  motor->step(100, FORWARD, INTERLEAVE); // steps away from the limit switch to position dispenser over gantry
}

int moveMotor(Adafruit_StepperMotor* motor, int stepCommand, int stepperPosition, int minPosition, int maxPosition) {
  // processes instructions into motor movement. 
  // motor: a pointer to a motor object. Either xStepper or yStepper in this code.
  // stepCommand: desired number of steps the motor should rotate. Negative
  // command denotes a backwards rotation.
  // stepperPosition: the current position of the motor
  // minPosition: minimum coordinate the stepper can move the dispenser to
  // maxPosition: maximum coordinate the stepper can move the dispenser to
  
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
    return stepperPosition; // this is used to update the position of the motor
}

void setup() {
  // initialize the button pin as an input:
  pinMode(switch1, INPUT);
  pinMode(switch2, INPUT);

  // attach servo object and set to starting position
  sprinkleServo.attach(servoPin);
  sprinkleServo.write(179);

  Serial.begin(9600);

  // allows us to communicate with the motor shields with I2C
  AFMSbot.begin();

  // set the stepper speeds
  xStepper->setSpeed(50);  // 50 rpm
  yStepper->setSpeed(50);

  // run the calibration sequence on the motors
  calibrate(xStepper, switch1, stop1);
  calibrate(yStepper, switch2, stop2);
  delay(100);
  Serial.flush(); // clears the serial buffer
  Serial.println("Ready");
}

void loop() {
  // In order to not get strange readings from serial, we want to make sure that
  // all 4 bytes needed to create a complete command sequence are available before reading from Serial
  if (Serial.available() >= 4) {
    
    // Because characters are 1 byte and ints are 4 bytes, we have to be careful to cast our Serial
    // readings to a character to ensure that the right information is being communicated!'

    // read direction command for xStepper
    char signX = (char)Serial.read();

    // read displacement of xStepper, scale to accomodate size of M&M
    int stepCommandX = 75 * (int)(char)(Serial.read());
      if (signX == 0) {
        stepCommandX *= -1; // negates the desired number of steps to indicate motor should rotate backwards
      }

    // read direction command for yStepper
    char signY = (char)Serial.read();

    // read displacement of xStepper, scale to accomodate size of M&M
    // we scaled this command by an extra factor of 2 because the step size of ystepper was half that of xStepper
    int stepCommandY = 75 * 2 * (int)(char)Serial.read();
      if (signY == 0) {
        stepCommandY *= -1; // negates the desired number of steps to indicate motor should rotate backwards
      }


    stepperPositionX = moveMotor(xStepper, stepCommandX, stepperPositionX, minPositionX, maxPositionX);  
    stepperPositionY = moveMotor(yStepper, stepCommandY, stepperPositionY, minPositionY, maxPositionY); 
    delay(1000); // large delay to allow time for motors to move
    

    // turn the dispenser to dump an m&m
    sprinkleServo.write(1);
    delay(500);
    sprinkleServo.write(179);
    delay(500);
  }
}

