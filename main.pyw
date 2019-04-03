import sys
import math
sys.stdout = open("mylog.txt", "w")
sys.stderr = open("errors.txt", "w")
# from rect import *
from circle import *
import os
# from multiprocessing import cpu_count
import time
from random import random


class Enum:
    dic = {}

    def __init__(self, *args):
        for i in range(0, len(args)):
            self.dic[args[i]] = i

    def __getitem__(self, item):
        return self.dic[item]

    def __getattr__(self, item):
        return self.dic[item]


try:
    import Tkinter

    import cPickle as pickle
    import tkFileDialog as filedialog
except ModuleNotFoundError:
    # import tkinter as Tkinter
    from tkinter import filedialog
    import pickle
    import tkinter as Tkinter


shapes = []
width = 1200
height = 800
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
active = True
running = True


def close():
    global running
    # os.system("start start.cmd")
    # os.system("start start.cmd")
    running = False


def destroy(event):
    global running
    running = False


def set_create(*args):
    global state
    state = States.create


def motion(event):
    global mouseX, mouseY
    mouseX, mouseY = event.x, event.y


def set_push(*args):
    global state
    state = States.push


def set_delete(*args):
    global state
    state = States.delete


def debug(*args):
    global state
    state = States.debug


def circle_at_pos(x, y):
    retval = []
    for i in shapes:
        if abs(line_length(Vector2D(x, y), i.coords))<i.radius:
            retval.append(i)
    return retval


def circle_at_pos2(x, y):
    retval = []
    for i in range(0, len(shapes)):
        if abs(line_length(Vector2D(x, y), shapes[i].coords))<shapes[i].radius:
            retval.append(i)
    return retval


def start_circle(event):
    global click
    click = True
    global x
    global y
    if state == States.create:

        global validShape
        if len(circle_at_pos(event.x, event.y)) <= 0:
            validShape = True
        else:
            validShape = False

        x = event.x
        y = event.y
    elif state == States.debug:
        for i in circle_at_pos(event.x, event.y):
            i.debugPrint()
    elif state == States.push:
        global shapeToMove
        shapeToMove = circle_at_pos2(event.x, event.y)
        x = event.x
        y = event.y


def circle_invalid(circle):
    retval = None
    for i in shapes:
        if line_length(circle.coords, i.coords)<= (circle.radius+i.radius)+10:
            retval = i
    return retval


def max_radius(coords, radius, collision):
    distance = line_length(coords, collision.coords)
    retval = distance-collision.radius-10
    return max(0, min(retval, radius))


def delete_shapes(index):
    global circleId
    for i in range(0, len(index)):
        del shapes[index[i]-i]
    for i in range(0, len(shapes)):
        shapes[i].id = i
    circleId = len(shapes)


def non_physics():
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
                collision = circle_invalid(retval)
                if collision:
                    retval.radius = max_radius(retval.coords, retval.radius, collision)
                noPhysicsShapes.append(retval)
        elif state == States.push:
            lines.append(Line(x, y, mouseX, mouseY, Tkinter.LAST))


def make_circle(event):
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
                # retval.velocity = Vector2D(((random()*2)-1)*.1, ((random()*2)-1)*.1)
                retval.velocity = Vector2D(0, 0)
                collision = circle_invalid(retval)
                if collision:
                    retval.radius = max_radius(retval.coords, retval.radius, collision)
                if retval.radius >3:
                    circleId += 1
                    shapes.append(retval)
        elif state == States.delete:
            playing = False
            index = circle_at_pos2(event.x, event.y)
            while isPlaying:
                time.sleep(0.001)
            delete_shapes(index)
            playing = True
        elif state == States.push and x and y:
            scale = 0.1
            for i in shapeToMove:
                shapes[i].velocity.x += (event.x-x)*scale
                shapes[i].velocity.y += (event.y-y)*scale


def to_delete(shape):
    return shape.coords.x +shape.radius < 0 or shape.coords.x -shape.radius > width or \
        shape.coords.y + shape.radius < 0 or shape.coords.y - shape.radius > height


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
    # shapes[5].rotationForce = -2
    global playing
    global isPlaying
    playing = True
    # cores = cpu_count()
    startTime = time.time()
    while running:
        if playing:
            isPlaying = True
            coords = []
            for i in range(0, len(shapes)):
                shapes = shapes[i].frame(shapes, i)
                coords.append(shapes[i])
            deleted = 0
            for i in range(0, len(shapes)):
                if to_delete(shapes[i - deleted]):
                    print ("deleting")
                    delete_shapes([i - deleted])
                    deleted += 1
            isPlaying=False

            # print(max(0.0, framerate-(time.time()-startTime)))

            time.sleep(max(0.0, framerate-(time.time()-startTime)))
            startTime = time.time()
        non_physics()
        w.delete("all")
        for i in shapes:
            # w.create_polygon(i[0].x, i[0].y, i[1].x, i[1].y, i[2].x, i[2].y, i[3].x, i[3].y)
            params = i.getParams()
            w.create_oval(params[0], params[1], params[2], params[3])
        for i in noPhysicsShapes:
            params = i.getParams()
            w.create_oval(params[0], params[1], params[2], params[3])
        for i in lines:
            params = i.getParams()
            w.create_line(params[0], params[1], params[2], params[3], arrow=params[4])
        w.update()
    root.destroy()

def toggle_play(event):
    global playing
    playing = not playing



def resize(event):
    global width
    global height
    width = event.width-4
    height = event.height-4
    w.configure(width=width, height=height)

def saveShapes():
    fileName = filedialog.asksaveasfilename(parent=root, title="Save As", filetypes=[("Saved Shapes File", "*.p")],
                                            defaultextension="p")
    if not fileName == "":
        f = open(fileName, "w")
        pickle.dump(shapes, f)
        f.close()

def loadShapes():
    fileName = filedialog.askopenfilename(parent=root, title="Load", filetypes=[("Saved Shapes File", "*.p")],
                                          defaultextension="p")
    if not fileName == "":
        global shapes
        f = open(fileName)
        shapes = pickle.load(f)
        f.close()

def test(event):
    global fileMenu
    fileMenu.post(mouseX, mouseY)
print(sys.argv)
print("hello world")
root = Tkinter.Tk()
# root.attributes('-fullscreen', True)
canvas = Vector2D(root.winfo_screenmmwidth(), root.winfo_screenheight())
root.bind("<Button-1>", start_circle)
root.bind("<ButtonRelease-1>", make_circle)
root.bind("<Motion>", motion)
root.bind("<Return>", debug)
root.bind("<Escape>", destroy)
root.bind("d", set_delete)
root.bind("c", set_create)
root.bind("p", set_push)
root.bind("<Configure>", resize)
root.bind("<space>", toggle_play)
root.bind("t", test)
root.protocol("WM_DELETE_WINDOW", close)
w = Tkinter.Canvas(root, width=width, height=height, )
w.pack()
menu = Tkinter.Menu(root)
fileMenu = Tkinter.Menu(menu, tearoff=0)
fileMenu.add_command(label="Save", command=saveShapes)
fileMenu.add_command(label="Open", command=loadShapes)
menu.add_cascade(label="File", menu=fileMenu)
editMenu = Tkinter.Menu(menu, tearoff=0)
editMenu.add_command(label="Create Circles", command=set_create)
editMenu.add_command(label="Delete Circles", command=set_delete)
editMenu.add_command(label="Change Circle Velocities", command=set_push)
menu.add_cascade(label="Edit", menu=editMenu)
root.config(menu=menu)
root.after(17, main)
root.mainloop()

sys.stdout.close()
sys.stderr.close()
