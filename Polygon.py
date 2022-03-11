from pygame import gfxdraw
import Points

class Polygon:
    def __init__(self, points, strokeColor, fillColor):
        self.points = points
        self.strokeColor = strokeColor
        self.fillColor = fillColor

    # Create a polygon that corresponds to a line starting at the origin, centered on the x-axis, 
    # and extending along the x-axis by length
    # This can then be rotated then translated to position it anywhere on the plane.
    @classmethod
    def fromLine(cls, length, thickness, strokeColor, fillColor):
        thickness = thickness/2
        points = [(0, thickness), (0, -thickness), (length, -thickness), (length, thickness)]
        return Polygon(points, strokeColor, fillColor)

    # rotate the polygon around (0,0) by angle radians
    def rotate(self, angle):
        points = Points.rotatePoints(self.points, angle)
        return Polygon(points, self.strokeColor, self.fillColor)
  
    def translate(self, amount):
        points = Points.translatePoints(self.points, amount)
        return Polygon(points, self.strokeColor, self.fillColor)

    def paint(self, surface):
        if len(self.points) > 0:
            if self.strokeColor != None:
                gfxdraw.aapolygon(surface, self.points, self.strokeColor)
            if self.fillColor != None:
                gfxdraw.filled_polygon(surface, self.points, self.fillColor)