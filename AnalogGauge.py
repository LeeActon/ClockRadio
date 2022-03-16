from Layer import Layer
from TickMarksLayer import TickMarksLayer
import math
import pygame

class AnalogGauge(Layer):
    def __init__(self):
        super().__init__()

        self.ticksStartAngle = 5/8
        self.ticksEndAngle = -1/8
        self.minValue = 0
        self.maxValue = 30
        self.tickMarks = []
        self.indicator = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if (value < self.minValue):
            value = self.minValue
        if (value > self.maxValue):
            value = self.maxValue

        self._value = value
        if (self.indicator != None):
            self.indicator.showLayers(0, value - self.minValue, True)
            self.indicator.showLayers(value + 1, self.maxValue + 1, False)
        

    def createIndicator(self, tickStyle):
        self.indicator = TickMarksLayer()
        self.indicator.ticksStartAngle = self.ticksStartAngle
        self.indicator.ticksEndAngle = self.ticksEndAngle
        self.indicator.minValue = self.minValue
        self.indicator.maxValue = self.maxValue
        self.indicator.style = tickStyle
        self.indicator.setTicks(range(self.minValue, self.maxValue + 1))
        self.addLayer(self.indicator)

    def createTickMarks(self, tickMods, tickStyles):
        ticks = []
        modCount = len(tickMods)
        print(f"creatTickMarks({tickMods}, {tickStyles}) modCount = {modCount}")
        for i in range(modCount):
            ticks.append([])

        for iValue in range(self.minValue, self.maxValue + 1):
            for iMod in range(modCount):
                if (iValue % tickMods[iMod] == 0):
                    ticks[iMod].append(iValue)
                    break

        self.tickMarksLayers = []
        for iMod in range(modCount):
            tickMarksLayer = TickMarksLayer()
            tickMarksLayer.ticksStartAngle = self.ticksStartAngle
            tickMarksLayer.ticksEndAngle = self.ticksEndAngle
            tickMarksLayer.minValue = self.minValue
            tickMarksLayer.maxValue = self.maxValue
            tickMarksLayer.style = tickStyles[iMod]
            tickMarksLayer.setTicks(ticks[iMod])
            self.tickMarksLayers.append(tickMarksLayer)
            self.addLayer(tickMarksLayer)
