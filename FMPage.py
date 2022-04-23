import time
from Layer import Layer
from Page import Page
from SevenSegmentLayer import SevenSegmentLayer
from Style import Style
from TextLayer import TextLayer

class FMPage(Page):
    MODE_FIRST = 0
    MODE_FREQ = 0
    MODE_PRESET = 1
    MODE_LAST = 1

    def __init__(self):
        super().__init__()
        self.rotaryId = 0
        self.fmStations = None
        self.mode = FMPage.MODE_FREQ
        self.preset = 0
        self.freq = 949

        self.style = Style()
        self.style.backColor = (0, 0, 0)

        self.freqText = SevenSegmentLayer()
        self.freqText.digits = 3
        self.freqText.decimalPlaces = 2
        self.addLayer(self.freqText);

        self.callSignText = TextLayer()
        self.callSignText.color = (0, 0, 255)
        self.callSignText.text = ""
        self.callSignText.position = (240, 240+100)
        self.addLayer(self.callSignText);

    @property
    def font(self):
        return self.freqText.font

    @font.setter
    def font(self, value):
        self.freqText.font = value

    @property
    def callSignFont(self):
        return self.callSignText.font

    @callSignFont.setter
    def callSignFont(self, value):
        self.callSignText.font = value

    def setFreq(self, value):
        self.freq = value
        self.freqText.value = value/10.0
        # auxDevice expects actual freq * 100 and self.freq is already 10 times actual freq.
        self.sendAuxDevices(f"f {self.freq*10}")

    def setPreset(self, value):
        self.preset = value
        count = len(self.fmStations)
        if self.preset >= count:
            self.preset = count - 1
        elif self.preset < 0:
            self.preset = 0
        self.showPreset()

    def showPreset(self):
        self.setFreq(self.fmStations[self.preset].frequency)
        self.callSignText.text = self.fmStations[self.preset].callSign

    def handleRotary(self, rotaryId, value):
        if (rotaryId == self.rotaryId):
            Page.pushIfNotCurrent(self)
            now = time.time()
            self.timeout = now + 5
            if self.mode == FMPage.MODE_FREQ:
                self.setFreq(value)
                self.callSignText.text = ""
            elif self.mode == FMPage.MODE_PRESET:
                self.setPreset(value)
            return True

        return False

    def setMode(self, value):
        self.mode = value
        if self.mode > FMPage.MODE_LAST:
            self.mode = FMPage.MODE_FIRST
        if self.mode == FMPage.MODE_FREQ:
            self.freqText.color = (255,0,0)
            self.freqText.shadowColor = (48,0,0)
            self.sendAuxDevices(f"R {self.rotaryId} : {self.freq}, 880, 1080, 150, 1")
        elif self.mode == FMPage.MODE_PRESET:
            count = len(self.fmStations)
            self.freqText.color = (0, 0, 255)
            self.freqText.shadowColor = (0,0,48)
            self.sendAuxDevices(f"R {self.rotaryId} : {self.preset}, 0, {count - 1}, 0, 1")
            self.showPreset()

    def handleButtonUp(self, buttonId):
        if buttonId == self.rotaryId:
            self.setMode(self.mode + 1)
