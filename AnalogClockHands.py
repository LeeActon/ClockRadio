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
from Style import Style

class AnalogClockHands(Layer):
    hoursStyle_type = Style
    minutesStyle_type = Style
    secondsStyle_type = Style

    def __init__(self):
        super().__init__()

        self.style = Style()
        self.style.radius = 240

        self.time = datetime.datetime.now()

        self.hoursStyle = Style()
        self.hoursStyle.fillColor = (0,0,0)
        self.hoursStyle.width = 11
        self.hoursStyle.length = -110
        self.hoursStyle.hubRadius = 20

        self.minutesStyle = Style()
        self.minutesStyle.fillColor = (0,0,0)
        self.minutesStyle.width = 6
        self.minutesStyle.length = -80
        self.minutesStyle.hubRadius = 15

        self.secondsStyle = Style()
        self.secondsStyle.fillColor = (0,0,0)
        self.secondsStyle.width = 3
        self.secondsStyle.length = -50
        self.secondsStyle.hubRadius = 10

        self.sweep = False

    def __str__(self):
        return f"AnalogClockHands"

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    def paint(self, surface):
        if (not self.visible):
            return

        super().paint(surface)

        # Compute the angle of each hand

        h = self.time.hour
        m = self.time.minute
        s = self.time.second
        us = self.time.microsecond

        if self.sweep:
            s += (us/1000000)
        a_s = 90 - s / 60.0 * 360.0

        a_m = 90 - (m/ 60.0 * 360.0 + (s / 60.0) * (360.0 / 60))

        a_h = 90 - ((h % 12) / 12.0 * 360.0 + (m/ 60.0) * (360.0 / 12))

        a_s %= 360
        a_m %= 360
        a_h %= 360

        a_s = math.radians(a_s)
        a_m = math.radians(a_m)
        a_h = math.radians(a_h)

        # Compute the start and end points of each hand based on their angle
        secondsStartPoint = Points.getPoint(Layer.center, a_s, self.secondsStyle.hubRadius)
        secondsEndPoint = Points.getPoint(Layer.center, a_s, self.getSecondsLength())

        minutesStartPoint = Points.getPoint(Layer.center, a_m, self.minutesStyle.hubRadius)
        minutesEndPoint = Points.getPoint(Layer.center, a_m, self.getMinutesLength())

        hoursStartPoint = Points.getPoint(Layer.center, a_h, self.hoursStyle.hubRadius)
        hoursEndPoint = Points.getPoint(Layer.center, a_h, self.getHoursLength())

        # Draw the hands and their hubs
        self.drawCircle(surface, Layer.center, self.hoursStyle.hubRadius, (0,0,0), self.hoursStyle.fillColor)
        self.drawLine(surface, hoursStartPoint, hoursEndPoint, self.hoursStyle.width, (0,0,0), self.hoursStyle.fillColor)
        self.drawCircle(surface, Layer.center, self.minutesStyle.hubRadius, (0,0,0), self.minutesStyle.fillColor)
        self.drawLine(surface, minutesStartPoint, minutesEndPoint, self.minutesStyle.width, (0,0,0), self.minutesStyle.fillColor)
        self.drawCircle(surface, Layer.center, self.secondsStyle.hubRadius, (0,0,0), self.secondsStyle.fillColor)
        self.drawLine(surface, secondsStartPoint, secondsEndPoint, self.secondsStyle.width, (0,0,0), self.secondsStyle.fillColor)

    def getHoursLength(self):
        if self.hoursStyle.length < 0:
            return self.style.radius + self.hoursStyle.length
        return self.hoursStyle.length

    def getMinutesLength(self):
        if self.minutesStyle.length < 0:
            return self.style.radius + self.minutesStyle.length
        return self.minutesStyle.length

    def getSecondsLength(self):
        if self.secondsStyle.length < 0:
            return self.style.radius + self.secondsStyle.length
        return self.secondsStyle.length

    def _exit(self, sig, frame):
        self._running = False
        print("\nExiting!...\n")

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
            self.time = datetime.datetime.now()
            self.paint(surface)

            pygame.display.flip()
            _clock.tick(30)  # Aim for 30fps

        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    surface = SurfaceHelper.OpenSurface()
    clockHands = AnalogClockHands()
    clockHands.style = Style()
    clockHands.style.backColor = (128, 128, 128)
    clockHands.style.radius = 220
    clockHands.run(surface)
