import debugpy
from Page import Page
import time
from Style import Style
from Polygon import Polygon
from Circle import Circle
from Layer import Layer
from TextLayer import TextLayer
from SevenSegmentLayer import SevenSegmentLayer
import Points

class SleepPage(Page):
    def __init__(self):
        super().__init__()
        self.rotaryId = 0
        self.auxDevices = None
        self.timeRemaining = 0

        self.digitalValue = SevenSegmentLayer()
        self.digitalValue.value = 0
        self.digitalValue.digits = 2
        self.digitalValue.decimalPlaces = 0
        self.digitalValue.color = (255,0,0)
        self.digitalValue.shadowColor = (255, 255-12,255-12)
        self.digitalValue.position = Layer.center
        self.addLayer(self.digitalValue);

        self.textLayer = TextLayer()
        self.textLayer.text = "Sleep"
        self.textLayer.color = (0,0,255)
        self.textLayer.position = Points.translatePoint(Layer.center, (0, 100))
        self.addLayer(self.textLayer)

        self.style = Style()
        self.style.backColor = (255, 255, 255)
        self.style.radius = 200

    @property
    def digitalValueFont(self):
        return self.digitalValue.font

    @digitalValueFont.setter
    def digitalValueFont(self, value):
        self.digitalValue.font = value

    @property
    def textFont(self):
        return self.textLayer.font

    @textFont.setter
    def textFont(self, value):
        self.textLayer.font = value

    def setTimeRemaining(self, value):
        self.timeRemaining = value
        self.digitalValue.value = self.timeRemaining

    def onActivate(self):
        debugpy.breakpoint()
        self.defaultTimeout()
        if self.timeRemaining == 0:
            self.setTimeRemaining(90)

        r = int(self.timeRemaining/15)

        self.sendAuxDevices(f"R {self.rotaryId} : {r}, 0, 12, 0, 0")

    def handleRotary(self, rotaryId, value):
        if (rotaryId == self.rotaryId):
            self.defaultTimeout()
            self.setTimeRemaining(value * 15)
            return True

        return False
