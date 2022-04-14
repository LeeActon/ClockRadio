#!/usr/bin/env python3
import math
import pygame
from pygame import gfxdraw
from Style import Style

class Layer:
    center = (240, 240)
    style_type = Style

    def __init__(self):
        self.layers = []
        self.parent = None
        self._style = None
        self.visible = True

    @classmethod
    def offsetX(cls, amount):
        cls.center = (cls.center[0] + amount, cls.center[1])
        print(f"Layer.center = {cls.center}")

    @classmethod
    def offsetY(cls, amount):
        cls.center = (cls.center[0], cls.center[1] + amount)
        print(f"Layer.center = {cls.center}")

    @property
    def style(self):
        if (self._style != None):
            return self._style

        if (self.parent != None):
            return self.parent.style

        return None

    @style.setter
    def style(self, style):
        self._style = style

    def getProperty(self, propertyName):
        propertyValue = None
        if self._style != None:
            propertyValue = self._style.getProperty(propertyName)

        if (propertyValue == None) and (self.parent != None):
            propertyValue = self.parent.getProperty(propertyName)

        return propertyValue

    def clearLayers(self):
        self.layers = []

    def addLayer(self, layer):
        layer.parent = self
        self.layers.append(layer)

    def drawCircle(self, surface, center, radius, strokeColor, fillColor, antialias=True):
        #print(f"circle({color}, {center}, {radius})")
        x, y = center
        x = int(x)
        y = int(y)
        gfxdraw.filled_circle(surface, x, y, radius, fillColor)
        if antialias:
            gfxdraw.aacircle(surface, x, y, radius, strokeColor)

    def drawLine(self, surface, start, end, thickness, strokeColor, fillColor):
        #print(f"line({color}, {start}, {end}, {thickness})")
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

        gfxdraw.filled_polygon(surface, (tl, tr, br, bl), fillColor)
        gfxdraw.aapolygon(surface, (tl, tr, br, bl), strokeColor)

    def showLayers(self, iMin, iMax, visible):
        # print(f"{self}.showLayers({iMin}, {iMax}, {visible})")
        for i in range(iMin, iMax):
            self.layers[i].visible = visible

    def paint(self, surface):
        if not self.visible:
            return

        # if this layer explicitly has a backColor then fill with it.
        if (self._style != None) and (self._style.backColor != None):
            surface.fill(self._style.backColor)

        for layer in self.layers:
            if (layer.visible):
                layer.paint(surface)
