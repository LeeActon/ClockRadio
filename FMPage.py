import time
from Layer import Layer
from Page import Page
from SevenSegmentLayer import SevenSegmentLayer
from Style import Style

class FMPage(Page):
    def __init__(self):
        super().__init__()
        self.rotaryId = 0
        self.auxDevices = None

        self.style = Style()
        self.style.backColor = (0, 0, 0)

        self.freqText = SevenSegmentLayer()
        self.freqText.digits = 3
        self.freqText.decimalPlaces = 2
        self.addLayer(self.freqText);

    @property
    def font(self):
        return self.freqText.font

    @font.setter
    def font(self, value):
        self.freqText.font = value

    def setValue(self, value):
        self.freqText.value = value/10.0

    def handleRotary(self, rotaryId, value):
        if (rotaryId == self.rotaryId):
            Page.pushIfNotCurrent(self)
            now = time.time()
            self.timeout = now + 5
            self.setValue(value)
            return True

        return False
