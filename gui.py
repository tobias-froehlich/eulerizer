import tkinter as tk
import numpy as np
import time
import const

if const.EULER_NET == "STANDARD":
  from Gui_standard import Gui
elif const.EULER_NET == "STANDARD7":
  from Gui_standard7 import Gui
elif const.EULER_NET == "MEANTONE":
  from Gui_meantone import Gui


root = tk.Tk()
gui = Gui(root)
gui.pack()

loop = 0
def task():
    root.update()
    i = input()
    words = i.split("=")
    if words[0] == "quit":
        root.destroy()
    elif words[0] == "region":
        gui.set_region(int(words[1]))
        root.after(1, task)
    elif words[0] == "note_on":
        subwords = words[1].split(",")
        gui.note_on(
            int(subwords[0]),
            int(subwords[1])
        )
        root.after(1, task)
    elif words[0] == "note_off":
        subwords = words[1].split(",")
        gui.note_off(
            int(subwords[0]),
            int(subwords[1])
        )
        root.after(1, task)
    elif words[0] == "reset":
        gui.reset()
        root.after(1, task)
    elif words[0] == "print":
        print("=".join(words[1:]))

root.after(0, task)

root.mainloop()

