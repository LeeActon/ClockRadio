#!/usr/bin/env python3
import math
import pygame
from pygame import gfxdraw

class Widget:
    surface = None
    backcolor = None
    def __init__(self, surface):
        self.surface = surface

    def _get_point(self, origin, angle, distance):
        r = math.radians(angle)
        cos = math.cos(r)
        sin = math.sin(r)
        x = origin[0] - distance * cos
        y = origin[1] - distance * sin
        return x, y

    def _circle(self, color, center, radius, antialias=True):
        #print("circle({}, {}, {})".format(color, center, radius))
        x, y = center
        if antialias:
            gfxdraw.aacircle(self.surface, x, y, radius, color)
        gfxdraw.filled_circle(self.surface, x, y, radius, color)

    def _line(self, color, start, end, thickness):
        #print("line({}, {}, {}, {})".format(color, start, end, thickness))
        # Draw a filled, antialiased line with a given thickness
        # there's no pygame builtin for this so we get technical.
        start = pygame.math.Vector2(start)
        end = pygame.math.Vector2(end)

        # get the angle between the start/end points
        angle = pygame.math.Vector2().angle_to(end - start)

        # angle_to returns degrees, sin/cos need radians
        angle = math.radians(angle)

        sin = math.sin(angle)
        cos = math.cos(angle)

        # Find the center of the line
        center = (start + end) / 2.0

        # Get the length of the line,
        # half it, because we're drawing out from the center
        length = (start - end).length() / 2.0

        # half thickness, for the same reason
        thickness /= 2.0

        tl = (center.x + length * cos - thickness * sin,
              center.y + thickness * cos + length * sin)
        tr = (center.x - length * cos - thickness * sin,
              center.y + thickness * cos - length * sin)
        bl = (center.x + length * cos + thickness * sin,
              center.y - thickness * cos + length * sin)
        br = (center.x - length * cos + thickness * sin,
              center.y - thickness * cos - length * sin)

        gfxdraw.aapolygon(self.surface, (tl, tr, br, bl), color)
        gfxdraw.filled_polygon(self.surface, (tl, tr, br, bl), color)

    def update(self):
        if self.backcolor != None:
            self.surface.fill(self.backcolor)

if __name__ == "__main__":
    clockRadio = ClockRadio()
    clockRadio.run()
