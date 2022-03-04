import datetime
import Page
import ImageLayer
import AnalogClockFace
import AnalogClockHands

class ClockPage(Page.Page):
    surface = None
    backgroundColor = (127,127,127)
    backgroundImage = None
    clockFace = None
    clockHands = None
    time = None

    def __init__(self, surface):
        super().__init__()
        self.surface = surface
        self.clockHands = AnalogClockHands.AnalogClockHands(self.surface)
        self.clockHands.setHoursColor((0,0,0))
        self.clockHands.setMinutesColor((0,0,0))
        self.clockHands.setSecondsColor((192,0,0))

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
            self.backgroundImage = ImageLayer.ImageLayer(self.surface)
        self.backgroundImage.loadImage(filename)
 
    def loadClockHandsSettings(self, settings):
        self.clockHands.loadSettings(settings)

    def loadClockFaceSettings(self, settings):
        if self.clockFace == None:
            self.clockFace = AnalogClockFace.AnalogClockFace(self.surface)
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
        if self.time != None:
            now = self.time
        else:
            now = datetime.datetime.now()
        if self.backgroundImage != None:
            self.backgroundImage.update()
        else:
            self.surface.fill(self.backgroundColor)

        if self.clockFace != None:
            self.clockFace.update()

        if self.clockHands != None:
            self.clockHands.update(now)


    def handleEnterButtonUp(self):
        print("ClockPage.handleEnterButtonUp")
        if self.time == None:
            print("freeze")
            self.time = datetime.datetime.now()
        else:
            print("unfreeze")
            self.time = None
