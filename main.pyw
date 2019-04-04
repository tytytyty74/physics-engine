import sys
import math
# sys.stdout = open("mylog.txt", "w")
# sys.stderr = open("errors.txt", "w")
# from rect import *
from circle import *
import os
import threading
# from multiprocessing import cpu_count
import time
from random import random
import json

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
    import tkMessageBox as messagebox
    import tkColorChooser as colorchooser
    import tkSimpleDialog as simpledialog
except ModuleNotFoundError:
    import tkinter as Tkinter
    import pickle
    from tkinter import filedialog
    from tkinter import messagebox
    from tkinter import colorchooser
    from tkinter import simpledialog


defaultJson = '''{  
   "delete":"d",
   "create":"c",
   "push":"p",
   "pause":"<space>"
}'''
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
globalX = 0
globalY = 0
active = True
running = True
color = "white"


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
    global mouseX, mouseY, globalX, globalY
    mouseX, mouseY = event.x, event.y
    globalX, globalY = root.winfo_pointerx() - root.winfo_vrootx(), root.winfo_pointery() - root.winfo_vrooty()


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
    retval = []
    for i in shapes:
        if line_length(circle.coords, i.coords)<= (circle.radius+i.radius)+10:
            retval.append(i)
    return retval


def max_radius(coords, radius, collision):
    closest = collision[0]
    smallestdist=line_length(coords, collision[0].coords)-collision[0].radius
    for i in collision:
        if line_length(coords, i.coords)-i.radius<smallestdist:
            smallestdist=line_length(coords, i.coords)-i.radius
            closest=i
    distance = line_length(coords, closest.coords)
    retval = distance-closest.radius-10
    return min(retval, radius)


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
                retval = Circle(Vector2D(x, y), line_length(Vector2D(x, y), Vector2D(mouseX, mouseY)), True, circleId,
                                color=color)
                # retval.velocity = Vector2D(((random()*2)-1)*.1, ((random()*2)-1)*.1)
                retval.velocity = Vector2D(0, 0)
                collision = circle_invalid(retval)
                if len(collision)>0:
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
                retval = Circle(Vector2D(x, y), line_length(Vector2D(x, y), Vector2D(event.x, event.y)), True, circleId,
                                color=color)
                # retval.velocity = Vector2D(((random()*2)-1)*.1, ((random()*2)-1)*.1)
                retval.velocity = Vector2D(0, 0)
                collision = circle_invalid(retval)
                if len(collision)>0:
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
            w.create_oval(params[0], params[1], params[2], params[3], fill=i.color)
        for i in noPhysicsShapes:
            params = i.getParams()
            w.create_oval(params[0], params[1], params[2], params[3], fill=i.color)
        for i in lines:
            params = i.getParams()
            w.create_line(params[0], params[1], params[2], params[3], arrow=params[4])
        w.update()
    root.destroy()
    sys.exit()

def toggle_play(event=None):
    global playing
    playing = not playing
    print (playing)



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
        f = open(fileName, "wb")
        pickle.dump(shapes, f)
        f.close()


def loadShapes():
    fileName = filedialog.askopenfilename(parent=root, title="Load", filetypes=[("Saved Shapes File", "*.p")],
                                          defaultextension="p")
    if not fileName == "":
        global shapes
        f = open(fileName, "rb")
        shapes = pickle.load(f)
        f.close()


def newCircle(xVal, yVal):
    radius = simpledialog.askinteger("Radius", "What should the radius be?", parent=root, minvalue=3)
    if radius is not None:
        global circleId
        retval = Circle(Vector2D(xVal, yVal), radius, True, circleId,color=color)
        # retval.velocity = Vector2D(((random()*2)-1)*.1, ((random()*2)-1)*.1)
        retval.velocity = Vector2D(0, 0)
        collision = circle_invalid(retval)
        if len(collision)>0:
            retval.radius = max_radius(retval.coords, retval.radius, collision)
        if retval.radius > 3:
            circleId += 1
            shapes.append(retval)


def test(event=None):
    pass


def changeColor(change):
    global shapes
    newColor = (colorchooser.askcolor(title="Pick a new color", parent=root))
    for i in change:
        shapes[i].color = newColor[1]

def stop(circles):
    global shapes
    for i in circles:
        shapes[i].velocity = Vector2D(0.0, 0.0)

def right_click(event):
    global playing
    playing = False
    clicked = circle_at_pos2(event.x, event.y)
    if len(clicked)==0:
        emptySpotMenu = Tkinter.Menu(tearoff=0)
        emptySpotMenu.add_command(label="New Circle", command=lambda: newCircle(event.x, event.y))
        emptySpotMenu.post(globalX, globalY)
    else:
        rightClickMenu = Tkinter.Menu()
        rightClickMenu.add_command(label="Delete Circle", command=lambda: delete_shapes(clicked))
        rightClickMenu.add_command(label="Change Color", command=lambda: changeColor(clicked))
        rightClickMenu.add_command(label="Stop Shape", command=lambda: stop(clicked))
        rightClickMenu.post(globalX, globalY)


def shortcutMenu():

    buttons = []
    shortcutStates = Enum("create", "delete", "push", "pause", "none")
    currentState = shortcutStates.none
    currentIndex = 10

    def activateButton(state, index):
        global currentState
        global currentIndex
        currentState = state
        currentIndex = index
        newRoot.bind("<Key>", changeVal)


    def changeVal(event):
        global shortcuts
        global currentIndex
        global currentState
        # global buttons
        buttons[currentIndex].config(text=event.keysym)
        try:
            newRoot.bind("<" + event.keysym + ">", test)
            newRoot.unbind("<" + event.keysym + ">")
            messagebox.showinfo("info", "test 2 success")
            shortcuts[currentState] = "<" + event.keysym + ">"
            f = open("shortcuts.json", "w")
            json.dump(shortcuts, f)
            f.close()
        except:
            try:
                newRoot.bind(event.keysym, test)
                newRoot.unbind(event.keysym)
                messagebox.showinfo(str(currentState), "test 1 success")
                shortcuts[str(currentState)] = event.keysym
                f = open("shortcuts.json", "w")
                json.dump(shortcuts, f)
                f.close()
            except:
                messagebox.showerror("error", "not a valid key")

        currentIndex=10
        currentState=shortcutStates.none


    newRoot = Tkinter.Tk()
    Tkinter.Label(newRoot, text="Change Keyboard Shortcuts").grid(row=0, column=0, columnspan=2)
    Tkinter.Label(newRoot, text="Create Circles").grid(row=1, column=0)
    Tkinter.Label(newRoot, text="Push Circles").grid(row=2, column=0)
    Tkinter.Label(newRoot, text="Delete Circles").grid(row=3, column=0)
    Tkinter.Label(newRoot, text="Toggle Pause/Play").grid(row=4, column=0)
    buttons.append(Tkinter.Button(newRoot, text=shortcuts["create"],
                                  command=lambda: activateButton("create", 0)))
    buttons.append(Tkinter.Button(newRoot, text=shortcuts["push"],
                                  command=lambda: activateButton("push", 1)))
    buttons.append(Tkinter.Button(newRoot, text=shortcuts["delete"],
                                  command=lambda: activateButton("delete", 2)))
    buttons.append(Tkinter.Button(newRoot, text=shortcuts["pause"],
                                  command=lambda: activateButton("pause", 3)))
    for i in range(0, len(buttons)):
        buttons[i].grid(row=i+1, column=1)
    newRoot.protocol("WM_DELETE_WINDOW", newRoot.destroy)
    print("hello 2")



print(sys.argv)
print("hello world")
# root.attributes('-fullscreen', True)
temp = Tkinter.Tk()
temp.withdraw()
try:
    f = open("shortcuts.json", "r")
    shortcuts = json.load(f)
    f.close()
    if shortcuts["delete"] and shortcuts["create"] and shortcuts["push"] and shortcuts["pause"]:
        pass
    for i in shortcuts.values():
        temp.bind(i, test)
except:
    try:
        f.close()
    except:
        pass
    result = messagebox.askyesno("Error", "Your Shortcuts file appears to be corrupted, would you like to recreate "
                                             "the default one?", icon="error", parent=temp)
    print (result)
    if result:
        f=open("shortcuts.json", "w")
        f.write(defaultJson)
        f.close()
        shortcuts = json.loads(defaultJson)
    else:
        messagebox.showinfo("Error", "the program will not function until the shortcuts file has been fixed")
        sys.exit()


root = Tkinter.Tk()
canvas = Vector2D(root.winfo_screenmmwidth(), root.winfo_screenheight())
root.bind("<Button-1>", start_circle)
root.bind("<ButtonRelease-1>", make_circle)
root.bind("<Motion>", motion)
# root.bind("<Return>", debug)
# root.bind("<Escape>", destroy)
root.bind(shortcuts["delete"], set_delete)
root.bind(shortcuts["create"], set_create)
root.bind(shortcuts["push"], set_push)
root.bind("<Configure>", resize)
root.bind(shortcuts["pause"], toggle_play)
root.bind("<ButtonRelease-3>", right_click)
# root.bind("t", test)
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
editMenu.add_separator()
editMenu.add_command(label="Edit Shortcuts", command=shortcutMenu)
menu.add_cascade(label="Edit", menu=editMenu)
menu.add_command(label="Pause/Play", command=toggle_play)
root.config(menu=menu)
root.after(17, main)
root.mainloop()

sys.stdout.close()
sys.stderr.close()
