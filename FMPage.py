import time
from Layer import Layer
from Page import Page
from TextLayer import TextLayer
from Style import Style

class FMPage(Page):
    def __init__(self):
        super().__init__()
        self.rotaryId = 0

        self.style = Style()
        self.style.backColor = (0, 0, 0)

        self.freqText = TextLayer()
        self.freqText.text = "088.00"
        self.freqText.position = Layer.center
        self.shadowText = TextLayer()
        self.shadowText.text = "888.88"
        self.shadowText.position = Layer.center
        #self.shadowText.color = (255-4, 255-8, 255-8)
        self.shadowText.color = (48, 0, 0)

        self.addLayer(self.shadowText);
        self.addLayer(self.freqText);

    @property
    def font(self):
        return self.freqText.font

    @font.setter
    def font(self, value):
        self.freqText.font = value
        self.shadowText.font = value

    def setValue(self, value):
        self.freqText.text = f"{value/10.0:6.2f}"

    def handleRotary(self, rotaryId, value):
        if (rotaryId == 12):
            now = time.time()
            self.timeout = now + 5
            self.setValue(value)
