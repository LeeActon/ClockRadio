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

class AnalogClockHands(Layer):
    hoursColor = (0,0,255)
    minutesColor = (0,255,0)
    secondsColor = (255,0,0)
    hoursHubColor = None
    minutesHubColor = None
    secondsHubColor = None

    hoursWidth = 11
    hoursLength = -110
    hoursHubRadius = 20
    minutesWidth = 6
    minutesLength = -80
    minutesHubRadius = 20
    secondsWidth = 3
    secondsLength = -50
    secondsHubRadius = 10
    sweep = False

    def __init__(self):
        super().__init__()

        # For some reason the canvas needs a 7px vertical offset
        # circular screens are weird...
        self.center = (240, 247)
        self._radius = 240
        self.time = datetime.datetime.now()

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    def loadSettings(self, settings):
        for key, value in settings.items():
            if key == 'hoursColor':
                self.setHoursColor(eval(value))
            elif key == 'minutesColor':
                self.setMinutesColor(eval(value))
            elif key == 'secondsColor':
                self.setSecondsColor(eval(value))
            elif key == 'hoursHubColor':
                self.setHoursHubColor(eval(value))
            elif key == 'minutesHubColor':
                self.setMinutesHubColor(eval(value))
            elif key == 'secondsHubColor':
                self.setSecondsHubColor(eval(value))
            elif key == 'hoursHubRadius':
                self.setHoursHubRadius(eval(value))
            elif key == 'minutesHubRadius':
                self.setMinutesHubRadius(eval(value))
            elif key == 'secondsHubRadius':
                self.setSecondsHubRadius(eval(value))
            elif key == 'hoursLength':
                self.setHoursLength(eval(value))
            elif key == 'minutesLength':
                self.setMinutesLength(eval(value))
            elif key == 'secondsLength':
                self.setSecondsLength(eval(value))
            elif key == 'sweep':
                self.sweep = (value == "True")

    def paint(self, surface):

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
        secondsStartPoint = Points.getPoint(self.center, a_s, self.secondsHubRadius)
        secondsEndPoint = Points.getPoint(self.center, a_s, self.getSecondsLength())

        minutesStartPoint = Points.getPoint(self.center, a_m, self.minutesHubRadius)
        minutesEndPoint = Points.getPoint(self.center, a_m, self.getMinutesLength())

        hoursStartPoint = Points.getPoint(self.center, a_h, self.hoursHubRadius)
        hoursEndPoint = Points.getPoint(self.center, a_h, self.getHoursLength())

        # Draw the hands and their hubs
        self.drawLine(surface, self.hoursColor, hoursStartPoint, hoursEndPoint, self.hoursWidth)
        self.drawCircle(surface, self.getHoursHubColor(), self.center, self.hoursHubRadius)
        self.drawLine(surface, self.minutesColor, minutesStartPoint, minutesEndPoint, self.minutesWidth)
        self.drawCircle(surface, self.getMinutesHubColor(), self.center, self.minutesHubRadius)
        self.drawLine(surface, self.secondsColor, secondsStartPoint, secondsEndPoint, self.secondsWidth)
        self.drawCircle(surface, self.getSecondsHubColor(), self.center, self.secondsHubRadius)

    def setSweep(self, sweep):
        self.sweep = sweep

    def setHoursColor(self, color):
        self.hoursColor = color

    def setMinutesColor(self, color):
        self.minutesColor = color

    def setSecondsColor(self, color):
        self.secondsColor = color

    def setHoursHubColor(self, color):
        self.hoursHubColor = color

    def getHoursHubColor(self):
        if self.hoursHubColor == None:
            return self.hoursColor
        return self.hoursHubColor

    def setMinutesHubColor(self, color):
        self.minutesHubColor = color

    def getMinutesHubColor(self):
        if self.minutesHubColor == None:
            return self.minutesColor
        return self.minutesHubColor

    def setSecondsHubColor(self, color):
        self.secondsHubColor = color

    def getSecondsHubColor(self):
        if self.secondsHubColor == None:
            return self.secondsColor
        return self.secondsHubColor

    def setHoursLength(self, length):
        self.hoursLength = length

    def getHoursLength(self):
        if self.hoursLength < 0:
            return self._radius + self.hoursLength
        return self.hoursLength

    def setMinutesLength(self, length):
        self.minutesLength = length

    def getMinutesLength(self):
        if self.minutesLength < 0:
            return self._radius + self.minutesLength
        return self.minutesLength

    def setSecondsLength(self, length):
        self.secondsLength = length

    def getSecondsLength(self):
        if self.secondsLength < 0:
            return self._radius + self.secondsLength
        return self.secondsLength

    def setHoursHubRadius(self, radius):
        self.hoursHubRadius = radius

    def setMinutesHubRadius(self, radius):
        self.minutesHubRadius = radius

    def setSecondsHubRadius(self, radius):
        self.secondsHubRadius = radius

    _running = False
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
    clockHands = AnalogClockHands(surface)
    clockHands.backcolor = (0,0,0)
    clockHands.setHoursColor((0,0,255))
    clockHands.setMinutesColor((0,255,0))
    clockHands.setSecondsColor((255,0,0))
    clockHands.run(surface)
