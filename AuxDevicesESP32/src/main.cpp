/*
  This project is built with PlatformIO.
  The target board is Helltec_Wifi_Kit_32 (ESP32).
  See:
    https://docs.platformio.org/en/latest/boards/espressif32/heltec_wifi_kit_32.html?utm_source=platformio&utm_medium=piohome
    https://robotzero.one/heltec-wifi-kit-32
*/

void DebugMessage(const char* szMessage);
#include <Arduino.h>
#include "RotaryEncoderEx.h"
#include "FMTuner.h"

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

#define DEBUG_PIN 14

void DebugMessage(const char* szMessage)
	{
	Serial.print("*");
	Serial.println(szMessage);
	}

void PulsePin(int pin, int microSeconds)
	{
	digitalWrite(pin, HIGH);
	delayMicroseconds(microSeconds);
	digitalWrite(pin, LOW);
	}

void DebugPulse(int count)
	{
	PulsePin(DEBUG_PIN, count * 10);
	}

// Connections (through 5V to 3.3V converter)
#define R_RST  19
#define R_SDIO 21
#define R_SCLK 22
#define R_INT  0

void HandleSerialInput();
void HandleSerialInput(char* sz);

FMTuner fmTuner(&Serial, R_RST, R_SDIO, R_SCLK, R_INT);

#define ROTARY_ENCODER_1_BUTTON_PIN 36
#define ROTARY_ENCODER_1_PIN_A      37
#define ROTARY_ENCODER_1_PIN_B      38

#define ROTARY_ENCODER_2_BUTTON_PIN 39
#define ROTARY_ENCODER_2_PIN_A      34
#define ROTARY_ENCODER_2_PIN_B      35

#define ROTARY_ENCODER_3_BUTTON_PIN 32
#define ROTARY_ENCODER_3_PIN_A      33
#define ROTARY_ENCODER_3_PIN_B      27

#define ROTARY_ENCODER_4_BUTTON_PIN 23
#define ROTARY_ENCODER_4_PIN_A      18
#define ROTARY_ENCODER_4_PIN_B      5

#define ROTARY_ENCODER_5_BUTTON_PIN 17
#define ROTARY_ENCODER_5_PIN_A      0
#define ROTARY_ENCODER_5_PIN_B      2

#define ROTARY_ENCODER_STEPS 4
#define ROTARY_ENCODER_COUNT 5

RotaryEncoderEx (rgRotaryEncoder)[ROTARY_ENCODER_COUNT] =
    {
    RotaryEncoderEx(11, ROTARY_ENCODER_1_PIN_A, ROTARY_ENCODER_1_PIN_B, ROTARY_ENCODER_1_BUTTON_PIN, AIESP32ROTARYENCODER_DEFAULT_VCC_PIN, ROTARY_ENCODER_STEPS ),
    RotaryEncoderEx(12, ROTARY_ENCODER_2_PIN_A, ROTARY_ENCODER_2_PIN_B, ROTARY_ENCODER_2_BUTTON_PIN, AIESP32ROTARYENCODER_DEFAULT_VCC_PIN, ROTARY_ENCODER_STEPS ),
    RotaryEncoderEx(13, ROTARY_ENCODER_3_PIN_A, ROTARY_ENCODER_3_PIN_B, ROTARY_ENCODER_3_BUTTON_PIN, AIESP32ROTARYENCODER_DEFAULT_VCC_PIN, ROTARY_ENCODER_STEPS ),
    RotaryEncoderEx(14, ROTARY_ENCODER_4_PIN_A, ROTARY_ENCODER_4_PIN_B, ROTARY_ENCODER_4_BUTTON_PIN, AIESP32ROTARYENCODER_DEFAULT_VCC_PIN, ROTARY_ENCODER_STEPS ),
    RotaryEncoderEx(15, ROTARY_ENCODER_5_PIN_A, ROTARY_ENCODER_5_PIN_B, ROTARY_ENCODER_5_BUTTON_PIN, AIESP32ROTARYENCODER_DEFAULT_VCC_PIN, ROTARY_ENCODER_STEPS )
    };

void IRAM_ATTR readEncoder1ISR()
{
    rgRotaryEncoder[0].readEncoder_ISR();
}

void IRAM_ATTR readEncoder2ISR()
{
    rgRotaryEncoder[1].readEncoder_ISR();
}

void IRAM_ATTR readEncoder3ISR()
{
    rgRotaryEncoder[2].readEncoder_ISR();
}

void IRAM_ATTR readEncoder4ISR()
{
    rgRotaryEncoder[3].readEncoder_ISR();
}

void IRAM_ATTR readEncoder5ISR()
{
    rgRotaryEncoder[4].readEncoder_ISR();
}

RotaryEncoderEx* FindRotaryEncoder(int id)
	{
	for (int i = 0; i < ROTARY_ENCODER_COUNT; i++)
		{
		if (rgRotaryEncoder[i].id == id)
			return &(rgRotaryEncoder[i]);
		}

	return NULL;
	}

void setup()
    {
    Serial.begin(115200);
	Serial.setTimeout(30000); // Wait up to thirty seconds for input
	Serial.println();
	Serial.println("Started");

	pinMode(DEBUG_PIN, OUTPUT);
	digitalWrite(DEBUG_PIN, LOW);

	DebugPulse(1);

	// Wait for input before going any further.
	// Makes debugging easier.
	while (!Serial.available())
		{

		Serial.println(".");
		delay(1000);
		}

    rgRotaryEncoder[0].begin();
    rgRotaryEncoder[0].setup(readEncoder1ISR);
    rgRotaryEncoder[1].begin();
    rgRotaryEncoder[1].setup(readEncoder2ISR);
    rgRotaryEncoder[2].begin();
    rgRotaryEncoder[2].setup(readEncoder3ISR);
    rgRotaryEncoder[3].begin();
    rgRotaryEncoder[3].setup(readEncoder4ISR);
    rgRotaryEncoder[4].begin();
    rgRotaryEncoder[4].setup(readEncoder5ISR);
    }

void loop()
    {
	if (Serial.available())
		HandleSerialInput(); // Radio control from serial interface

    for (int i = 0; i < 5; i++)
        {
        rgRotaryEncoder[i].reportPosition(&Serial);
        rgRotaryEncoder[i].reportButton(&Serial);
        }
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
		case 'r':
			DebugPulse(1);

			pinMode(R_RST, OUTPUT);
			pinMode(R_SDIO, OUTPUT);
			pinMode(R_SCLK, OUTPUT);

			// Set communcation mode to 2-Wire
			digitalWrite(R_RST, LOW);   // Put Si4703 into reset
			delay(1);                     // Delay to allow pins to settle
			digitalWrite(R_SDIO, LOW);   // A low SDIO indicates a 2-wire interface
			delay(1);                     // Delay to allow pins to settle
			digitalWrite(R_RST, HIGH);  // Bring Si4703 out of reset with SDIO set to low and SEN pulled high with on-board resistor
			delay(1);                     // Allow Si4703 to come out of reset
			digitalWrite(R_SDIO, HIGH);
			digitalWrite(R_SCLK, HIGH);
			break;

		case 'P':
			// Power on
			{
			DebugMessage("Before fmTuner.start()");
			DebugPulse(2);
			fmTuner.start();          // Power Up Device
			DebugPulse(3);
			DebugMessage("After fmTuner.start()");
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
			// Frequency: f{[+|-]|<space><n>}
			{
			if (sz[0] == '+')
				{
				fmTuner.incChannel();
				}
			else if (sz[0] == '-')
				{
				fmTuner.decChannel();
				}
			else if (sz[0] == ' ')
				{
				int f = atoi(sz + 1);
				if (f != 0)
					fmTuner.setChannel(f);
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

		case 'R':
			{
			int id;
			int value;
			int min;
			int max;
			int acceleration;
			int wrap;

			if (sz[0] == '-')
				{
				id = atoi(sz + 1);
				RotaryEncoderEx *pRotaryEncoder = FindRotaryEncoder(id);
				if (pRotaryEncoder != NULL)
					{
					pRotaryEncoder->restorePosition();
					}
				}
			else
				{
				int count = sscanf(sz, "%d : %d, %d, %d, %d, %d", &id, &value, &min, &max, &acceleration, &wrap);
				if (count == 6)
					{
					RotaryEncoderEx *pRotaryEncoder = FindRotaryEncoder(id);
					if (pRotaryEncoder != NULL)
						{
						pRotaryEncoder->setBoundaries(min, max, wrap != 0);
						pRotaryEncoder->setEncoderValue(value);
						pRotaryEncoder->setAcceleration(acceleration);
						}
					}
				}
			}
			break;

		case '?':
			{
			fmTuner.reportAll();
			Serial.println(".");
			}
			break;
		}
	}