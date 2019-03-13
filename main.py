from rect import *
from enum import *
from circle import *
from multiprocessing import cpu_count
import time
from random import random

try:
    import Tkinter
    from enum import Enum
except ModuleNotFoundError:
    import tkinter as Tkinter
    class Enum:
        dic = {}
        def __init__(self, *args):
            for i in range(0, len(args)):
                self.dic[args[i]] = i

        def __getitem__(self, item):
            return self.dic[item]

        def __getattr__(self, item):
            return self.dic[item]

shapes = []
noPhysicsShapes = []
lines = []
mass = 10
circleId = 0
States = Enum("debug", "create", "delete", "push", "none")
state = States.none
validShape = False
click = False
shapeToMove = []
framerate = 1.0/60.0
x = 0
y = 0
mouseX = 0
mouseY = 0
active=True

def destroy(event):
    global active
    active = False

def setCreate(event):
    global state
    state = States.create


def motion(event):
    global mouseX, mouseY
    mouseX, mouseY = event.x, event.y


def setPush(event):
    global state
    state = States.push


def setDelete(event):
    global state
    state = States.delete


def debug(event):
    global state
    state = States.debug


def circleAtPos(x, y):
    retval = []
    for i in shapes:
        if abs(line_length(Vector2D(x, y), i.coords))<i.radius:
            retval.append(i)
    return retval


def circleAtPos2(x, y):
    retval = []
    for i in range(0, len(shapes)):
        if abs(line_length(Vector2D(x, y), shapes[i].coords))<shapes[i].radius:
            retval.append(i)
    return retval


def startCircle(event):
    global click
    click = True
    global x
    global y
    if state == States.create:

        global validShape
        if (len(circleAtPos(event.x, event.y)) <= 0):
            validShape = True
        else:
            validShape = False

        x = event.x
        y = event.y
    elif state == States.debug:
        for i in circleAtPos(event.x, event.y):
            i.debugPrint()
    elif state == States.push:
        global shapeToMove
        shapeToMove = circleAtPos2(event.x, event.y)
        x = event.x
        y = event.y



def circleInvalid(circle):
    retval = None
    for i in shapes:
        if line_length(circle.coords, i.coords)<= (circle.radius+i.radius)+10:
            retval = i
    return retval


def maxRadius(coords, radius, collision):
    distance = line_length(coords, collision.coords)
    retval = distance-collision.radius-10
    return(max(0, min(retval, radius)))
def deleteShapes(index):
    global circleId
    for i in range(0, len(index)):
        del shapes[index[i]-i]
    for i in range(0, len(shapes)):
        shapes[i].id = i
    circleId = len(shapes)


def nonPhysics():
    global noPhysicsShapes
    global lines
    noPhysicsShapes = []
    lines = []
    if click:
        if state == States.create:
            if validShape:
                retval = Circle(Vector2D(x, y), line_length(Vector2D(x, y), Vector2D(mouseX, mouseY)), True, circleId)
                # retval.velocity = Vector2D(((random()*2)-1)*.1, ((random()*2)-1)*.1)
                retval.velocity = Vector2D(0, 0)
                collision = circleInvalid(retval)
                if collision:
                    retval.radius = maxRadius(retval.coords, retval.radius, collision)
                noPhysicsShapes.append(retval)
        elif state == States.push:
            lines.append(Line(x, y, mouseX, mouseY, Tkinter.LAST))






def makeCircle(event):
    global click
    click = False
    global x
    global y
    global playing
    global circleId
    if state != States.debug:
        global shapes
        if state == States.create and x and y:
            if validShape:
                retval = Circle(Vector2D(x, y), line_length(Vector2D(x, y), Vector2D(event.x, event.y)), True, circleId)
                #retval.velocity = Vector2D(((random()*2)-1)*.1, ((random()*2)-1)*.1)
                retval.velocity = Vector2D(0, 0)
                collision = circleInvalid(retval)
                if collision:
                    retval.radius = maxRadius(retval.coords, retval.radius, collision)
                if retval.radius >3:
                    circleId += 1
                    shapes.append(retval)
        elif state == States.delete:
            playing = False
            index = circleAtPos2(event.x, event.y)
            while isPlaying:
                time.sleep(0.001)
            deleteShapes(index)
            playing = True
        elif state == States.push and x and y:
            scale = 0.1
            for i in shapeToMove:
                shapes[i].velocity.x += (event.x-x)*scale
                shapes[i].velocity.y += (event.y-y)*scale

def toDelete(shape):
    return shape.coords.x +shape.radius < 0 or shape.coords.x -shape.radius > 1200 or \
        shape.coords.y + shape.radius < 0 or shape.coords.y - shape.radius > 800




def main():
    '''shapes = [Shape([Vector2D(0.0, 0.0), Vector2D(10.0, 0.0),
                     Vector2D(10.0, 800.0), Vector2D(0.0, 800.0)], 5.972 * 10.0 ** 24, False, 0),
              Shape([Vector2D(11.0, 0.0), Vector2D(1189.0, 0.0),
                     Vector2D(1189.0, 10.0), Vector2D(11.0, 10.0)], 5.972 * 10 ** 24, False, 1),
              Shape([Vector2D(1190.0, 0.0), Vector2D(1200.0, 0.0),
                     Vector2D(1200.0, 800.0), Vector2D(1190.0, 800.0)], 5.972 * 10 ** 24, False, 2),
              Shape([Vector2D(11.0, 790.0), Vector2D(1189.0, 790.0),
                     Vector2D(1189.0, 800.0), Vector2D(11.0, 800.0)], 5.972 * 10 ** 24, False, 3),
              Shape([Vector2D(50.0, 100.0), Vector2D(60.0, 100.0),
                     Vector2D(60.0, 110.0), Vector2D(50.0, 110.0)], 1000, True, 4),
              Shape([Vector2D(70.0, 90.0), Vector2D(80.0, 90.0),
                     Vector2D(80.0, 200.0), Vector2D(70.0, 200.0)], 10, True, 5),
              ]'''
    global shapes
    #shapes[5].rotationForce = -2
    global playing
    global isPlaying
    playing = True
    cores = cpu_count()
    startTime = time.time()
    while active:
        if playing:
            isPlaying = True
            coords = []
            for i in range(0, len(shapes)):
                shapes = shapes[i].frame(shapes, i)
                coords.append(shapes[i])
            deleted = 0
            for i in range(0, len(shapes)):
                if toDelete(shapes[i-deleted]):
                    print ("deleting")
                    deleteShapes([i-deleted])
                    deleted += 1
            isPlaying=False
            w.delete("all")
            for i in coords:
                #w.create_polygon(i[0].x, i[0].y, i[1].x, i[1].y, i[2].x, i[2].y, i[3].x, i[3].y)
                params = i.getParams()
                w.create_oval(params[0], params[1], params[2], params[3])
            #print(max(0.0, framerate-(time.time()-startTime)))
            time.sleep(max(0.0, framerate-(time.time()-startTime)))
            startTime = time.time()
        nonPhysics()
        for i in noPhysicsShapes:
            params = i.getParams()
            w.create_oval(params[0], params[1], params[2], params[3])
        for i in lines:
            params = i.getParams()
            w.create_line(params[0], params[1], params[2], params[3], arrow=params[4])
        w.update()
    root.destroy()


root = Tkinter.Tk()
root.attributes('-fullscreen', True)
canvas = Vector2D(root.winfo_screenmmwidth(), root.winfo_screenheight())
root.bind("<Button-1>", startCircle)
root.bind("<ButtonRelease-1>", makeCircle)
root.bind("<Motion>", motion)
root.bind("<Return>", debug)
root.bind("<Escape>", destroy)
root.bind("d", setDelete)
root.bind("c", setCreate)
root.bind("p", setPush)
w = Tkinter.Canvas(root, width=1200, height=800)
w.pack()
root.after(17, main)
root.mainloop()
