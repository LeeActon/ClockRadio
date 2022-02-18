/*
 Name:		Radio.ino
 Created:	2/6/2022 9:33:55 AM
 Author:	Lee
*/

void DebugMessage(char* szMessage);
#include "fmtuner.h"
#include "debounce.h"
#include "RotaryEncoderEx.h"

ButtonDebouncer buttons[6];

RotaryEncoderEx *pRotaryEncoder1;

void rotaryEncoder1PinAInterrupt()
{
	if (pRotaryEncoder1 != NULL)
		{
		pRotaryEncoder1->tickA();
		}
}
void rotaryEncoder1PinBInterrupt()
{
	if (pRotaryEncoder1 != NULL)
		{
		pRotaryEncoder1->tickB();
		}
}

RotaryEncoderEx *pRotaryEncoder2;

void rotaryEncoder2PinAInterrupt()
{
	if (pRotaryEncoder2 != NULL)
		{
		pRotaryEncoder2->tickA();
		}
}
void rotaryEncoder2PinBInterrupt()
{
	if (pRotaryEncoder2 != NULL)
		{
		pRotaryEncoder2->tickB();
		}
}

int favoriteChannels[] =
	{
	9730,   // KIRO
	9990,   // KISW
	10690,  // KRWM
	9570,   // KJR
	9330,   // KUBE
	9490,   // KUOW
	10250,  // KZOK
	9810,   // KING
	8850,   // KPLU
	9030,   // KEXP
	9490    // KUOW
	};

// MicroView PINS
// RESET		VIN
// A5			+5V
// A4			6
// A3			5
// A2			3
// A1			2
// A0			1
// GND			0

// Si4703 breakout pins (top right corner going down)
// L OUT
// R OUT
// GND
// VCC
// SDIO
// SLCK
// -SEN
// -RST
// GPIO1
// GPIO2

// Other Si4793 breakout pins
// 3.3V
// GND
// SDIO
// SCLK
// -SEN
// -RST
// GPIO1
// GPIO2

// Connections (through 5V to 3.3V converter)
#define R_RST  9
#define R_SDIO 2
#define R_SCLK 3
#define R_INT  0

void HandleSerialInput();
void HandleSerialInput(char* sz);

FMTuner fmTuner(&Serial, R_RST, R_SDIO, R_SCLK, R_INT);

#define DEBUG_PIN 13

void DebugMessage(char* szMessage)
	{
	Serial.print("*");
	Serial.println(szMessage);
	}

// the setup function runs once when you press reset or power the board
int pinAInt = NOT_AN_INTERRUPT;
int pinBInt = NOT_AN_INTERRUPT;
void setup()
	{
	pRotaryEncoder1 = new RotaryEncoderEx(5, 7, RotaryEncoder::LatchMode::TWO03, rotaryEncoder1PinAInterrupt, rotaryEncoder1PinBInterrupt);
	pRotaryEncoder2 = new RotaryEncoderEx(0, 1, RotaryEncoder::LatchMode::FOUR3, rotaryEncoder2PinAInterrupt, rotaryEncoder2PinBInterrupt);

	pinMode(DEBUG_PIN, OUTPUT);
	digitalWrite(DEBUG_PIN, LOW);
	DebugPulse(1);
	pinMode(R_RST, OUTPUT);
	PulsePin(R_RST, 10);
	pinMode(R_SDIO, OUTPUT);
	PulsePin(R_SDIO, 10);
	pinMode(R_SCLK, OUTPUT);
	PulsePin(R_SCLK, 10);

	Serial.begin(115200);       // start serial
	Serial.println();

	buttons[0].Init(A0);
	buttons[1].Init(A1);
	buttons[2].Init(A2);
	buttons[3].Init(A3);
	buttons[4].Init(A4);
	buttons[5].Init(A5);
#if 1
	DebugPulse(1);
	pinMode(R_RST, OUTPUT);    // Reset pin
	pinMode(R_SDIO, OUTPUT);    // I2C data IO pin
	digitalWrite(R_RST, HIGH);  // Bring Si4703 out of reset with SDIO set to low and SEN pulled high with on-board resistor
	DebugPulse(1);
#endif
#if 0
	// Set IO pins directions
	pinMode(R_RST, OUTPUT);    // Reset pin
	pinMode(R_SDIO, OUTPUT);    // I2C data IO pin
	DebugPulse(1);
	digitalWrite(R_RST, HIGH);  // Bring Si4703 out of reset with SDIO set to low and SEN pulled high with on-board resistor
	delay(1);                     // Delay to allow pins to settle
	DebugPulse(1);

	// Set communcation mode to 2-Wire
	digitalWrite(R_SDIO, LOW);   // A low SDIO indicates a 2-wire interface
	digitalWrite(R_RST, LOW);   // Put Si4703 into reset
	delay(1);                     // Delay to allow pins to settle
	DebugPulse(1);
	digitalWrite(R_RST, HIGH);  // Bring Si4703 out of reset with SDIO set to low and SEN pulled high with on-board resistor
	delay(1);                     // Allow Si4703 to come out of reset
	DebugPulse(1);
#endif
	DebugMessage("Before fmTuner.start()");
	DebugPulse(2);
	fmTuner.start();          // Power Up Device
	DebugPulse(3);
	DebugMessage("After fmTuner.start()");
	DebugPulse(4);
	fmTuner.reportAll();
	DebugPulse(5);
	}

void DebugPulse(int count)
	{
	PulsePin(DEBUG_PIN, count * 10);
	}

void PulsePin(int pin, int microSeconds)
	{
	digitalWrite(pin, HIGH);
	delayMicroseconds(microSeconds);
	digitalWrite(pin, LOW);
	}

// the loop function runs over and over again until power down or reset
long prevPosition1 = -999;
long prevPosition2 = -999;
void loop()
	{
	if (Serial.available())
		HandleSerialInput(); // Radio control from serial interface

	for (int i = 0; i < 6; i++)
		{
		if (buttons[i].Poll())
			{
			Serial.print("B");
			Serial.print(i);
			Serial.print(" : ");
			Serial.print(buttons[i].getState());
			Serial.println();
			}
		}

    pRotaryEncoder1->tick();

	long position1 = pRotaryEncoder1->getPosition();
	long delta1 = position1 - prevPosition1;
	if (delta1 != 0)
		{
		Serial.print("rotary encoder 1 : ");
		Serial.println(delta1);
		prevPosition1 = position1;
		fmTuner.addVolume((int)delta1);
		}

    pRotaryEncoder2->tick();

	int position2 = pRotaryEncoder2->getPosition();
	int delta2 = position2 - prevPosition2;
	if (delta2 != 0)
		{
		Serial.print("rotary encoder 2 : ");
		Serial.println(delta2);
		prevPosition2 = position2;
		fmTuner.addVolume((int)delta2);
		}
	}

void HandleSerialInput()
	{
	char buffer[80+1];

	int cb = Serial.readBytesUntil('\n', buffer, sizeof(buffer));
	if (cb > 0)
		{
		buffer[cb] = '\0';
		HandleSerialInput(buffer);
		}
	}

void HandleSerialInput(char* sz)
	{
	char command = *sz++;

	switch (command)
		{
		case 'v':
			// Volume: v{+,-}{n}
			{
			int sign = 0;
			int n = 0;
			if (sz[0] == '+')
				{
				sign = 1;
				n = 1;
				sz++;
				}
			else if (sz[0] == '-')
				{
				sz++;
				sign = -1;
				n = 1;
				}

			if (sz[0] != '\0')
				{
				n = atoi(sz);
				}
			if (sign != 0)
				{
				fmTuner.addVolume(sign * n);
				}
			else
				{
				fmTuner.setVolume(n);
				}
			}
			break;

		case '+':
			// Increment Volume
			{
			fmTuner.addVolume(1);
			}
			break;
		case '-':
			// Decrement Volume
			{
			fmTuner.addVolume(-1);
			}
			break;
		case 'm':
			// Mute/Unmute volume
			{
			fmTuner.toggleMute();
			}
			break;
		case 's':
			// Set Mono/Sterio"
			{
			fmTuner.toggleMono();
			}
			break;
		case 'u':
			// Tune Frequency up
			{
			fmTuner.incChannel();
			}
			break;
		case 'd':
			// Tune Frequency down
			{
			fmTuner.decChannel();
			}
			break;
		case 'n':
			// Channel Seek next
			{
			if (!fmTuner.seekUp())
				{
				DebugMessage("Error: Seek failure or band limit reached!!");
				}
			}
			break;
		case 'l':
			// Channel Seek last
			{
			if (!fmTuner.seekDown())
				{
				DebugMessage("Error: Seek failure or band limit reached!!");
				}
			}
			break;
		case 'p':
			{
			int i = atoi(sz);
			if (i < 0)
				i = 0;
			else if (i > 9)
				i = 9;

			fmTuner.setChannel(favoriteChannels[i]);
			}
			break;
		case 'r':             // Listen for RDS Data
			{
			// TODO:
			}
			break;

		case '?':
			{
			fmTuner.reportAll();
			if (pRotaryEncoder1 != NULL)
				{
				pRotaryEncoder1->reportStats(&Serial);
				}
			if (pRotaryEncoder2 != NULL)
				{
				pRotaryEncoder2->reportStats(&Serial);
				}
			}
			break;
		}
	}
