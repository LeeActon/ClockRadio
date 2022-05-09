
from Layer import Layer

class Circle(Layer):
    def __init__(self):
        super().__init__()

        self.center = (0,0)

    # rotate the circle around (0,0) by angle radians
    def rotate(self, angle):
        return self
  
    def translate(self, amount):
        circle = Circle()
        x, y = self.center
        dx, dy = amount
        circle.style = self.style
        circle.center = (x + dx, y + dy)

        return circle

    def paint(self, surface):
        if not self.visible:
            return

        super().paint(surface)

        self.drawCircle(surface, self.center, self.radius, self.strokeColor, self.fillColor)

