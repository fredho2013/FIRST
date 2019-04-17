
import sys
if (sys.version_info > (3, 0)):
    from tkinter import *
else:
    from Tkinter import *


root = Tk()

canvas = Canvas(root, width = 500, height = 500)
canvas.pack()
radius = 10
bbox = (-radius, -radius, radius, radius)
oval = canvas.create_oval(*bbox)

def move_oval():
    canvas.move(oval, 1, 1)
    canvas.after(20, move_oval)

# Start moving!
move_oval()

root.mainloop()