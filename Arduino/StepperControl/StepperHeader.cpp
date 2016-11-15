class StepperMotor {
private:

	Adafruit_StepperMotor * motor;

	int minPosition
	int maxPosition;
	int position;

public:

	StepperMotor(Adafruit_StepperMotor * motor, int minPosition, int maxPosition) {
		
		this->minPosition = minPosition;
		this->maxPosition = maxPosition;

		// initialize position
		this->position = 0;
	}

	void Update(int stepCommand) {
		position += stepCommand;

		if (position > maxPosition) {
			// limits number of steps to below the maximum position
        	// only goes as many steps as possible before maximum is reached
			motor->step(position - maxPosition, FORWARD, INTERLEAVE);
			position = maxPosition;
			delay(3);
		}

		else if (position < 0) {
			motor->step(position - stepCommand, BACKWARD, INTERLEAVE);
			position = 0;
			delay(3);
		}

		else {
			if (stepCommand > 0) {
				motor->step(stepCommand, FORWARD, INTERLEAVE);
				delay(3);
			}

			else {
				motor->step(stepCommand, BACKWARD, INTERLEAVE);
				delay(3);
			}
		}

	}

}