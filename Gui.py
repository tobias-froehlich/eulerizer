import tkinter as tk
import numpy as np
import time
import const

class Gui(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.__make_canvas()
        self.__make_regions()
        self.__make_dots()

    def __euler_to_coords(self, i, j):
        x = int(
                (
                    (i + 1)
                  + j * 0.5
                ) * const.EULERNET_DISTANCE
            )
        y = int(
                (const.EULER_ROWS - j)
              * np.sqrt(3) * 0.5
              * const.EULERNET_DISTANCE
            )
        return (x, y)

    def __make_canvas(self):
        (w, h) = self.__euler_to_coords(
            const.EULER_COLS,
            0
        )
        w += const.EULERNET_DISTANCE
        h += const.EULERNET_DISTANCE
        self.__canvas = tk.Canvas(
            self,
            width=w,
            height=h,
            bg=const.BACKGROUND_COLOR
        )
        self.__canvas.pack()

    def __make_regions(self):
        self.__regions = []
        for i in range(const.EULER_COLS - 3):
            (x0, y0) = self.__euler_to_coords(
                i-0.5,
                -0.5
            )
            (x1, y1) = self.__euler_to_coords(
                i-0.5,
                const.EULER_ROWS - 0.5
            )
            (x2, y2) = self.__euler_to_coords(
                i+3.5,
                const.EULER_ROWS - 0.5
            )
            (x3, y3) = self.__euler_to_coords(
                i+3.5,
                -0.5
            )
            self.__regions.append(
                self.__canvas.create_polygon(
                    x0, y0, x1, y1, x2, y2, x3, y3,
                    fill=const.REGION_COLOR,
                    width=
                        const.REGION_BORDER_WIDTH,
                    outline=
                        const.REGION_BORDER_COLOR,
                    state=tk.HIDDEN
                )
            )
        self.set_region(4)

    def __make_dots(self):
        self.__dots_small = []
        self.__dots_big = []
        self.__images = [] # preventing garbage
                           # collection
        self.__playing = []
        for j in range(const.EULER_ROWS):
            self.__playing.append([])
            for i in range(const.EULER_COLS):
                self.__playing[-1].append(0)
        index_init = const.NOTE_NAMES.index(
            const.INIT_NAME
        )
        i_init = const.INIT_POS[0]
        j_init = const.INIT_POS[1]
        for j in range(const.EULER_ROWS):
            self.__dots_small.append([])
            self.__dots_big.append([])
            for i in range(const.EULER_COLS):
                index = index_init - i_init + i - (j_init - j)*4
                if (0 <= index < len(const.NOTE_NAMES)):
                    name = const.NOTE_NAMES[index]

                    image = tk.PhotoImage(
                        file="figs/%s_small.png"%(name)
                    )
                else:
                    image = tk.PhotoImage(
                        file="figs/o_small.png"
                    )
                self.__images.append(image)
                (x, y) = self.__euler_to_coords(
                    i, j
                )
                self.__dots_small[-1].append(
                    self.__canvas.create_image(
                        x,
                        y,
                        image=image,
                        anchor=tk.CENTER
                    )
                )
                if (0 <= index < len(const.NOTE_NAMES)):
                    name = const.NOTE_NAMES[index]

                    image = tk.PhotoImage(
                        file="figs/%s_big.png"%(name)
                    )
                else:
                    image = tk.PhotoImage(
                        file="figs/o_big.png"
                    )
                self.__images.append(image)
                (x, y) = self.__euler_to_coords(
                    i, j
                )
                self.__dots_big[-1].append(
                    self.__canvas.create_image(
                        x,
                        y,
                        image=image,
                        anchor=tk.CENTER,
                        state=tk.HIDDEN
                    )
                )



    def set_region(self, index):
        for i in range(const.EULER_COLS - 3):
            if i == index:
                value = tk.NORMAL
            else:
                value = tk.HIDDEN
            self.__canvas.itemconfigure(
                self.__regions[i],
                state=value
            )

    def note_on(self, i, j):
        self.__playing[j][i] += 1
        if self.__playing[j][i] > 0:
            self.__canvas.itemconfigure(
                self.__dots_small[j][i],
                state=tk.HIDDEN
            )
            self.__canvas.itemconfigure(
                self.__dots_big[j][i],
                state=tk.NORMAL
            )

    def note_off(self, i, j):
        self.__playing[j][i] -= 1
        if self.__playing[j][i] == 0:
            self.__canvas.itemconfigure(
                self.__dots_small[j][i],
                state=tk.NORMAL
            )
            self.__canvas.itemconfigure(
                self.__dots_big[j][i],
                state=tk.HIDDEN
            )

    def reset(self):
        for j in range(const.EULER_ROWS):
            for i in range(const.EULER_COLS):
                self.__playing[j][i] = 0
                self.__canvas.itemconfigure(
                    self.__dots_small[j][i],
                    state=tk.NORMAL
                )
                self.__canvas.itemconfigure(
                    self.__dots_big[j][i],
                    state=tk.HIDDEN
                )


if __name__ == "__main__":
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
    
