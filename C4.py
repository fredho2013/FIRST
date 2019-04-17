
import sys
if (sys.version_info > (3, 0)):
    from tkinter import *
else:
    from Tkinter import *

def hello(e=None):
    print('Hello')

root = Tk()
Button(root, text='say hello', command=hello).pack()
root.bind('<Escape>', lambda e: root.quit())
root.bind('h', hello)
root.mainloop()