from Layer import Layer
from TextLayer import TextLayer

class SevenSegmentLayer(Layer):
    def __init__(self):
        super().__init__()
        self._value = 0
        self.digits = 3
        self.decimalPlaces = 2

        self.shadowText = TextLayer()
        self.shadowText.text = "";
        self.shadowText.position = Layer.center
        self.shadowText.color = (48, 0, 0)

        self.valueText = TextLayer()
        self.valueText.text = ""
        self.valueText.position = Layer.center
        self.valueText.color = (255, 0, 0)

        self.addLayer(self.shadowText);
        self.addLayer(self.valueText);

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value;

        totalDigits = self.digits
        if (self.decimalPlaces > 0):
            totalDigits += self.decimalPlaces + 1
        self.valueText.text = f"{self.value:{totalDigits}.{self.decimalPlaces}f}"

    @property
    def font(self):
        return self.valueText.font

    @font.setter
    def font(self, value):
        self.valueText.font = value
        self.shadowText.font = value

    @property
    def color(self):
        return self.valueText.color

    @color.setter
    def color(self, value):
        self.valueText.color = value

    @property
    def shadowColor(self):
        return self.shadowText.color

    @shadowColor.setter
    def shadowColor(self, value):
        self.shadowText.color = value

    def createShadow(self):
        shadow = ""
        for i in range(0,self.digits):
            shadow = shadow + "8"
        if self.decimalPlaces > 0:
            shadow = shadow + "."
            for i in range(0, self.decimalPlaces):
                shadow = shadow + "8"
        self.shadowText.text = shadow

    def paint(self, surface):
        if self.shadowText.text == "":
            self.createShadow()

        super().paint(surface)
