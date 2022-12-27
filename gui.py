import tkinter as tk
import numpy as np
import time
from const import updateConst

const = {} # never dereference!

updateConst(const, "standard")

def selectGui(const):
    if const["EULER_NET"] == "STANDARD":
        from Gui_standard import Gui
    elif const["EULER_NET"] == "STANDARD7":
        from Gui_standard7 import Gui
    elif const["EULER_NET"] == "MEANTONE":
        from Gui_meantone import Gui
    return Gui


Gui = selectGui(const)

root = tk.Tk()
gui = [Gui(const, root),]
gui[0].pack()

#loop = 0
def task():
    root.update()
    i = input()
    words = i.split("=")
    if words[0] == "quit":
        root.destroy()
    elif words[0] == "region":
        gui[0].set_region(int(words[1]))
        root.after(1, task)
    elif words[0] == "note_on":
        gui[0].note_on(
            words[1]
        )
        root.after(1, task)
    elif words[0] == "note_off":
        gui[0].note_off(
            words[1]
        )
        root.after(1, task)
    elif words[0] == "reset":
        gui[0].reset()
        root.after(1, task)
    elif words[0] == "config":
        gui[0].pack_forget()
        gui.clear()
        updateConst(const, words[1])
        Gui = selectGui(const)
        gui.append(Gui(const, root))
        gui[0].pack()
        root.after(1, task)
    elif words[0] == "print":
        print("=".join(words[1:]))
        root.after(1, task)

root.after(0, task)

root.mainloop()

