from Page import Page
from AnalogClockFace import AnalogClockFace
from AnalogAlarmIndicator import AnalogAlarmIndicator
import datetime
from ImageLayer import ImageLayer
from TextLayer import TextLayer
import Points
from Layer import Layer

class AlarmPage(Page):
    onoffMode = 0
    hourMode = 1
    minuteMode = 2
    ampmMode = 3
    maxMode = 3

    offState = 0
    onState = 1
    maxState = 1

    noon = datetime.time(12,0)

    def __init__(self):
        super().__init__()

        self._backgroundImage = None
        self.alarmIndicator = AnalogAlarmIndicator()
        self.alarmIndicator.style.strokeColor = (255,0,0)
        self.alarmIndicator.style.fillColor = (255,0,0)
        self.alarmIndicator.style.radius = 200
        self.titleTextLayer = TextLayer()
        self.titleTextLayer.position = Points.translatePoint(Layer.center, (0, -75))
        self.timeTextLayer = TextLayer()
        self.timeTextLayer.position = Points.translatePoint(Layer.center, (0, 0))
        self.stateTextLayer = TextLayer()
        self.stateTextLayer.position = Points.translatePoint(Layer.center, (0, 75))
        self.stateTextLayer.text = "ON"

        self.time = datetime.time(6, 30)
        self.setState(AlarmPage.onState)

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

    @property
    def font(self):
        return self.titleTextLayer.font

    @font.setter
    def font(self, font):
        self.titleTextLayer.font = font

    @property
    def title(self):
        return self.titleTextLayer.text

    @title.setter
    def title(self, text):
        print(f"title = ''{text}''")
        self.titleTextLayer.text = text

    @property
    def timeFont(self):
        return self.timeTextLayer.font

    @timeFont.setter
    def timeFont(self, font):
        self.timeTextLayer.font = font

    @property
    def stateFont(self):
        return self.stateTextLayer.font

    @stateFont.setter
    def stateFont(self, font):
        self.stateTextLayer.font = font

    @property
    def time(self):
        return self.alarmIndicator.time
    
    @time.setter
    def time(self, time):
        self.alarmIndicator.time = time
        hour = time.hour
        if time >= AlarmPage.noon:
            ampm = "PM"
            hour -= 12
        else:
            ampm = "AM"

        if hour < 1:
            hour = 12
        self.timeTextLayer.text = f"{hour:2}:{time.minute:02}{ampm}"

    def setState(self, state):
        if state > AlarmPage.maxState:
            state = 0
        self.state = state
        if self.state == AlarmPage.offState:
            self.stateTextLayer.text = "OFF"
            self.alarmIndicator.visible = False
        elif self.state == AlarmPage.onState:
            self.stateTextLayer.text = "ON"
            self.alarmIndicator.visible = True

    def setMode(self, mode):
        if mode > AlarmPage.maxMode:
            mode = 0
        self.mode = mode
        if self.mode == AlarmPage.onoffMode:
            self.sendAuxDevices(f"R {self.rotaryId} : {self.state}, 0, 9, 0, 1")
        elif self.mode == AlarmPage.hourMode:
            hour = (self.time.hour % 12) + 1
            self.sendAuxDevices(f"R {self.rotaryId} : {hour}, 1, 12, 0, 1")
            pass
        elif self.mode == AlarmPage.minuteMode:
            hour = (self.time.hour % 12) + 1
            self.sendAuxDevices(f"R {self.rotaryId} : {hour}, 0, 59, 50, 1")
        elif self.mode == AlarmPage.ampmMode:
            self.sendAuxDevices(f"R {self.rotaryId} : 0, 0, 9, 0, 1")

    def onActivate(self):
        self.defaultTimeout()
        self.setMode(AlarmPage.onoffMode)
        return super().onActivate()

    def update(self):
        # make sure self.layers is up to date
        if len(self.layers) == 0:
            if self.backgroundImage != None:
                self.addLayer(self.backgroundImage)
            if self.alarmIndicator != None:
                self.addLayer(self.alarmIndicator)
            if self.titleTextLayer != None:
                self.addLayer(self.titleTextLayer)
            if self.timeTextLayer != None:
                self.addLayer(self.timeTextLayer)
            if self.stateTextLayer != None:
                self.addLayer(self.stateTextLayer)

        super().update()

    def handleRotary(self, rotaryId, value):
        if rotaryId == self.rotaryId:
            self.defaultTimeout()
            if self.mode == AlarmPage.onoffMode:
                self.setState(value % 2)
            elif self.mode == AlarmPage.hourMode:
                self.time = datetime.time(value, self.time.minute)
            elif self.mode == AlarmPage.minuteMode:
                self.time = datetime.time(self.time.hour, value)
            elif self.mode == AlarmPage.ampmMode:
                # Doesn't matter what value is... just flip back and forth
                t = self.time
                hour = (t.hour + 12) % 24
                minute = t.minute
                self.time = datetime.time(hour, minute)
            
            return True

        return False
    
    def handleButtonUp(self, buttonId, ns):
        if buttonId == self.rotaryId:
            self.defaultTimeout()
            self.setMode(self.mode + 1)

