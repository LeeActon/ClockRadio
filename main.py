#!/usr/bin/env python3

import datetime
import getopt
import math
import os
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
    def __init__(self):
        self.surface = SurfaceHelper.OpenSurface()

        self.clockFace = AnalogClockFace.AnalogClockFace(self.surface)

        self.clockImage = ImageWidget.ImageWidget(self.surface)
        self.clockImage.loadImage('New Clock Face.png')

        self.clockHands = AnalogClockHands.AnalogClockHands(self.surface)
        self.clockHands.setHourHandColor((0,0,0))
        self.clockHands.setMinuteHandColor((0,0,0))
        self.clockHands.setSecondHandColor((192,0,0))
        self.clockHands.setOuterHubColor((192,0,0))

    def run(self):
        self._running = True
        _clock = pygame.time.Clock()
        signal.signal(signal.SIGINT, self._exit)
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._running = False
                        break

            now = datetime.datetime.now()
            if self.clockImage != None:
                self.clockImage.update()
            if self.clockFace != None:
                self.clockFace.update()
            if self.clockHands != None:
                self.clockHands.update(now)

            pygame.display.flip()
            _clock.tick(30)  # Aim for 30fps

    def _exit(self, sig, frame):
        self._running = False
        print("\nExiting!...\n")

    def printHelp(self):
       print('main.py -c <clockface> -h <hour color> -m <minute color> -s <second color> -t <tick color>')

    def main(self, argv):

       try:
           opts, args = getopt.getopt(argv,"b:f:h:m:s:t:",["backColor=", "face=","hour=", "minute=", "second=", "ticks=", "sweep", "help"])
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
               self.clockHands.setHourHandColor(eval(arg))
           elif opt in ("-m", "--minute"):
               self.clockHands.setMinuteHandColor(eval(arg))
           elif opt in ("-s", "--second"):
               self.clockHands.setSecondHandColor(eval(arg))
           elif opt in ("-t", "--tick"):
               self.clockFace.setTickColor(eval(arg))
           elif opt in ("-b", "--backColor"):
               self.clockFace.setBackColor(eval(arg))
           elif opt == "--sweep":
               self.clockHands.setSweep(True)

       self.run()

if __name__ == "__main__":
   clockRadio = ClockRadio()
   clockRadio.main(sys.argv[1:])
