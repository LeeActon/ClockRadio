#!/usr/bin/env python3

#UNDONE: Remove when no longer debugging
#{
import debugpy
debugpy.listen(("0.0.0.0", 5678))
#}

import datetime
import getopt
import json
import math
import os
import serial
import signal
import sys
import time
import select


import pygame

import SurfaceHelper
from Page import Page
from ClockPage import ClockPage
from TextLayer import TextLayer
from VolumePage import VolumePage
from Layer import Layer
from Settings import Settings
from Style import Style
from AnalogClockFace import AnalogClockFace
from FMPage import FMPage

class ClockRadio:

    def __init__(self):
        self.surface = SurfaceHelper.OpenSurface()

        self.auxDevices = None
        self.fontM = None
        self.fontL = None
        self.fontXL = None

    def run(self):
        self._running = True
        _clock = pygame.time.Clock()
        signal.signal(signal.SIGINT, self._exit)

        textLayer = TextLayer()
        textLayer.text = "Hello World"
        textLayer.font = self.fontM
        textLayer.position = (480/2, 480*5/8)

        while self._running:
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                line = sys.stdin.readline()
                if line:
                    if line[0] == 'q':
                        self._running = False
                    elif line[0] == 'l':
                        Layer.offsetX(-1)
                    elif line[0] == 'r':
                        Layer.offsetX(1)
                    elif line[0] == 'u':
                        Layer.offsetY(-1)
                    elif line[0] == 'd':
                        Layer.offsetY(1)
                    elif line[0] == 'p':
                        Page.pushIfNotCurrent(self.volumePage)
                        self.volumePage.timeOut = time.time() + 55
                    elif line[0] == 'x':
                        textLayer.visible = not textLayer.visible
                    elif line[0] == 'z':
                        self.volumePage.toggleZeroIndicator()
                    elif line[0] == 'b':
                        debugpy.breakpoint()

            if self.auxDevices.in_waiting > 0:
                self.handleAuxInput()

            Page.updateCurrentPage()

            now = datetime.datetime.now()
            hour = now.hour
            if hour > 12:
                hour -= 12
            textLayer.text = f"{hour}:{now.minute:02d}:{now.second:02d}"
            textLayer.paint(self.surface)

            pygame.display.flip()
            _clock.tick(30)  # Aim for 30fps

    def handleAuxInput(self):
        page = Page.getCurrentPage()
        line = self.auxDevices.readline().decode("utf-8").strip()
        parts = line.split()
        print(f"<-- {line}\n")
        if len(line) > 0:
            ch = line[0]
        if (ch == '*'):
            # Just debug spew
            pass
        elif (ch == '.'):
            self.sendAuxDevices("")
            self.sendAuxDevices(f"R {self.volumePage.rotaryId} : 0, 0, 30, 150, 0")
            self.sendAuxDevices(f"R {self.fmPage.rotaryId} : 949, 880, 1080, 150, 1")
            self.sendAuxDevices(f"R 13 : 0, -8000, 8000, 0, 1")
        elif (ch == 'B'):
            # Button pressed/released report
            # B <n> : <s>
            # where <n> is the button number
            #       <s> is state (0 - not pressed, 1 - pressed)
            if len(parts) == 4:
                if (page != None):
                    buttonId = int(parts[1])
                    state = int(parts[3])
                    page.handleButton(buttonId, state)
        elif (ch == 'R'):
            # Rotary Encoder changed report
            # R <n> : <d>
            # where <n> is the encoder number\
            #       <d> is the amount the encoder has changed
            if len(parts) >= 4:
                if (page != None):
                    rotaryId = int(parts[1])
                    value = int(parts[3].rstrip(", "))
                    for p in [self.volumePage, self.fmPage, page]:
                        if p.handleRotary(rotaryId, value):
                            break;

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
       print("main.py -c <clockface> -h <hour color> -m <minute color> -s <second color> -t <tick color>")

    def sendAuxDevices(self, s):
        print(f"--> {s}")
        self.auxDevices.write(s.encode("utf-8"))
        self.auxDevices.write("\n".encode("utf-8"))

    def main(self, argv):

       try:
           opts, args = getopt.getopt(argv,"b:f:h:m:s:",["backColor=", "face=","hour=", "minute=", "second=", "sweep", "debug", "help"])
       except getopt.GetoptError:
           self.printHelp()
           sys.exit(2)

       settings = Settings.loadSettings("settings.json")

       self.auxDevices = serial.Serial("/dev/ttyUSB0", 115200)

       pygame.font.init()

       self.fontM = pygame.font.Font("/usr/share/fonts/7segment.ttf", 64)
       self.fontL = pygame.font.Font("/usr/share/fonts/7segment.ttf", 64+64)
       self.fontXL = pygame.font.Font("/usr/share/fonts/7segment.ttf", 64+64+32+8)

       clockPages = list(settings.clockPages.values())
       for clockPage in clockPages:
           clockPage.surface = self.surface

       self.clockPage = clockPages[0]

       self.clockPage.linkUp(clockPages[1:])

       self.volumePage = VolumePage()
       self.volumePage.rotaryId = 11
       self.volumePage.auxDevices = self.auxDevices
       self.volumePage.font = self.fontXL
       self.volumePage.surface = self.surface
       self.fmPage = FMPage()
       self.fmPage.rotaryId = 12
       self.fmPage.auxDevices = self.auxDevices
       self.fmPage.font = self.fontXL
       self.fmPage.surface = self.surface
       self.clockPage.linkRight([self.volumePage, self.fmPage])

       Page.setCurrentPage(self.clockPage)

       for opt, arg in opts:
           if opt == "--help":
               self.printHelp()
               sys.exit()
           elif opt == "--debug":
               print("Waiting for debugger to attach")
               debugpy.wait_for_client()
           elif opt in ("-f", "--face"):
               self.clockPage.backgroundImage = arg
               self.clockPage.clockFace = None
           elif opt == "--sweep":
               self.clockPage.clockHands.setSweep(True)

       self.run()

if __name__ == "__main__":
   clockRadio = ClockRadio()
   clockRadio.main(sys.argv[1:])
