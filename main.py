#!/usr/bin/env python3

import datetime
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

if __name__ == "__main__":
    clockRadio = ClockRadio()
    clockRadio.run()
