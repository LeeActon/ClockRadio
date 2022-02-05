#!/usr/bin/env python3
import datetime
import os
import sys
import signal
import pygame
from pygame import gfxdraw
import math
from colorsys import hsv_to_rgb
import Widget
import SurfaceHelper

class AnalogClockFace(Widget.Widget):
    clockFaceBackground = None
    tickColor = (0,0,255)

    def __init__(self, surface):
        super().__init__(surface)

        self.backColor = (0,0,0)

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

    def update(self):

        super().update()

        if self.clockFaceBackground != None:

            self.surface.blit(self.clockFaceBackground, (0,0))

        else:

            for s in range(60):
                a = 360 / 60.0 * s
                end = self._get_point(self.center, a, self._marks + 5)
                self._line(self.tickColor, self.center, end, 3)

            if (self.backColor != None):
                self._circle(self.backColor, self.center, self._marks - 5)

            for s in range(12):
                a = 360 / 12.0 * s
                x, y = self._get_point(self.center, a, self._marks)

                r = 5
                if s % 3 == 0:
                    r = 10

                x = int(x)
                y = int(y)

                self._circle(self.tickColor, (x, y), r)

    def setTickColor(self, color):
        self.tickColor = color

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
    clockFace.run()
