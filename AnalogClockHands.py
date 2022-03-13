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

    def __init__(self):
        super().__init__()

        # For some reason the canvas needs a 7px vertical offset
        # circular screens are weird...
        self.center = (240, 247)
        self._radius = 240
        self.time = datetime.datetime.now()

        self.hoursColor = (0,0,255)
        self.minutesColor = (0,255,0)
        self.secondsColor = (255,0,0)
        self.hoursHubColor = None
        self.minutesHubColor = None
        self.secondsHubColor = None

        self.hoursWidth = 11
        self.hoursLength = -110
        self.hoursHubRadius = 20
        self.minutesWidth = 6
        self.minutesLength = -80
        self.minutesHubRadius = 20
        self.secondsWidth = 3
        self.secondsLength = -50
        self.secondsHubRadius = 10
        self.sweep = False

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
                self.hoursColor = eval(value)
            elif key == 'minutesColor':
                self.minutesColor = eval(value)
            elif key == 'secondsColor':
                self.secondsColor = eval(value)
            elif key == 'hoursHubColor':
                self.hoursHubColor = eval(value)
            elif key == 'minutesHubColor':
                self.minutesHubColor = eval(value)
            elif key == 'secondsHubColor':
                self.secondsHubColor = eval(value)
            elif key == 'hoursHubRadius':
                self.hoursHubRadius = eval(value)
            elif key == 'minutesHubRadius':
                self.minutesHubRadius = eval(value)
            elif key == 'secondsHubRadius':
                self.secondsHubRadius = eval(value)
            elif key == 'hoursLength':
                self.hoursLength = eval(value)
            elif key == 'minutesLength':
                self.minutesLength = eval(value)
            elif key == 'secondsLength':
                self.secondsLength = eval(value)
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
        secondsStartPoint = self.center # Points.getPoint(self.center, a_s, self.secondsHubRadius)
        secondsEndPoint = Points.getPoint(self.center, a_s, self.getSecondsLength())

        minutesStartPoint =  self.center #Points.getPoint(self.center, a_m, self.minutesHubRadius)
        minutesEndPoint = Points.getPoint(self.center, a_m, self.getMinutesLength())

        hoursStartPoint =  self.center #Points.getPoint(self.center, a_h, self.hoursHubRadius)
        hoursEndPoint = Points.getPoint(self.center, a_h, self.getHoursLength())

        # Draw the hands and their hubs
        self.drawCircle(surface, self.center, self.hoursHubRadius, (0,0,0), self.hoursHubColor)
        self.drawLine(surface, hoursStartPoint, hoursEndPoint, self.hoursWidth, (0,0,0), self.hoursColor)
        self.drawCircle(surface, self.center, self.minutesHubRadius, (0,0,0), self.minutesHubColor)
        self.drawLine(surface, minutesStartPoint, minutesEndPoint, self.minutesWidth, (0,0,0), self.minutesColor)
        self.drawCircle(surface, self.center, self.secondsHubRadius, (0,0,0), self.secondsHubColor)
        self.drawLine(surface, secondsStartPoint, secondsEndPoint, self.secondsWidth, (0,0,0), self.secondsColor)

    @property
    def hoursHubColor(self):
        if self._hoursHubColor == None:
            return self.hoursColor

        return self._hoursHubColor

    @hoursHubColor.setter
    def hoursHubColor(self, value):
        self._hoursHubColor = value

    @property
    def minutesHubColor(self):
        if self._minutesHubColor == None:
            return self.minutesColor
        return self._minutesHubColor

    @minutesHubColor.setter
    def minutesHubColor(self, value):
        self._minutesHubColor = value

    @property
    def secondsHubColor(self):
        if self._secondsHubColor == None:
            return self.secondsColor
        return self._secondsHubColor

    @secondsHubColor.setter
    def secondsHubColor(self, value):
        self._secondsHubColor = value

    def getHoursLength(self):
        if self.hoursLength < 0:
            return self._radius + self.hoursLength
        return self.hoursLength

    def getMinutesLength(self):
        if self.minutesLength < 0:
            return self._radius + self.minutesLength
        return self.minutesLength

    def getSecondsLength(self):
        if self.secondsLength < 0:
            return self._radius + self.secondsLength
        return self.secondsLength

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
    clockHands.hoursColor = (0,0,255)
    clockHands.minutesColor = (0,255,0)
    clockHands.secondsColor = (255,0,0)
    clockHands.run(surface)
