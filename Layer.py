#!/usr/bin/env python3
import math
import pygame
from pygame import gfxdraw
from Polygon import Polygon

class Layer:
    def __init__(self):
        self.backColor = None
        self.polygons = []

    def setBackColor(self, color):
        self.backColor = color

    def clearPolygons(self):
        self.polygons = []

    def addPolygon(self, polygon):
        self.polygons.append(polygon)

    def _circle(self, surface, color, center, radius, antialias=True):
        #print("circle({}, {}, {})".format(color, center, radius))
        x, y = center
        if antialias:
            gfxdraw.aacircle(surface, x, y, radius, color)
        gfxdraw.filled_circle(surface, x, y, radius, color)

    def _line(self, surface, color, start, end, thickness):
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

        gfxdraw.aapolygon(surface, (tl, tr, br, bl), color)
        gfxdraw.filled_polygon(surface, (tl, tr, br, bl), color)

    def paint(self, surface):
        if self.backColor != None:
            surface.fill(self.backColor)

        for polygon in self.polygons:
            polygon.paint(surface)
