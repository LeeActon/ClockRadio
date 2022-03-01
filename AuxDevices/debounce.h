
class ButtonDebouncer
	{
	private:
		int pinNumber;
		bool debouncing;
		bool state;
		bool prevState;
		long timeout;

	public:
		void Init(int pinNumber)
			{
			this->pinNumber = pinNumber;
			pinMode(pinNumber, INPUT_PULLUP);
			this->prevState = digitalRead(this->pinNumber);
			this->debouncing = false;
			this->timeout = 0;
			}

		bool Poll()
			{
			this->state = digitalRead(this->pinNumber);

			if (this->state != this->prevState)
				{
				this->debouncing = true;
				this->prevState = state;
				this->timeout = millis() + 1;
				}
			else if (this->debouncing && (millis() > this->timeout))
				{
				this->debouncing = false;
				return true;
				}

			return false;
			}

		bool getState()
			{
			return this->state;
			}

		void reportButton(Stream* pStream, int id)
			{
			if (this->Poll())
				{
				pStream->print("B ");
				pStream->print(id);
				pStream->print(" : ");
				pStream->print(this->getState());
				pStream->println();
				}
			}
	};
