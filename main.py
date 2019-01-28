from rect import *
from multiprocessing import cpu_count
import Tkinter
# shapes = [Shape()]
playing = True
cores = cpu_count()


def main():
    coords = []
    for i in range(0, len(shapes)):
        coords.append(shapes[i].frame())
    w.delete("all")
    for i in coords:
        w.create_polygon(i[0].x, i[0].y, i[1].x, i[1].y, i[2].x, i[2].y, i[3].x, i[3].y)



'''root = Tkinter.Tk()
w = Tkinter.Canvas(root, width=1200, height=800)
w.pack()
root.after(17, main)
root.mainloop()'''
