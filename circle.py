from functions import *
from math import acos, radians, pi


class Circle:
    coords = Vector2D(0.0, 0.0)
    oldCoords = Vector2D(0.0, 0.0)
    radius = 0
    velocity = Vector2D(0.0, 0.0)
    oldVelocity = Vector2D(0.0, 0.0)
    rotationForce = 0.0
    lines = []
    angle = 0.0
    mass = 0.0
    dynamic = False
    id = 0
    collidedWith = []
    density = .05

    def __init__(self, coords, radius, mass, dynamic, id):
        self.coords = coords
        self.radius = radius
        self.mass = mass
        self.dynamic = dynamic
        self.id = id

    def __init__(self, coords, radius, dynamic, id):
        self.coords = coords
        self.radius = radius
        self.mass = self.density*pi*radius**2
        self.dynamic = dynamic
        self.id = id

    def _translational_collision_(self, shapes, collisions, i, CoM):
        otherCoM = shapes[collisions[i]].oldCoords
        oldVelocity = self.velocity
        oldVelocity2 = shapes[collisions[i]].velocity
        velocityP1 = ((2 * shapes[collisions[i]].mass) / (self.mass + shapes[collisions[i]].mass))
        velocityP1 = (((self.velocity - shapes[collisions[i]].velocity) * (CoM - otherCoM)) / float(CoM - otherCoM) ** 2)
        velocityP1 = (CoM - otherCoM)
        velocity = (
                self.oldVelocity -
                (CoM - otherCoM)
                * ((2 * shapes[collisions[i]].mass) / (self.mass + shapes[collisions[i]].mass))
                * (((self.oldVelocity - shapes[collisions[i]].oldVelocity) * (CoM - otherCoM)) / float(CoM - otherCoM) ** 2)
        )
        self.velocity = velocity
        velocity.y *= 1
        velocity.x *= 1

        velocity = (
                shapes[collisions[i]].oldVelocity -
                (otherCoM - CoM)
                * ((2 * self.mass) / (self.mass + shapes[collisions[i]].mass))
                * (((shapes[collisions[i]].oldVelocity - self.oldVelocity) * (otherCoM - CoM)) / float(otherCoM - CoM) ** 2)
        )
        velocity.y *= 1
        velocity.x *= 1
        return velocity

    '''def _rotational_collision_(self, shapes, collisions, collisionPoints, i, CoM, oldVelocity, oldVelocity2, otherCoM):
        #return 0
        f = (self.mass * float(self.velocity - oldVelocity)) * 60
        closeEdge = self.get_nearest_edge(collisionPoints[i])
        try:
            b = Vector2D(1, -1 / closeEdge.m)
        except ZeroDivisionError:
            b = Vector2D(1, -maxsize)
        r = find_r(CoM, collisionPoints[i])
        bigF = b * ((r * b) / (float(b) ** 2))
        phi = acos(((r * bigF) / (float(r) * float(bigF)) if (r * bigF) / (float(r) * float(bigF))<1 else 1))
        tau = float(r) * float(bigF) * sin(phi)
        h = line_length(self.coords[0], self.coords[1])
        w = line_length(self.coords[1], self.coords[2])
        x = 1/12
        x = self.mass
        x = h**2+w**2
        inertia = (1.0 / 12.0) * self.mass * (h ** 2 + w ** 2)
        self.rotationForce += tau / inertia / 60
        f = (shapes[collisions[i]].mass * float(shapes[collisions[i]].velocity - oldVelocity2)) * 60
        try:
            b = Vector2D(1, 1/closeEdge.m)
        except ZeroDivisionError:
            b = Vector2D(1, -maxsize)
        r = find_r(otherCoM, collisionPoints[i])
        bigF = b * ((r * b) / (float(b)**2))
        phi = acos(((r * bigF) / (float(r) * float(bigF)) if (r * bigF) / (float(r) * float(bigF))<1 else 1))
        tau = float(r) * float(f) * sin(phi)
        h = line_length(shapes[collisions[i]].coords[0], shapes[collisions[i]].coords[1])
        w = line_length(shapes[collisions[i]].coords[1], shapes[collisions[i]].coords[2])
        inertia = (1.0/12.0)*shapes[collisions[i]].mass*(h**2+w**2)
        return (tau/inertia/60)'''
    def move(self):
        if self.dynamic:
            self.coords= (self.coords + self.velocity)
        else:
            self.rotationForce = 0
            self.velocity = Vector2D(0, 0)

    def check_collider(self, collider):
        #return False
        return Collision(getMidpoint(self.coords, collider.coords),
                         line_length(self.coords, collider.coords)<= (self.radius+collider.radius))



    '''def findLines(self):
        for i in range(0, 3):
            if i < 3:
                j = i+1
            else:
                j = 0
            self.lines.append(Line(self.coords[i], self.coords[j]))'''

    '''def get_nearest_edge(self, point):
        self.findLines()
        dists = []
        retval = 0
        for i in range(0, 3):
            dists.append(abs(self.lines[i].m*point.x + (-point.y)+self.lines[i].b)/sqrt(self.lines[i].m**2+1))
        smallest = dists[0]
        for i in range(1, 3):
            if dists[i] < smallest:
                smallest = dists[i]
                retval = i
        return self.lines[retval]'''
    def getParams(self):
        retval =[0, 0, 0, 0]
        retval[0] = self.coords.x-self.radius
        retval[1] = self.coords.y-self.radius
        retval[2] = self.coords.x+self.radius
        retval[3] = self.coords.y+self.radius
        return retval

    def checkNearestEdge(self):
        loss = min(1500/self.mass, 1)
        #print(loss)
        #loss = 0.2
        if (not (20 <= self.coords.x -self.radius) and self.velocity.x < 0) or \
                (not (self.coords.x +self.radius <= 1180) and self.velocity.x > 0):
            self.velocity.x = -self.velocity.x * loss
        elif (not (20 <= self.coords.y -self.radius ) and self.velocity.y < 0) or \
                (not (self.coords.y + self.radius <= 780) and self.velocity.y > 0):
            self.velocity.y = -self.velocity.y * loss


    def frame(self, shapes, exclude):
        self.velocity.y += 0.000001
        #self.move()
        collisions = []
        collisionPoints = []
        self.oldCoords = self.coords
        self.oldVelocity = self.velocity
        for i in range(self.id, len(shapes)):
            if i != exclude or i in self.collidedWith:
                col = self.check_collider(shapes[i])
                if col.collided:
                    collisions.append(i)
                    collisionPoints.append(col.collisionPoint)
        CoM = self.coords
        for i in range(0, len(collisions)):
            otherCoM = shapes[collisions[i]].coords
            oldVelocity = self.velocity
            oldVelocity2 = shapes[collisions[i]].velocity
            shapes[collisions[i]].velocity = -self._translational_collision_(shapes, collisions, i, CoM)
            '''shapes[collisions[i]].rotationForce += self._rotational_collision_(shapes, collisions, collisionPoints, i,
                                                                              CoM, oldVelocity, oldVelocity2, otherCoM)'''
        self.checkNearestEdge()
        self.move()
        return shapes
    def debugPrint(self):
        print ("coords: "+str(self.coords))
        print ("velocity: "+str(self.velocity))






