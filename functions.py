from sys import maxsize
from math import sqrt, cos, sin, radians

'''
********************************************************************************

    Class: Vector2D

    Definition:

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
class Vector2D:
    x = 0
    y = 0


    '''
********************************************************************************

    Function: __init__

    Definition:

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y


    '''
********************************************************************************

    Function: __str__

    Definition:

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
    '''
    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+")"


    '''
********************************************************************************

    Function: __float__

    Definition:

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
    '''
    def __float__(self):
        return sqrt(self.x**2+self.y**2)

    
    '''
********************************************************************************

    Function: __getitem__

    Definition:

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
    '''
    def __getitem__(self, key):
        if key == 0:
            retval = self.x
        elif key == 1:
            retval = self.y
        else:
            raise IndexError("Vector index out of range")
        return retval


    '''
********************************************************************************

    Function: __add__

    Definition:

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
    '''
    def __add__(self, b):
        if isinstance(b, Vector2D):
            retval = Vector2D(self.x+b.x, self.y+b.y)
        else:
            raise TypeError("Can only add vectors with vectors")
        return retval


    '''
********************************************************************************

    Function: __sub__

    Definition:

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
    '''
    def __sub__(self, b):
        if isinstance(b, Vector2D):
            retval = Vector2D(self.x-b.x, self.y-b.y)
        else:
            raise TypeError("Can only Subtract vectors with vectors")
        return retval


    '''
********************************************************************************

    Function: __mul__

    Definition:

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
    '''
    def __mul__(self, b):
        if type(b) is int or type(b) is float:
            retval = Vector2D(self.x*b, self.y*b)
        elif isinstance(b, Vector2D):
            retval = (self.x * b.x + self.y * b.y)
        else:
            raise TypeError("Can only multiply vectors and scalars (integers and floats), can only use dot product on \
            2 vectors")
        return retval


    '''
********************************************************************************

    Function: __neg__

    Definition:

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
    '''
    def __neg__(self):
        return self*-1


'''
********************************************************************************

    Class: Line

    Definition:

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
class Line:
    m = 0
    b = 0

    '''
********************************************************************************

    Function: __init__

    Definition:

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
    '''
    def __init__(self, point1, point2):
        try:
            self.m = (point2.y-point1.y)/(point2.x-point1.x)
        except ZeroDivisionError:
            self.m = maxsize
        self.b = point1.y-self.m*point1.x


'''
********************************************************************************

    Class: Collision

    Definition:

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
class Collision:
    collisionPoint = Vector2D(0, 0)
    collided = False


    '''
********************************************************************************

    Function: __init__

    Definition:

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
    '''
    def __init__(self, collisionPoint, collided):
        self.collisionPoint = collisionPoint
        self.collided = collided


'''
********************************************************************************

    Function: getMidpoint

    Definition:

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def getMidpoint(a, b):
    return Vector2D((a.x + b.x) / 2, (a.y + b.y) / 2)


'''
********************************************************************************

    Function: triangle_area

    Definition:

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def triangle_area(a, b, c):
    return abs((a.x*(b.y-c.y)+b.x*(c.y-a.y)+c.x*(a.y-b.y))/2)


'''
********************************************************************************

    Function: line_length

    Definition:

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def line_length(a, b):
    return sqrt((b.x-a.x)**2+(b.y-a.y)**2)


'''
********************************************************************************

    Function: getCoM

    Definition:

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def getCoM(coords):
    return Vector2D((coords[0].x+coords[2].x)/2, (coords[0].y+coords[2].y)/2)


'''
********************************************************************************

    Function: find_r

    Definition:

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def find_r(CoM, point):
    return Vector2D(point.x-CoM.x, point.y-CoM.y)


'''
********************************************************************************

    Function: get_point_after_rotation

    Definition:

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def get_point_after_rotation(position, rotPoint, rotVel):
    rotation = rotVel/60
    position -= rotPoint
    rotation = radians(rotation)
    newPos = Vector2D(rotPoint.x+position.x*cos(rotation)-position.y*sin(rotation),
                      rotPoint.y+position.x*sin(rotation)+position.y*cos(rotation))
    return newPos