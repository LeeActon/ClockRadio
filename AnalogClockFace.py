#!/usr/bin/env python3
import datetime
import os
import sys
import signal
import pygame
from pygame import gfxdraw
import math
from colorsys import hsv_to_rgb
from Layer import Layer
import SurfaceHelper
import Points

class AnalogClockFace(Layer):

    def __init__(self):
        super().__init__()

        self.backColor = None
        self._radius = 240

        # Distance of hour marks from center
        self._marks = 220

        self.quarterHourColor = (0,0,255)
        self.hourColor = (0,0,192)
        self.minuteColor = (0,192,192)
        self._running = False

    def _exit(self, sig, frame):
        self._running = False
        print("\nExiting!...\n")

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def loadSettings(self, settings):
        for key, value in settings.items():
            if key == "quarterHourColor":
                self.quarterHourColor = eval(value)
            elif key == "hourColor":
                self.hourColor = eval(value)
            elif key == "minuteColor":
                self.minuteColor = eval(value)

    def paint(self, surface):
        if (not self.visible):
            return

        super().paint(surface)

        for s in range(60):
            angle = math.radians(90 - 360 / 60.0 * s)
            start = Points.getPoint(Layer.center, angle, self._marks - 5)
            end = Points.getPoint(Layer.center, angle, self._marks + 5)
            self.drawLine(surface, start, end, 3, (0, 0, 0), self.minuteColor)

        for s in range(12):
            angle = math.radians(90 - 360 / 12.0 * s)
            x, y = Points.getPoint(Layer.center, angle, self._marks)

            x = int(x)
            y = int(y)

            if s % 3 == 0:
                self.drawCircle(surface, (x, y), 10, (0, 0, 0), self.quarterHourColor)
            else:
                self.drawCircle(surface, (x, y), 5, (0, 0, 0), self.hourColor)


    def run(self, surface):
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
            self.paint(surface)

            pygame.display.flip()
            _clock.tick(30)  # Aim for 30fps

        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    surface = SurfaceHelper.OpenSurface()
    clockFace = AnalogClockFace(surface)
    clockFace.style.backColor = (0, 0, 0)
    clockFace.run(surface)
