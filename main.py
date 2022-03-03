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
import ImageLayer
import SurfaceHelper
import Page
import ClockPage

class ClockRadio:
    surface = None
    clockPage = None
    settings = None
    auxDevices = None
    page = None

    def __init__(self):
        self.surface = SurfaceHelper.OpenSurface()

        self.clockPage = ClockPage.ClockPage(self.surface)

        self.page = self.clockPage

    def loadSettings(self):
        f = open('settings.json')

        settings = json.load(f)

        for key, value in settings.items():
            if key == 'clock':
                if (self.clockPage != None):
                    self.clockPage.loadSettings(value)

    def run(self):
        self._running = True
        _clock = pygame.time.Clock()
        signal.signal(signal.SIGINT, self._exit)

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

            if self.clockPage != None:
                now = datetime.datetime.now()
                self.clockPage.update(now)

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
            pass
        elif (ch == '.'):
            self.sendAuxDevices('')
        elif (ch == 'B'):
            # Button pressed/released report
            # B <n> : <s>
            # where <n> is the button number
            #       <s> is state (0 - not pressed, 1 - pressed)
            if (self.page != None):
                buttonId = int(parts[1])
                state = int(parts[3])
                if state != 0:
                    self.page.handleButtonDown(buttonId)
                else:
                    self.page.handleButtonUp(buttonId)
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
            pass
        elif (ch == 'F'):
            # Frequency report
            # F: <f> MHz, <s>[, stereo]
            # where <f> is the megahertz of the tuned station
            #       <s> is the signal strength
            #       optional "stereo" indicates the tuner has detected a stereo signal
            pass

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

       self.loadSettings()
       for opt, arg in opts:
           if opt == '--help':
               self.printHelp()
               sys.exit()
           elif opt in ("-f", "--face"):
               self.clockPage.loadBackgroundImage(arg)
               self.clockPage.clockFace = None
           elif opt in ("-h", "--hour"):
               self.clockPage.clockHands.setHoursColor(eval(arg))
           elif opt in ("-m", "--minute"):
               self.clockPage.clockHands.setMinutesColor(eval(arg))
           elif opt in ("-s", "--second"):
               self.clockPage.clockHands.setSecondsColor(eval(arg))
           elif opt == "--sweep":
               self.clockPage.clockHands.setSweep(True)

       self.run()

if __name__ == "__main__":
   clockRadio = ClockRadio()
   clockRadio.main(sys.argv[1:])
