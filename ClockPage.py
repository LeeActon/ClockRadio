import Page
import ImageLayer
import AnalogClockFace
import AnalogClockHands

class ClockPage(Page.Page):
    surface = None
    backgroundImage = None
    clockFace = None
    clockHands = None

    def __init__(self, surface):
        super().__init__()
        self.surface = surface
        self.backgroundImage = ImageLayer.ImageLayer(self.surface)
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

    def update(self, time):
        if self.backgroundImage != None:
            self.backgroundImage.update()

        if self.clockFace != None:
            self.clockFace.update()

        if self.clockHands != None:
            self.clockHands.update(time)

