#!/usr/bin/env python3

import datetime
import getopt
import json
import math
import os
import serial
import signal
import sys
import time

import pygame

import AnalogClockFace
import AnalogClockHands
import ImageWidget
import SurfaceHelper

class ClockRadio:
    surface = None
    clockImage = None
    clockFace = None
    clockHands = None
    settings = None
    auxDevices = None

    def __init__(self):
        self.surface = SurfaceHelper.OpenSurface()

        self.clockHands = AnalogClockHands.AnalogClockHands(self.surface)
        self.clockHands.setHourColor((0,0,0))
        self.clockHands.setMinuteColor((0,0,0))
        self.clockHands.setSecondColor((192,0,0))

    def loadSettings(self):
        f = open('settings.json')

        settings = json.load(f)

        for key, value in settings.items():
            if key == 'backgroundImage':
                if self.clockImage == None:
                    self.clockImage = ImageWidget.ImageWidget(self.surface)
                self.clockImage.loadImage(value)
            elif key == 'AnalogClockHands':
                if self.clockHands == None:
                    self.clockHands = AnalogClockHands.AnalogClockHands(self.surface)
                self.clockHands.loadSettings(value)
            elif key == 'AnalogClockTickMarks':
                if self.clockFace == None:
                    self.clockFace = AnalogClockFace.AnalogClockFace(self.surface)
                self.clockFace.loadSettings(value)

    def run(self):
        self._running = True
        _clock = pygame.time.Clock()
        signal.signal(signal.SIGINT, self._exit)

        self.loadSettings()
        self.auxDevices = serial.Serial('/dev/ttyACM0', 115200)

        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._running = False
                        break

            if self.auxDevices.in_waiting > 0:
                self.handleAuxInput()

            now = datetime.datetime.now()
            if self.clockImage != None:
                self.clockImage.update()
            if self.clockFace != None:
                self.clockFace.update()
            if self.clockHands != None:
                self.clockHands.update(now)

            pygame.display.flip()
            _clock.tick(30)  # Aim for 30fps

    def handleAuxInput(self):
        line = self.auxDevices.readline().decode('utf-8').strip()
        parts = line.split()
        print(f'<-- {line} - {parts}')
        if len(line) > 0:
            ch = line[0]
        if (ch == '*'):
            # Just debug spew
            x = 1
        elif (ch == '.'):
            self.sendAuxDevices('')
        elif (ch == 'B'):
            # Button pressed/released report
            # B <n> : <s>
            # where <n> is the button number
            #       <s> is state (0 - not pressed, 1 - pressed)
            x = 1
        elif (ch == 'R'):
            # Rotary Encoder changed report
            # R <n> : <d>
            # where <n> is the encoder number\
            #       <d> is the amount the encoder has changed
            if len(parts) == 4:
                if parts[1] == '1':
                    v = int(parts[3])
                    if (v > 0):
                        self.sendAuxDevices('v+1')
                    else:
                        self.sendAuxDevices('v-1')

        elif (ch == 'V'):
            # Volume report
            # V: <v>[, mute][, mono]
            # where <v> is the current volume
            #       optional "mute" indcates output is muted
            #       optional "mono" indcates output is forced to mono
            x = 1
        elif (ch == 'F'):
            # Frequency report
            # F: <f> MHz, <s>[, stereo]
            # where <f> is the megahertz of the tuned station
            #       <s> is the signal strength
            #       optional "stereo" indicates the tuner has detected a stereo signal
            x = 1

    def _exit(self, sig, frame):
        self._running = False
        print("\nExiting!...\n")

    def printHelp(self):
       print('main.py -c <clockface> -h <hour color> -m <minute color> -s <second color> -t <tick color>')

    def sendAuxDevices(self, s):
        print(f'--> {s}')
        self.auxDevices.write(s.encode('utf-8'))
        self.auxDevices.write('\n'.encode('utf-8'))

    def main(self, argv):

       try:
           opts, args = getopt.getopt(argv,"b:f:h:m:s:",["backColor=", "face=","hour=", "minute=", "second=", "sweep", "help"])
       except getopt.GetoptError:
           self.printHelp()
           sys.exit(2)

       for opt, arg in opts:
           if opt == '--help':
               self.printHelp()
               sys.exit()
           elif opt in ("-f", "--face"):
               self.clockImage.loadImage(arg)
               self.clockFace = None
           elif opt in ("-h", "--hour"):
               self.clockHands.setHourColor(eval(arg))
           elif opt in ("-m", "--minute"):
               self.clockHands.setMinuteColor(eval(arg))
           elif opt in ("-s", "--second"):
               self.clockHands.setSecondColor(eval(arg))
           elif opt in ("-b", "--backColor"):
               self.clockFace.setBackColor(eval(arg))
           elif opt == "--sweep":
               self.clockHands.setSweep(True)

       self.run()

if __name__ == "__main__":
   clockRadio = ClockRadio()
   clockRadio.main(sys.argv[1:])
