# ==================================  Imports  =================================
import sys
# sys.stdout = open("mylog.txt", "w")
# sys.stderr = open("errors.txt", "w")
import time
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
from circle import *

# =================================  variables  ================================
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
        for j in range(0, len(args)):
            self.dic[args[j]] = j

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

    def key_name(self, item):
        return self.dic.keys()[item]


# This is the default JSON file for the shotcuts, in case the original one gets
# Corrupted
defaultJson = '''{  
   "delete":"<d>",
   "create":"<c>",
   "push":"<p>",
   "pause":"<space>"
}'''
framerate = 1.0 / 60.0  # Determines the number of seconds per frame.
shapes = []  # Where all of the circles that physics applies to are stored
width = 1200  # Width of the screen
height = 800  # Height of the screen
noPhysicsShapes = []  # Where all of the other circles will be placed
lines = []  # Where individual lines are stored, no physics is applied
circleId = 0  # The highest circle ID currently used.
# This is an enum of all the states that the cursor can be in
States = Enum("debug", "create", "delete", "push", "move", "none")
state = States.none  # This is the current state that cursor is in.
# This is used for communication between onclick and onrelease mouse events.
validShape = False
click = False  # This is used for a similar purpose.
shapeToMove = []  # Again, used for communication.
# This is used to communicate where mouse was from onclick to onrelease events
x = 0
y = 0
# This is used to store the mouse position relative to the window
mouseX = 0
mouseY = 0
# This is used to store the mouse position relative to the screen (top left of
# Leftmost screen)
globalX = 0
globalY = 0
playing = True  # Whether or not the simulation is playing
running = True  # Whether or not the program should be running
color = "white"  # Default color for circles.
showVel = False  # Whether to show velocities or not
trail_length = 10  # Default length of the trail, if trails are turned on.

# ================================  functions  ================================

# ============================  state controllers  ============================

'''
********************************************************************************

    Function: ToggleVelocities

    Definition: Toggles whether or not velocities are shown.

    Author: Tyler Silva

    Date: 5-1-2019

    History:

********************************************************************************
'''


def toggle_velocities():
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
    if args:  # To get rid of useless parameter warning
        pass
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
    if args:  # To get rid of useless parameter argument
        pass
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
    if args:  # To get rid of useless parameter argument
        pass
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
    if args:  # To get rid of useless parameter argument
        pass
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
    if args:  # To get rid of useless parameter argument
        pass
    global state
    state = States.move


'''
********************************************************************************

    Function: start_trail

    Definition: sets the shape that was clicked on to leave a trail.

    Author: Tyler Silva

    Date: 5-1-2019

    History:

********************************************************************************
'''


def start_trail(circles):
    global shapes
    for j in circles:
        shapes[j].use_trail = not shapes[j].use_trail


# =============================  Misc Functions  ==============================


'''
********************************************************************************

    Function: test

    Definition: Generic function i can use for testing things, changes often and
                rarely kept here. Disabled for public tests.

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''


def test(event=None):
    if event:  # To get rid of useless parameter argument
        pass
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
    for j in shapes:
        retval += j.velocity
    print (retval.x + retval.y)


'''
********************************************************************************

    Function: destroy

    Definition: Closes the window safely, so there isn't an error. It takes 
                *args so that it can be called from keypress or click of a 
                button, as a keypress passes the "event" argument

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''


def destroy(*args):
    if args:  # To get rid of useless parameter argument
        pass
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
    globalX = root.winfo_pointerx() - root.winfo_vrootx()
    globalY = root.winfo_pointery() - root.winfo_vrooty()


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
    if event:  # To get rid of useless parameter argument
        pass
    global playing
    playing = not playing


'''
********************************************************************************

    Function: resize

    Definition: This event is called on the window being resized, among other 
                things, but i'm using it only to handle resizing of the window. 
                When the window is resized, the canvas is also changed to take 
                up the entire screen.

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


# ============================  Circle Functions  ==============================
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
    local_x = simpledialog.askinteger("Coords", "X coordinate", minvalue=0,
                                      maxvalue=width, parent=root)
    # Gets the y coordinate to place the circle at
    local_y = simpledialog.askinteger("Coords", "Y coordinate", minvalue=0,
                                      maxvalue=height, parent=root,
                                      initialvalue=300)
    # Gets the radius to make the circle.
    radius = simpledialog.askinteger("Radius", "Radius", parent=root,
                                     minvalue=3, initialvalue=50)
    # Gets the x velocity to make the circle move at
    vx = simpledialog.askfloat("Velocity", "X Velocity", minvalue=0,
                               parent=root, initialvalue=0)
    # Gets the y velocity to make the circle move at
    vy = simpledialog.askfloat("Velocity", "Y Velocity", minvalue=0,
                               parent=root, initialvalue=0)
    # If all popups got an answer
    if not (local_x is None or local_y is None or radius is None or
            vx is None or vy is None):
        global circleId
        # Create a circle object, with the x, y, and radius defined earlier.
        retval = Circle(Vector2D(local_x, local_y), radius, True, circleId,
                        color=color)
        # retval.velocity = Vector2D(((random()*2)-1)*.1, ((random()*2)-1)*.1)
        vel = Vector2D(vx, vy)  # Set velocity to what was defined earlier.
        retval.velocity = vel
        collision = circle_invalid(retval, 2)
        if len(collision) > 0:  # If the circle can be placed there
            messagebox.showinfo("Error", "Cannot place a circle, position "
                                         "requested is obstructed.",
                                icon="error", parent=temp)  # Tell the user no
        else:
            circleId += 1
            shapes.append(retval)  # Add circle to array of circles.


'''
********************************************************************************

    Function: circle_at_pos

    Definition: Checks if there is a circle at the given x and y value. Returns 
                the circle object

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''


def circle_at_pos(local_x, local_y):
    retval = []
    for j in shapes:
        # If the distance from where the circle is to the point it's checking is
        # Is less than the radius of the circle
        if abs(line_length(Vector2D(local_x, local_y), j.coords)) < j.radius:
            retval.append(j)
    return retval


'''
********************************************************************************

    Function: circle_at_pos2

    Definition: Checks if there is a circle at the given x and y value. Returns 
                the index where the circle object is object

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''


def circle_at_pos2(local_x, local_y):
    retval = []
    for j in range(0, len(shapes)):
        # If the distance from where the circle is to the point it's checking is
        # Is less than the radius of the circle
        if abs(line_length(Vector2D(local_x, local_y), shapes[j].coords)) < \
                shapes[j].radius:
            retval.append(j)
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
    for j in shapes:
        # If the distance from one circle's center to another circle's center is
        # Greater than the sum of their radii
        if line_length(circle.coords, j.coords
                       ) <= (circle.radius + j.radius) + error:
            retval.append(j)
    return retval


'''
********************************************************************************

    Function: max_radius

    Definition: This takes a point, a desired radius, and the circle that causes
                the desired radius to be a problem. It then uses that 
                information to get the largest possible radius the circle can 
                have while still not touching anything. 

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''


def max_radius(coords, radius, collision):
    closest = collision[0]  # Assumes that the closest one is the first one.
    smallestdist = line_length(coords, collision[0].coords) - collision[
        0].radius
    for j in collision:
        # If another is closer
        if line_length(coords, j.coords) - j.radius < smallestdist:
            # Set that to be the smallest
            smallestdist = line_length(coords, j.coords) - j.radius
            closest = j
    # Get the distance to closeset circle
    distance = line_length(coords, closest.coords)
    # The distance to the nearest circle minus that circle's radius is the
    # Closest it can get. Subtract 10 just in case.
    retval = distance - closest.radius - 10
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
    for j in range(0, len(index)):
        del shapes[index[j] - j]
    for j in range(0, len(shapes)):
        shapes[j].id = j
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

    Function: new_circle

    Definition: Creates a new circle, if someone tries to create a circle with a 
                radius too small to be used.

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''


def new_circle(x_val, y_val):
    radius = simpledialog.askinteger("Radius", "What should the radius be?",
                                     parent=root, minvalue=3)
    if radius is not None:  # If something was enetered in the popup
        global circleId
        # Creates a circle where the mouse was, with the radius from the popup.
        retval = Circle(Vector2D(x_val, y_val), radius, True, circleId,
                        color=color)
        # retval.velocity = Vector2D(((random()*2)-1)*.1, ((random()*2)-1)*.1)
        retval.velocity = Vector2D(0, 0)
        collision = circle_invalid(retval)  # Check if a circle fits there.
        if len(collision) > 0:
            # Make the radius smaller if it can't fit where it was attempted to
            # be placed
            retval.radius = max_radius(retval.coords, retval.radius, collision)
        if retval.radius > 3:
            circleId += 1
            shapes.append(retval)  # Create the circle


'''
********************************************************************************

    Function: change_color

    Definition: Changes the color of a cirlce.

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''


def change_color(change):
    global shapes
    # Gets the color to change to
    new_color = (colorchooser.askcolor(title="Pick a new color", parent=root))
    for j in change:
        shapes[j].color = new_color[1]  # Changes the color, using the hex value


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
    for j in circles:
        shapes[j].velocity = Vector2D(0.0, 0.0)  # Sets the velocity to 0


# =======================  File Manipulation Functions  ========================

'''
********************************************************************************

    Function: save_shapes

    Definition: Saves the shapes file to a location of the user's choice.

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''


def save_shapes():
    # Asks the user where to save the file to
    file_name = filedialog.asksaveasfilename(parent=root, title="Save As",
                                             filetypes=[("Saved Shapes File",
                                                         "*.p")],
                                             defaultextension="p")
    if not file_name == "":  # If user entered something
        fi = open(file_name, "wb")  # Open the file
        pickle.dump(shapes, fi)  # Save the shapes to the file
        fi.close()


'''
********************************************************************************

    Function: load_shapes

    Definition: Loads the shapes from a file of the user's choice

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''


def load_shapes():
    # Gets the file directory of the file to load from the user
    file_name = filedialog.askopenfilename(parent=root, title="Load",
                                           filetypes=[("Saved Shapes File",
                                                       "*.p")],
                                           defaultextension="p")
    if not file_name == "":  # If the user provided a file name
        global shapes
        fi = open(file_name, "rb")
        shapes = pickle.load(fi)  # Put the contents of the file into the
        fi.close()


# ==========================  Menu Making Functions  ===========================

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
    playing = False  # Stops the simulation from running
    # Finds the circles that were clicked, if any.
    clicked = circle_at_pos2(event.x, event.y)
    if len(clicked) == 0:  # If none were clicked
        # Create menu with 1 option, create a new circle.
        empty_spot_menu = Tkinter.Menu(tearoff=0)
        empty_spot_menu.add_command(label="New Circle",
                                    command=lambda: new_circle(event.x, event.y)
                                    )
        empty_spot_menu.post(globalX, globalY)
    else:
        # Creates a new menu with many options, related to the circle clicked.
        right_click_menu = Tkinter.Menu()
        right_click_menu.add_command(label="Delete Circle",
                                     command=lambda: delete_shapes(clicked))
        right_click_menu.add_command(label="Change Color",
                                     command=lambda: change_color(clicked))
        right_click_menu.add_command(label="Stop Shape",
                                     command=lambda: stop(clicked))
        right_click_menu.add_command(label="Add Trail",
                                     command=lambda: start_trail(clicked))
        right_click_menu.post(globalX, globalY)


'''
********************************************************************************

    Function: shortcut_menu

    Definition: this creates a menu that is used to change the keyboard 
                shortcuts

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''


def shortcut_menu():
    buttons = []  # Array storing the
    # The diffrent functions of the buttons
    shortcut_states = Enum("create", "delete", "push", "pause", "none")
    currentState = shortcut_states.none  # The function currently being changed
    currentIndex = 10  # Used to get the name instead of an integer.

    '''
********************************************************************************

    Function: resetShortcuts

    Definition: resets the shortcuts file back to the default file.

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
    '''

    def reset_shortcuts():
        fi = open("shortcuts.json", "w")
        fi.write(defaultJson)
        fi.close()
        local_shortcuts = json.loads(defaultJson)
        print (local_shortcuts)
        buttons[0].config(text=local_shortcuts["create"])
        buttons[1].config(text=local_shortcuts["delete"])
        buttons[2].config(text=local_shortcuts["push"])
        buttons[3].config(text=local_shortcuts["pause"])

    '''
********************************************************************************

    Function: activateButton

    Definition: sets the state variables to match the most recent button 
                pressed. This function is the callback of the buttons pressed to 
                change the keyboard shortcuts.

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
    '''

    def activate_button(local_state, index):
        global currentState
        global currentIndex
        currentState = local_state
        currentIndex = index
        new_root.bind("<Key>", change_val)

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

    def change_val(event):
        global shortcuts
        global currentIndex
        global currentState
        # Global buttons
        # Change button text to the button that was just pressed
        buttons[currentIndex].config(text=event.keysym)
        # Try binding and unbinding the key, while adding <> around it.
        # If the button does not exist, then it will move on to the next catch,
        # As tkinter will throw an error. If it works, then write the shortcut
        # To the shortcuts file.
        try:
            new_root.bind("<" + event.keysym + ">", test)
            new_root.unbind("<" + event.keysym + ">")
            messagebox.showinfo("info", "test 2 success")
            shortcuts[currentState] = "<" + event.keysym + ">"
            fi = open("shortcuts.json", "w")
            json.dump(shortcuts, fi)
            fi.close()
        except Tkinter.TclError:
            # Does similar, and attempts to bind the key without brackets. If
            # This works, then the key is saved to the shortcuts file.
            try:
                new_root.bind(event.keysym, test)
                new_root.unbind(event.keysym)
                messagebox.showinfo(str(currentState), "test 1 success")
                shortcuts[str(currentState)] = event.keysym
                fi = open("shortcuts.json", "w")
                json.dump(shortcuts, fi)
                fi.close()
            # If neither work, then the program gives up, and just tells you
            # That the key is invalid
            except Tkinter.TclError:
                messagebox.showerror("error", "not a valid key")
        # Rest the states, as we're no longer listening for a button
        currentIndex = 10
        currentState = shortcut_states.none

    new_root = Tkinter.Tk()  # Creates the new window
    # Creates all of the text that the user ssees
    Tkinter.Label(new_root, text="Change Keyboard Shortcuts"
                  ).grid(row=0, column=0, columnspan=2)
    Tkinter.Label(new_root, text="Create Circles").grid(row=1, column=0)
    Tkinter.Label(new_root, text="Push Circles").grid(row=2, column=0)
    Tkinter.Label(new_root, text="Delete Circles").grid(row=3, column=0)
    Tkinter.Label(new_root, text="Toggle Pause/Play").grid(row=4, column=0)
    # Creates all of the buttons, in the same order as the labels
    buttons.append(Tkinter.Button(new_root, text=shortcuts["create"],
                                  command=lambda: activate_button("create", 0)))
    buttons.append(Tkinter.Button(new_root, text=shortcuts["push"],
                                  command=lambda: activate_button("push", 1)))
    buttons.append(Tkinter.Button(new_root, text=shortcuts["delete"],
                                  command=lambda: activate_button("delete", 2)))
    buttons.append(Tkinter.Button(new_root, text=shortcuts["pause"],
                                  command=lambda: activate_button("pause", 3)))
    # Button to reset shortcuts
    Tkinter.Button(new_root, text="Reset Shortcuts", command=reset_shortcuts
                   ).grid(row=5, column=0, columnspan=2)
    for j in range(0, len(buttons)):  # Places all using a loop
        buttons[j].grid(row=j + 1, column=1)
    # Causes the window to close cleanly, without errors
    new_root.protocol("WM_DELETE_WINDOW", new_root.destroy)


# =============================  Click Handlers  ===============================

'''
********************************************************************************

    Function: left_click

    Definition: this is the click handler for when the left mouse button is 
                pressed. For the most part, it just records data on what was 
                clicked on.

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''


def left_click(event):
    global click
    click = True
    global x
    global y
    if state == States.create:  # If creating a circle

        global validShape
        # If a circle can be placed there
        if len(circle_at_pos(event.x, event.y)) <= 0:
            validShape = True
        else:
            validShape = False

        x = event.x
        y = event.y
    elif state == States.debug:
        # For every shape that was clicked on
        for j in circle_at_pos(event.x, event.y):
            j.debug_print()

    elif state == States.push or state == States.move:
        global shapeToMove
        shapeToMove = circle_at_pos2(event.x, event.y)
        x = event.x
        y = event.y


'''
********************************************************************************

    Function: non_physics

    Definition: This is the function used for calculations done on all of the 
                objects that don't need physics calculations. This function 
                handles line trails, showing the user where the circle will be 
                made and how large it will be, showing the arrow when the user 
                attempts to push a circle, and creating a line to show the 
                circle velocities

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''


def non_physics():
    global noPhysicsShapes, lines, state, playing, x, y
    noPhysicsShapes = []  # Resets the array with all of the shapes, to refill
    lines = []
    for j in shapes:
        if j.use_trail:  # If the shape should use a trail
            for k in range(0, len(j.trail)):
                # Create a new circle, at the old coordinates, with a radius
                # That gradually gets smaller, to a final size of 1/10 of the
                # Intial radius.
                retval = Circle(Vector2D(j.trail[k].x, j.trail[k].y),
                                ((float(len(j.trail)) - float(k))
                                 / float(len(j.trail))) * j.radius,
                                True, 0, color=j.color)
                retval.velocity = Vector2D(0, 0)
                noPhysicsShapes.append(retval)
        if showVel:
            # Creates a line, starting at the circle's coordinates, and going to
            # The coordinates plus the velocity. Multiplied by 10 just to make
            # It more visible
            lines.append(Line(j.coords.x, j.coords.y,
                              j.coords.x + j.velocity.x * 10,
                              j.coords.y + j.velocity.y * 10, Tkinter.LAST))
    if click:  # If the mouse is clicked
        if state == States.create:  # If the cursor is in create mode
            if validShape:  # if the shape was started in a valid spot
                # Create a circle that shows what will be made when the mouse is
                # released
                retval = Circle(Vector2D(x, y),
                                line_length(Vector2D(x, y),
                                            Vector2D(mouseX, mouseY)),
                                True, circleId, color=color)
                # Retval.velocity = Vector2D(((random()*2)-1)*.1,
                #                            ((random()*2)-1)*.1)
                retval.velocity = Vector2D(0, 0)
                collision = circle_invalid(retval)
                if len(collision) > 0:
                    retval.radius = max_radius(retval.coords, retval.radius,
                                               collision)
                noPhysicsShapes.append(retval)
        elif state == States.push:  # if the cursor is in push mode
            # create a line from where the mouse was pressed to the current
            # mouse position
            lines.append(Line(x, y, mouseX, mouseY, Tkinter.LAST))
        elif state == States.move:  # If the cursor is in move mode
            playing = False
            for j in shapeToMove:
                # find all circles colliding with the circle being moved
                collisions = circle_invalid(shapes[j])
                collisions.remove(shapes[j])  # remove the circle being moved
                # if the circle being moved isn't colliding with anything
                if len(collisions) == 0:
                    # move the circle to that new position
                    shapes[j].coords = Vector2D(mouseX, mouseY)
                    x, y = mouseX, mouseY
                else:
                    # this checks to see if the user is moving the circle away
                    # from colliding with a another circle, and if it is, then
                    # it allows the movement even if it is still colliding with
                    # another circle with the move.
                    dist = line_length(Vector2D(mouseX, mouseY),
                                       collisions[0].coords)
                    if dist >= line_length(shapes[j].coords,
                                           collisions[0].coords):
                        shapes[j].coords = Vector2D(mouseX, mouseY)
                    else:
                        shapes[j].coords = Vector2D(x, y)


'''
********************************************************************************

    Function: release_click

    Definition: This is the event listener for releasing of the left mouse 
                button. it checks the state of the cursor, and uses global 
                information to create, delete, or push a shape.

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''


def release_click(event):
    # grab all the needed global variables
    global click, x, y, playing, circleId, shapes
    click = False

    if state != States.debug:  # if not debugging
        # if creating a shape, x and y are defined, and the shape is in a valid
        # location
        if state == States.create and x and y:
            if validShape:
                # create the shape at the x and y location that was specified
                # during the onclick listener, a radius that is calculated from
                # the distance between the initial point, and the current mouse
                # position, the current highest ID, and the default color.
                retval = Circle(Vector2D(x, y),
                                line_length(Vector2D(x, y),
                                            Vector2D(event.x, event.y)),
                                True, circleId, color=color)
                # Retval.velocity = Vector2D(((random()*2)-1)*.1,
                #                            ((random()*2)-1)*.1)
                retval.velocity = Vector2D(0, 0)
                # get all circles that would collide with this circle
                collision = circle_invalid(retval)
                if len(collision) > 0:  # if more than 0 circles collide
                    # find the maximum radius the circle can still be, without
                    # colliding into any other circles
                    retval.radius = max_radius(retval.coords, retval.radius,
                                               collision)
                # if the radius is greater than 3, so the circle isn't too tiny
                if retval.radius > 3:
                    circleId += 1
                    shapes.append(retval)
        elif state == States.delete:
            playing = False
            # get the index of the circle under the mouse
            index = circle_at_pos2(event.x, event.y)
            while isPlaying:  # makes sure the simulation has paused
                time.sleep(0.001)
            delete_shapes(index)  # deletes the circle
            playing = True  # unpauses the simulation
        elif state == States.push and x and y:
            # scale to multiply by, as pure pixel distance is too large
            scale = 0.1
            for j in shapeToMove:
                # add the distance of the line, multiplied  by the scale factor,
                # to change the velocity
                shapes[j].velocity.x += (event.x - x) * scale
                shapes[j].velocity.y += (event.y - y) * scale


# ================================  GUI Loop  ==================================

'''
********************************************************************************

    Function: main

    Definition: This is the main gui loop for the entire program. this loop 
                handles all of the physics calculations, as well as does all of 
                the drawing to the canvas. it also regulates the framerate to a
                maximum of 60 fps.

    Author: Tyler Silva

    Date: 4-5-2019

    History:

********************************************************************************
'''


def main():
    # this is the array containing all of the shapes to apply physics to
    global shapes, playing, isPlaying
    # shapes[5].rotationForce = -2
    playing = True
    # cores = cpu_count()
    start_time = time.time()  # gets the time to regulate fps
    while running:  # while the program is meant to be running.
        if playing:  # while the simulation is meant to be running.
            # this tells the rest of the program to not change important
            # variables, as they are being used.
            isPlaying = True
            # for every shape, run it's frame method, which does all of the
            # physics calculations and returns the shapes array after all of
            # that object's collisions have been dealt with
            for j in range(0, len(shapes)):
                shapes = shapes[j].frame(shapes, j, width, height, trail_length)
                # Shapes[i].move()
            deleted = 0
            # apply all velocities that are necessary.
            for j in shapes:
                j.move()
            # delete all shapes that need to be deleted
            for j in range(0, len(shapes)):
                if to_delete(shapes[j - deleted]):
                    print ("deleting")
                    delete_shapes([j - deleted])
                    deleted += 1
            isPlaying = False
            # Print(max(0.0, framerate-(time.time()-startTime)))
            # regulates framrate
            time.sleep(max(0.0, framerate - (time.time() - start_time)))
            start_time = time.time()
        non_physics()  # runs gui calculations, not physics ones
        w.delete("all")  # clears the canvas so that shapes don't overlap
        for j in shapes:  # draws all physics related circles
            # w.create_polygon(i[0].x, i[0].y, i[1].x, i[1].y, i[2].x, i[2].y,
            #                  i[3].x, i[3].y)
            params = j.get_params()
            w.create_oval(params[0], params[1], params[2], params[3],
                          fill=j.color)
        for j in noPhysicsShapes:  # draws all other circles shapes
            params = j.get_params()
            temp2 = w.create_oval(params[0], params[1], params[2], params[3],
                                  fill=j.color)
            w.tag_lower(temp2)  # if shapes overlap, these ones go underneath
        for j in lines:  # draws all lines
            params = j.get_params()
            w.create_line(params[0], params[1], params[2], params[3],
                          arrow=params[4])
        w.update()  # updates the canvas
    root.destroy()
    sys.exit()


# ==================================  Main  ====================================

# temporary window in case there's a problem with the shorcuts file
temp = Tkinter.Tk()
temp.withdraw()
try:  # try to open the shortcuts file and bind all the values there
    # this raises a IOError if the file doesn't exist
    f = open("shortcuts.json", "r")
    shortcuts = json.load(f)
    f.close()
    # this raises a KeyError if any of them don't exist
    if shortcuts["delete"] and shortcuts["create"] and shortcuts["push"] and \
            shortcuts["pause"]:
        pass
    for i in shortcuts.values():
        # this raises a TclError if one of them is an invalid binding
        temp.bind(i, test)
except (IOError, KeyError, Tkinter.TclError):
    # attempts to close the file, assumes that the file wasn't opened if it
    # can't be closed
    try:
        f.close()
    except NameError:
        pass

    # asks the user if they want to remake the shortcuts file.
    result = messagebox.askyesno("Error", "Your Shortcuts file appears to be " +
                                 "corrupted, would you like to " +
                                 "recreate the default one?",
                                 icon="error", parent=temp)
    # result can be either True, False, or None if the user closed the box.
    if result:
        # overwrites the json file with the default json
        f = open("shortcuts.json", "w")
        f.write(defaultJson)
        f.close()
        shortcuts = json.loads(defaultJson)
    else:
        # warns the user that they cannot use the program without the shortcuts
        # file
        messagebox.showinfo("Error", "the program will not function until the" +
                            " shortcuts file has been fixed",
                            icon="error", parent=temp)
        sys.exit()
# create the window
root = Tkinter.Tk()
canvas = Vector2D(root.winfo_screenmmwidth(), root.winfo_screenheight())
# binds all of the important events
root.bind("<Button-1>", left_click)
root.bind("<ButtonRelease-1>", release_click)
root.bind("<Motion>", motion)
# root.bind("<Return>", debug)
# root.bind("<Escape>", destroy)
root.bind(shortcuts["delete"], set_delete)
root.bind(shortcuts["create"], set_create)
root.bind(shortcuts["push"], set_push)
root.bind(shortcuts["pause"], toggle_play)
root.bind("<Configure>", resize)  # on resize or movement of the window
root.bind("<ButtonRelease-3>", right_click)
root.bind("t", test)
root.protocol("WM_DELETE_WINDOW", destroy)  # onclick of the red x
w = Tkinter.Canvas(root, width=width, height=height, bd=0, highlightthickness=0)
w.pack()  # pack the cavas into the window

# creates the menus
menu = Tkinter.Menu(root)
fileMenu = Tkinter.Menu(menu, tearoff=0)
fileMenu.add_command(label="Save", command=save_shapes)
fileMenu.add_command(label="Open", command=load_shapes)
menu.add_cascade(label="File", menu=fileMenu)
editMenu = Tkinter.Menu(menu, tearoff=0)
editMenu.add_command(label="Create Circles", command=set_create)
editMenu.add_command(label="Delete Circles", command=set_delete)
editMenu.add_command(label="Change Circle Velocities", command=set_push)
editMenu.add_command(label="Move Circles", command=set_move)
editMenu.add_separator()
editMenu.add_command(label="Edit Shortcuts", command=shortcut_menu)
menu.add_cascade(label="Edit", menu=editMenu)
createMenu = Tkinter.Menu(menu, tearoff=0)
createMenu.add_command(label="Create Precise Circle", command=precise_circle)
menu.add_cascade(label="Create", menu=createMenu)
optionsMenu = Tkinter.Menu(menu, tearoff=0)
optionsMenu.add_command(label="Show/Hide Velocities", command=toggle_velocities)
menu.add_cascade(label="Options", menu=optionsMenu)
menu.add_command(label="Pause/Play", command=toggle_play)
root.config(menu=menu)
# after 17 milliseconds (~1/60th of a second), starts the main program
root.after(17, main)
root.mainloop()
# closes the output files, if they are used. when running outside of code
# editors, outputs are changed so that they are readable
sys.stdout.close()
sys.stderr.close()
