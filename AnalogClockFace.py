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
from AnalogGauge import AnalogGauge
from Style import Style
from Polygon import Polygon


class AnalogClockFace(Layer):

    def __init__(self):
        super().__init__()

        self.quarterHourColor = (0,0,255)
        self.hourColor = (0,0,192)
        self.minuteColor = (0,192,192)
        self._running = False
    def __str__(self):
        return f"AnalogClockFace"

    def createClockFace(self):
        self.analogGauge = AnalogGauge()
        self.addLayer(self.analogGauge)

        self.analogGauge.ticksStartAngle = 1/4
        self.analogGauge.ticksEndAngle = self.analogGauge.ticksStartAngle - 59/60
        self.analogGauge.minValue = 0
        self.analogGauge.maxValue = 59
        self.analogGauge.value = 0

        self.minutesStyle = Style()
        self.minutesStyle.length = 10
        self.minutesStyle.width = 3
        self.minutesStyle.strokeColor = (0, 0, 0)
        self.minutesStyle.fillColor = (0, 0, 0)

        self.hoursStyle = Style()
        self.hoursStyle.length = 20
        self.hoursStyle.width = 5
        self.hoursStyle.strokeColor = (0, 0, 255)
        self.hoursStyle.fillColor = (0, 0, 255)

        self.quarterHoursStyle = Style()
        self.quarterHoursStyle.length = 30
        self.quarterHoursStyle.width = 7
        self.quarterHoursStyle.strokeColor = (255, 0, 0)
        self.quarterHoursStyle.fillColor = (255, 0, 0)
        points = [[0, 0], [15, 15], [30, 0], [15, -15], [0, 0]] # Diamond
        self.quarterHoursStyle.shape = Polygon(points)

        self.analogGauge.createTickMarks([15,5,1], [self.quarterHoursStyle, self.hoursStyle, self.minutesStyle])

    def _exit(self, sig, frame):
        self._running = False
        print("\nExiting!...\n")

    def run(self, surface):
        self._running = True
        signal.signal(signal.SIGINT, self._exit)
        _clock = pygame.time.Clock()
        while self._running:
            self.paint(surface)

            pygame.display.flip()
            _clock.tick(30)  # Aim for 30fps

        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    surface = SurfaceHelper.OpenSurface()
    clockFace = AnalogClockFace()

    clockFace.style = Style()
    clockFace.style.radius = 210
    clockFace.style.backColor = (127, 127, 127)

    clockFace.run(surface)
