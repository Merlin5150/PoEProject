#include <Wire.h>
#include <Adafruit_MotorShield.h>

class PoEStepper {
  private:

    // Create the motor shield object with the default I2C address
    Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
    
    // Connect a stepper motor with 200 steps per revolution (1.8 degree)
    // to motor port #2 (M3 and M4)
    Adafruit_StepperMotor *myStepper = AFMS.getStepper(200, 2);
};

