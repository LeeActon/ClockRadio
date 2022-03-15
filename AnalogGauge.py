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
