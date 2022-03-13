from Page import Page
from AnalogGauge import AnalogGauge
import time

class VolumePage(Page):
    def __init__(self, surface):
        super().__init__(surface)
        self.analogGauge = AnalogGauge()
        self.analogGauge.backColor = (255, 255, 255)
        self.addLayer(self.analogGauge)

    def handleRotary(self, rotaryId, value):
        if (rotaryId == 1):
            now = time.time()
            self.timeout = now + 5
