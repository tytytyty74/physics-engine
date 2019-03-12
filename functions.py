from sys import maxsize
from math import sqrt, cos, sin, radians


class Vector2D:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+")"

    def __float__(self):
        return sqrt(self.x**2+self.y**2)

    def __getitem__(self, key):
        if key == 0:
            retval = self.x
        elif key == 1:
            retval = self.y
        else:
            raise IndexError("Vector index out of range")
        return retval

    def __add__(self, b):
        if isinstance(b, Vector2D):
            retval = Vector2D(self.x+b.x, self.y+b.y)
        else:
            raise TypeError("Can only add vectors with vectors")
        return retval

    def __sub__(self, b):
        if isinstance(b, Vector2D):
            retval = Vector2D(self.x-b.x, self.y-b.y)
        else:
            raise TypeError("Can only Subtract vectors with vectors")
        return retval

    def __mul__(self, b):
        if type(b) is int or type(b) is float:
            retval = Vector2D(self.x*b, self.y*b)
        elif isinstance(b, Vector2D):
            retval = (self.x * b.x + self.y * b.y)
        else:
            raise TypeError("Can only multiply vectors and scalars (integers and floats), can only use dot product on \
            2 vectors")
        return retval
    def __neg__(self):
        return self*-1


class Line:
    m = 0
    b = 0

    def __init__(self, point1, point2):
        try:
            self.m = (point2.y-point1.y)/(point2.x-point1.x)
        except ZeroDivisionError:
            self.m = maxsize
        self.b = point1.y-self.m*point1.x


class Collision:
    collisionPoint = Vector2D(0, 0)
    collided = False

    def __init__(self, collisionPoint, collided):
        self.collisionPoint = collisionPoint
        self.collided = collided

def getMidpoint(a, b):
    return Vector2D((a.x + b.x) / 2, (a.y + b.y) / 2)


def triangle_area(a, b, c):
    return abs((a.x*(b.y-c.y)+b.x*(c.y-a.y)+c.x*(a.y-b.y))/2)


def line_length(a, b):
    return sqrt((b.x-a.x)**2+(b.y-a.y)**2)


def getCoM(coords):
    return Vector2D((coords[0].x+coords[2].x)/2, (coords[0].y+coords[2].y)/2)


def find_r(CoM, point):
    return Vector2D(point.x-CoM.x, point.y-CoM.y)


def get_point_after_rotation(position, rotPoint, rotVel):
    rotation = rotVel/60
    position -= rotPoint
    rotation = radians(rotation)
    newPos = Vector2D(rotPoint.x+position.x*cos(rotation)-position.y*sin(rotation),
                      rotPoint.y+position.x*sin(rotation)+position.y*cos(rotation))
    return newPos