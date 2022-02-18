
// RotaryEncoder library 1.5.2
// see: https://github.com/mathertel/RotaryEncoder
#include <RotaryEncoder.h>

struct PinState
	{
	int pinNumber;
	int pinInterrupt;
	long interruptCount;
	int value;
	};

class RotaryEncoderEx : public RotaryEncoder
	{
	public:
		PinState pinStateA;
		PinState pinStateB;

		RotaryEncoderEx(int pinA, int pinB, LatchMode mode, void (*pinAISR)(void), void (*pinBISR)(void)) : RotaryEncoder(pinA, pinB, mode)
			{
			this->pinStateA.pinNumber = pinA;
			this->pinStateA.pinInterrupt = digitalPinToInterrupt(this->pinStateA.pinNumber);
			this->pinStateA.interruptCount = 0;
			this->pinStateA.value = 0;

			this->pinStateB.pinNumber = pinB;
			this->pinStateB.pinInterrupt = digitalPinToInterrupt(this->pinStateB.pinNumber);
			this->pinStateB.interruptCount = 0;
			this->pinStateB.value = 0;

			if (this->pinStateA.pinInterrupt == NOT_AN_INTERRUPT)
				{
				DebugMessage("pinA not an interrupt");
				}
			else
				{
				attachInterrupt(this->pinStateA.pinInterrupt, pinAISR, CHANGE);
				}

			if (this->pinStateB.pinInterrupt == NOT_AN_INTERRUPT)
				{
				DebugMessage("pinB not an interrupt");
				}
			else
				{
				attachInterrupt(this->pinStateB.pinInterrupt, pinBISR, CHANGE);
				}
			}

		void tickA()
			{
			RotaryEncoder::tick();
			this->pinStateA.interruptCount++;
			this->pinStateA.value = digitalRead(this->pinStateA.pinNumber);
			}

		void tickB()
			{
			RotaryEncoder::tick();
			this->pinStateB.interruptCount++;
			this->pinStateB.value = digitalRead(this->pinStateB.pinNumber);
			}

		void reportPin(Stream* pStream, PinState* pState, char* szPin)
			{
			pStream->print("Pin ");
			pStream->print(szPin);
			pStream->print(" (");
			pStream->print(pState->pinNumber);
			pStream->print(") : ");
			pStream->print(pState->value);
			pStream->println();

			pStream->print("    interrupt # : ");
			if (pState->pinInterrupt == NOT_AN_INTERRUPT)
				{
				pStream->print("NOT_AN_INTERRUPT");
				}
			else
				{
				pStream->print(pState->pinInterrupt);
				}
			pStream->println();

			if (pState->pinInterrupt != NOT_AN_INTERRUPT)
				{
				pStream->print("    interrupt count : ");
				pStream->print(pState->interruptCount);
				pStream->println();
				}
			}

		void reportStats(Stream* pStream)
			{
			reportPin(pStream, &(this->pinStateA), "A");
			reportPin(pStream, &(this->pinStateB), "B");
			}
	};