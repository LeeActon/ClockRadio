import datetime
from Page import Page
from ImageLayer import ImageLayer
from AnalogClockFace import AnalogClockFace
from AnalogClockHands import AnalogClockHands
from Style import Style

class ClockPage(Page):
    surface = None
    backgroundColor = (127,127,127)
    clockHands_type = AnalogClockHands
    clockHands = None
    clockFace_type = AnalogClockFace
    time = None

    def __init__(self):
        super().__init__()
        self._backgroundImage = None
        self._clockFace = None
        self.clockHands = AnalogClockHands()
        self.clockHands.hoursColor = (0,0,0)
        self.clockHands.minutesColor = (0,0,0)
        self.clockHands.secondsColor = (192,0,0)

    def __str__(self):
        return f"ClockPage {{{self._backgroundImage}, {self._clockFace}, {self.clockHands}}}"

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
    def clockFace(self):
        return self._clockFace

    @clockFace.setter
    def clockFace(self, value):
        self._clockFace = value

    def loadClockFaceSettings(self, settings):
        self.clockFace.loadSettings(settings)
        self.clockFace.createClockFace()

    def setHoursColor(self, color):
        if self.clockHands != None:
            self.clockHands.setHoursColor(color)
            
    def setMinutesColor(self, color):
        if self.clockHands != None:
            self.clockHands.setMinutesColor(color)

    def setSecondssColor(self, color):
        if self.clockHands != None:
            self.clockHands.setSecondsColor(color)

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

        if self.clockHands != None:
            self.clockHands.time = self.time or datetime.datetime.now()

        # if no bacground image, use the background color
        if self.backgroundImage == None:
            self.surface.fill(self.backgroundColor)

        super().update()

    def handleEnterButtonUp(self):
        print("ClockPage.handleEnterButtonUp")
        if self.time == None:
            print("freeze")
            self.time = datetime.datetime.now()
        else:
            print("unfreeze")
            self.time = None
