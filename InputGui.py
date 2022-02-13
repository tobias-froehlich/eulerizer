import tkinter as tk
import numpy as np
from const import *

class InputGui(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.__bendingOn = tk.IntVar()
        self.__bendingOnCheckbutton = tk.Checkbutton(
            self,
            text="do bending",
            variable=self.__bendingOn,
            onvalue=1,
            offvalue=0,
            command=self.__changeBending

        )
        self.__bendingOnCheckbutton.grid(column=0, row=0)
        self.__resetButton = tk.Button(
            self,
            text="reset",
            command=self.__reset
        )
        self.__resetButton.grid(column=0, row=1)
        self.__factorTwo = tk.DoubleVar()
        self.__scaleFactorTwo = tk.Scale(
          self,
          from_=2.5,
          to=1.5,
          resolution=0.001,
          variable=self.__factorTwo,
          command=self.__changeFactorTwo,
          length=600,
          showvalue=True,
        )
        self.__scaleFactorTwo.grid(column=1, row=1)
        self.__factorThree = tk.DoubleVar()
        self.__scaleFactorThree = tk.Scale(
          self,
          from_=3.5,
          to=2.5,
          resolution=0.001,
          variable=self.__factorThree,
          command=self.__changeFactorThree,
          length=600,
          showvalue=True,
        )
        self.__scaleFactorThree.grid(column=2, row=1)
        self.__factorFive = tk.DoubleVar()
        self.__scaleFactorFive = tk.Scale(
          self,
          from_=5.5,
          to=4.5,
          resolution=0.001,
          variable=self.__factorFive,
          command=self.__changeFactorFive,
          length=600,
          showvalue=True,
        )
        self.__scaleFactorFive.grid(column=3, row=1)
        self.__reset()

    def __reset(self):
        if NO_BENDING:
            self.__bendingOn.set(0)
        else:
            self.__bendingOn.set(1)
        self.__factorTwo.set(FACTOR_TWO)
        self.__factorThree.set(FACTOR_THREE)
        self.__factorFive.set(FACTOR_FIVE)
        self.__changeBending()
        self.__changeFactorTwo()
        self.__changeFactorThree()
        self.__changeFactorFive()


    def __changeBending(self):
        if self.__bendingOn.get():
            print("on", flush=True)
        else:
            print("off", flush=True)

    def __changeFactorTwo(self, ignored=None):
        print("set FACTOR_TWO %f"%(self.__factorTwo.get()), flush=True)

    def __changeFactorThree(self, ignored=None):
        print("set FACTOR_THREE %f"%(self.__factorThree.get()), flush=True)

    def __changeFactorFive(self, ignored=None):
        print("set FACTOR_FIVE %f"%(self.__factorFive.get()), flush=True)

    def destroy(self):
        print("quit", flush=True)


if __name__ == "__main__":
    root = tk.Tk()
    inputGui = InputGui(root)
    inputGui.pack()
    root.mainloop()
