import tkinter as tk
import numpy as np
import time
import const

class Gui(tk.Frame):

    def __init__(self, const, master):
        super().__init__(master)
        self.__const = const
        self.__make_canvas()
        self.__make_regions()
        self.__make_dots()

    def __euler_to_coords(self, i, j, k):
        x = int(
                (
                    (i + 0.5)
                  + j * 0.5
                  + k * 0.5
                ) * self.__const["EULERNET_DISTANCE"] * 1.3
            )
        y = int(
                (- k) * self.__const["EULERNET_DISTANCE"] * 1.3 * (0.5 / np.sqrt(3))
              + (self.__const["EULER_ROWS"] - j)
              * np.sqrt(3) * 0.5
              * self.__const["EULERNET_DISTANCE"] * 1.3
            )
        return (x, y)

    def __make_canvas(self):
        (w, h) = self.__euler_to_coords(
            self.__const["EULER_PEDALS"] + 3,
            0,
            0
        )
        w += self.__const["EULERNET_DISTANCE"]
        h += self.__const["EULERNET_DISTANCE"]
        self.__canvas = tk.Canvas(
            self,
            width=w,
            height=h,
            bg=self.__const["BACKGROUND_COLOR"]
        )
        self.__canvas.pack()

    def __make_regions(self):
        self.__regions = []
        for i in range(self.__const["EULER_PEDALS"]):
            (x0, y0) = self.__euler_to_coords(
                i-0.5,
                -0.5,
                0
            )
            (x1, y1) = self.__euler_to_coords(
                i-0.5,
                self.__const["EULER_ROWS"] - 0.5,
                0
            )


            (x2, y2) = self.__euler_to_coords(
                i-0.5,
                -0.5,
                1
            )
            (x3, y3) = self.__euler_to_coords(
                i-0.5,
                self.__const["EULER_ROWS"] - 0.5,
                1
            )
            (x4, y4) = self.__euler_to_coords(
                i+1.5,
                self.__const["EULER_ROWS"] - 0.5,
                1
            )
            (x5, y5) = self.__euler_to_coords(
                i+1.5,
                -0.5,
                1
            )


            (x6, y6) = self.__euler_to_coords(
                i+1.5,
                self.__const["EULER_ROWS"] - 0.5,
                0
            )
            (x7, y7) = self.__euler_to_coords(
                i+1.5,
                -0.5,
                0
            )
            self.__regions.append(
                self.__canvas.create_polygon(
                    x0, y0, x3, y3, x4, y4, x7, y7,
                    fill=self.__const["REGION_COLOR"],
                    width=
                        self.__const["REGION_BORDER_WIDTH"],
                    outline=
                        self.__const["REGION_BORDER_COLOR"],
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
        for k in range(self.__const["EULER_LAYERS"]):
            self.__playing.append([])
            for j in range(self.__const["EULER_ROWS"]):
                self.__playing[-1].append([])
                for i in range(self.__const["EULER_PEDALS"] + 3):
                    self.__playing[-1][-1].append(0)
        index_init = self.__const["NOTE_NAMES"].index(
            self.__const["INIT_NAME"]
        )
        i_init = self.__const["INIT_POS"][0]
        j_init = self.__const["INIT_POS"][1]
        k_init = self.__const["INIT_POS"][2]
        for k in range(self.__const["EULER_LAYERS"]):
            self.__dots_small.append([])
            self.__dots_big.append([])
            for j in range(self.__const["EULER_ROWS"]):
                self.__dots_small[-1].append([])
                self.__dots_big[-1].append([])
                for i in range(self.__const["EULER_PEDALS"] + 1):
                    index = index_init - i_init + i - (j_init - j)*4 + (k_init - k)*2
                    if (0 <= index < len(self.__const["NOTE_NAMES"])):
                        name = self.__const["NOTE_NAMES"][index]
                        if k == 0:
                            image = tk.PhotoImage(
                                file="figs/%s_small.png"%(name)
                            )
                        else:
                            image = tk.PhotoImage(
                                file="figs/%s_small_gray.png"%(name)
                            )
                    else:
                        if k == 0:
                            image = tk.PhotoImage(
                                file="figs/o_small.png"
                            )
                        else:
                            image = tk.PhotoImage(
                                file="figs/o_small_gray.png"
                            )
                    self.__images.append(image)
                    (x, y) = self.__euler_to_coords(
                        i, j, k
                    )
                    self.__dots_small[-1][-1].append(
                        self.__canvas.create_image(
                            x,
                            y,
                            image=image,
                            anchor=tk.CENTER
                        )
                    )
                    if (0 <= index < len(self.__const["NOTE_NAMES"])):
                        name = self.__const["NOTE_NAMES"][index]
                        if k == 0:
                            image = tk.PhotoImage(
                                file="figs/%s_big.png"%(name)
                            )
                        else:
                            image = tk.PhotoImage(
                                file="figs/%s_big_gray.png"%(name)
                            )
                    else:
                        if k == 0:
                            image = tk.PhotoImage(
                                file="figs/o_big.png"
                            )
                        else:
                            image = tk.PhotoImage(
                                file="figs/o_big_gray.png"
                            )
                    self.__images.append(image)
                    (x, y) = self.__euler_to_coords(
                        i, j, k
                    )
                    self.__dots_big[-1][-1].append(
                        self.__canvas.create_image(
                            x,
                            y,
                            image=image,
                            anchor=tk.CENTER,
                            state=tk.HIDDEN
                        )
                    )



    def set_region(self, index):
        for i in range(self.__const["EULER_PEDALS"]):
            if i == index:
                value = tk.NORMAL
            else:
                value = tk.HIDDEN
            self.__canvas.itemconfigure(
                self.__regions[i],
                state=value
            )

    def note_on(self, position):
        [i, j, k] = [int(word) for word in position.split(",")]
        self.__playing[k][j][i] += 1
        if self.__playing[k][j][i] > 0:
            self.__canvas.itemconfigure(
                self.__dots_small[k][j][i],
                state=tk.HIDDEN
            )
            self.__canvas.itemconfigure(
                self.__dots_big[k][j][i],
                state=tk.NORMAL
            )

    def note_off(self, position):
        [i, j, k] = [int(word) for word in position.split(",")]
        self.__playing[k][j][i] -= 1
        if self.__playing[k][j][i] == 0:
            self.__canvas.itemconfigure(
                self.__dots_small[k][j][i],
                state=tk.NORMAL
            )
            self.__canvas.itemconfigure(
                self.__dots_big[k][j][i],
                state=tk.HIDDEN
            )

    def reset(self):
        for k in range(self.__const["EULER_LAYERS"]):
            for j in range(self.__const["EULER_ROWS"]):
                for i in range(self.__const["EULER_PEDAlS"] + 1):
                    self.__playing[k][j][i] = 0
                    self.__canvas.itemconfigure(
                        self.__dots_small[k][j][i],
                        state=tk.NORMAL
                    )
                    self.__canvas.itemconfigure(
                        self.__dots_big[k][j][i],
                        state=tk.HIDDEN
                    )
   
