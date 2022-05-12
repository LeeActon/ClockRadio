from Page import Page
from AnalogClockFace import AnalogClockFace
from AnalogAlarmIndicator import AnalogAlarmIndicator
import datetime
from ImageLayer import ImageLayer
from TextLayer import TextLayer
import Points
from Layer import Layer

class AlarmPage(Page):
    def __init__(self):
        super().__init__()

        self._backgroundImage = None
        self.alarmIndicator = AnalogAlarmIndicator()
        self.alarmIndicator.style.strokeColor = (255,0,0)
        self.alarmIndicator.style.fillColor = (255,0,0)
        self.alarmIndicator.style.radius = 200
        self.alarmIndicator.time = datetime.time(6, 30)
        self.titleTextLayer = TextLayer()
        self.titleTextLayer.position = Points.translatePoint(Layer.center, (0, -75))
        self.timeTextLayer = TextLayer()
        self.timeTextLayer.text = "12:30PM"
        self.timeTextLayer.position = Points.translatePoint(Layer.center, (0, 0))
        self.stateTextLayer = TextLayer()
        self.stateTextLayer.position = Points.translatePoint(Layer.center, (0, 75))
        self.stateTextLayer.text = "ON"

    @property
    def backgroundImage(self):
        return self._backgroundImage

    @backgroundImage.setter
    def backgroundImage(self, value):
        if value is ImageLayer:
            self._backgroundImage = value
        else:
            if self._backgroundImage is None:
                self._backgroundImage = ImageLayer()
            self._backgroundImage.loadImage(value)

    @property
    def font(self):
        return self.titleTextLayer.font

    @font.setter
    def font(self, font):
        self.titleTextLayer.font = font

    @property
    def title(self):
        return self.titleTextLayer.text

    @title.setter
    def title(self, text):
        print(f"title = ''{text}''")
        self.titleTextLayer.text = text

    @property
    def timeFont(self):
        return self.timeTextLayer.font

    @timeFont.setter
    def timeFont(self, font):
        self.timeTextLayer.font = font

    @property
    def stateFont(self):
        return self.stateTextLayer.font

    @stateFont.setter
    def stateFont(self, font):
        self.stateTextLayer.font = font

    def onActivate(self):
        self.defaultTimeout()
        return super().onActivate()

    def update(self):
        # make sure self.layers is up to date
        if len(self.layers) == 0:
            if self.backgroundImage != None:
                self.addLayer(self.backgroundImage)
            if self.alarmIndicator != None:
                self.addLayer(self.alarmIndicator)
            if self.titleTextLayer != None:
                self.addLayer(self.titleTextLayer)
            if self.timeTextLayer != None:
                self.addLayer(self.timeTextLayer)
            if self.stateTextLayer != None:
                self.addLayer(self.stateTextLayer)

        super().update()