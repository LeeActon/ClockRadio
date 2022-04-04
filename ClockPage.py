import datetime
from Page import Page
from ImageLayer import ImageLayer
from AnalogClockFace import AnalogClockFace
from AnalogClockHands import AnalogClockHands
from Style import Style

class ClockPage(Page):
    surface = None
    clockHands_type = AnalogClockHands
    clockHands = None
    clockFace_type = AnalogClockFace

    def __init__(self):
        super().__init__()
        self.time = None
        self._backgroundImage = None
        self.clockFace = None
        self.clockHands = AnalogClockHands()

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

        if self.clockHands != None:
            self.clockHands.time = self.time or datetime.datetime.now()

        # if no bacground image, use the background color
        if self.backgroundImage == None:
            if (self.style != None) and (self.style.backColor != None):
                self.surface.fill(self.style.backColor)

        super().update()

    def handleEnterButtonUp(self):
        print("ClockPage.handleEnterButtonUp")
        if self.time == None:
            print("freeze")
            self.time = datetime.datetime.now()
        else:
            print("unfreeze")
            self.time = None
