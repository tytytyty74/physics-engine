#==================================  Imports  ==================================
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
from random import random, randint
import json

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

#=================================  variables  =================================
'''
********************************************************************************

    Class: Enum

    Definition: this is a class i made to represent the Enum datatype available 
                in most languages.


    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
class Enum:
    dic = {}
    
    '''
********************************************************************************

    Function: __init__

    Definition: this takes all of the arguments, assumes they are strings, and
                adds them to a dictionary, with the string as the key, and an 
                integer as the value

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
    '''
    def __init__(self, *args):
        for i in range(0, len(args)):
            self.dic[args[i]] = i

    '''
********************************************************************************

    Function: __getitem__

    Definition: this is a magic function called when enum is indexed into, ie:
                hello["world"] would call hello.__getitem__("world")

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
    '''
    def __getitem__(self, item):
        return self.dic[item]

    '''
********************************************************************************

    Function: __getattr__

    Definition: this function is called when you attempt to get an attribute 
                from the object, ie: hello.world would call 
                hello.__getattr__("world")

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
    '''
    def __getattr__(self, item):
        return self.dic[item]

    '''
********************************************************************************

    Function: keyName

    Definition: this function is called to get the keyname of a key as a string
                from the enum value

    Author: Tyler Silva

    Date: 5-1-2019

    History:

********************************************************************************
    '''
    def keyName(self, item):
        return self.dic.keys()[item]

# this is the default JSON file for the shotcuts, in case the original one gets
# corrupted
defaultJson = '''{  
   "delete":"<d>",
   "create":"<c>",
   "push":"<p>",
   "pause":"<space>"
}'''
framerate = 1.0/60.0  # determines the number of seconds per frame.
shapes = []  # where all of the circles that physics applies to are stored
width = 1200  # width of the screen
height = 800  # height of the screen
noPhysicsShapes = []  # where all of the other circles will be placed
lines = []  # where individual lines are stored, no physics is applied
circleId = 0  # the highest circle ID currently used.
# this is an enum of all the states that the cursor can be in
States = Enum("debug", "create", "delete", "push", "move", "none")
state = States.none  # this is the current state that cursor is in.
# this is used for communication between onclick and onrelease mouse events.
validShape = False
click = False  # this is used for a similar purpose.
shapeToMove = []  # again, used for communication.
# this is used to communicate where mouse was from onclick to onrelease events
x = 0
y = 0
# this is used to store the mouse position relative to the window
mouseX = 0
mouseY = 0
# this is used to store the mouse position relative to the screen (top left of
# leftmost screen)
globalX = 0
globalY = 0
playing = True  # whether or not the simulation is playing
running = True  # whether or not the program should be running
color = "white"  # default color for circles.
showVel = False  # whether to show velocities or not
trail_length = 10  # default length of the trail, if trails are turned on.


#=================================  functions  =================================

#=============================  state controllers  =============================

'''
********************************************************************************

    Function: ToggleVelocities

    Definition: Toggles whether or not velocities are shown.

    Author: Tyler Silva

    Date: 5-1-2019

    History:

********************************************************************************
'''
def ToggleVelocities():
    global showVel
    showVel = not showVel

'''
********************************************************************************

    Function: set_create

    Definition: Sets the cursor state to create 

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def set_create(*args):
    global state
    state = States.create


'''
********************************************************************************

    Function: set_push

    Definition: Sets the cursor state to push

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def set_push(*args):
    global state
    state = States.push


'''
********************************************************************************

    Function: set_delete

    Definition: Sets the cursor state to delete

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def set_delete(*args):
    global state
    state = States.delete


'''
********************************************************************************

    Function: debug

    Definition: Sets the cursor state to debug

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def debug(*args):
    global state
    state = States.debug


'''
********************************************************************************

    Function: set_move

    Definition: Sets the cursor state to move

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def set_move(*args):
    #messagebox.showwarning("Warning", "This feature is not yet properly implimented, use at your own risk")
    global state
    state = States.move

'''
********************************************************************************

    Function: startTrail

    Definition: sets the shape that was clicked on to leave a trail.

    Author: Tyler Silva

    Date: 5-1-2019

    History:

********************************************************************************
'''
def startTrail(circles):
    global shapes
    for i in circles:
        shapes[i].useTrail = not shapes[i].useTrail

#==============================  Misc Functions  ===============================

'''
********************************************************************************

    Function: test

    Definition: Generic function i can use for testing things, changes often and
                rarely kept here. disabled for public tests.

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def test(event=None):
    '''root.overrideredirect(True)
    #root.geometry("+250+250")
    root.lift()
    root.wm_attributes("-topmost", True)
    #root.wm_attributes("-disabled", True)
    root.wm_attributes("-transparentcolor", "white")
    root.config(menu = Tkinter.Menu(root))
    root.unbind(shortcuts["delete"])
    root.unbind(shortcuts["create"])
    root.unbind(shortcuts["push"])
    root.unbind(shortcuts["pause"])
    root.attributes("-fullscreen", True)
#    root.wm_attributes("-transparentcolor", "black")'''
    retval = Vector2D(0.0, 0.0)
    for i in shapes:
        retval += i.velocity
    print (retval.x + retval.y)



'''
********************************************************************************

    Function: destroy

    Definition: Closes the window safely, so there isn't an error. it takes 
                *args so that it can be called from keypress or click of a 
                button, as a keypress passes the "event" argument

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def destroy(*args):
    global running
    running = False


'''
********************************************************************************

    Function: motion

    Definition: This event is called on the motion of the mouse. It saves the 
                local and global mouse position to the correct global variables.

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def motion(event):
    global mouseX, mouseY, globalX, globalY
    mouseX, mouseY = event.x, event.y
    globalX, globalY = root.winfo_pointerx() - root.winfo_vrootx(), root.winfo_pointery() - root.winfo_vrooty()


'''
********************************************************************************

    Function: toggle_play

    Definition: Toggles whether the simulation is playing or not.

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def toggle_play(event=None):
    global playing
    playing = not playing


'''
********************************************************************************

    Function: resize

    Definition: This event is called on the window being resized, among other 
                things, but i'm using it only to handle resizing of the window. 
                When the window is resized, the canvas is also changed to take up the entire screen.

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def resize(event):
    global width
    global height
    width = event.width
    height = event.height
    w.configure(width=width, height=height)

#=============================  Circle Functions  ==============================
'''
********************************************************************************

    Function: precise_circle

    Definition: creates a precise circle at a given point, using 

    Author: Tyler Silva

    Date: 5-1-2019

    History:

********************************************************************************
'''
def precise_circle():
    # Gets the x coordinate to place the circle at
    x = simpledialog.askinteger("Coords", "X coordinate", minvalue=0,
                                maxvalue=width, parent=root)
    # Gets the y coordinate to place the circle at
    y = simpledialog.askinteger("Coords", "Y coordinate", minvalue=0,
                                maxvalue=height, parent=root, initialvalue=300)
    # Gets the radius to make the circle.
    radius = simpledialog.askinteger("Radius", "Radius", parent=root,
                                     minvalue=3, initialvalue=50)
    # Gets the x velocity to make the circle move at
    Vx = simpledialog.askfloat("Velocity", "X Velocity", minvalue=0,
                               parent=root, initialvalue=0)
    # Gets the y velocity to make the circle move at
    Vy = simpledialog.askfloat("Velocity", "Y Velocity", minvalue=0,
                               parent=root, initialvalue=0)
    # If all popups got an answer
    if not (x is None or y is None or radius is None or Vx is None or Vy is None
    ):
        global circleId
        # Create a circle object, with the x, y, and radius defined earlier.
        retval = Circle(Vector2D(x, y), radius, True, circleId, color=color)
        # retval.velocity = Vector2D(((random()*2)-1)*.1, ((random()*2)-1)*.1)
        vel = Vector2D(Vx, Vy)  # set velocity to what was defined earlier.
        retval.velocity = vel
        collision = circle_invalid(retval, 2)
        if len(collision) > 0:  # if the circle can be placed there
            messagebox.showinfo("Error", "Cannot place a circle, position "
                                         "requested is obstructed.",
                                icon="error", parent=temp)  # tell the user no
        else:
            circleId += 1
            shapes.append(retval)  # add circle to array of circles.




'''
********************************************************************************

    Function: circle_at_pos

    Definition: Checks if there is a circle at the given x and y value. returns 
                the circle object

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def circle_at_pos(x, y):
    retval = []
    for i in shapes:
        # if the distance from where the circle is to the point it's checking is
        # is less than the radius of the circle
        if abs(line_length(Vector2D(x, y), i.coords))<i.radius:
            retval.append(i)
    return retval

'''
********************************************************************************

    Function: circle_at_pos2

    Definition: Checks if there is a circle at the given x and y value. returns 
                the index where the circle object is object

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def circle_at_pos2(x, y):
    retval = []
    for i in range(0, len(shapes)):
        # if the distance from where the circle is to the point it's checking is
        # is less than the radius of the circle
        if abs(line_length(Vector2D(x, y), shapes[i].coords))<shapes[i].radius:
            retval.append(i)
    return retval


'''
********************************************************************************

    Function: circle_invalid

    Definition: Checks to see if a circle is able to be placed where it 
                currently is, without colliding with any other circles.

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def circle_invalid(circle, error=10):
    retval = []
    for i in shapes:
        # If the distance from one circle's center to another circle's center is
        # greater than the sum of their radii
        if line_length(circle.coords, i.coords
                       )<= (circle.radius+i.radius)+error:
            retval.append(i)
    return retval


'''
********************************************************************************

    Function: max_radius

    Definition: This takes a point, a desired radius, and the circle that causes
                the desired radius to be a problem. it then uses that 
                information to get the largest possible radius the circle can 
                have while still not touching anything. 

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def max_radius(coords, radius, collision):
    closest = collision[0]  # assumes that the closest one is the first one.
    smallestdist=line_length(coords, collision[0].coords)-collision[0].radius
    for i in collision:
        # if another is closer
        if line_length(coords, i.coords)-i.radius<smallestdist:
            # set that to be the smallest
            smallestdist=line_length(coords, i.coords)-i.radius
            closest=i
    # get the distance to closeset circle
    distance = line_length(coords, closest.coords)
    # The distance to the nearest circle minus that circle's radius is the
    # closest it can get. subtract 10 just in case.
    retval = distance-closest.radius-10
    return min(retval, radius)


'''
********************************************************************************

    Function: delete_shapes

    Definition: Deletes a circle from the array, and then re-id's them, so that 
                none of the Ids are missing.

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def delete_shapes(index):
    global circleId
    for i in range(0, len(index)):
        del shapes[index[i]-i]
    for i in range(0, len(shapes)):
        shapes[i].id = i
    circleId = len(shapes)


'''
********************************************************************************

    Function: to_delete

    Definition: Checks if the shape is completely off the screen.

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def to_delete(shape):
    return (shape.coords.x + shape.radius < 0 or
            shape.coords.x - shape.radius > width or
            shape.coords.y + shape.radius < 0 or
            shape.coords.y - shape.radius > height)


'''
********************************************************************************

    Function: newCircle

    Definition: Creates a new circle, if someone tries to create a circle with a 
                radius too small to be used.

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def newCircle(xVal, yVal):
    radius = simpledialog.askinteger("Radius", "What should the radius be?",
                                     parent=root, minvalue=3)
    if radius is not None:  # if something was enetered in the popup
        global circleId
        # creates a circle where the mouse was, with the radius from the popup.
        retval = Circle(Vector2D(xVal, yVal), radius, True, circleId,
                        color=color)
        # retval.velocity = Vector2D(((random()*2)-1)*.1, ((random()*2)-1)*.1)
        retval.velocity = Vector2D(0, 0)
        collision = circle_invalid(retval)  # check if a circle fits there.
        if len(collision)>0:
            # make the radius smaller if it can't fit where it was attempted to
            # be placed
            retval.radius = max_radius(retval.coords, retval.radius, collision)
        if retval.radius > 3:
            circleId += 1
            shapes.append(retval) #create the circle


'''
********************************************************************************

    Function: changeColor

    Definition: Changes the color of a cirlce.

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def changeColor(change):
    global shapes
    # Gets the color to change to
    newColor = (colorchooser.askcolor(title="Pick a new color", parent=root))
    for i in change:
        shapes[i].color = newColor[1] #changes the color, using the hex value


'''
********************************************************************************

    Function: stop

    Definition: Stops a circle at a position

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def stop(circles):
    global shapes
    for i in circles:
        shapes[i].velocity = Vector2D(0.0, 0.0) #sets the velocity to 0

#========================  File Manipulation Functions  ========================

'''
********************************************************************************

    Function: saveShapes

    Definition: Saves the shapes file to a location of the user's choice.

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def saveShapes():
    # asks the user where to save the file to
    fileName = filedialog.asksaveasfilename(parent=root, title="Save As",
                                            filetypes=[("Saved Shapes File",
                                                        "*.p")],
                                            defaultextension="p")
    if not fileName == "":  # if user entered something
        f = open(fileName, "wb")  # open the file
        pickle.dump(shapes, f)  # save the shapes to the file
        f.close()


'''
********************************************************************************

    Function: loadShapes

    Definition: Loads the shapes from a file of the user's choice

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def loadShapes():
    # gets the file directory of the file to load from the user
    fileName = filedialog.askopenfilename(parent=root, title="Load",
                                          filetypes=[("Saved Shapes File",
                                                      "*.p")],
                                          defaultextension="p")
    if not fileName == "": #if the user provided a file name
        global shapes
        f = open(fileName, "rb")
        shapes = pickle.load(f)  # put the contents of the file into the
        f.close()

#===========================  Menu Making Functions  ===========================

'''
********************************************************************************

    Function: right_click

    Definition: This is the handler for when the right mouse button is pressed. 
                it opens a new menu for all these options

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def right_click(event):
    global playing
    playing = False  # stops the simulation from running
    # finds the circles that were clicked, if any.
    clicked = circle_at_pos2(event.x, event.y)
    if len(clicked)==0:  # if none were clicked
        # create menu with 1 option, create a new circle.
        emptySpotMenu = Tkinter.Menu(tearoff=0)
        emptySpotMenu.add_command(label="New Circle",
                                  command=lambda: newCircle(event.x, event.y))
        emptySpotMenu.post(globalX, globalY)
    else:
        # creates a new menu with many options, related to the circle clicked.
        rightClickMenu = Tkinter.Menu()
        rightClickMenu.add_command(label="Delete Circle",
                                   command=lambda: delete_shapes(clicked))
        rightClickMenu.add_command(label="Change Color",
                                   command=lambda: changeColor(clicked))
        rightClickMenu.add_command(label="Stop Shape",
                                   command=lambda: stop(clicked))
        rightClickMenu.add_command(label="Add Trail",
                                   command=lambda: startTrail(clicked))
        rightClickMenu.post(globalX, globalY)


'''
********************************************************************************

    Function: shortcutMenu

    Definition: this creates a menu that is used to change the keyboard 
                shortcuts

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def shortcutMenu():
    buttons = []  # array storing the
    # the diffrent functions of the buttons
    shortcutStates = Enum("create", "delete", "push", "pause", "none")
    currentState = shortcutStates.none  # the function currently being changed
    currentIndex = 10  # used to get the name instead of an integer.


    '''
********************************************************************************

    Function: resetShortcuts

    Definition: resets the shortcuts file back to the default file.

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
    '''
    def resetShortcuts():
        f = open("shortcuts.json", "w")
        f.write(defaultJson)
        f.close()
        shortcuts = json.loads(defaultJson)
        print (shortcuts)
        buttons[0].config(text=shortcuts["create"])
        buttons[1].config(text=shortcuts["delete"])
        buttons[2].config(text=shortcuts["push"])
        buttons[3].config(text=shortcuts["pause"])


    '''
********************************************************************************

    Function: activateButton

    Definition: sets the state variables to match the most recent button 
                pressed. this function is the callback of the buttons pressed to 
                change the keyboard shortcuts.

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
    '''
    def activateButton(state, index):
        global currentState
        global currentIndex
        currentState = state
        currentIndex = index
        newRoot.bind("<Key>", changeVal)

    
    '''
********************************************************************************

    Function: changeVal

    Definition: This is the callback from any key being pressed, and tests to 
                see if the new key can be used as a keyboard shortcut, and if it
                then it makes the new keyboard shortcut.

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
    '''
    def changeVal(event):
        global shortcuts
        global currentIndex
        global currentState
        # global buttons
        # change button text to the button that was just pressed
        buttons[currentIndex].config(text=event.keysym)
        # try binding and unbinding the key, while adding <> around it.
        # if the button does not exist, then it will move on to the next catch,
        # as tkinter will throw an error. if it works, then write the shortcut
        # to the shortcuts file.
        try:
            newRoot.bind("<" + event.keysym + ">", test)
            newRoot.unbind("<" + event.keysym + ">")
            messagebox.showinfo("info", "test 2 success")
            shortcuts[currentState] = "<" + event.keysym + ">"
            f = open("shortcuts.json", "w")
            json.dump(shortcuts, f)
            f.close()
        except:
            # does similar, and attempts to bind the key without brackets. if
            # this works, then the key is saved to the shortcuts file.
            try:
                newRoot.bind(event.keysym, test)
                newRoot.unbind(event.keysym)
                messagebox.showinfo(str(currentState), "test 1 success")
                shortcuts[str(currentState)] = event.keysym
                f = open("shortcuts.json", "w")
                json.dump(shortcuts, f)
                f.close()
            # if neither work, then the program gives up, and just tells you
            # that the key is invalid
            except:
                messagebox.showerror("error", "not a valid key")
        # rest the states, as we're no longer listening for a button
        currentIndex = 10
        currentState = shortcutStates.none


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
    Tkinter.Button(newRoot, text="Reset Shortcuts", command=resetShortcuts).grid(row=5, column=0, columnspan=2)
    for i in range(0, len(buttons)):
        buttons[i].grid(row=i+1, column=1)
    newRoot.protocol("WM_DELETE_WINDOW", newRoot.destroy)
    print("hello 2")

#==============================  Click Handlers  ===============================

'''
********************************************************************************

    Function: start_circle

    Definition:

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
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
    elif state == States.push or state == States.move:
        global shapeToMove
        shapeToMove = circle_at_pos2(event.x, event.y)
        x = event.x
        y = event.y


'''
********************************************************************************

    Function: non_physics

    Definition:

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
def non_physics():
    global noPhysicsShapes, lines, state, playing, x, y
    noPhysicsShapes = []
    lines = []
    for i in shapes:
        if i.useTrail:
            for j in range(0, len(i.trail)):
                retval = Circle(Vector2D(i.trail[j].x, i.trail[j].y),
                                ((float(len(i.trail))-float(j))/float(len(i.trail)))*i.radius, True, 0, color=i.color)
                retval.velocity = Vector2D(0, 0)
                noPhysicsShapes.append(retval)
        if showVel:
            lines.append(Line(i.coords.x, i.coords.y, i.coords.x+i.velocity.x*10, i.coords.y+i.velocity.y*10, Tkinter.LAST))
    if click:
        if state == States.create:
            if validShape:
                retval = Circle(Vector2D(x, y), line_length(Vector2D(x, y), Vector2D(mouseX, mouseY)), True, circleId,
                                color=color)
                # retval.velocity = Vector2D(((random()*2)-1)*.1, ((random()*2)-1)*.1)
                retval.velocity = Vector2D(0, 0)
                collision = circle_invalid(retval)
                if len(collision) > 0:
                    retval.radius = max_radius(retval.coords, retval.radius, collision)
                noPhysicsShapes.append(retval)
        elif state == States.push:
            lines.append(Line(x, y, mouseX, mouseY, Tkinter.LAST))
        elif state == States.move:
            playing = False
            for i in shapeToMove:
                collisions = circle_invalid(shapes[i])
                collisions.remove(shapes[i])
                if len(collisions) == 0:
                    shapes[i].coords = Vector2D(mouseX, mouseY)
                    x, y = mouseX, mouseY
                else:
                    dist = line_length(Vector2D(mouseX, mouseY), collisions[0].coords)
                    if dist >= line_length(shapes[i].coords, collisions[0].coords):
                        shapes[i].coords = Vector2D(mouseX, mouseY)
                    else:
                        shapes[i].coords = Vector2D(x, y)


'''
********************************************************************************

    Function: make_circle

    Definition:

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
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
                if len(collision) > 0:
                    retval.radius = max_radius(retval.coords, retval.radius, collision)
                if retval.radius > 3:
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
                shapes[i].velocity.x += (event.x - x) * scale
                shapes[i].velocity.y += (event.y - y) * scale

#=================================  GUI Loop  ==================================

'''
********************************************************************************

    Function: main

    Definition:

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''
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
                shapes = shapes[i].frame(shapes, i, width, height, trail_length)
                coords.append(shapes[i])
                #shapes[i].move()
            deleted = 0
            for i in shapes:
                i.move()
            for i in range(0, len(shapes)):
                if to_delete(shapes[i - deleted]):
                    print ("deleting")
                    delete_shapes([i - deleted])
                    deleted += 1
            isPlaying = False

            # print(max(0.0, framerate-(time.time()-startTime)))

            time.sleep(max(0.0, framerate - (time.time() - startTime)))
            startTime = time.time()
        non_physics()
        w.delete("all")
        for i in shapes:
            # w.create_polygon(i[0].x, i[0].y, i[1].x, i[1].y, i[2].x, i[2].y, i[3].x, i[3].y)
            params = i.getParams()
            w.create_oval(params[0], params[1], params[2], params[3], fill=i.color)
        for i in noPhysicsShapes:
            params = i.getParams()
            temp2 = w.create_oval(params[0], params[1], params[2], params[3], fill=i.color)
            w.tag_lower(temp2)
        for i in lines:
            params = i.getParams()
            w.create_line(params[0], params[1], params[2], params[3], arrow=params[4])
        w.update()
    root.destroy()
    sys.exit()

#===================================  Main  ====================================

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
        messagebox.showinfo("Error", "the program will not function until the shortcuts file has been fixed",
                            icon="error", parent=temp)
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
root.bind(shortcuts["pause"], toggle_play)
root.bind("<Configure>", resize)
root.bind("<ButtonRelease-3>", right_click)
root.bind("t", test)
root.protocol("WM_DELETE_WINDOW", destroy)
w = Tkinter.Canvas(root, width=width, height=height, bd=0, highlightthickness=0)
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
editMenu.add_command(label="Move Circles", command=set_move)
editMenu.add_separator()
editMenu.add_command(label="Edit Shortcuts", command=shortcutMenu)
menu.add_cascade(label="Edit", menu=editMenu)
createMenu = Tkinter.Menu(menu, tearoff=0)
createMenu.add_command(label="Create Precise Circle", command=precise_circle)
menu.add_cascade(label="Create", menu=createMenu)
optionsMenu = Tkinter.Menu(menu, tearoff=0)
optionsMenu.add_command(label="Show/Hide Velocities", command=ToggleVelocities)
menu.add_cascade(label="Options", menu=optionsMenu)
menu.add_command(label="Pause/Play", command=toggle_play)
root.config(menu=menu)
root.after(17, main)
root.mainloop()

sys.stdout.close()
sys.stderr.close()
