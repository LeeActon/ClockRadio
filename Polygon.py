from pygame import gfxdraw
import Points
from Layer import Layer

class Polygon(Layer):
    def __init__(self, points = None):
        super().__init__()
        self.points = points

    # Create a polygon that corresponds to a line starting at the origin, centered on the x-axis, 
    # and extending along the x-axis by length
    # This can then be rotated then translated to position it anywhere on the plane.
    @classmethod
    def fromLine(cls, length, thickness):
        thickness = thickness/2
        points = [(0, thickness), (0, -thickness), (length, -thickness), (length, thickness)]
        return Polygon(points)

    # rotate the polygon around (0,0) by angle radians
    def rotate(self, angle):
        points = Points.rotatePoints(self.points, angle)
        return Polygon(points)
  
    def translate(self, amount):
        points = Points.translatePoints(self.points, amount)
        return Polygon(points)

    def paint(self, surface):

        if len(self.points) > 0:
            strokeColor = self.strokeColor
            if strokeColor != None:
                gfxdraw.aapolygon(surface, self.points, strokeColor)
            fillColor = self.fillColor
            if fillColor != None:
                gfxdraw.filled_polygon(surface, self.points, fillColor)