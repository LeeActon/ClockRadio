
#include <AiEsp32RotaryEncoder.h>
#include "debounce.h"

class RotaryEncoderEx : public AiEsp32RotaryEncoder 
	{
	public:
		uint8_t id;
		uint8_t buttonPin;
		ButtonDebouncer buttonDebouncer;

		RotaryEncoderEx(uint8_t id, uint8_t pinA, uint8_t pinB, uint8_t pinButton, uint8_t pinVCC, uint8_t steps)
			: AiEsp32RotaryEncoder(pinA, pinB, pinVCC, steps)
			{
			this->id = id;
			this->buttonPin = pinButton;
			}
		
		void begin()
			{
			AiEsp32RotaryEncoder::begin();
			this->buttonDebouncer.Init(this->buttonPin);
			}

		void reportPosition(Stream *pStream)
			{
			if (this->encoderChanged())
				{
				long position = this->readEncoder();
				pStream->print("R ");
				pStream->print(this->id);
				pStream->print(" : ");
				pStream->print(position);
				pStream->print(", ");
				pStream->print(this->_minEncoderValue / this->encoderSteps );
				pStream->print(", ");
				pStream->print(this->_maxEncoderValue / this->encoderSteps);
				pStream->print(", ");
				pStream->print(this->rotaryAccelerationCoef);
				pStream->print(", ");
				pStream->print(this->_circleValues);
				pStream->println();
				}
			}

		void reportButton(Stream *pStream)
			{
			if (this->buttonDebouncer.Poll())
				{
				pStream->print("B ");
				pStream->print(this->id);
				pStream->print(" : ");
				pStream->print(this->buttonDebouncer.getState());
				pStream->println();
				}
			}
	};