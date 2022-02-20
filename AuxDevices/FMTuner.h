
// Uses Silicon Labs Si4703 Arduino Library
// see: https://github.com/mkhuthir/Si4703
#include <Si4703.h>
#include <Wire.h>
#include <EEPROM.h>

// EEPROM Usage Map
#define eeprom_signature 1
#define eeprom_signature_value 0xCA
#define eeprom_chn_msb   2
#define eeprom_chn_lsb   3
#define eeprom_vol       4

class FMTuner : public Si4703
	{
	private:
		Stream* pStream = NULL;
		int volume;
		int channel;

	public:
		FMTuner(Stream* pStream, int resetPin, int sdioPin, int sclkPin, int interrupt)
			: Si4703(resetPin, sdioPin, sclkPin, interrupt)
			{
			this->pStream = pStream;
			this->volume = -1;
			this->channel = -1;
			}

		void setVolume(int volume)
			{
			//  0 -> 0 0000 - Mute
			//  1 -> 1 0001 : -58 dBFS
			//  2 -> 1 0010 : -56 dBFS
			//  3 -> 1 0011 : -54 dBFS
			//  4 -> 1 0100 : -52 dBFS
			//  5 -> 1 0101 : -50 dBFS
			//  6 -> 1 0110 : -48 dBFS
			//  7 -> 1 0111 : -46 dBFS
			//  8 -> 1 1000 : -44 dBFS
			//  9 -> 1 1001 : -42 dBFS
			// 10 -> 1 1010 : -40 dBFS
			// 11 -> 1 1011 : -38 dBFS
			// 12 -> 1 1100 : -36 dBFS
			// 13 -> 1 1101 : -34 dBFS
			// 14 -> 1 1110 : -32 dBFS
			// 15 -> 1 1111 : -30 dBFS
			// 16 -> 0 0001 : -28 dBFS Skip 0 0000 because that's mute too
			// 17 -> 0 0010 : -26 dBFS
			// 18 -> 0 0011 : -24 dBFS
			// 19 -> 0 0100 : -22 dBFS
			// 20 -> 0 0101 : -20 dBFS
			// 21 -> 0 0110 : -18 dBFS
			// 22 -> 0 0111 : -16 dBFS
			// 23 -> 0 1000 : -14 dBFS
			// 24 -> 0 1001 : -12 dBFS
			// 25 -> 0 1010 : -10 dBFS
			// 26 -> 0 1011 :  -8 dBFS
			// 27 -> 0 1100 :  -6 dBFS
			// 28 -> 0 1101 :  -4 dBFS
			// 29 -> 0 1110 :  -2 dBFS
			// 30 -> 0 1111 :  -0 dBFS

			if (volume < 0)
				volume = 0;
			else if (volume > 30)
				volume = 30;

			this->volume = volume;
			int v = (this->volume & 0x0F);
			if (this->volume >= 16)
				v++;
			Si4703::setVolExt(this->volume <= 15);
			Si4703::setVolume(v);
			save();
			reportVolume();
			}

		void reportVolume()
			{
			if (this->pStream != NULL)
				{
				this->pStream->print("V : ");
				this->pStream->print(this->volume);
				if (getMute())
					{
					pStream->print(", mute");
					}
				if (getMono())
					{
					pStream->print(", mono");
					}
				this->pStream->println();
				}
			}

		void addVolume(int delta)
			{
			this->setVolume(this->volume + delta);
			}

		int getVolume()
			{
			return this->volume;
			}

		void toggleMute()
			{
			this->setMute(!this->getMute());
			}

		void setMute(bool mute)
			{
			// Si4703's mute is opposite of what you'd expect.
			// It's true if mute is disabled.
			// So we invert it to make more sense.
			Si4703::setMute(!mute);
			reportVolume();
			}

		bool getMute()
			{
			// Si4703's mute is opposite of what you'd expect.
			// It's true if mute is disabled.
			// So we invert it to make more sense.
			return !Si4703::getMute();
			}

		void toggleMono()
			{
			this->setMono(!this->getMono());
			}

		void setMono(bool mono)
			{
			Si4703::setMono(mono);
			reportVolume();
			}

		void reportFrequency()
			{
			if (this->pStream != NULL)
				{
				int whole = this->channel / 100;
				int frac = this->channel % 100;
				this->pStream->print("F : ");
				this->pStream->print(whole);
				this->pStream->print(".");
				this->pStream->print(frac);
				this->pStream->print(" Mhz, S : ");
				this->pStream->print(this->getRSSI());
				if (this->getST())
					{
					this->pStream->print(", stereo");
					}
				this->pStream->println();
				}
			}

		int getChannel()
			{
			return this->channel;
			}

		void syncChannel()
			{
			this->channel = Si4703::getChannel();
			save();
			reportFrequency();
			}

		void setChannel(int channel)
			{
			Si4703::setChannel(channel);
			syncChannel();
			}

		void incChannel()
			{
			Si4703::incChannel();
			syncChannel();
			}

		void decChannel()
			{
			Si4703::decChannel();
			syncChannel();
			}

		bool seekUp()
			{
			bool fOk = Si4703::seekUp();
			if (fOk)
				syncChannel();

			return fOk;
			}

		bool seekDown()
			{
			bool fOk = Si4703::seekDown();
			if (fOk)
				syncChannel();

			return fOk;
			}

		void start()
			{
			Si4703::start();

			DebugMessage("Before read_EEPROM()");
			restore();
			DebugMessage("After read_EEPROM()");

			Si4703::setChannel(this->channel);
			Si4703::setVolume(this->volume);
			}

		void save()
			{
			EEPROM.write(eeprom_signature, eeprom_signature_value);

			int chan = this->channel;
			int msb = chan >> 8;
			int lsb = chan & 0x00FF;
			EEPROM.write(eeprom_chn_msb, msb);
			EEPROM.write(eeprom_chn_lsb, lsb);

			EEPROM.write(eeprom_vol, this->volume);
			}

		void restore()
			{
			int signature = EEPROM.read(eeprom_signature);
			if (signature == eeprom_signature_value)
				{
				// Read channel value
				int MSB = EEPROM.read(eeprom_chn_msb);
				int LSB = EEPROM.read(eeprom_chn_lsb);
				this->channel = (MSB << 8) | LSB;

				// Read Volume
				this->volume = EEPROM.read(eeprom_vol);
				}
			}

		void reportAll()
			{
			if (this->pStream != NULL)
				{
				reportFrequency();
				reportVolume();
				}
			}
	};