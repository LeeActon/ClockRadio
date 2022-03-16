import math
from Layer import Layer
from Polygon import Polygon
import Points
from Style import Style

class TickMarksLayer(Layer):

    def __init__(self):
        super().__init__()

        self.tickStartRadius = 210
        self.style = Style()
        self.style.length = 30
        self.style.width = 3
        self.style.strokeColor = (0, 0, 0)
        self.style.fillColor = (0, 0, 0)

        # Angles are in turns around the circle
        # 1.0 turn is all the way around the circle.
        # 0.5 turn is half way around the circle.
        # 0.25 turn is one quarter way around the circle
        # 0 turns is at (1,0) in standard cartesian co-ordinates (i.e. 3 o'clock)
        # 0.25 turn is (0, 1) (i.e. 12 o'clock)
        # 0.50 turn is (-1, 0) (i.e. 9 o'clock)
        # 0.75 turn is (0, -1) (i.e. 6 o'clock)

        self.ticksStartAngle = 0.25                  # Default is to start at the top of circle
        self.ticksEndAngle = self.ticksStartAngle - 1.0   # go all the way around clockwise

        self.ticks = []
        self.minValue = 0
        self.maxValue = 100

        self._tickMark = None

    def loadSettings(self, settings):
        pass

    def valueToAngle(self, value):
        angleRange = self.ticksEndAngle - self.ticksStartAngle
        valueRange =  self.maxValue - self.minValue
        valueToAngle = angleRange / valueRange
        angle = self.ticksStartAngle + (value - self.minValue)*valueToAngle
        return angle

    # A prototypical tick mark.
    # Starting at the origin pointing along the positive x-axis
    # This tick mark will be copied, rotated, and translated
    # into position where ever a tick mark should be displayed.
    @property
    def tickMark(self):
        if self._tickMark == None:
            if self.style.shape != None:
                self._tickMark = self.style.shape
            else:
                self._tickMark = Polygon.fromLine(self.style.length, self.style.width)

        return self._tickMark

    def setTicks(self, ticks):
        self.ticks = ticks;

        # Make a copy of the prototypical tick mark for each tick (rotating and translating it into position)
        for tick in self.ticks:
            a = self.valueToAngle(tick)*2*math.pi
            start = Points.getPoint(Layer.center, a, self.tickStartRadius)
            poly = self.tickMark.rotate(a)
            poly2= poly.translate(start)
            self.addLayer(poly2)
