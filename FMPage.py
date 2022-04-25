import time
from Layer import Layer
from Page import Page
from SevenSegmentLayer import SevenSegmentLayer
from Style import Style
from TextLayer import TextLayer

class FMPage(Page):
    MODE_FIRST = 0
    MODE_FREQ = 0
    MODE_SCAN = 1
    MODE_PRESET = 2
    MODE_LAST = 2

    def __init__(self):
        super().__init__()
        self.rotaryId = 0
        self._fmStations = None
        self.presetFMStations = None
        self.mode = FMPage.MODE_PRESET
        self.preset = 0
        self.freq = 949
        self.prevRotaryValue = 0

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

        self.formatText = TextLayer()
        self.formatText.color = (0, 0, 255)
        self.formatText.text = ""
        self.formatText.position = (240, 240+150)
        self.addLayer(self.formatText);

    @property
    def fmStations(self):
        return self._fmStations

    @fmStations.setter
    def fmStations(self, value):
        self._fmStations = value
        self.freqToFMStation = {}
        for station in self._fmStations:
            self.freqToFMStation[station.frequency] = station

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

    @property
    def formatFont(self):
        return self.formatText.font

    @formatFont.setter
    def formatFont(self, value):
        self.formatText.font = value

    def tuningReport(self, freq, strength, stereo):
        self.freq = freq
        self.strength = strength
        self.stereo = stereo
        self.freqText.value = freq
        self.callSignText.text = ""
        self.formatText.text = ""
        if freq in self.freqToFMStation:
            fmStation = self.freqToFMStation[freq]
            self.callSignText.text = fmStation.callSign
            self.formatText.text = fmStation.format

    def setFreq(self, value):
        self.freq = value
        # auxDevice expects actual freq * 100
        self.sendAuxDevices(f"f {int(self.freq*100)}")

    def setPreset(self, value):
        self.preset = value
        count = len(self.presetFMStations)
        if self.preset >= count:
            self.preset = count - 1
        elif self.preset < 0:
            self.preset = 0
        self.showPreset()

    def showPreset(self):
        self.setFreq(self.presetFMStations[self.preset])

    def handleRotary(self, rotaryId, value):
        if (rotaryId == self.rotaryId):
            if Page.pushIfNotCurrent(self):
                now = time.time()
                self.timeout = now + 5
                if self.mode == FMPage.MODE_FREQ:
                    f = value/10.0
                    self.setFreq(f)
                    self.callSignText.text = ""
                elif self.mode == FMPage.MODE_SCAN:
                    delta = value - self.prevRotaryValue
                    if delta > 0:
                        self.sendAuxDevices("S+")
                    elif delta < 0:
                        self.sendAuxDevices("S-")
                elif self.mode == FMPage.MODE_PRESET:
                    self.setPreset(value)

            self.prevRotaryValue = value
            return True

        return False

    def setMode(self, value):
        self.mode = value
        if self.mode > FMPage.MODE_LAST:
            self.mode = FMPage.MODE_FIRST
        if self.mode == FMPage.MODE_FREQ:
            self.freqText.color = (255,0,0)
            self.freqText.shadowColor = (48,0,0)
            self.sendAuxDevices(f"R {self.rotaryId} : {int(self.freq*10)}, 880, 1080, 150, 1")
        elif self.mode == FMPage.MODE_SCAN:
            self.freqText.color = (0,255,0)
            self.freqText.shadowColor = (0,48,0)
            self.sendAuxDevices(f"R {self.rotaryId} : 0, -8000, 8000, 0, 1")
            self.prevRotaryValue = 0
        elif self.mode == FMPage.MODE_PRESET:
            count = len(self.presetFMStations)
            self.freqText.color = (0, 0, 255)
            self.freqText.shadowColor = (0,0,48)
            self.sendAuxDevices(f"R {self.rotaryId} : {self.preset}, 0, {count - 1}, 0, 1")
            self.showPreset()

    def handleButtonDownRepeat(self, buttonId, count):
        if buttonId == self.rotaryId:
            if (self.mode != FMPage.MODE_FREQ):
                self.setMode(FMPage.MODE_FREQ)
            now = time.time()
            self.timeout = now + 5

    def handleButtonUp(self, buttonId, ns):
        if buttonId == self.rotaryId:
            now = time.time()
            self.timeout = now + 5
            if ns > 1000000000:
                pass    # should have been handled by handleButtonDownRepeat
            elif self.mode == FMPage.MODE_FREQ:
                self.setMode(FMPage.MODE_PRESET)
            elif self.mode == FMPage.MODE_PRESET:
                self.setMode(FMPage.MODE_SCAN)
            elif self.mode == FMPage.MODE_SCAN:
                self.setMode(FMPage.MODE_PRESET)
