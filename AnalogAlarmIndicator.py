from Layer import Layer
from Style import Style
from Polygon import Polygon
import Points
import math

class AnalogAlarmIndicator(Layer):

    def __init__(self):
        super().__init__()
        self._time = None
        points = [[0, 0], [50, 10], [50, -10], [0, 0]]
        self.indicatorShape = Polygon(points)
        self.indicator = None
        self.style = Style()

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        if self.indicator != None:
            self.removeLayer(self.indicator)

        self._time = value
        if self._time == None:
            return

        # Compute the angle

        h = self._time.hour
        m = self._time.minute

        a_m = m/ 60.0

        a_h = 0.25 - ((h % 12) / 12.0 + a_m/ 12)
        a_h_radians = a_h * 2 * math.pi
        #print(f"AnalogAlarmIndicator.time - {self._time}, {a_h} ({a_h_radians})")

        rotated = self.indicatorShape.rotate(a_h_radians)

        radius = self.getProperty("radius")
        t = Points.getPoint(Layer.center, a_h_radians, radius)
        self.indicator  = rotated.translate(t)
        self.addLayer(self.indicator)
