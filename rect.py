from functions import *
from math import acos, radians


class Shape:
    coords = [Vector2D(0, 0), Vector2D(0, 100), Vector2D(100, 100), Vector2D(100, 0)]
    velocity = Vector2D(0, 0)
    rotationForce = 0
    lines = []
    angle = 0
    mass = 0
    dynamic = False

    def __init__(self, coords, mass, dynamic):
        if len(coords) != 4:
            raise ValueError("coords must have a length of 4")
        self.coords = coords
        self.mass = mass
        self.dynamic = dynamic

    def _translational_collision_(self, shapes, collisions, i, CoM):
        otherCoM = getCoM(shapes[collisions[i]])
        oldVelocity = self.velocity
        oldVelocity2 = shapes[collisions[i]].velocity
        velocity = (
                self.velocity -
                ((2 * shapes[collisions[i]].mass) / (self.mass + shapes[collisions[i]].mass))
                * (((self.velocity - shapes[collisions[i]].velocity) * (CoM - otherCoM)) / float(CoM - otherCoM) ** 2)
                * (CoM - otherCoM)
        )
        self.velocity = velocity
        velocity = (
                shapes[collisions[i]].velocity -
                ((2 * self.mass) / (self.mass + shapes[collisions[i]].mass))
                * (((shapes[collisions[i]].velocity - self.velocity) * (otherCoM - CoM)) / float(otherCoM - CoM) ** 2)
                * (otherCoM - CoM)
        )
        return velocity

    def _rotational_collision_(self, shapes, collisions, collisionPoints, i, CoM, oldVelocity, oldVelocity2):

        f = (self.mass * float(self.velocity - oldVelocity)) * 60
        closeEdge = self.get_nearest_edge(collisionPoints[i])
        b = Vector2D(1, -1 / closeEdge.m)
        r = find_r(CoM, collisionPoints[i])
        bigF = ((r * b) / (float(b) ** 2)) * b
        phi = acos(radians((r * bigF) / (float(r) * float(f))))
        tau = float(r) * float(bigF) * sin(phi)
        h = line_length(self.coords[0], self.coords[1])
        w = line_length(self.coords[1], self.coords[2])
        inertia = (1 / 12) * self.mass * (h ** 2 + w ** 2)
        self.rotationForce += tau / inertia / 60
        f = (shapes[collisions[i]].mass * float(shapes[collisions[i]].velocity - oldVelocity2)) * 60


    def move(self):
        if self.dynamic:
            for i in range(0, len(self.coords)):
                self.coords[i] = (get_point_after_rotation(self.coords[i], getCoM(self.coords), self.rotationForce) +
                self.velocity)
        else:
            self.rotationForce = 0
            self.velocity = Vector2D(0, 0)


    def check_collider(self, collider):
        retval = Collision(Vector2D(0, 0), False)
        Ccoords = collider.coords
        square = triangle_area(Ccoords[0], Ccoords[1], Ccoords[2])*2
        for i in range(0, 4):
            total = 0
            for j in range(0, 4):
                corner = 0
                if j < 3:
                    corner = j+1
                total += triangle_area(Ccoords[j], self.coords[i], Ccoords[corner])
            if total <= square+0.01:
                retval = Collision(self.coords[i], True)
        return retval

    def findLines(self):
        for i in range(0, 3):
            if i < 3:
                j = i+1
            else:
                j = 0
            self.lines.append(Line(self.coords[i], self.coords[j]))

    def get_nearest_edge(self, point):
        self.findLines()
        dists = []
        retval = 0
        for i in range(0, 3):
            dists.append(abs(self.lines[i].m*point.x + (-point.y)+self.lines[i].b)/sqrt(self.lines[i].m))
        smallest = dists[0]
        for i in range(1, 3):
            if dists[i] < smallest:
                smallest = dists[i]
                retval = i
        return self.lines[retval]

    def frame(self, shapes):
        self.move()
        collisions = []
        collisionPoints = []
        for i in range(0, len(shapes)):
            col = self.check_collider(shapes[i])
            if col.collided:
                collisions.append(i)
                collisionPoints.append(col)
        CoM = getCoM(self.coords)
        for i in range(0, len(collisions)):
            oldVelocity = self.velocity
            oldVelocity2 = shapes[collisions[i]].velocity
            shapes[collisions[i]].velocity = self._translational_collision_(shapes, collisions, i, CoM)
            shapes[collisions[i]].rotationForce = self._rotational_collision_(shapes, collisions, collisionPoints, i,
                                                                              CoM, oldVelocity)






