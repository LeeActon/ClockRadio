import Layer
import TickMarksLayer
import math
import pygame

class AnalogGauge(Layer.Layer):
    def __init__(self, surface):
        super().__init__(surface)

        self.ticksStartAngle = 5/8
        self.ticksEndAngle = -1/8
        self.minValue = 0
        self.maxValue = 30

        ticks1 = []
        ticks5 = []
        ticks10 = []
        for i in range(self.minValue, self.maxValue + 1):
            if (i % 10) == 0:
                ticks10.append(i)
            elif (i % 5) == 0:
                ticks5.append(i)
            else:
                ticks1.append(i)

        self.tickMarks10 = TickMarksLayer.TickMarksLayer(self.surface)
        self.tickMarks10.ticksStartAngle = self.ticksStartAngle
        self.tickMarks10.ticksEndAngle = self.ticksEndAngle
        self.tickMarks10.minValue = self.minValue
        self.tickMarks10.maxValue = self.maxValue
        self.tickMarks10.tickLength = 30
        self.tickMarks10.tickWidth = 7
        self.tickMarks10.tickColor = (255,0,0)
        self.tickMarks10.setTicks(ticks10)
        self.tickMarks5 = TickMarksLayer.TickMarksLayer(self.surface)
        self.tickMarks5.ticksStartAngle = self.ticksStartAngle
        self.tickMarks5.ticksEndAngle = self.ticksEndAngle
        self.tickMarks5.minValue = self.minValue
        self.tickMarks5.maxValue = self.maxValue
        self.tickMarks5.tickLength = 20
        self.tickMarks5.tickWidth = 5
        self.tickMarks5.tickColor = (0,0,255)
        self.tickMarks5.setTicks(ticks5)
        self.tickMarks1 = TickMarksLayer.TickMarksLayer(self.surface)
        self.tickMarks1.ticksStartAngle = self.ticksStartAngle
        self.tickMarks1.ticksEndAngle = self.ticksEndAngle
        self.tickMarks1.minValue = self.minValue
        self.tickMarks1.maxValue = self.maxValue
        self.tickMarks1.tickLength = 10
        self.tickMarks1.tickWidth = 3
        self.tickMarks1.tickColor = (0,0,0)
        self.tickMarks1.setTicks(ticks1)

    def update(self):
        self.tickMarks10.update()
        self.tickMarks5.update()
        self.tickMarks1.update()
