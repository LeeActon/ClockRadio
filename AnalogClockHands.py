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

class AnalogClockHands(Widget.Widget):
    hourColor = (0,0,255)
    minuteColor = (0,255,0)
    secondColor = (255,0,0)
    hourHubColor = None
    minuteHubColor = None
    secondHubColor = None

    hourWidth = 11
    hourLength = -110
    hourHubRadius = 20
    minuteWidth = 6
    minuteLength = -80
    minuteHubRadius = 20
    secondWidth = 3
    secondLength = -50
    secondHubRadius = 10
    sweep = False

    def __init__(self, surface):
        super().__init__(surface)

        # For some reason the canvas needs a 7px vertical offset
        # circular screens are weird...
        self.center = (240, 247)
        self._radius = 240

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def loadSettings(self, settings):
        for key, value in settings.items():
            if key == 'hourColor':
                self.setHourColor(eval(value))
            elif key == 'minuteColor':
                self.setMinuteColor(eval(value))
            elif key == 'secondColor':
                self.setSecondColor(eval(value))
            elif key == 'hourHubColor':
                self.setHourHubColor(eval(value))
            elif key == 'minuteHubColor':
                self.setMinuteHubColor(eval(value))
            elif key == 'secondHubColor':
                self.setSecondHubColor(eval(value))
            elif key == 'hourHubRadius':
                self.setHourHubRadius(eval(value))
            elif key == 'minuteHubRadius':
                self.setMinuteHubRadius(eval(value))
            elif key == 'secondHubRadius':
                self.setSecondHubRadius(eval(value))
            elif key == 'hourLength':
                self.setHourLength(eval(value))
            elif key == 'minuteLength':
                self.setMinuteLength(eval(value))
            elif key == 'secondLength':
                self.setSecondLength(eval(value))
            elif key == 'sweep':
                self.sweep = (value == "True")

    def update(self, time):

        super().update()

        # Compute the angle of each hand

        s = time.second
        if self.sweep:
            s += (time.microsecond/1000000)
        a_s = s / 60.0 * 360.0

        a_m = time.minute / 60.0 * 360.0
        a_m += (time.second / 60.0) * (360.0 / 60)

        a_h = (time.hour % 12) / 12.0 * 360.0
        a_h += (time.minute / 60.0) * (360.0 / 12)

        a_s += 90
        a_m += 90
        a_h += 90

        a_s %= 360
        a_m %= 360
        a_h %= 360

        # Compute the start and end points of each hand based on their angle
        point_second_start = self._get_point(self.center, a_s, self.secondHubRadius)
        point_second_end = self._get_point(self.center, a_s, self.getSecondLength())

        point_minute_start = self._get_point(self.center, a_m, self.minuteHubRadius)
        point_minute_end = self._get_point(self.center, a_m, self.getMinuteLength())

        point_hour_start = self._get_point(self.center, a_h, self.hourHubRadius)
        point_hour_end = self._get_point(self.center, a_h, self.getHourLength())

        # Draw the hands and their hubs
        self._line(self.hourColor, point_hour_start, point_hour_end, self.hourWidth)
        self._circle(self.getHourHubColor(), self.center, self.hourHubRadius)
        self._line(self.minuteColor, point_minute_start, point_minute_end, self.minuteWidth)
        self._circle(self.getMinuteHubColor(), self.center, self.minuteHubRadius)
        self._line(self.secondColor, point_second_start, point_second_end, self.secondWidth)
        self._circle(self.getSecondHubColor(), self.center, self.secondHubRadius)

    def setSweep(self, sweep):
        self.sweep = sweep

    def setHourColor(self, color):
        self.hourColor = color

    def setMinuteColor(self, color):
        self.minuteColor = color

    def setSecondColor(self, color):
        self.secondColor = color

    def setHourHubColor(self, color):
        self.hourHubColor = color

    def getHourHubColor(self):
        if self.hourHubColor == None:
            return self.hourColor
        return self.hourHubColor

    def setMinuteHubColor(self, color):
        self.minuteHubColor = color

    def getMinuteHubColor(self):
        if self.minuteHubColor == None:
            return self.minuteColor
        return self.minuteHubColor

    def setSecondHubColor(self, color):
        self.secondHubColor = color

    def getSecondHubColor(self):
        if self.secondHubColor == None:
            return self.secondColor
        return self.secondHubColor

    def setHourLength(self, length):
        self.hourLength = length

    def getHourLength(self):
        if self.hourLength < 0:
            return self._radius + self.hourLength
        return self.hourLength

    def setMinuteLength(self, length):
        self.minuteLength = length

    def getMinuteLength(self):
        if self.minuteLength < 0:
            return self._radius + self.minuteLength
        return self.minuteLength

    def setSecondLength(self, length):
        self.secondLength = length

    def getSecondLength(self):
        if self.secondLength < 0:
            return self._radius + self.secondLength
        return self.secondLength

    def setHourHubRadius(self, radius):
        self.hourHubRadius = radius

    def setMinuteHubRadius(self, radius):
        self.minuteHubRadius = radius

    def setSecondHubRadius(self, radius):
        self.secondHubRadius = radius

    _running = False
    def _exit(self, sig, frame):
        self._running = False
        print("\nExiting!...\n")

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
            self.update(datetime.datetime.now())

            pygame.display.flip()
            _clock.tick(30)  # Aim for 30fps

        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    surface = SurfaceHelper.OpenSurface()
    clockHands = AnalogClockHands(surface)
    clockHands.backcolor = (0,0,0)
    clockHands.setHourColor((0,0,255))
    clockHands.setMinuteColor((0,255,0))
    clockHands.setSecondColor((255,0,0))
    clockHands.run()
