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
    hourColor = (255,255,255)
    minuteColor = (255,255,255)
    secondColor = (255,0,0)
    innerHubColor = (0,0,0)
    outerHubColor = (255,0,0)
    sweep = False

    def __init__(self, surface):
        super().__init__(surface)

        # For some reason the canvas needs a 7px vertical offset
        # circular screens are weird...
        self.center = (240, 247)
        self._radius = 240

        self.hourHandLength = self._radius - 110
        self.minuteHandLength = self._radius - 80
        self.secondHandLength = self._radius - 50

        #self._origin = pygame.math.Vector2(*self.center)

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
            elif key == 'sweep':
                self.sweep = (value == "True")

    def update(self, time):

        super().update()
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

        point_second_start = self._get_point(self.center, a_s, 10)
        point_second_end = self._get_point(self.center, a_s, self.secondHandLength)

        point_minute_start = self._get_point(self.center, a_m, 10)
        point_minute_end = self._get_point(self.center, a_m, self.minuteHandLength)

        point_hour_start = self._get_point(self.center, a_h, 10)
        point_hour_end = self._get_point(self.center, a_h, self.hourHandLength)

        # Draw the second, minute and hour hands
        self._line(self.hourColor, point_hour_start, point_hour_end, 11)
        self._line(self.minuteColor, point_minute_start, point_minute_end, 6)
        self._line(self.secondColor, point_second_start, point_second_end, 3)

        # Draw the hub
        self._circle(self.outerHubColor, self.center, 20)
        self._circle(self.innerHubColor, self.center, 10)

    def setSweep(self, sweep):
        self.sweep = sweep

    def setHourColor(self, color):
        self.hourColor = color

    def setMinuteColor(self, color):
        self.minuteColor = color

    def setSecondColor(self, color):
        self.secondColor = color

    def setInnerHubColor(self, color):
        self.InnerHubColor = color

    def setOuterHubColor(self, color):
        self.outerHubColor = color


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
