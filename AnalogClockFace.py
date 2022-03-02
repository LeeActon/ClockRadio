#!/usr/bin/env python3
import datetime
import os
import sys
import signal
import pygame
from pygame import gfxdraw
import math
from colorsys import hsv_to_rgb
import Layer
import SurfaceHelper

class AnalogClockFace(Layer.Layer):
    quarterHourColor = (0,0,255)
    hourColor = (0,0,192)
    minuteColor = (0,192,192)

    def __init__(self, surface):
        super().__init__(surface)

        self.backColor = None

        # For some reason the canvas needs a 7px vertical offset
        # circular screens are weird...
        self.center = (240, 247)
        self._radius = 240

        # Distance of hour marks from center
        self._marks = 220

        self._running = False
        #self._origin = pygame.math.Vector2(*self.center)

    def _exit(self, sig, frame):
        self._running = False
        print("\nExiting!...\n")

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def loadSettings(self, settings):
        for key, value in settings.items():
            if key == 'quarterHourColor':
                self.setQuarterHourColor(eval(value))
            elif key == 'hourColor':
                self.setHourColor(eval(value))
            elif key == 'minuteColor':
                self.setMinuteColor(eval(value))

    def update(self):

        super().update()

        for s in range(60):
            a = 360 / 60.0 * s
            start = self._get_point(self.center, a, self._marks - 5)
            end = self._get_point(self.center, a, self._marks + 5)
            self._line(self.minuteColor, start, end, 3)

        for s in range(12):
            a = 360 / 12.0 * s
            x, y = self._get_point(self.center, a, self._marks)

            x = int(x)
            y = int(y)

            if s % 3 == 0:
                self._circle(self.quarterHourColor, (x, y), 10)
            else:
                self._circle(self.hourColor, (x, y), 5)


    def setQuarterHourColor(self, color):
        self.quarterHourColor = color

    def setHourColor(self, color):
        self.hourColor = color

    def setMinuteColor(self, color):
        self.minuteColor = color

    def run(self):
        self._running = True
        signal.signal(signal.SIGINT, self._exit)
        _clock = pygame.time.Clock()
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._running = False
                        break
            self.update()

            pygame.display.flip()
            _clock.tick(30)  # Aim for 30fps

        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    surface = SurfaceHelper.OpenSurface()
    clockFace = AnalogClockFace(surface)
    clockFace.setBackColor((0,0,0))
    clockFace.setTickColor((0,0,192))
    clockFace.run()
