import datetime
from Page import Page
from ImageLayer import ImageLayer
from AnalogClockFace import AnalogClockFace
from AnalogClockHands import AnalogClockHands
from AnalogAlarmIndicator import AnalogAlarmIndicator
from Style import Style

class ClockPage(Page):
    clockHands_type = AnalogClockHands
    clockHands = None
    clockFace_type = AnalogClockFace

    def __init__(self):
        super().__init__()
        self.time = None
        self._backgroundImage = None
        self.clockFace = None
        self.clockHands = AnalogClockHands()
        self.alarmIndicator1 = AnalogAlarmIndicator()
        self.alarmIndicator1.style.strokeColor = (255,0,0)
        self.alarmIndicator1.style.fillColor = (255,0,0)
        self.alarmIndicator1.style.radius = 200
        self.alarmIndicator1.time = datetime.time(6, 30)

        self.alarmIndicator2 = AnalogAlarmIndicator()
        self.alarmIndicator2.style.strokeColor = (192,0,255)
        self.alarmIndicator2.style.fillColor = (192,0,255)
        self.alarmIndicator2.style.radius = 200
        self.alarmIndicator2.time = datetime.time(10, 30)

    def __str__(self):
        return f"ClockPage {{{self._backgroundImage}, {self.clockFace}, {self.clockHands}}}"

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

    def update(self):
        # make sure self.layers is up to date
        if len(self.layers) == 0:
            if self.backgroundImage != None:
                self.addLayer(self.backgroundImage)
            if self.clockFace != None:
                self.addLayer(self.clockFace)
                self.clockFace.createClockFace()
            if self.clockHands != None:
                self.addLayer(self.clockHands)
            if self.alarmIndicator1 != None:
                self.addLayer(self.alarmIndicator1)
            if self.alarmIndicator2 != None:
                self.addLayer(self.alarmIndicator2)

        if self.clockHands != None:
            self.clockHands.time = self.time or datetime.datetime.now()

        super().update()

    def handleEnterButtonUp(self):
        print("ClockPage.handleEnterButtonUp")
        if self.time == None:
            print("freeze")
            self.time = datetime.datetime.now()
        else:
            print("unfreeze")
            self.time = None
