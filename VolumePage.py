from Page import Page
from AnalogGauge import AnalogGauge
import time
from Style import Style
from Polygon import Polygon
from Circle import Circle
from TextLayer import TextLayer
from Layer import Layer

class VolumePage(Page):
    def __init__(self):
        super().__init__()

        self.label = TextLayer()
        self.label.text = "0"
        self.label.position = Layer.center
        self.addLayer(self.label);

        self.analogGauge = AnalogGauge()
        self.addLayer(self.analogGauge)
        self.style = Style()
        self.style.backColor = (255, 255, 255)
        self.style.radius = 200

        self.analogGauge.ticksStartAngle = 5/8
        self.analogGauge.ticksEndAngle = -1/8
        self.analogGauge.minValue = 0
        self.analogGauge.maxValue = 30
        self.analogGauge.value = 0

        self.indicatorStyle = Style()
        self.indicatorStyle.length = -60
        self.indicatorStyle.width = 20
        self.indicatorStyle.strokeColor = (0, 255, 0)
        self.indicatorStyle.fillColor = (0, 255, 0)
        self.analogGauge.createIndicator(self.indicatorStyle)
        self.style1s = Style()
        self.style1s.length = 10
        self.style1s.width = 3
        self.style1s.strokeColor = (0, 0, 0)
        self.style1s.fillColor = (0, 0, 0)
        print(f"style1s.strokeColor = {self.style1s.strokeColor}, style1s.fillColor = {self.style1s.fillColor}")
        self.style5s = Style()
        self.style5s.length = 20
        self.style5s.width = 5
        self.style5s.shape = Circle()
        self.style5s.shape.style = Style()
        self.style5s.shape.style.radius = 8
        self.style5s.strokeColor = (0, 0, 255)
        self.style5s.fillColor = (0, 0, 255)
        print(f"style5s.strokeColor = {self.style5s.strokeColor}, style5s.fillColor = {self.style5s.fillColor}")
        self.style10s = Style()
        self.style10s.length = 30
        self.style10s.width = 7
        self.style10s.strokeColor = (255, 0, 0)
        self.style10s.fillColor = (255, 0, 0)
        points = [[0, 4], [30, 0], [0, -4], [0, 4]]
        self.style10s.shape = Polygon(points)
        print(f"style10s.strokeColor = {self.style10s.strokeColor}, style1s.fillColor = {self.style10s.fillColor}")

        self.analogGauge.createTickMarks([10,5,1], [self.style10s, self.style5s, self.style1s])

    @property
    def font(self):
        return self.label.font

    @font.setter
    def font(self, value):
        self.label.font = value

    def setValue(self, value):
        self.analogGauge.value = value
        self.label.text = f"{value}"

    def toggleZeroIndicator(self):
        self.analogGauge.showZeroIndicator = not self.analogGauge.showZeroIndicator

    def handleRotary(self, rotaryId, value):
        if (rotaryId == 10):
            now = time.time()
            self.timeout = now + 5
            self.setValue(value)
