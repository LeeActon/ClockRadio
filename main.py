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
import SurfaceHelper

class ClockRadio:
    surface = None
    clockFace = None
    def __init__(self):
        self.surface = SurfaceHelper.OpenSurface()

        self.clockFace = AnalogClockFace.AnalogClockFace(self.surface)
        self.clockFace.setBackground('New Clock Face.png')
        self.clockFace.setHourHandColor((0,0,0))
        self.clockFace.setMinuteHandColor((0,0,0))
        self.clockFace.setSecondHandColor((255,0,0))
        self.clockFace.setOuterHubColor((255,0,0))

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
            sweep = (math.floor(now.second / 5) % 2) == 0
            self.clockFace.update(now, sweep)

            pygame.display.flip()
            _clock.tick(30)  # Aim for 30fps

    def _exit(self, sig, frame):
        self._running = False
        print("\nExiting!...\n")

    def printHelp(self):
       print('main.py -c <clockface> -h <hour color> -m <minute color> -s <second color> -t <tick color>')

    def main(self, argv):

       try:
           opts, args = getopt.getopt(argv,"c:h:m:s:t:",["clockFace=","hour=", "minute=", "second=", "ticks=", "help"])
       except getopt.GetoptError:
           self.printHelp()
           sys.exit(2)

       for opt, arg in opts:
           if opt == '--help':
               self.printHelp()
               sys.exit()
           elif opt in ("-c", "--clockFace"):
               self.clockFace.setBackground(arg)
           elif opt in ("-h", "--hour"):
               self.clockFace.setHourHandColor(eval(arg))
           elif opt in ("-m", "--minute"):
               self.clockFace.setMinuteHandColor(eval(arg))
           elif opt in ("-s", "--second"):
               self.clockFace.setSecondHandColor(eval(arg))
           elif opt in ("-t", "--tick"):
               self.clockFace.setTickColor(eval(arg))

       self.run()

if __name__ == "__main__":
   clockRadio = ClockRadio()
   clockRadio.main(sys.argv[1:])
