import math

# get the point located at angle radians and distance from point
def getPoint(point, angle, distance):
    r = angle
    x, y = point
    return x + distance*math.cos(r), y - distance*math.sin(r)

# translate a point by amount
def translatePoint(point, amount):
    x, y = point
    dx, dy = amount
    return (x + dx, y + dy)

def translatePoints(points, amount):
    results = []
    for point in points:
        results.append(translatePoint(point, amount))

    return results

# translate a point by negative amount
def translatePointFrom(point, amount):
    x, y = point
    dx, dy = amount
    return (x - dx, y - dy)

def translatePointsFrom(points, amount):
    results = []
    for point in points:
        results.append(translatePointFrom(point, amount))

    return results

# rotate point angle radians around the origin
def rotatePoint(point, angle):
    x, y = point
    sin = math.sin(angle)
    cos = math.cos(angle)
    
    return (x*cos + y*sin, y*cos - x*sin)

def rotatePointAround(point, angle, center):
    point = translatePointFrom(point, center)
    point = rotatePoint(point, angle)
    
    return translatePoint(point, center)

def rotatePoints(points, angle):
    results = []
    for point in points:
        results.append(rotatePoint(point, angle))

    return results

def rotatePointsAround(points, angle, center):
    result= []
    for point in points:
        results.append(rotatePointAround(point, center))

    return results
