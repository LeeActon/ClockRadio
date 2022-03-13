import datetime
from Page import Page
from ImageLayer import ImageLayer
from AnalogClockFace import AnalogClockFace
from AnalogClockHands import AnalogClockHands

class ClockPage(Page):
    surface = None
    backgroundColor = (127,127,127)
    backgroundImage = None
    clockFace = None
    clockHands = None
    time = None

    def __init__(self, surface):
        super().__init__(surface)
        self.clockHands = AnalogClockHands()
        self.clockHands.hoursColor = (0,0,0)
        self.clockHands.minutesColor = (0,0,0)
        self.clockHands.secondsColor = (192,0,0)

    def loadSettings(self, settings):
        for key, value in settings.items():
            if key == 'backgroundImage':
                self.loadBackgroundImage(value)
            elif key == 'hands':
                self.loadClockHandsSettings(value)
            elif key == 'face':
                self.loadClockFaceSettings(value)
        
    def loadBackgroundImage(self, filename):
        if self.backgroundImage == None:
            self.backgroundImage = ImageLayer()
        self.backgroundImage.loadImage(filename)
 
    def loadClockHandsSettings(self, settings):
        self.clockHands.loadSettings(settings)

    def loadClockFaceSettings(self, settings):
        if self.clockFace == None:
            self.clockFace = AnalogClockFace()
        self.clockFace.loadSettings(settings)

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
