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
from SleepPage import SleepPage
from Layer import Layer

class ClockRadio:

    def __init__(self):
        self.surface = SurfaceHelper.OpenSurface()

        self.auxDevices = None
        self.fontLED_M = None
        self.fontLED_L = None
        self.fontLED_XL = None

    def run(self):
        self._running = True
        _clock = pygame.time.Clock()
        signal.signal(signal.SIGINT, self._exit)

        while self._running:
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                line = sys.stdin.readline()
                if line:
                    if line[0] == 'q':
                        self._running = False
                    elif line[0] == 'b':
                        debugpy.breakpoint()
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
                    elif line[0] == 'z':
                        self.volumePage.toggleZeroIndicator()
                    elif line[0] == 'a':
                        n = line[1]
                        t = datetime.datetime.strptime(line.strip(), f"a{n} %I:%M")
                        if n == '1':
                            self.clockPage.alarmIndicator1.time = t
                        elif n == '2':
                            self.clockPage.alarmIndicator2.time = t

            if self.auxDevices.in_waiting > 0:
                self.handleAuxInput()

            Page.updateCurrentPage()

            now = datetime.datetime.now()
            hour = now.hour
            if hour > 12:
                hour -= 12

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
            self.sendAuxDevices("P") # power on the FM tuner
            self.fmPage.setMode(FMPage.MODE_PRESET)
        elif (ch == 'B'):
            # Button pressed/released report
            # B <n> : <s>
            # where <n> is the button number
            #       <s> is state (0 - not pressed, 1 - pressed)
            if len(parts) == 4:
                if (page != None):
                    buttonId = int(parts[1])
                    state = int(parts[3])
                    for p in [self.volumePage, self.fmPage, page]:
                        if p != None:
                            if p.handleButton(buttonId, state):
                                break;

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
        elif (ch == 'F'):
            # Frequency report
            # F: <f> MHz, <s>[, stereo]
            # where <f> is the megahertz of the tuned station
            #       <s> is the signal strength
            #       optional "stereo" indicates the tuner has detected a stereo signal
            if len(parts) >= 2:
                freq = eval(parts[1])
                strength = 0
                stereo = ""
                if len(parts) >= 3:
                    strength = eval(parts[2])
                    if len (parts) >= 4:
                        stereo = parts[3]
                self.fmPage.tuningReport(freq, strength, stereo)

        elif (ch == 'V'):
            # Volume report
            # V: <v>[, mute][, mono]
            # where <v> is the current volume
            #       optional "mute" indcates output is muted
            #       optional "mono" indcates output is forced to mono
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

    def waitForDebugger(self):
        print("Waiting for debugger to attach")
        debugpy.wait_for_client()
        print("Debugger attached")

    def main(self, argv):

       try:
           opts, args = getopt.getopt(argv,"b:f:h:m:s:",["backColor=", "face=","hour=", "minute=", "second=", "sweep", "debug", "help"])
       except getopt.GetoptError:
           self.printHelp()
           sys.exit(2)

       for opt, arg in opts:
           if opt == "--help":
               self.printHelp()
               sys.exit()
           elif opt == "--debug":
               self.waitForDebugger()

       pygame.font.init()

       settings = Settings.loadSettings("settings.json")

       Layer.settings = settings

       self.auxDevices = serial.Serial("/dev/ttyUSB0", 115200)
       self.sendAuxDevices("?")

       self.fontLED_M = settings.fonts["LED_M"]
       self.fontLED_L = settings.fonts["LED_L"]
       self.fontLED_XL = settings.fonts["LED_XL"]
       self.font_S = settings.fonts["text_S"]
       self.font_M = settings.fonts["text_M"]

       clockPages = list(settings.clockPages.values())
       for clockPage in clockPages:
           clockPage.surface = self.surface

       alarmPages = list(settings.alarmPages.values())
       for alarmPage in alarmPages:
           alarmPage.surface = self.surface
           alarmPage.auxDevices = self.auxDevices
           alarmPage.rotaryId = Page.menuRotaryId

       self.clockPage = clockPages[0]
       if len(alarmPages) > 0:
           self.clockPage.alarmIndicator1 = alarmPages[0].alarmIndicator
           alarmPages[0].time = datetime.time(6,0)
       if len(alarmPages) > 1:
           self.clockPage.alarmIndicator2 = alarmPages[1].alarmIndicator
           alarmPages[1].time = datetime.time(7,0)

       self.mainMenuPage = settings.menuPages["main"]
       self.mainMenuPage.surface = self.surface
       self.mainMenuPage.auxDevices = self.auxDevices
       self.mainMenuPage.rotaryId = Page.menuRotaryId

       self.clockPage.menuPage = self.mainMenuPage

       #self.clockPage.linkUp([self.mainMenuPage])
       #self.mainMenuPage.linkUp(alarmPages)
       #alarmPages[1].linkUp(clockPages[1:])

       self.sleepPage = SleepPage()
       self.sleepPage.rotaryId = Page.volumeRotaryId
       self.sleepPage.auxDevices = self.auxDevices
       self.sleepPage.digitalValueFont = self.fontLED_XL
       self.sleepPage.textFont = self.font_M
       self.sleepPage.surface = self.surface


       self.volumePage = VolumePage()
       self.volumePage.rotaryId = Page.volumeRotaryId
       self.volumePage.auxDevices = self.auxDevices
       self.volumePage.digitalValueFont = self.fontLED_XL
       self.volumePage.textFont = self.font_M
       self.volumePage.surface = self.surface
       self.volumePage.sleepPage = self.sleepPage

       self.fmPage = FMPage()
       self.fmPage.rotaryId = Page.FMRotaryId
       Page.setButtonRepeatRate(self.fmPage.rotaryId, 1000000000) # in ns this is one second
       self.fmPage.auxDevices = self.auxDevices
       self.fmPage.fmStations = settings.fmStations
       self.fmPage.presetFMStations = settings.presetFMStations
       self.fmPage.font = self.fontLED_XL
       self.fmPage.callSignFont = self.font_M
       self.fmPage.formatFont = self.font_S
       self.fmPage.stereoFont = self.font_S
       self.fmPage.surface = self.surface
       self.clockPage.linkRight([self.volumePage, self.fmPage])

       Page.setCurrentPage(self.clockPage)

       for opt, arg in opts:
           if opt in ("-f", "--face"):
               self.clockPage.backgroundImage = arg
               self.clockPage.clockFace = None
           elif opt == "--sweep":
               self.clockPage.clockHands.setSweep(True)

       self.run()

if __name__ == "__main__":
   clockRadio = ClockRadio()
   clockRadio.main(sys.argv[1:])
