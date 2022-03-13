from Page import Page
from AnalogGauge import AnalogGauge

class VolumePage(Page):
    def __init__(self, surface):
        super().__init__(surface)
        self.analogGauge = AnalogGauge()
        self.analogGauge.backColor = (255, 255, 255)
        self.addLayer(self.analogGauge)

