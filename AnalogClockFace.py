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
    backgroundColor = (0, 0, 0)
    hourHandColor = (255,255,255)
    minuteHandColor = (255,255,255)
    secondHandColor = (255,0,0)
    innerHubColor = (0,0,0)
    outerHubColor = (255,0,0)
    tickColor = (0,0,255)

    def __init__(self, surface):
        super().__init__(surface)

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

    def update(self, time, sweep):

        s = time.second
        if sweep:
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
        point_second_end = self._get_point(self.center, a_s, self._marks - 30)

        point_minute_start = self._get_point(self.center, a_m, 10)
        point_minute_end = self._get_point(self.center, a_m, self._marks - 60)

        point_hour_start = self._get_point(self.center, a_h, 10)
        point_hour_end = self._get_point(self.center, a_h, self._marks - 90)

        if self.clockFaceBackground == None:
            self._circle(self.backgroundColor, self.center, self._radius, antialias=False)

            for s in range(60):
                a = 360 / 60.0 * s
                end = self._get_point(self.center, a, self._marks + 5)
                self._line(self.tickColor, self.center, end, 3)

            self._circle(self.backgroundColor, self.center, self._marks - 5)

            for s in range(12):
                a = 360 / 12.0 * s
                x, y = self._get_point(self.center, a, self._marks)

                r = 5
                if s % 3 == 0:
                    r = 10

                x = int(x)
                y = int(y)

                self._circle(self.tickColor, (x, y), r)

        else:
            self.surface.blit(self.clockFaceBackground, (0,0))

        # Draw the second, minute and hour hands
        self._line(self.hourHandColor, point_hour_start, point_hour_end, 11)
        self._line(self.minuteHandColor, point_minute_start, point_minute_end, 6)
        self._line(self.secondHandColor, point_second_start, point_second_end, 3)

        # Draw the hub
        self._circle(self.outerHubColor, self.center, 20)
        self._circle(self.innerHubColor, self.center, 10)

    def setBackground(self, image):
        self.clockFaceBackground = pygame.image.load(image)

    def setHourHandColor(self, color):
        self.hourHandColor = color

    def setMinuteHandColor(self, color):
        self.minuteHandColor = color

    def setSecondHandColor(self, color):
        self.secondHandColor = color

    def setOuterHubColor(self, color):
        self.outerHubColor = color

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
            self.update(datetime.datetime.now(), True)

            pygame.display.flip()
            _clock.tick(30)  # Aim for 30fps

        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    surface = SurfaceHelper.OpenSurface()
    clockFace = AnalogClockFace(surface)
    clockFace.run()
