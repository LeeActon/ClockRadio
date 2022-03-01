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

RotaryEncoderEx* pRotaryEncoder1;

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

RotaryEncoderEx* pRotaryEncoder2;

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

#define DEBUG_PIN 8

void DebugMessage(char* szMessage)
	{
	Serial.print("*");
	Serial.println(szMessage);
	}

void setup()
	{
	Serial.begin(115200);       // start serial
	Serial.println();
	Serial.println("Started");

	// Wait for input before going any further.
	// Makes debugging easier.
	while (!Serial.available())
		{

		Serial.println(".");
		delay(1000);
		}

	pRotaryEncoder1 = new RotaryEncoderEx(0, 1, RotaryEncoder::LatchMode::TWO03, rotaryEncoder1PinAInterrupt, rotaryEncoder1PinBInterrupt);
	pRotaryEncoder2 = new RotaryEncoderEx(5, 7, RotaryEncoder::LatchMode::FOUR3, rotaryEncoder2PinAInterrupt, rotaryEncoder2PinBInterrupt);

	pinMode(DEBUG_PIN, OUTPUT);
	digitalWrite(DEBUG_PIN, LOW);
	DebugPulse(1);
	pinMode(R_RST, OUTPUT);
	pinMode(R_SDIO, OUTPUT);
	pinMode(R_SCLK, OUTPUT);

	buttons[0].Init(A0);
	buttons[1].Init(A1);
	buttons[2].Init(A2);
	buttons[3].Init(A3);
	buttons[4].Init(A4);
	buttons[5].Init(A5);
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

long prevPosition1 = -999;
long prevPosition2 = -999;
void loop()
	{
	if (Serial.available())
		HandleSerialInput(); // Radio control from serial interface

	for (int i = 0; i < 6; i++)
		{
		buttons[i].reportButton(&Serial, i);
		}

	pRotaryEncoder1->tick();
	pRotaryEncoder1->reportDelta(&Serial, 1);

	pRotaryEncoder2->tick();
	pRotaryEncoder2->reportDelta(&Serial, 2);
	}

void HandleSerialInput()
	{
	char buffer[80 + 1];

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

	// Commands:
	//     P) Power
	//     v) Volume: v[+|-][<n>]
	//     m) Mute on/off
	//     s) Stero on/off
	//     f) Frequency: f{[+\-]|[<n>]}
	//     p) Preset: p<n>
	//     S) Scan: S{+|-}
	//     ?) Print all info
	switch (command)
		{
		case 'P':
			// Power on
			{
			DebugMessage("Before fmTuner.start()");
			DebugPulse(2);
			fmTuner.start();          // Power Up Device
#if 0
			while (fmTuner.getShadow2() ==0)
				{
				DebugMessage("repeat fmTuner.start()");
				fmTuner.start();          // Power Up Device
				}
#endif
			DebugPulse(3);
			DebugMessage("After fmTuner.start()");
			DebugPulse(4);
			fmTuner.reportAll();
			DebugPulse(5);
			}
			break;
		case 'v':
			// Volume: v[+,-][n]
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
		case 'm':
			// Mute on/off
			{
			fmTuner.toggleMute();
			}
			break;
		case 's':
			// Stereo on/off
			{
			fmTuner.toggleMono();
			}
			break;
		case 'f':
			// Frequency: f{[+\-]|[<n>]}
			{
			if (sz[0] == '+')
				{
				fmTuner.incChannel();
				}
			else if (sz[0] == '+')
				{
				fmTuner.decChannel();
				}
			else
				{
				//UNDONE: parse frequency
				}
			}
			break;
		case 'S':
			// Scan: S{+|-}
			{
			if (sz[0] == '+')
				{
				if (!fmTuner.seekUp())
					{
					DebugMessage("Error: Seek failure or band limit reached!!");
					}
				}
			else if (sz[0] == '-')
				{
				if (!fmTuner.seekDown())
					{
					DebugMessage("Error: Seek failure or band limit reached!!");
					}
				}
			}
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
