from rect import *
from circle import *
from multiprocessing import cpu_count
import time
from random import random
import Tkinter
shapes = []
mass = 10
circleId = 0
debugState = False
createState = False

def debug(event):
    global debugState
    debugState = not debugState


def circleAtPos(x, y):
    retval = []
    for i in shapes:
        if abs(line_length(Vector2D(x, y), i.coords))<i.radius:
            retval.append(i)
    return retval

def circleAtPos2(x, y, null):
    retval = []
    for i in range(0, len(shapes)):
        if abs(line_length(Vector2D(x, y), shapes[i].coords))<shapes[i].radius:
            retval.append(i)
    return retval

def startCircle(event):
    if not debugState:
        global x
        global y
        global createState
        if (len(circleAtPos(event.x, event.y)) <= 0):
            createState = True
        else:
            createState = False

        x = event.x
        y = event.y
    else:
        for i in circleAtPos(event.x, event.y):
            i.debugPrint()
def circleInvalid(circle):
    retval = True
    for i in shapes:
        if line_length(circle.coords, i.coords)<= (circle.radius+i.radius):
            retval = False
    return retval
def makeCircle(event):
    global x
    global y
    if not debugState and x and y:
        global shapes
        if createState:
            global circleId
            global shapes
            retval = Circle(Vector2D(x, y), line_length(Vector2D(x, y), Vector2D(event.x, event.y)), True, circleId)
            #retval.velocity = Vector2D(((random()*2)-1)*.1, ((random()*2)-1)*.1)
            retval.velocity = Vector2D(0, 0)
            if circleInvalid(retval):
                circleId += 1
                shapes.append(retval)

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
    playing = True
    cores = cpu_count()
    start_time = time.time()
    x = 1  # displays the frame rate every 1 second
    counter = 0
    while playing:
        counter += 1
        coords = []
        for i in range(0, len(shapes)):
            shapes = shapes[i].frame(shapes, i)
            coords.append(shapes[i])
        w.delete("all")
        for i in coords:
            #w.create_polygon(i[0].x, i[0].y, i[1].x, i[1].y, i[2].x, i[2].y, i[3].x, i[3].y)
            params = i.getParams()
            w.create_oval(params[0], params[1], params[2], params[3])
        playing = True
        w.update()
        counter += 1
        if (time.time() - start_time) > x:
            print("FPS: ", counter / (time.time() - start_time))
            counter = 0
            start_time = time.time()

root = Tkinter.Tk()
root.bind("<Button-1>", startCircle)
root.bind("<ButtonRelease-1>", makeCircle)
root.bind("<Return>", debug)
w = Tkinter.Canvas(root, width=1200, height=800)
w.pack()
root.after(17, main)
root.mainloop()
