from functions import *
from math import acos, radians, pi


'''
********************************************************************************

    Class: Circle

    Definition: This is the giant class that represents a circle on screen. it 
                has a main function, frame(), which is called for every circle 
                on every loop, many attributes for the circle such as 
                coordinates, radius, mass, velocity, etc. read more comments for
                 more in depth explanations.

    Author: Tyler Silva

    Date: 4-29-2019

    History:

********************************************************************************
'''


class Circle:
    coords = Vector2D(0.0, 0.0)  # where the circle is on the canvas
    # the coordinates during the start of the frame, these aaren't updated until
    # the end of the frame
    oldCoords = Vector2D(0.0, 0.0)
    radius = 0  # radius of the circle
    velocity = Vector2D(0.0, 0.0)  # current velocity of the circle
    # velocity of the circle at the beginning of the frame
    oldVelocity = Vector2D(0.0, 0.0)
    rotationForce = 0.0  # the angular velocity, vestigial from rectangles
    lines = []  # the lines that make up the edges, vestigial from rectangles
    angle = 0.0  # the angle that the shape is facing, vestigial from rectangles
    mass = 0.0  # mass of the circle
    dynamic = False  # whether the shape is able to move
    id = 0  # identification integer, set incrementally
    collidedWith = []  # array remembering what the circle has collided with.
    density = .05  # density of the circles.
    bounciness = 500  # bounciness of the circles, vestigial from gravity.
    color = "white"  # color of the circle
    use_trail = False  # whether or not to draw the trail of this circle
    trailSkip = 5  # how many frames in between each circle in the trail
    trailCounter = 0  # used to keep track of when to add to the trail.
    '''
********************************************************************************

    Function: __init__

    Definition: Creates the circle, assigns private values to their arguments. 
                this one takes a custom mass, as opposed to assigning the mass 
                using the radius to find the area and the denisty.

    Author: Tyler Silva

    Date: 4-29-2019

    History:

********************************************************************************
    '''
    def __init__(self, coords, radius, mass, dynamic, local_id, color="white"):
        self.trail = []
        self.secretVal = 0
        self.coords = coords
        self.radius = radius
        self.mass = mass
        self.dynamic = dynamic
        self.id = local_id
        self.color = color

    '''
********************************************************************************

    Function: __init__

    Definition: Creates the circle, assigns private values to their arguments. 
                this one assigns the mass using the radius to find the area and 
                the density, as opposed to taking a custom mass 

    Author: Tyler Silva

    Date: 4-29-2019

    History:

********************************************************************************
    '''
    def __init__(self, coords, radius, dynamic, local_id, color="white"):
        self.trail = []
        self.secretVal = 0
        self.coords = coords
        self.radius = radius
        self.mass = self.density*pi*radius**2
        self.dynamic = dynamic
        self.id = local_id
        self.color = color

    '''
********************************************************************************

    Function: _translational_collision_

    Definition: This function defines what happens when two circle collide, what
                happens to their velocities.

    Author: Tyler Silva

    Date: 4-29-2019

    History:

********************************************************************************
    '''
    def _translational_collision_(self, shapes, collisions, i):
        # Vesitial from another type of collision calculation
        # otherCoM = shapes[collisions[i]].oldCoords
        old_velocity = self.velocity  # velocity at the beggining of the frame.
        # velocity of the other shape at the beggining of the calculation.
        old_velocity2 = shapes[collisions[i]].velocity
        '''velocityP1 = ((2 * shapes[collisions[i]].mass) / 
                      (self.mass + shapes[collisions[i]].mass))
        velocityP1 = (((self.velocity - shapes[collisions[i]].velocity) * 
                       (CoM - otherCoM)) / float(CoM - otherCoM) ** 2)
        velocityP1 = (CoM - otherCoM)'''
        '''velocity = (
                self.oldVelocity -
                (CoM - otherCoM)
                * ((2 * shapes[collisions[i]].mass) / 
                   (self.mass + shapes[collisions[i]].mass))
                * (((self.oldVelocity - shapes[collisions[i]].oldVelocity) * 
                    (CoM - otherCoM)) / float(CoM - otherCoM) ** 2)
        )'''
        # Velocity calculations for x and y coordinates.
        v_x = (old_velocity.x*(self.mass-shapes[collisions[i]].mass) +
               (2*shapes[collisions[i]].mass*old_velocity2.x))/(
                self.mass+shapes[collisions[i]].mass
        )
        v_y = (old_velocity.y*(self.mass-shapes[collisions[i]].mass) +
               (2*shapes[collisions[i]].mass*old_velocity2.y))/(
                self.mass+shapes[collisions[i]].mass
        )
        velocity = Vector2D(v_x, v_y)
        self.velocity = velocity
        velocity.y *= 1
        velocity.x *= 1

        '''velocity = (
                shapes[collisions[i]].oldVelocity -
                (otherCoM - CoM)
                * ((2 * self.mass) / (self.mass + shapes[collisions[i]].mass))
                * (((shapes[collisions[i]].oldVelocity - self.oldVelocity) * 
                    (otherCoM - CoM)) / float(otherCoM - CoM) ** 2)
        )'''
        v_x = (old_velocity2.x * (shapes[collisions[i]].mass - self.mass) + (
                    2 * self.mass * old_velocity.x)) / (
                     self.mass + shapes[collisions[i]].mass
             )
        v_y = (old_velocity2.y * (shapes[collisions[i]].mass - self.mass) + (
                    2 * self.mass * old_velocity.y)) / (
                    self.mass + shapes[collisions[i]].mass
             )
        velocity = Vector2D(v_x, v_y)
        velocity.y *= 1
        velocity.x *= 1

        '''if velocity == Vector2D(0, 0) and self.velocity == Vector2D(0, 0):
            self.velocity = (self.coords-shapes[collisions[i]].coords)*\
                            (1/self.radius)
            velocity = (shapes[collisions[i]].coords-self.coords)*\
                        (1/shapes[collisions[i]].radius)'''

        return velocity

    '''def _rotational_collision_(self, shapes, collisions, collisionPoints, i, 
                               CoM, oldVelocity, oldVelocity2, otherCoM):
        #return 0
        f = (self.mass * float(self.velocity - oldVelocity)) * 60
        closeEdge = self.get_nearest_edge(collisionPoints[i])
        try:
            b = Vector2D(1, -1 / closeEdge.m)
        except ZeroDivisionError:
            b = Vector2D(1, -maxsize)
        r = find_r(CoM, collisionPoints[i])
        bigF = b * ((r * b) / (float(b) ** 2))
        phi = acos(((r * bigF) / (float(r) * float(bigF)) if (r * bigF) / 
                                                             (float(r) * 
                                                              float(bigF))<1
                    else 1))
        tau = float(r) * float(bigF) * sin(phi)
        h = line_length(self.coords[0], self.coords[1])
        w = line_length(self.coords[1], self.coords[2])
        x = 1/12
        x = self.mass
        x = h**2+w**2
        inertia = (1.0 / 12.0) * self.mass * (h ** 2 + w ** 2)
        self.rotationForce += tau / inertia / 60
        f = (shapes[collisions[i]].mass * float(shapes[collisions[i]].velocity - 
                                                oldVelocity2)) * 60
        try:
            b = Vector2D(1, 1/closeEdge.m)
        except ZeroDivisionError:
            b = Vector2D(1, -maxsize)
        r = find_r(otherCoM, collisionPoints[i])
        bigF = b * ((r * b) / (float(b)**2))
        phi = acos(((r * bigF) / (float(r) * float(bigF)) if (r * bigF) / 
                                                             (float(r) * 
                                                              float(bigF))<1 
                    else 1))
        tau = float(r) * float(f) * sin(phi)
        h = line_length(shapes[collisions[i]].coords[0], 
                        shapes[collisions[i]].coords[1])
        w = line_length(shapes[collisions[i]].coords[1], 
                        shapes[collisions[i]].coords[2])
        inertia = (1.0/12.0)*shapes[collisions[i]].mass*(h**2+w**2)
        return (tau/inertia/60)'''
    '''
********************************************************************************

    Function: move

    Definition: This applies the new velocity to the shape, and moves it the 
                correct amount.

    Author: Tyler Silva

    Date: 4-29-2019

    History:

********************************************************************************
    '''
    def move(self):
        if self.dynamic:
            self.coords = (self.coords + self.velocity)
        else:
            self.rotationForce = 0
            self.velocity = Vector2D(0, 0)
    '''
********************************************************************************

    Function: check_collider

    Definition: Checks to see if the two circles are colliding. returns a 
                collision object, which is just a structure used to hold a 
                position and a boolean. the position is the point of the 
                collision, which for circles is the midpoint of the line created 
                with the endpoints being the centers of each circle. the boolean
                is weather or not there is a collision, which is determined by 
                checking if the distance between the two circles is greater than
                the sum of their radii

    Author: Tyler Silva

    Date: 4-29-2019

    History:

********************************************************************************
    '''
    def check_collider(self, collider):
        # return False
        return Collision(get_midpoint(self.coords, collider.coords),
                         line_length(self.coords, collider.coords) <=
                         (self.radius+collider.radius))

    '''def findLines(self):
        for i in range(0, 3):
            if i < 3:
                j = i+1
            else:
                j = 0
            self.lines.append(Line(self.coords[i], self.coords[j]))'''

    '''
********************************************************************************

    Function: get_nearest_edge

    Definition: Vestigial code from rectangles

    Author: Tyler Silva

    Date: 4-29-2019

    History:

********************************************************************************
    '''
    def get_nearest_edge(self, point):
        self.findLines()
        dists = []
        retval = 0
        for i in range(0, 3):
            dists.append(abs(self.lines[i].m*point.x + (-point.y) +
                             self.lines[i].b)/sqrt(self.lines[i].m**2+1))
        smallest = dists[0]
        for i in range(1, 3):
            if dists[i] < smallest:
                smallest = dists[i]
                retval = i
        return self.lines[retval]
    '''
********************************************************************************

    Function: get_params

    Definition: Tkinter requires 2 corners, not a center point and a radius to 
                create a new circle, so this converts a centerpoint and a radius
                into 2 opposite corners.

    Author: Tyler Silva

    Date: 4-29-2019

    History:

********************************************************************************
    '''
    def get_params(self):
        retval = [0, 0, 0, 0]
        retval[0] = self.coords.x-self.radius
        retval[1] = self.coords.y-self.radius
        retval[2] = self.coords.x+self.radius
        retval[3] = self.coords.y+self.radius
        return retval

    '''
********************************************************************************

    Function: check_nearest_edge

    Definition: this checks to see if the circle is touching an edge, and 
                heading towards that edge. if it is, then it reverses the 
                velocity to simulate a bounce.

    Author: Tyler Silva

    Date: 4-29-2019

    History:

********************************************************************************
    '''
    def check_nearest_edge(self, width, height):
        retval = True
        # if (not (to the right of the left edge) and heading left) or
        # (not (to the left of the right edge) and going right)
        if (not (0 <= self.coords.x - self.radius) and self.velocity.x < 0)or\
                (not (self.coords.x + self.radius <= width) and
                 self.velocity.x > 0):
            self.velocity.x = -self.velocity.x  # bounce
            retval = False
        # if (not (below top of screen) and going up) or (not (above top of
        # screen) and going down)
        elif (not (0 <= self.coords.y - self.radius) and self.velocity.y < 0)or\
                (not (self.coords.y + self.radius <= height) and
                 self.velocity.y > 0):
            self.velocity.y = -self.velocity.y  # bounce
            retval = False
        return retval

    '''
********************************************************************************

    Function: frame

    Definition: This is the main function, it handles all physics and other 
                calculations, as well as remembering coordinates for the trail.

    Author: Tyler Silva

    Date: 4-29-2019

    History:

********************************************************************************
    '''
    def frame(self, shapes, exclude, width, height, trail_length):
        # self.move()
        collisions = []
        collision_points = []
        self.oldCoords = self.coords  # old coords updated
        self.oldVelocity = self.velocity  # old velocity updated
        for i in range(self.id, len(shapes)):
            if i != exclude:
                col = self.check_collider(shapes[i])  # check for collision
                if col.collided:  # if there was a collision
                    collisions.append(i)  # make note of it, then continue
                    collision_points.append(col.collisionPoint)
        # center_of_mass = self.coords
        for i in range(0, len(collisions)):
            # process collision
            shapes[collisions[i]].velocity = \
                -self._translational_collision_(shapes, collisions, i)
            '''shapes[collisions[i]].rotationForce += \
                self._rotational_collision_(shapes, collisions, collisionPoints, 
                                            i, CoM, oldVelocity, oldVelocity2,  
                                            otherCoM)'''
        # bounce if at wall
        self.check_nearest_edge(width, height)

        if self.use_trail:
            while len(self.trail) > trail_length:
                self.trail.pop()
            else:
                # if trail needs to be lengthened
                if self.trailCounter == self.trailSkip:
                    self.trail.insert(0, self.coords)
                    self.trailCounter = 0
                else:
                    self.trailCounter += 1

        return shapes

    '''
********************************************************************************

    Function: debug_print

    Definition: prints out info on the shape, used for debugging purposes

    Author: Tyler Silva

    Date: 4-29-2019

    History:

********************************************************************************
    '''
    def debug_print(self):
        pass
        # print ("coords: "+str(self.coords))
        # print ("velocity: "+str(self.velocity))
        # print ("mass: "+str(self.mass))


'''
********************************************************************************

    Class: Line

    Definition: This class is used to hold all the information that is needed 
                for a line 

    Author: Tyler Silva

    Date: 4-29-2019

    History:

********************************************************************************
'''


class Line:
    '''
********************************************************************************

    Function: __init__

    Definition: saves a few private variables.

    Author: Tyler Silva

    Date: 4-29-2019

    History:

********************************************************************************
    '''
    def __init__(self, x1, y1, x2, y2, arrow):
        self.x1 = x1  # start x position
        self.y1 = y1  # start y position
        self.x2 = x2  # end x position
        self.y2 = y2  # end y position
        self.arrow = arrow  # arrow to put on the line

    '''
********************************************************************************

    Function: get_params

    Definition: returns the private variables in the order tkinter needs them.

    Author: Tyler Silva

    Date: 4-29-2019

    History:

********************************************************************************
    '''
    def get_params(self):
        return [self.x1, self.y1, self.x2, self.y2, self.arrow]
