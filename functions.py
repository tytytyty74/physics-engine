from sys import maxsize
from math import sqrt, cos, sin, radians

'''
********************************************************************************

    Class: Vector2D

    Definition: This class is meant to represent a 2 dimensional Vector, using 
                X, Y; as opposed to angle, magnitude

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

    Definition: stores X and Y coordinates to the private variables

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

    Definition: String representation of the vector, returns the values to look 
                like "(X, Y)"

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

    Definition: this is what is called when you attempt to convert the vector to
                a float. i'm using it to easily find the magnitude of the vector

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

    Definition: This function is called when you attempt to index into the 
                vector, ie: x[0]. it returns the x value if you ask for the 0th 
                index, and the y value if you ask for the 1st index

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

    Definition: this function is called when you try to add a vector to 
                something else. it checks if the other thing is a vector, and if
                it is, it makes a new vector with the x and y values of the 
                other two vectors summed.

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
    '''
    def __add__(self, b):
        if isinstance(b, Vector2D):
            retval = Vector2D(self.x + b.x, self.y + b.y)
        else:
            raise TypeError("Can only add vectors with vectors")
        return retval

    '''
    ********************************************************************************

        Function: __eq__

        Definition: this function is called when you try to check for eqaulity 
                    on an array. if the other object is an array, and the x and
                    y values are the same, then it will return true.

        Author: Tyler Silva

        Date: 4-5-2019

        History:

    ********************************************************************************
    '''
    def __eq__(self, b):
        retval = False
        if isinstance(b, Vector2D):
            if self.x == b.x and self.y == b.y:
                retval = True
        return retval
    '''
********************************************************************************

    Function: __sub__

    Definition: this function is called when you try to subtract something from 
                a vector. if the other thing is a vector, then it subtracts
                the x and y values of each vector, and puts it into a new vector

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
    '''
    def __sub__(self, b):
        if isinstance(b, Vector2D):
            retval = Vector2D(self.x - b.x, self.y - b.y)
        else:
            raise TypeError("Can only Subtract vectors with vectors")
        return retval

    '''
********************************************************************************

    Function: __mul__

    Definition: this is what happens if you multiply something with a vector. if 
                the other thing is an integer or a float, then it multiplies the 
                x and y values by that constant. if the other thing is a vector, 
                then it finds the dot product of the two.

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
    '''
    def __mul__(self, b):
        if type(b) is int or type(b) is float:
            retval = Vector2D(self.x * b, self.y * b)
        elif isinstance(b, Vector2D):
            retval = (self.x * b.x + self.y * b.y)
        else:
            raise TypeError("Can only multiply vectors and scalars (integers " +
                            "and floats), can only use dot product on 2 vectors"
                            )
        return retval

    '''
********************************************************************************

    Function: __neg__

    Definition: This function is called when you want to get the negative of the
                vector. it multiplies the vector by -1

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
    '''
    def __neg__(self):
        return self*-1


'''
********************************************************************************

    Class: Collision

    Definition: simple structure used to store the location of a collision, and 
                where the collision occurred.

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

    Definition: saves arguments to private variables. 

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
    '''
    def __init__(self, collision_point, collided):
        self.collisionPoint = collision_point
        self.collided = collided


'''
********************************************************************************

    Function: get_midpoint

    Definition: gets the midpoint of two lines, using the midpoint formula

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''


def get_midpoint(a, b):
    return Vector2D((a.x + b.x) / 2, (a.y + b.y) / 2)


'''
********************************************************************************

    Function: triangle_area

    Definition: gets the area of a triangle made by 3 vectors

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

    Definition: gets the length of a line, made by 2 vectors

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''


def line_length(a, b):
    return sqrt((b.x-a.x)**2+(b.y-a.y)**2)


'''
********************************************************************************

    Function: get_center_of_mass

    Definition: gets the center of mass of a rectangle, given it's coordinates

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''


def get_center_of_mass(coords):
    return Vector2D((coords[0].x + coords[2].x) / 2, (coords[0].y + coords[2].y)
                    / 2)


'''
********************************************************************************

    Function: find_r

    Definition: finds the radius of a square in a collision

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''


def find_r(center_of_mass, point):
    return Vector2D(point.x - center_of_mass.x, point.y - center_of_mass.y)


'''
********************************************************************************

    Function: get_point_after_rotation

    Definition: takes the position of a square and the amount to rotate it by. 
                returns the new coordinates.

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''


def get_point_after_rotation(position, rot_point, rot_vel):
    rotation = rot_vel / 60
    position -= rot_point
    rotation = radians(rotation)
    new_pos = Vector2D(rot_point.x + position.x * cos(rotation) - position.y *
                      sin(rotation),
                      rot_point.y + position.x * sin(rotation) + position.y *
                      cos(rotation))
    return new_pos