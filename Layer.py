#!/usr/bin/env python3
import math
import pygame
from pygame import gfxdraw
from Style import Style

class Layer:
    center = (240, 240)
    style_type = Style
    styles_type = Style

    def __init__(self):
        self.layers = []
        self.parent = None
        self._style = None
        self.visible = True
        self.styles = []

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

        # First look on the additional styles associated with this layer
        for style in self.styles:
            propertyValue = style.getProperty(propertyName)
            if propertyValue != None:
                return propertyValue

        # Next look on the style and the style's ancestors
        if self.style != None:
            propertyValue = self.style.getProperty(propertyName)
            if propertyValue != None:
                return propertyValue

        # Finally look on the layer's ancestors
        if self.parent != None:
            propertyValue = self.parent.getProperty(propertyName)

        return propertyValue

    def setProperty(self, propertyName, value):
        if self._style == None:
            self._style = Style()

        self._style.setProperty(propertyName, value)

    @property
    def color(self):
        return self.getProperty("color")

    @color.setter
    def color(self, value):
        self.setProperty("color", value)


    @property
    def backColor(self):
        return self.getProperty("backColor")

    @backColor.setter
    def backColor(self, value):
        self.setProperty("backColor", value)

    @property
    def strokeColor(self):
        return self.getProperty("strokeColor")

    @strokeColor.setter
    def strokeColor(self, value):
        self.setProperty("strokeColor", value)

    @property
    def fillColor(self):
        return self.getProperty("fillColor")

    @fillColor.setter
    def fillColor(self, value):
        self.setProperty("fillColor", value)

    @property
    def width(self):
        return self.getProperty("width")

    @width.setter
    def width(self, value):
        self.setProperty("width", value)

    @property
    def length(self):
        return self.getProperty("length")

    @length.setter
    def length(self, value):
        self.setProperty("length", value)

    @property
    def shape(self):
        return self.getProperty("shape")

    @shape.setter
    def shape(self, value):
        self.setProperty("shape", value)

    @property
    def radius(self):
        return self.getProperty("radius")

    @radius.setter
    def radius(self, value):
        self.setProperty("radius", value)

    @property
    def font(self):
        return self.getProperty("font")

    @font.setter
    def font(self, value):
        self.setProperty("font", value)

    def clearLayers(self):
        self.layers = []

    def addLayer(self, layer):
        if layer.parent == None:
            layer.parent = self
        self.layers.append(layer)

    def removeLayer(self, layer):
        layer.parent = None
        self.layers.remove(layer)

    def addStyle(self, style):
        self.styles.append(style)

    def removeStyle(self, style):
        self.styles.remove(style)

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
